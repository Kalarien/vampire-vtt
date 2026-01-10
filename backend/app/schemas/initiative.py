from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class InitiativeStart(BaseModel):
    name: Optional[str] = None


class InitiativeEntryAdd(BaseModel):
    character_id: Optional[str] = None
    character_name: str
    initiative_value: int = 0
    initiative_modifier: int = 0
    is_npc: bool = False


class InitiativeEntryUpdate(BaseModel):
    initiative_value: Optional[int] = None
    has_acted: Optional[bool] = None
    is_delayed: Optional[bool] = None


class InitiativeEntryResponse(BaseModel):
    id: str
    order_id: str
    character_id: Optional[str]
    character_name: str
    initiative_value: int
    initiative_modifier: int
    is_npc: bool
    has_acted: bool
    is_delayed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class InitiativeOrderResponse(BaseModel):
    id: str
    session_id: str
    name: Optional[str]
    is_active: bool
    current_round: int
    current_turn_index: int
    entries: List[InitiativeEntryResponse] = []
    created_at: datetime
    ended_at: Optional[datetime]

    class Config:
        from_attributes = True
