from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from app.models.schemas import SkillAnalysisResponse, RecommendationItem
from app.core.security import get_current_user
from app.services.parser import parse_resume_bytes
import logging
from typing import List, Optional
import json

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

@router.post("/analyze", response_model=SkillAnalysisResponse)
async def analyze_skills(
    target_role: str = Form(...),
    experience_level: str = Form("Entry Level"),
    manual_skills: Optional[str] = Form(None), # comma-separated list or JSON array string
    file: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Analyzes skills from either a manual skill list input OR an uploaded resume PDF/text,
    comparing them to a target job role. Returns a comprehensive skill-gap analysis.
    """
    user_id = current_user["id"]
    resume_text = ""
    skills_list = []
    
    # 1. Gather manual skills list if provided
    if manual_skills:
        try:
            # Check if it is a JSON array string
            parsed = json.loads(manual_skills)
            if isinstance(parsed, list):
                skills_list = [str(x).strip() for x in parsed]
            else:
                skills_list = [x.strip() for x in str(manual_skills).split(",") if x.strip()]
        except json.JSONDecodeError:
            skills_list = [x.strip() for x in str(manual_skills).split(",") if x.strip()]

    # 2. Parse resume document file if uploaded
    if file:
        try:
            file_bytes = await file.read()
            resume_text = parse_resume_bytes(file_bytes, file.filename)
            logger.info(f"Successfully extracted {len(resume_text)} characters from {file.filename}")
        except Exception as e:
            logger.error(f"Failed to read/parse uploaded file: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Could not parse resume upload file: {str(e)}"
            )

    # 3. Call Gemini AI or High-Fidelity Simulator
    # Prepare text for Gemini: if no file was uploaded, summarize the manual skills list
    if not resume_text and skills_list:
        resume_text = f"Student manual skill list: {', '.join(skills_list)}"
    elif not resume_text:
        resume_text = "[No resume document or skills list supplied. Student is beginning from scratch.]"

    try:
        from app.services.gemini import analyze_skill_gap
        analysis = analyze_skill_gap(resume_text, target_role, experience_level)
        
        # Parse recommendations into list of RecommendationItem objects
        recs = []
        for r in analysis.get("recommendations", []):
            recs.append(RecommendationItem(
                skill=r.get("skill", "Unknown Skill"),
                actionable_step=r.get("actionable_step", "Study core concepts.")
            ))
            
        return SkillAnalysisResponse(
            gap_score=analysis.get("gap_score", 50),
            matching_skills=analysis.get("matching_skills", []),
            missing_skills=analysis.get("missing_skills", []),
            recommendations=recs,
            ai_disclaimer="Suggestions are AI-generated based on current trends. Please cross-verify details."
        )
    except Exception as e:
        logger.error(f"Gemini analysis service call failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI analysis execution failed: {str(e)}"
        )
