from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import (
    InterviewStartRequest, InterviewStartResponse,
    InterviewRespondRequest, InterviewRespondResponse,
    InterviewEvaluationResponse, DetailedFeedbackItem
)
from app.core.security import get_current_user
from app.services.gemini import evaluate_interview
from app.services.supabase_client import supabase_client
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Any

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

# Local in-memory session manager cache for resilient demo execution
# Map: session_id -> {role, language, current_idx, questions: [], answers: [], completed: bool}
_active_sessions: Dict[str, Dict[str, Any]] = {}

# Hardcoded standard job role questions mapping to guarantee instant question retrieval on slow connections
ROLE_QUESTIONS_MAP = {
    "frontend": [
        "Explain the difference between State and Props in React.",
        "What is the Virtual DOM and how does React optimize rendering performance?",
        "How do you ensure a web layout is responsive and performs well on slow internet networks?"
    ],
    "backend": [
        "Explain what RESTful API design is and list the standard HTTP method usages.",
        "What is the difference between SQL and NoSQL databases, and when would you use which?",
        "How do you handle asynchronous operations or concurrency bottlenecks in Python backend applications?"
    ],
    "generic": [
        "Describe a difficult technical problem you faced and how you went about solving it.",
        "How do you manage your time and learning schedule when picking up a completely new skill?",
        "Why are you interested in this target career track, and what steps have you taken so far to prepare?"
    ]
}

def get_questions_for_role(role: str) -> List[str]:
    """
    Selects a set of 3 practice interview questions matching the target job role.
    """
    norm = role.lower()
    if "front" in norm or "react" in norm:
        return ROLE_QUESTIONS_MAP["frontend"]
    elif "back" in norm or "py" in norm or "fastapi" in norm:
        return ROLE_QUESTIONS_MAP["backend"]
    else:
        return ROLE_QUESTIONS_MAP["generic"]

@router.post("/start", response_model=InterviewStartResponse)
async def start_interview(
    payload: InterviewStartRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Starts a new technical/HR practice interview session.
    Retrieves the customized questions set and returns the first question immediately.
    """
    user_id = current_user["id"]
    session_id = str(uuid.uuid4())
    
    questions = get_questions_for_role(payload.target_role)
    
    # Store interview session details in active local memory cache
    session_data = {
        "id": session_id,
        "user_id": user_id,
        "target_role": payload.target_role,
        "language": payload.language,
        "current_question_index": 0,
        "questions": questions,
        "answers": [],
        "is_completed": False,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    _active_sessions[session_id] = session_data

    # Optional: Save session header in Supabase database
    if supabase_client is not None and not current_user.get("is_mock"):
        try:
            db_record = {
                "id": session_id,
                "user_id": user_id,
                "target_role": payload.target_role,
                "status": "active",
                "current_question_index": 0,
                "created_at": session_data["created_at"]
            }
            supabase_client.table("interview_sessions").insert(db_record).execute()
        except Exception as e:
            logger.error(f"Failed to save interview session header in Supabase: {str(e)}")

    return InterviewStartResponse(
        session_id=session_id,
        question=questions[0],
        current_question_index=0
    )

@router.post("/respond", response_model=InterviewRespondResponse)
async def submit_response(
    payload: InterviewRespondRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Processes the student's answer text, updates session state,
    and returns either the next question OR signals completion of the session.
    """
    session_id = payload.session_id
    
    if session_id not in _active_sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active interview session not found. Please start a new session."
        )
        
    session = _active_sessions[session_id]
    
    if session["is_completed"]:
        return InterviewRespondResponse(
            is_completed=True,
            next_question=None,
            current_question_index=session["current_question_index"]
        )

    # 1. Record the student's answer
    session["answers"].append(payload.user_response)
    
    # Optional: Save user response dialogue in Supabase database
    if supabase_client is not None and not current_user.get("is_mock"):
        try:
            # Save AI question dialogue
            q_num = session["current_question_index"]
            q_text = session["questions"][q_num]
            supabase_client.table("interview_messages").insert({
                "session_id": session_id,
                "sender": "ai",
                "text_content": q_text
            }).execute()
            # Save Student answer dialogue
            supabase_client.table("interview_messages").insert({
                "session_id": session_id,
                "sender": "user",
                "text_content": payload.user_response
            }).execute()
        except Exception as e:
            logger.error(f"Failed to save dialogues in Supabase: {str(e)}")

    # 2. Advance the question tracker index
    next_idx = session["current_question_index"] + 1
    session["current_question_index"] = next_idx
    
    # Check if we have asked all 3 questions
    if next_idx >= len(session["questions"]):
        session["is_completed"] = True
        
        # Update session status in Supabase database if connected
        if supabase_client is not None and not current_user.get("is_mock"):
            try:
                supabase_client.table("interview_sessions").update({
                    "status": "completed",
                    "current_question_index": next_idx
                }).eq("id", session_id).execute()
            except Exception as e:
                logger.error(f"Failed to update session header completion in Supabase: {str(e)}")

        return InterviewRespondResponse(
            is_completed=True,
            next_question=None,
            current_question_index=next_idx
        )
        
    next_question = session["questions"][next_idx]
    
    return InterviewRespondResponse(
        is_completed=False,
        next_question=next_question,
        current_question_index=next_idx
    )

