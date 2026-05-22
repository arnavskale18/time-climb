from fastapi import APIRouter, HTTPException, status, Depends
from app.models.auth_models import (
    SignupRequest,
    LoginRequest,
    AuthResponse,
    UserProfile,
)
from app.config.supabase import get_supabase
from app.middlewares.auth_middleware import get_current_user
from app.utils.logger import get_logger

router = APIRouter(prefix="/auth", tags=["Auth"])
logger = get_logger(__name__)


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED
)
async def signup(body: SignupRequest):
    """
    Register a new user via Supabase Auth.
    """

    try:
        supabase = get_supabase()

        res = supabase.auth.sign_up({
            "email": body.email,
            "password": body.password,
            "options": {
                "data": {
                    "full_name": body.full_name
                }
            }
        })

        if not res.user:
            raise HTTPException(
                status_code=400,
                detail="Signup failed"
            )

        access_token = ""

        if res.session:
            access_token = res.session.access_token

        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=res.user.id
        )

    except Exception as e:
        logger.error(f"Signup error: {e}")

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login", response_model=AuthResponse)
async def login(body: LoginRequest):
    """
    Authenticate an existing user.
    """

    try:
        supabase = get_supabase()

        res = supabase.auth.sign_in_with_password({
            "email": body.email,
            "password": body.password
        })

        if not res.user or not res.session:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        return AuthResponse(
            access_token=res.session.access_token,
            token_type="bearer",
            user_id=res.user.id
        )

    except Exception as e:
        logger.error(f"Login error: {e}")

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )


@router.get("/me", response_model=UserProfile)
async def me(current_user: dict = Depends(get_current_user)):
    """
    Return the authenticated user's profile.
    """

    return UserProfile(
        id=current_user["id"],
        email=current_user["email"]
    )