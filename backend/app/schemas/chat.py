from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatMessageCreate(BaseModel):
    content: str
    message_type: str = "chat"  # "chat", "action", "whisper", "ooc", "system"
    character_id: Optional[str] = None
    recipient_id: Optional[str] = None  # For whispers


class ChatMessageResponse(BaseModel):
    id: str
    chronicle_id: str
    session_id: Optional[str]
    user_id: str
    character_id: Optional[str]
    message_type: str
    content: str
    recipient_id: Optional[str]
    sender_name: str
    character_name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
