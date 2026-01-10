from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class XPRequestCreate(BaseModel):
    character_id: str
    trait_type: str  # "attribute", "skill", "discipline", etc.
    trait_name: str
    trait_category: Optional[str] = None
    current_value: int = 0
    requested_value: int
    xp_cost: int
    justification: Optional[str] = None


class XPRequestResponse(BaseModel):
    id: str
    chronicle_id: str
    character_id: str
    character_name: str
    requester_id: str
    requester_name: str
    trait_type: str
    trait_name: str
    trait_category: Optional[str]
    current_value: int
    requested_value: int
    xp_cost: int
    justification: Optional[str]
    status: str
    storyteller_message: Optional[str]
    reviewed_by_id: Optional[str]
    reviewed_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class XPApproveRequest(BaseModel):
    message: Optional[str] = None


class XPRejectRequest(BaseModel):
    message: Optional[str] = None


class XPAwardRequest(BaseModel):
    character_id: str
    amount: int
    description: str
    session_id: Optional[str] = None


class XPLogResponse(BaseModel):
    id: str
    character_id: str
    chronicle_id: Optional[str]
    session_id: Optional[str]
    change_type: str
    amount: int
    previous_total: int
    new_total: int
    description: str
    trait_affected: Optional[str]
    performed_by_name: str
    created_at: datetime

    class Config:
        from_attributes = True
