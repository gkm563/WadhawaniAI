import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.router import api_router
from app.services.supabase_client import supabase_client
import os

# Initialize main FastAPI application
app = FastAPI(
    title="PathPilot AI - Core API",
    description="Multilingual AI-assisted employability infrastructure API for Wadhwani AI + Google.org track",
    version="1.0.0"
)

# Enable CORS for local Next.js frontend calls and deployed environments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, lock this down to specific domains (e.g. Vercel)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core diagnostic health check
@app.get("/health", tags=["Diagnostics"])
def health_check():
    # Verify Supabase configuration state
    supabase_configured = supabase_client is not None
    
    # Verify Gemini configurations
    gemini_key = settings.GEMINI_API_KEY
    gemini_configured = bool(gemini_key and "your-gemini" not in gemini_key)
    
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "supabase_connected": supabase_configured,
        "gemini_configured": gemini_configured
    }

# Include API Router under /api/v1 prefix
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
