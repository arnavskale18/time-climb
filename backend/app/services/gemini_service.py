# app/services/gemini_service.py
import google.generativeai as genai
from app.config.settings import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
_settings = get_settings()

# Configure SDK once at import time
genai.configure(api_key=_settings.gemini_api_key)


def get_model():
    """Returns a configured Gemini GenerativeModel instance."""
    return genai.GenerativeModel(_settings.gemini_model)


async def generate_text(prompt: str) -> str:
    """
    Low-level wrapper: sends a prompt and returns the text response.
    All feature-specific AI calls should go through higher-level service functions.
    """
    try:
        model = get_model()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        raise


# ── Feature stubs (implement when building each feature) ──────────────────

async def generate_tasks(context: dict) -> list[dict]:
    """Generate daily study tasks. Stub — implement in scheduler_service."""
    raise NotImplementedError


async def coach_reply(history: list, message: str, profile: dict) -> str:
    """Generate a coach chat reply. Stub — implement in coach route."""
    raise NotImplementedError
