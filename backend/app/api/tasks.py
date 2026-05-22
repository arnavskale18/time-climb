# app/api/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from app.models.task_models import Task, TaskUpdateRequest, TaskGenerateRequest
from app.middlewares.auth_middleware import get_current_user
from app.utils.logger import get_logger

router = APIRouter(prefix="/tasks", tags=["Tasks"])
logger = get_logger(__name__)


@router.get("", response_model=list[Task])
async def get_tasks(current_user: dict = Depends(get_current_user)):
    """Fetch all tasks for the authenticated user. (Stub)"""
    # TODO: query supabase tasks table filtered by user_id
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/generate", response_model=list[Task])
async def generate_tasks(body: TaskGenerateRequest, current_user: dict = Depends(get_current_user)):
    """AI-generate a daily study plan. (Stub)"""
    # TODO: call scheduler_service.build_daily_plan
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.patch("/{task_id}", response_model=Task)
async def update_task(task_id: str, body: TaskUpdateRequest, current_user: dict = Depends(get_current_user)):
    """Update task status or priority. (Stub)"""
    # TODO: validate ownership, update row in supabase
    raise HTTPException(status_code=501, detail="Not implemented yet")
