# app/utils/logger.py
import logging
import sys
from app.config.settings import get_settings

_settings = get_settings()

def get_logger(name: str) -> logging.Logger:
    """Returns a named logger with consistent formatting."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        level = logging.DEBUG if not _settings.is_production else logging.INFO
        fmt = logging.Formatter(
            "[%(asctime)s] %(levelname)s %(name)s — %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        logger.setLevel(level)

    return logger
