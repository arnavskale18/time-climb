# app/models/subject_models.py
from pydantic import BaseModel, Field
from datetime import datetime


class SubjectCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class Subject(BaseModel):
    id: str
    user_id: str
    name: str
    created_at: datetime | None = None
