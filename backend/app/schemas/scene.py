from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SceneBase(BaseModel):
    name: str
    description: Optional[str] = None
    location: Optional[str] = None


class SceneCreate(SceneBase):
    pass


class SceneUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None


class SceneResponse(SceneBase):
    id: str
    chronicle_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
