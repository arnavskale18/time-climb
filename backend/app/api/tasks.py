# app/api/tasks.py
from datetime import datetime, timezone
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException, status

from app.config.supabase import get_supabase
from app.models.task_models import (
    Task,
    TaskCreateRequest,
    TaskGenerateRequest,
    TaskStatus,
    TaskStatusUpdateRequest,
    TaskUpdateRequest,
)
from app.middlewares.auth_middleware import get_current_user
from app.utils.logger import get_logger

router = APIRouter(prefix="/tasks", tags=["Tasks"])
logger = get_logger(__name__)


def _serialize_task_payload(payload: dict) -> dict:
    """
    Convert Pydantic payload values into Supabase-friendly JSON values.
    """
    serialized = {}

    for key, value in payload.items():
        if isinstance(value, Enum):
            serialized[key] = value.value
        elif hasattr(value, "isoformat"):
            serialized[key] = value.isoformat()
        else:
            serialized[key] = value

    return serialized


def _completed_at_for_status(status_value: TaskStatus | str | None) -> str | None:
    if status_value == TaskStatus.completed or status_value == TaskStatus.completed.value:
        return datetime.now(timezone.utc).isoformat()
    return None


def _get_owned_subject(subject_id: str, user_id: str) -> dict:
    try:
        supabase = get_supabase()
        res = (
            supabase.table("subjects")
            .select("id")
            .eq("id", subject_id)
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )
    except Exception as e:
        logger.error(f"Error validating subject ownership: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to validate subject ownership",
        )

    if not res.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )

    return res.data[0]


def _get_owned_task(task_id: str, user_id: str) -> dict:
    try:
        supabase = get_supabase()
        res = (
            supabase.table("tasks")
            .select("*")
            .eq("id", task_id)
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )
    except Exception as e:
        logger.error(f"Error validating task ownership: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to validate task ownership",
        )

    if not res.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return res.data[0]


@router.get("", response_model=list[Task])
async def get_tasks(current_user: dict = Depends(get_current_user)):
    """Fetch all tasks for the authenticated user."""
    try:
        supabase = get_supabase()
        res = (
            supabase.table("tasks")
            .select("*")
            .eq("user_id", current_user["id"])
            .order("due_date")
            .order("created_at")
            .execute()
        )
        return res.data or []
    except Exception as e:
        logger.error(f"Error fetching tasks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks",
        )


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    body: TaskCreateRequest,
    current_user: dict = Depends(get_current_user),
):
    """Create a task for the authenticated user."""
    _get_owned_subject(body.subject_id, current_user["id"])

    payload = _serialize_task_payload(body.model_dump())
    payload["user_id"] = current_user["id"]
    payload["completed_at"] = _completed_at_for_status(body.status)

    try:
        supabase = get_supabase()
        res = supabase.table("tasks").insert(payload).execute()

        if not res.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create task",
            )

        return res.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task",
        )


@router.post("/generate", response_model=list[Task])
async def generate_tasks(body: TaskGenerateRequest, current_user: dict = Depends(get_current_user)):
    """AI-generate a daily study plan. (Stub)"""
    # TODO: call scheduler_service.build_daily_plan
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.patch("/{task_id}", response_model=Task)
async def update_task(task_id: str, body: TaskUpdateRequest, current_user: dict = Depends(get_current_user)):
    """Partially update a task owned by the authenticated user."""
    _get_owned_task(task_id, current_user["id"])

    update_payload = body.model_dump(exclude_unset=True)

    if not update_payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No task fields provided",
        )

    if "subject_id" in update_payload:
        _get_owned_subject(update_payload["subject_id"], current_user["id"])

    if "status" in update_payload:
        update_payload["completed_at"] = _completed_at_for_status(update_payload["status"])

    payload = _serialize_task_payload(update_payload)

    try:
        supabase = get_supabase()
        res = (
            supabase.table("tasks")
            .update(payload)
            .eq("id", task_id)
            .eq("user_id", current_user["id"])
            .execute()
        )

        if not res.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return res.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task",
        )


@router.patch("/{task_id}/status", response_model=Task)
async def update_task_status(
    task_id: str,
    body: TaskStatusUpdateRequest,
    current_user: dict = Depends(get_current_user),
):
    """Update task status and manage completion timestamp automatically."""
    _get_owned_task(task_id, current_user["id"])

    payload = {
        "status": body.status.value,
        "completed_at": _completed_at_for_status(body.status),
    }

    try:
        supabase = get_supabase()
        res = (
            supabase.table("tasks")
            .update(payload)
            .eq("id", task_id)
            .eq("user_id", current_user["id"])
            .execute()
        )

        if not res.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return res.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task status",
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a task owned by the authenticated user."""
    _get_owned_task(task_id, current_user["id"])

    try:
        supabase = get_supabase()
        res = (
            supabase.table("tasks")
            .delete()
            .eq("id", task_id)
            .eq("user_id", current_user["id"])
            .execute()
        )

        if not res.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task",
        )
