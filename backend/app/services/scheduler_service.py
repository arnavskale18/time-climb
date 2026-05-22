# app/services/scheduler_service.py
# Handles task scheduling logic — AI-assisted prioritization lives here.
# The service layer keeps business logic OUT of the API routes.

from datetime import date
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def build_daily_plan(user_id: str, target_date: date, subjects: list[str] | None = None) -> list[dict]:
    """
    Orchestrates task generation:
    1. Fetch user subjects + grades from Supabase
    2. Fetch timetable availability
    3. Call gemini_service to generate prioritized tasks
    4. Validate and persist tasks
    5. Return task list
    (Full implementation in next phase)
    """
    logger.info(f"build_daily_plan called for user={user_id} date={target_date}")
    raise NotImplementedError("Scheduler not yet implemented")
