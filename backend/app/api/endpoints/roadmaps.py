from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import RoadmapRequest, RoadmapResponse, RoadmapMilestone
from app.core.security import get_current_user
from app.services.gemini import generate_career_roadmap
from app.services.supabase_client import supabase_client
import logging
from datetime import datetime

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

@router.post("/generate", response_model=RoadmapResponse)
async def create_roadmap(
    payload: RoadmapRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Triggers Gemini AI to generate a highly customized weekly milestone roadmap (30/60 day duration)
    targeted towards the student's dream role. Supports multilingual English and Hindi outputs.
    """
    user_id = current_user["id"]
    
    try:
        # Generate the structured milestone path via Gemini Service
        roadmap_data = generate_career_roadmap(
            target_role=payload.target_role,
            missing_skills=payload.missing_skills,
            duration_days=payload.duration_days,
            language=payload.language
        )
        
        # Format the milestones into RoadmapMilestone objects
        milestones = []
        for ms in roadmap_data.get("milestones", []):
            milestones.append(RoadmapMilestone(
                week=ms.get("week", 1),
                title=ms.get("title", "Foundations"),
                tasks=ms.get("tasks", []),
                resources=ms.get("resources", [])
            ))

        response = RoadmapResponse(
            title=roadmap_data.get("title", f"{payload.duration_days}-Day {payload.target_role} Study Guide"),
            target_role=payload.target_role,
            duration_days=payload.duration_days,
            language=payload.language,
            milestones=milestones,
            ai_disclaimer="Suggestions are AI-generated based on current trends. Keep practising."
        )

        # Optional: Save generated roadmap to Supabase database if configured
        if supabase_client is not None and not current_user.get("is_mock"):
            try:
                db_record = {
                    "user_id": user_id,
                    "target_role": payload.target_role,
                    "duration_days": payload.duration_days,
                    "title": response.title,
                    "language": payload.language,
                    "milestones": [m.model_dump() for m in milestones],
                    "created_at": datetime.utcnow().isoformat() + "Z"
                }
                supabase_client.table("roadmaps").insert(db_record).execute()
                logger.info(f"Successfully saved generated roadmap for user {user_id} in database.")
            except Exception as dbe:
                logger.error(f"Failed to save roadmap to Supabase: {str(dbe)}")
                # Do not block the API return if database insert fails during high-pressure runs

        return response
        
    except Exception as e:
        logger.error(f"Failed to generate career roadmap: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI Roadmap compilation failed: {str(e)}"
        )
