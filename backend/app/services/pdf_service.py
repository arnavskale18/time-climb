# app/services/pdf_service.py
# Handles PDF parsing for grade sheets and timetables.

import PyPDF2
import io
from app.utils.logger import get_logger

logger = get_logger(__name__)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract raw text from a PDF file."""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        logger.info(f"Extracted {len(text)} chars from PDF ({len(reader.pages)} pages)")
        return text
    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        raise


async def parse_grades_pdf(file_bytes: bytes) -> list[dict]:
    """
    Parse a grades PDF into structured subject/grade objects.
    Uses extract_text_from_pdf + Gemini for structuring (next phase).
    """
    raise NotImplementedError("Grade PDF parsing not yet implemented")


async def parse_timetable_pdf(file_bytes: bytes) -> dict:
    """
    Parse a timetable PDF into a structured weekly schedule.
    (Full implementation in next phase)
    """
    raise NotImplementedError("Timetable PDF parsing not yet implemented")
