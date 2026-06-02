from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any

# --- Health Check ---
class HealthResponse(BaseModel):
    status: str
    environment: str
    supabase_connected: bool
    gemini_configured: bool

# --- Authentication & User Profile ---
class ProfileBase(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    preferred_language: str = "en"
    target_role: Optional[str] = None
    current_experience_level: str = "Entry Level"

class ProfileCreate(ProfileBase):
    id: str  # References Supabase Auth UID

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    preferred_language: Optional[str] = None
    target_role: Optional[str] = None
    current_experience_level: Optional[str] = None

class ProfileResponse(ProfileBase):
    id: str
    created_at: str

    class Config:
        from_attributes = True

# --- Skill Gap Analysis ---
class SkillAnalysisRequest(BaseModel):
    target_role: str
    manual_skills: Optional[List[str]] = None
    experience_level: Optional[str] = "Entry Level"

class RecommendationItem(BaseModel):
    skill: str
    actionable_step: str

class SkillAnalysisResponse(BaseModel):
    gap_score: int = Field(..., ge=0, le=100)
    matching_skills: List[str]
    missing_skills: List[str]
    recommendations: List[RecommendationItem]
    ai_disclaimer: str = "Suggestions are AI-generated based on current trends. Please cross-verify details."

# --- Career Roadmap Generator ---
class RoadmapRequest(BaseModel):
    target_role: str
    duration_days: int = 30
    missing_skills: List[str]
    language: str = "en"

class RoadmapTask(BaseModel):
    task_name: str
    description: str

class RoadmapMilestone(BaseModel):
    week: int
    title: str
    tasks: List[str]
    resources: List[str]

class RoadmapResponse(BaseModel):
    title: str
    target_role: str
    duration_days: int
    language: str
    milestones: List[RoadmapMilestone]
    ai_disclaimer: str = "Suggestions are AI-generated based on current trends."

# --- Mock Interview Engine ---
class InterviewStartRequest(BaseModel):
    target_role: str
    language: str = "en"

class InterviewStartResponse(BaseModel):
    session_id: str
    question: str
    current_question_index: int

class InterviewRespondRequest(BaseModel):
    session_id: str
    user_response: str

class InterviewRespondResponse(BaseModel):
    is_completed: bool
    next_question: Optional[str] = None
    current_question_index: int

class DetailedFeedbackItem(BaseModel):
    question: str
    user_answer: str
    feedback: str
    model_answer: str

class InterviewEvaluationResponse(BaseModel):
    session_id: str
    overall_score: int = Field(..., ge=0, le=100)
    technical_score: int = Field(..., ge=0, le=100)
    communication_score: int = Field(..., ge=0, le=100)
    strengths: List[str]
    weaknesses: List[str]
    detailed_feedback: List[DetailedFeedbackItem]
    ai_disclaimer: str = "Evaluations are AI-generated. Use for practicing purposes."
