from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.supabase_client import supabase_client
import logging

# Security bearer helper
security_bearer = HTTPBearer(auto_error=False)
logger = logging.getLogger("uvicorn.error")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_bearer)) -> dict:
    """
    Dependency injection function to authenticate incoming requests via Supabase JWT.
    Returns user details dictionary or raises HTTP 401 Unauthorized.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization credentials"
        )
        
    token = credentials.credentials
    
    # Check if Supabase client is initialized. If not, return a mock user profile to support dry-run hackathon demo mode.
    if supabase_client is None:
        logger.warning("Supabase client is uninitialized. Returning mock user for dry-run/development mode.")
        return {
            "id": "00000000-0000-0000-0000-000000000000",
            "email": "student@wadhwani.org",
            "role": "authenticated",
            "is_mock": True
        }

    try:
        # Call Supabase to fetch the active user matching this JWT
        response = supabase_client.auth.get_user(token)
        if response and response.user:
            user = response.user
            return {
                "id": str(user.id),
                "email": user.email,
                "role": "authenticated",
                "is_mock": False
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired authentication token"
            )
    except Exception as e:
        logger.error(f"Supabase auth check failed: {str(e)}")
        # Fallback to check for local test/debug token in development
        if token == "mock-dev-token-wadhwani":
            return {
                "id": "00000000-0000-0000-0000-000000000000",
                "email": "student@wadhwani.org",
                "role": "authenticated",
                "is_mock": True
            }
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )
