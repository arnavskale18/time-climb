# app/utils/validators.py
import re


def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.\+\-]+@[\w\-]+\.[a-z]{2,}$"
    return bool(re.match(pattern, email, re.IGNORECASE))


def is_strong_password(password: str) -> bool:
    """Minimum 8 chars, at least one digit and one letter."""
    return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a number between min and max."""
    return max(min_val, min(max_val, value))
