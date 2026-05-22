# app/services/analytics_service.py
# Computes performance metrics from Supabase data.
# Keeps heavy aggregation logic out of API routes.

from app.utils.logger import get_logger

logger = get_logger(__name__)


async def get_overview(user_id: str) -> dict:
    """
    Aggregates:
    - Task completion rates
    - Subject performance
    - Weekly trends
    - Weak subject detection
    (Full implementation in next phase)
    """
    logger.info(f"get_overview called for user={user_id}")
    raise NotImplementedError("Analytics not yet implemented")
