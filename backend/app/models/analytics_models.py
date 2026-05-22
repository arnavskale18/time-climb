# app/models/analytics_models.py
from pydantic import BaseModel


class SubjectPerformance(BaseModel):
    subject: str
    average_grade: float
    tasks_completed: int
    tasks_total: int
    completion_rate: float       # 0.0 – 1.0
    trend: str                   # "improving" | "declining" | "stable"


class WeeklyStats(BaseModel):
    week_start: str
    tasks_completed: int
    tasks_total: int
    study_minutes: int


class AnalyticsOverview(BaseModel):
    total_tasks: int
    completed_tasks: int
    overall_completion_rate: float
    weak_subjects: list[str]
    subject_performance: list[SubjectPerformance]
    weekly_stats: list[WeeklyStats]
