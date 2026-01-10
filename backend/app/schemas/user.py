from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None


class UserCreate(UserBase):
    discord_id: str
    avatar: Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None


class UserResponse(UserBase):
    id: str
    discord_id: str
    avatar: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserPublic(BaseModel):
    id: str
    username: str
    avatar: Optional[str] = None

    class Config:
        from_attributes = True
