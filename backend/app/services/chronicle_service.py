from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.models.chronicle import Chronicle, ChronicleMember
from app.models.character import Character
from app.schemas.chronicle import ChronicleCreate, ChronicleUpdate


class ChronicleService:
    """Service for handling chronicle operations"""

    @staticmethod
    async def create_chronicle(
        db: AsyncSession,
        storyteller_id: str,
        data: ChronicleCreate
    ) -> Chronicle:
        """Create a new chronicle"""
        chronicle = Chronicle(
            name=data.name,
            description=data.description,
            game_version=data.game_version,
            storyteller_id=storyteller_id,
        )
        db.add(chronicle)
        await db.flush()

        # Add storyteller as member
        member = ChronicleMember(
            chronicle_id=chronicle.id,
            user_id=storyteller_id,
            role="storyteller",
        )
        db.add(member)

        await db.commit()
        await db.refresh(chronicle)
        return chronicle

    @staticmethod
    async def get_chronicle(
        db: AsyncSession,
        chronicle_id: str,
        include_members: bool = True
    ) -> Optional[Chronicle]:
        """Get chronicle by ID"""
        query = select(Chronicle).where(Chronicle.id == chronicle_id)

        if include_members:
            query = query.options(selectinload(Chronicle.members))

        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_chronicles(
        db: AsyncSession,
        user_id: str
    ) -> List[Chronicle]:
        """Get all chronicles where user is a member"""
        result = await db.execute(
            select(Chronicle)
            .join(ChronicleMember)
            .where(ChronicleMember.user_id == user_id)
            .options(selectinload(Chronicle.members))
            .order_by(Chronicle.updated_at.desc())
        )
        return list(result.scalars().unique().all())

    @staticmethod
    async def update_chronicle(
        db: AsyncSession,
        chronicle: Chronicle,
        data: ChronicleUpdate
    ) -> Chronicle:
        """Update chronicle"""
        if data.name is not None:
            chronicle.name = data.name
        if data.description is not None:
            chronicle.description = data.description

        await db.commit()
        await db.refresh(chronicle)
        return chronicle

    @staticmethod
    async def delete_chronicle(
        db: AsyncSession,
        chronicle: Chronicle
    ) -> None:
        """Delete chronicle and all related data"""
        # Characters will be unlinked (chronicle_id set to null)
        await db.execute(
            select(Character)
            .where(Character.chronicle_id == chronicle.id)
        )
        result = await db.execute(
            select(Character).where(Character.chronicle_id == chronicle.id)
        )
        for char in result.scalars():
            char.chronicle_id = None

        await db.delete(chronicle)
        await db.commit()

    @staticmethod
    async def add_member(
        db: AsyncSession,
        chronicle_id: str,
        user_id: str,
        role: str = "player"
    ) -> ChronicleMember:
        """Add a member to chronicle"""
        # Check if already member
        result = await db.execute(
            select(ChronicleMember)
            .where(ChronicleMember.chronicle_id == chronicle_id)
            .where(ChronicleMember.user_id == user_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            return existing

        member = ChronicleMember(
            chronicle_id=chronicle_id,
            user_id=user_id,
            role=role,
        )
        db.add(member)
        await db.commit()
        await db.refresh(member)
        return member

    @staticmethod
    async def remove_member(
        db: AsyncSession,
        chronicle_id: str,
        user_id: str
    ) -> bool:
        """Remove a member from chronicle"""
        result = await db.execute(
            select(ChronicleMember)
            .where(ChronicleMember.chronicle_id == chronicle_id)
            .where(ChronicleMember.user_id == user_id)
        )
        member = result.scalar_one_or_none()
        if member:
            await db.delete(member)
            await db.commit()
            return True
        return False

    @staticmethod
    async def is_member(
        db: AsyncSession,
        chronicle_id: str,
        user_id: str
    ) -> bool:
        """Check if user is member of chronicle"""
        result = await db.execute(
            select(ChronicleMember)
            .where(ChronicleMember.chronicle_id == chronicle_id)
            .where(ChronicleMember.user_id == user_id)
        )
        return result.scalar_one_or_none() is not None

    @staticmethod
    async def is_storyteller(
        db: AsyncSession,
        chronicle_id: str,
        user_id: str
    ) -> bool:
        """Check if user is storyteller of chronicle"""
        result = await db.execute(
            select(Chronicle)
            .where(Chronicle.id == chronicle_id)
            .where(Chronicle.storyteller_id == user_id)
        )
        return result.scalar_one_or_none() is not None


chronicle_service = ChronicleService()
