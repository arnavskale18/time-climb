# app/utils/prompts.py
# Gemini prompt templates will live here.
# Each prompt is a function that accepts context and returns a formatted string.
# Keep prompts versioned and named clearly.

# Example structure (not implemented yet):
#
# def task_generation_prompt(subjects: list, weak_areas: list, timetable: dict) -> str:
#     ...
#
# def coach_chat_prompt(history: list, user_message: str, profile: dict) -> str:
#     ...

PROMPTS: dict[str, str] = {}  # will be populated per feature
