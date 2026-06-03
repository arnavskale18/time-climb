# app/models/task_models.py
from pydantic import BaseModel, Field
from enum import Enum
from datetime import date, datetime


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
    subject_id: str
    title: str
    description: str | None = None
    due_date: date
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.medium
    estimated_minutes: int = Field(default=30, ge=5, le=480)
    ai_generated: bool = False
    completed_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TaskCreateRequest(BaseModel):
    subject_id: str
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    due_date: date
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.medium
    estimated_minutes: int = Field(default=30, ge=5, le=480)


class TaskUpdateRequest(BaseModel):
    subject_id: str | None = None
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    due_date: date | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    estimated_minutes: int | None = Field(default=None, ge=5, le=480)


class TaskStatusUpdateRequest(BaseModel):
    status: TaskStatus


class TaskGenerateRequest(BaseModel):
    target_date: date
    subjects: list[str] | None = None   # None = use all subjects
    max_tasks: int = Field(default=5, ge=1, le=20)

