from fastapi import APIRouter

# Initialize main api router
api_router = APIRouter()

from app.api.endpoints import profiles, skills, roadmaps, interviews

api_router.include_router(profiles.router, prefix="/profiles", tags=["Profiles System"])
api_router.include_router(skills.router, prefix="/skills", tags=["Skills Analysis"])
api_router.include_router(roadmaps.router, prefix="/roadmaps", tags=["Roadmap Generator"])
api_router.include_router(interviews.router, prefix="/interviews", tags=["Mock Interview"])

@api_router.get("/ping", tags=["Diagnostics"])
def ping():
    return {"message": "API service is active"}
