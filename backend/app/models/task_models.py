# app/models/task_models.py
from pydantic import BaseModel, Field
from enum import Enum
from datetime import date


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    skipped = "skipped"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Task(BaseModel):
    id: str
    user_id: str
    subject: str
    title: str
    description: str | None = None
    due_date: date
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.medium
    estimated_minutes: int = Field(default=30, ge=5, le=480)
    ai_generated: bool = False


class TaskUpdateRequest(BaseModel):
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    estimated_minutes: int | None = Field(default=None, ge=5, le=480)


class TaskGenerateRequest(BaseModel):
    target_date: date
    subjects: list[str] | None = None   # None = use all subjects
    max_tasks: int = Field(default=5, ge=1, le=20)
