from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .user import UserPublic


class ChronicleBase(BaseModel):
    name: str
    description: Optional[str] = None
    game_version: str = "v5"


class ChronicleCreate(ChronicleBase):
    pass


class ChronicleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ChronicleMemberResponse(BaseModel):
    user_id: str
    username: Optional[str] = None
    role: str
    joined_at: datetime

    class Config:
        from_attributes = True


class ChronicleResponse(ChronicleBase):
    id: str
    storyteller_id: str
    created_at: datetime
    updated_at: datetime
    members: List[ChronicleMemberResponse] = []

    class Config:
        from_attributes = True


class ChronicleListResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    game_version: str
    storyteller_id: str
    created_at: datetime
    members_count: int = 0

    class Config:
        from_attributes = True
