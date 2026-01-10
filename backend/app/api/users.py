from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .deps import get_current_user

router = APIRouter()


@router.get("/me")
async def get_current_user_profile(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user profile"""
    # TODO: Implement properly
    return current_user


@router.patch("/me")
async def update_current_user(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user profile"""
    # TODO: Implement
    raise HTTPException(status_code=501, detail="Not implemented")
