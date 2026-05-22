# app/api/settings_api.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.middlewares.auth_middleware import get_current_user
from app.utils.logger import get_logger

router = APIRouter(prefix="/settings", tags=["Settings"])
logger = get_logger(__name__)


class UserSettings(BaseModel):
    daily_study_goal_minutes: int | None = None
    preferred_study_start: str | None = None   # "HH:MM" 24h
    notifications_enabled: bool | None = None
    theme: str | None = None                   # "light" | "dark"


@router.get("", response_model=UserSettings)
async def get_settings(current_user: dict = Depends(get_current_user)):
    """Fetch user settings. (Stub)"""
    # TODO: fetch from supabase settings table
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.patch("", response_model=UserSettings)
async def update_settings(body: UserSettings, current_user: dict = Depends(get_current_user)):
    """Update user settings. (Stub)"""
    # TODO: upsert to supabase settings table
    raise HTTPException(status_code=501, detail="Not implemented yet")
