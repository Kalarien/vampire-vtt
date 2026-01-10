from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SessionStart(BaseModel):
    name: Optional[str] = None
    notes: Optional[str] = None


class SessionEnd(BaseModel):
    notes: Optional[str] = None
    xp_amount: int = 0
    xp_description: str = "XP de sessao"


class SessionJoin(BaseModel):
    character_id: str


class SessionParticipantResponse(BaseModel):
    id: str
    character_id: str
    character_name: str
    user_id: str
    username: str
    joined_at: datetime
    left_at: Optional[datetime] = None
    xp_received: int = 0

    class Config:
        from_attributes = True


class SessionResponse(BaseModel):
    id: str
    chronicle_id: str
    name: Optional[str]
    number: Optional[int]
    notes: Optional[str]
    started_at: datetime
    ended_at: Optional[datetime]
    is_active: bool
    active_scene_id: Optional[str]
    xp_awarded: int
    started_by_id: str
    started_by_name: str
    participants: List[SessionParticipantResponse] = []

    class Config:
        from_attributes = True


class SessionListResponse(BaseModel):
    id: str
    chronicle_id: str
    name: Optional[str]
    number: Optional[int]
    started_at: datetime
    ended_at: Optional[datetime]
    is_active: bool
    xp_awarded: int
    participant_count: int = 0

    class Config:
        from_attributes = True
