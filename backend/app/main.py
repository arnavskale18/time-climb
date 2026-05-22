# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import get_settings
from app.utils.logger import get_logger

# ── API routers ────────────────────────────────────────
from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router
from app.api.analytics import router as analytics_router
from app.api.uploads import router as uploads_router
from app.api.coach import router as coach_router
from app.api.settings_api import router as settings_router

settings = get_settings()
logger = get_logger(__name__)

# ── App init ───────────────────────────────────────────
app = FastAPI(
    title="Time-Climb API",
    version="0.1.0",
    description="Backend for the Time-Climb academic productivity platform.",
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)

# ── CORS ───────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────
API_PREFIX = "/api"

app.include_router(auth_router,      prefix=API_PREFIX)
app.include_router(tasks_router,     prefix=API_PREFIX)
app.include_router(analytics_router, prefix=API_PREFIX)
app.include_router(uploads_router,   prefix=API_PREFIX)
app.include_router(coach_router,     prefix=API_PREFIX)
app.include_router(settings_router,  prefix=API_PREFIX)

# ── Health check ───────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health():
    """Basic liveness probe."""
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}


# ── Startup / shutdown hooks ───────────────────────────
@app.on_event("startup")
async def on_startup():
    logger.info(f"{settings.app_name} starting — env={settings.app_env}")


@app.on_event("shutdown")
async def on_shutdown():
    logger.info(f"{settings.app_name} shutting down")
