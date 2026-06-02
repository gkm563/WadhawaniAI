from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import ProfileCreate, ProfileResponse, ProfileUpdate
from app.core.security import get_current_user
from app.services.supabase_client import supabase_client
import logging
from datetime import datetime

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

# Local fallback cache for development/offline mock runs
_mock_profiles_cache = {}

@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    """
    Fetch the profile metadata for the currently authenticated user.
    """
    user_id = current_user["id"]
    
    # If using offline mock mode or database client is uninitialized
    if current_user.get("is_mock") or supabase_client is None:
        if user_id not in _mock_profiles_cache:
            _mock_profiles_cache[user_id] = {
                "id": user_id,
                "full_name": "Wadhwani Aspirant",
                "email": current_user.get("email", "student@wadhwani.org"),
                "phone_number": "+91 9999999999",
                "preferred_language": "en",
                "target_role": "Full Stack Developer",
                "current_experience_level": "Entry Level",
                "created_at": datetime.utcnow().isoformat() + "Z"
            }
        return _mock_profiles_cache[user_id]

    try:
        # Retrieve profile from Supabase profiles table
        result = supabase_client.table("profiles").select("*").eq("id", user_id).execute()
        if result and len(result.data) > 0:
            return result.data[0]
        else:
            # Profile doesn't exist yet, auto-create a default profile skeleton
            default_profile = {
                "id": user_id,
                "full_name": "Aspirant",
                "email": current_user.get("email"),
                "preferred_language": "en",
                "target_role": "Software Engineer",
                "current_experience_level": "Entry Level",
                "created_at": datetime.utcnow().isoformat() + "Z"
            }
            supabase_client.table("profiles").insert(default_profile).execute()
            return default_profile
    except Exception as e:
        logger.error(f"Failed to fetch profile from database: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database retrieval failure: {str(e)}"
        )

@router.post("", response_model=ProfileResponse)
async def create_profile(profile: ProfileCreate, current_user: dict = Depends(get_current_user)):
    """
    Create a new student profile linked to Supabase authentication ID.
    """
    if profile.id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create profile metadata for another user identity."
        )

    # Dry-run mock logic
    if current_user.get("is_mock") or supabase_client is None:
        new_profile = {
            **profile.model_dump(),
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        _mock_profiles_cache[profile.id] = new_profile
        return new_profile

    try:
        # Insert profile record into Supabase
        profile_data = {
            **profile.model_dump(),
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        result = supabase_client.table("profiles").insert(profile_data).execute()
        if result and len(result.data) > 0:
            return result.data[0]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to insert student profile."
        )
    except Exception as e:
        logger.error(f"Error inserting user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database write error: {str(e)}"
        )

@router.put("/me", response_model=ProfileResponse)
async def update_profile(profile_updates: ProfileUpdate, current_user: dict = Depends(get_current_user)):
    """
    Update profile details for the currently logged-in student.
    """
    user_id = current_user["id"]
    
    # Dry-run mock implementation
    if current_user.get("is_mock") or supabase_client is None:
        existing = _mock_profiles_cache.get(
            user_id,
            {
                "id": user_id,
                "full_name": "Wadhwani Aspirant",
                "email": current_user.get("email"),
                "preferred_language": "en",
                "target_role": "Full Stack Developer",
                "current_experience_level": "Entry Level",
                "created_at": datetime.utcnow().isoformat() + "Z"
            }
        )
        updated = {**existing, **profile_updates.model_dump(exclude_unset=True)}
        _mock_profiles_cache[user_id] = updated
        return updated

    try:
        updates = profile_updates.model_dump(exclude_unset=True)
        if not updates:
            raise HTTPException(status_code=400, detail="No updates provided.")
            
        result = supabase_client.table("profiles").update(updates).eq("id", user_id).execute()
        if result and len(result.data) > 0:
            return result.data[0]
        raise HTTPException(status_code=404, detail="Student profile profile not found.")
    except Exception as e:
        logger.error(f"Failed to update profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database update error: {str(e)}"
        )
