# app/api/analytics.py
from fastapi import APIRouter, Depends, HTTPException
from app.models.analytics_models import AnalyticsOverview
from app.middlewares.auth_middleware import get_current_user
from app.utils.logger import get_logger

router = APIRouter(prefix="/analytics", tags=["Analytics"])
logger = get_logger(__name__)


@router.get("/overview", response_model=AnalyticsOverview)
async def analytics_overview(current_user: dict = Depends(get_current_user)):
    """Return aggregated performance overview. (Stub)"""
    # TODO: call analytics_service.get_overview(current_user["id"])
    raise HTTPException(status_code=501, detail="Not implemented yet")
