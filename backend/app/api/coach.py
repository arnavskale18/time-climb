# app/api/coach.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.middlewares.auth_middleware import get_current_user
from app.utils.logger import get_logger

router = APIRouter(prefix="/coach", tags=["Coach"])
logger = get_logger(__name__)


class ChatMessage(BaseModel):
    message: str
    history: list[dict] = []   # [{"role": "user"|"assistant", "content": "..."}]


class ChatResponse(BaseModel):
    reply: str
    conversation_id: str | None = None


@router.post("/chat", response_model=ChatResponse)
async def coach_chat(body: ChatMessage, current_user: dict = Depends(get_current_user)):
    """Send a message to the AI study coach. (Stub)"""
    # TODO: call gemini_service.coach_reply, persist to ai_conversations
    raise HTTPException(status_code=501, detail="Not implemented yet")
