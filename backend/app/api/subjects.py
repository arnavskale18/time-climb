# app/api/subjects.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.config.supabase import get_supabase
from app.middlewares.auth_middleware import get_current_user
from app.models.subject_models import Subject, SubjectCreateRequest
from app.utils.logger import get_logger

router = APIRouter(prefix="/subjects", tags=["Subjects"])
logger = get_logger(__name__)


@router.get("", response_model=list[Subject])
async def get_subjects(current_user: dict = Depends(get_current_user)):
    """
    Fetch all subjects for the authenticated user.
    """
    try:
        supabase = get_supabase()
        res = supabase.table("subjects").select("*").eq("user_id", current_user["id"]).execute()
        return res.data or []
    except Exception as e:
        logger.error(f"Error fetching subjects: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve subjects"
        )


@router.post("", response_model=Subject, status_code=status.HTTP_201_CREATED)
async def create_subject(
    body: SubjectCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new subject with duplicate protection.
    """
    trimmed_name = body.name.strip()
    if not trimmed_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subject name cannot be empty"
        )

    try:
        supabase = get_supabase()

        # Fetch all subjects for this user to check duplicates case-insensitively
        res = supabase.table("subjects").select("*").eq("user_id", current_user["id"]).execute()
        existing_subjects = res.data or []

        for subject in existing_subjects:
            if subject["name"].strip().lower() == trimmed_name.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Subject '{trimmed_name}' already exists"
                )

        # Insert new subject
        insert_res = supabase.table("subjects").insert({
            "name": trimmed_name,
            "user_id": current_user["id"]
        }).execute()

        if not insert_res.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to insert subject"
            )

        return insert_res.data[0]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating subject: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal database error: {str(e)}"
        )
