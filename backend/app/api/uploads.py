# app/api/uploads.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.middlewares.auth_middleware import get_current_user
from app.utils.logger import get_logger

router = APIRouter(prefix="/upload", tags=["Uploads"])
logger = get_logger(__name__)

ALLOWED_MIME = {"application/pdf", "text/plain"}
MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


def _validate_upload(file: UploadFile):
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(status_code=415, detail="Only PDF or plain-text files are accepted")


@router.post("/grades")
async def upload_grades(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """Upload a grade PDF for parsing. (Stub)"""
    _validate_upload(file)
    # TODO: read file bytes, call pdf_service.parse_grades_pdf, persist to Supabase
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/timetable")
async def upload_timetable(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """Upload a timetable PDF for parsing. (Stub)"""
    _validate_upload(file)
    # TODO: read file bytes, call pdf_service.parse_timetable_pdf, persist to Supabase
    raise HTTPException(status_code=501, detail="Not implemented yet")
