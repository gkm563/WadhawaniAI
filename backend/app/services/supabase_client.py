import logging
from supabase import create_client, Client
from app.core.config import settings

# Setup standard logging logger
logger = logging.getLogger("uvicorn.error")

supabase_client: Client = None

def init_supabase() -> Client:
    global supabase_client
    if supabase_client is not None:
        return supabase_client

    url = settings.SUPABASE_URL
    key = settings.SUPABASE_ANON_KEY

    # Allow mock initialization if keys are blank to maintain smooth dev/hackathon boot
    if not url or "your-supabase" in url or not key:
        logger.warning(
            "Supabase credentials not configured or using placeholders. "
            "Supabase database connection operations will fail or operate in dry-run mode."
        )
        return None

    try:
        supabase_client = create_client(url, key)
        logger.info("Supabase client initialized successfully.")
        return supabase_client
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {str(e)}")
        return None

# Try initializing on boot
supabase_client = init_supabase()