@router.get("/{session_id}/evaluate", response_model=InterviewEvaluationResponse)
async def evaluate_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Submits the recorded dialogues to Gemini AI to generate a detailed feedback scorecard.
    """
    if session_id not in _active_sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session details not found."
        )
        
    session = _active_sessions[session_id]
    
    # Fill in empty strings if mock interview was stopped early
    while len(session["answers"]) < len(session["questions"]):
        session["answers"].append("[No response provided]")
        
    try:
        # Request detailed assessment feedback scorecard from Gemini AI Client
        evaluation = evaluate_interview(
            role=session["target_role"],
            questions=session["questions"],
            answers=session["answers"]
        )
        
        # Parse the structured response
        feedback_items = []
        for item in evaluation.get("detailed_feedback", []):
            feedback_items.append(DetailedFeedbackItem(
                question=item.get("question", "Question"),
                user_answer=item.get("user_answer", "Answer"),
                feedback=item.get("feedback", "No feedback recorded."),
                model_answer=item.get("model_answer", "Standard answer blueprint.")
            ))

        response = InterviewEvaluationResponse(
            session_id=session_id,
            overall_score=evaluation.get("overall_score", 75),
            technical_score=evaluation.get("technical_score", 75),
            communication_score=evaluation.get("communication_score", 75),
            strengths=evaluation.get("strengths", []),
            weaknesses=evaluation.get("weaknesses", []),
            detailed_feedback=feedback_items,
            ai_disclaimer="Evaluations are AI-generated. Use for practicing purposes."
        )

        # Optional: Save evaluation report in Supabase database if connected
        if supabase_client is not None and not current_user.get("is_mock"):
            try:
                db_record = {
                    "session_id": session_id,
                    "overall_score": response.overall_score,
                    "technical_score": response.technical_score,
                    "communication_score": response.communication_score,
                    "strengths": response.strengths,
                    "weaknesses": response.weaknesses,
                    "detailed_feedback": [item.model_dump() for item in feedback_items],
                    "created_at": datetime.utcnow().isoformat() + "Z"
                }
                supabase_client.table("interview_evaluations").insert(db_record).execute()
                logger.info(f"Successfully saved evaluation report for session {session_id} in database.")
            except Exception as e:
                logger.error(f"Failed to insert evaluation report record in database: {str(e)}")

        return response
        
    except Exception as e:
        logger.error(f"Failed to compute mock evaluation report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Interview assessment failed: {str(e)}"
        )
