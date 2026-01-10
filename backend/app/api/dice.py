from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from pydantic import BaseModel

from ..database import get_db
from .deps import get_current_user
from ..core.v5.dice import V5DiceRoller
from ..core.v20.dice import V20DiceRoller

router = APIRouter()


class V5RollRequest(BaseModel):
    pool: int
    hunger: int = 0
    difficulty: int = 1
    description: Optional[str] = None
    chronicle_id: Optional[str] = None
    character_id: Optional[str] = None
    is_secret: bool = False


class V20RollRequest(BaseModel):
    pool: int
    difficulty: int = 6
    specialty: bool = False
    description: Optional[str] = None
    chronicle_id: Optional[str] = None
    character_id: Optional[str] = None
    is_secret: bool = False


class RouseCheckRequest(BaseModel):
    reroll: bool = False
    chronicle_id: Optional[str] = None
    character_id: Optional[str] = None


class FrenzyCheckRequest(BaseModel):
    willpower: int
    humanity: int
    difficulty: int = 3
    chronicle_id: Optional[str] = None
    character_id: Optional[str] = None


class RemorseCheckRequest(BaseModel):
    humanity: int
    stains: int
    chronicle_id: Optional[str] = None
    character_id: Optional[str] = None


@router.post("/v5/roll")
async def roll_v5(
    roll_request: V5RollRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Roll dice using V5 rules"""
    result = V5DiceRoller.roll(
        pool=roll_request.pool,
        hunger=roll_request.hunger,
        difficulty=roll_request.difficulty,
    )

    # TODO: Save to database and broadcast via WebSocket

    return {
        "regular_dice": result.regular_dice,
        "hunger_dice": result.hunger_dice,
        "difficulty": result.difficulty,
        "successes": result.successes,
        "regular_tens": result.regular_tens,
        "hunger_tens": result.hunger_tens,
        "hunger_ones": result.hunger_ones,
        "critical_pairs": result.critical_pairs,
        "result_type": result.result_type.value,
        "margin": result.margin,
        "description": roll_request.description,
    }


@router.post("/v5/rouse")
async def rouse_check(
    request: RouseCheckRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Perform a Rouse Check"""
    success, dice = V5DiceRoller.rouse_check(reroll=request.reroll)

    return {
        "success": success,
        "dice": dice,
        "hunger_increase": 0 if success else 1,
    }


@router.post("/v5/frenzy")
async def frenzy_check(
    request: FrenzyCheckRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Perform a Frenzy Check"""
    result = V5DiceRoller.frenzy_check(
        willpower=request.willpower,
        humanity=request.humanity,
        difficulty=request.difficulty,
    )

    return {
        "dice": result.regular_dice,
        "successes": result.successes,
        "difficulty": result.difficulty,
        "success": result.margin >= 0,
        "margin": result.margin,
    }


@router.post("/v5/remorse")
async def remorse_check(
    request: RemorseCheckRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Perform a Remorse Check"""
    success, roll = V5DiceRoller.remorse_check(
        humanity=request.humanity,
        stains=request.stains,
    )

    return {
        "dice": roll.regular_dice,
        "successes": roll.successes,
        "success": success,
        "humanity_loss": 0 if success else 1,
    }


@router.post("/v20/roll")
async def roll_v20(
    roll_request: V20RollRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Roll dice using V20 rules"""
    result = V20DiceRoller.roll(
        pool=roll_request.pool,
        difficulty=roll_request.difficulty,
        specialty=roll_request.specialty,
    )

    return {
        "dice": result.dice,
        "difficulty": result.difficulty,
        "successes": result.successes,
        "ones": result.ones,
        "tens": result.tens,
        "result_type": result.result_type.value,
        "description": roll_request.description,
    }


@router.get("/history/{chronicle_id}")
async def get_roll_history(
    chronicle_id: str,
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get roll history for a chronicle"""
    # TODO: Implement
    return []
