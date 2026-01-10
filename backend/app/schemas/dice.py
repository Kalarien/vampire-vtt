from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# V5 Dice Schemas
class DiceRollV5Request(BaseModel):
    pool: int = Field(..., ge=1, le=30, description="Number of dice to roll")
    hunger: int = Field(default=0, ge=0, le=5, description="Hunger dice")
    difficulty: int = Field(default=1, ge=1, le=10, description="Required successes")
    character_id: Optional[str] = None
    description: Optional[str] = None


class DiceRollV5Response(BaseModel):
    pool: int
    hunger: int
    difficulty: int
    regular_dice: List[int]
    hunger_dice: List[int]
    successes: int
    is_success: bool
    is_critical: bool
    is_messy_critical: bool
    is_bestial_failure: bool
    margin: int
    description: Optional[str] = None


class RouseCheckRequest(BaseModel):
    reroll: bool = False
    character_id: Optional[str] = None


class RouseCheckResponse(BaseModel):
    dice: List[int]
    success: bool  # True = no hunger gain
    hunger_gain: int
    rerolled: bool


class FrenzyCheckRequest(BaseModel):
    willpower: int = Field(..., ge=0, le=10)
    humanity: int = Field(..., ge=0, le=10)
    difficulty: int = Field(default=3, ge=1, le=10)
    character_id: Optional[str] = None


class FrenzyCheckResponse(BaseModel):
    pool: int
    difficulty: int
    dice: List[int]
    successes: int
    resisted: bool


class RemorseCheckRequest(BaseModel):
    humanity: int = Field(..., ge=0, le=10)
    stains: int = Field(..., ge=0, le=10)
    character_id: Optional[str] = None


class RemorseCheckResponse(BaseModel):
    pool: int
    dice: List[int]
    successes: int
    humanity_lost: bool
    new_humanity: int


# V20 Dice Schemas
class DiceRollV20Request(BaseModel):
    pool: int = Field(..., ge=1, le=30, description="Number of dice to roll")
    difficulty: int = Field(default=6, ge=2, le=10, description="Target number")
    specialty: bool = Field(default=False, description="Reroll 10s")
    character_id: Optional[str] = None
    description: Optional[str] = None


class DiceRollV20Response(BaseModel):
    pool: int
    difficulty: int
    specialty: bool
    dice: List[int]
    successes: int
    is_success: bool
    is_botch: bool
    ones_count: int
    tens_count: int
    description: Optional[str] = None


# Stored Dice Roll
class DiceRollStored(BaseModel):
    id: str
    character_id: Optional[str]
    chronicle_id: Optional[str]
    roller_id: str
    game_version: str
    roll_type: str
    dice_pool: int
    difficulty: int
    result: dict
    created_at: datetime

    class Config:
        from_attributes = True
