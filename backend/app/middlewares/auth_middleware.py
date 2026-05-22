# app/middlewares/auth_middleware.py
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.supabase import get_supabase
from app.utils.logger import get_logger

logger = get_logger(__name__)
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(request: Request) -> dict:
    """
    Dependency: validates the Bearer token via Supabase and returns the user dict.
    Usage: user = Depends(get_current_user)
    """
    credentials: HTTPAuthorizationCredentials | None = await bearer_scheme(request)

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
        )

    token = credentials.credentials
    try:
        supabase = get_supabase()
        response = supabase.auth.get_user(token)
        if not response or not response.user:
            raise ValueError("Invalid token")
        return {"id": response.user.id, "email": response.user.email}
    except Exception as e:
        logger.warning(f"Auth failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
