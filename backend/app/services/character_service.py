from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterUpdate


class CharacterService:
    """Service for handling character operations"""

    @staticmethod
    def get_default_sheet_v5() -> dict:
        """Get default V5 character sheet structure"""
        return {
            "concept": "",
            "clan": "",
            "sire": "",
            "generation": 13,
            "predator_type": "",
            "ambition": "",
            "desire": "",
            "attributes": {
                "strength": 1, "dexterity": 1, "stamina": 1,
                "charisma": 1, "manipulation": 1, "composure": 1,
                "intelligence": 1, "wits": 1, "resolve": 1,
            },
            "skills": {},
            "disciplines": {},
            "health": {"max": 3, "superficial": 0, "aggravated": 0},
            "willpower": {"max": 3, "superficial": 0, "aggravated": 0},
            "hunger": 1,
            "humanity": 7,
            "blood_potency": 1,
            "merits": [],
            "flaws": [],
            "backgrounds": [],
            "notes": "",
        }

    @staticmethod
    def get_default_sheet_v20() -> dict:
        """Get default V20 character sheet structure"""
        return {
            "concept": "",
            "clan": "",
            "sire": "",
            "nature": "",
            "demeanor": "",
            "generation": 13,
            "attributes": {
                "strength": 1, "dexterity": 1, "stamina": 1,
                "charisma": 1, "manipulation": 1, "appearance": 1,
                "perception": 1, "intelligence": 1, "wits": 1,
            },
            "abilities": {},
            "disciplines": {},
            "backgrounds": {},
            "virtues": {
                "conscience": 1,
                "self_control": 1,
                "courage": 1,
            },
            "health": {
                "bruised": "",
                "hurt": "",
                "injured": "",
                "wounded": "",
                "mauled": "",
                "crippled": "",
                "incapacitated": "",
            },
            "willpower": {"permanent": 3, "temporary": 3},
            "blood_pool": {"current": 10, "max": 10},
            "humanity": 7,
            "experience": {"total": 0, "current": 0},
            "merits": [],
            "flaws": [],
            "notes": "",
        }

    @staticmethod
    async def create_character(
        db: AsyncSession,
        owner_id: str,
        data: CharacterCreate
    ) -> Character:
        """Create a new character"""
        # Get default sheet based on game version
        default_sheet = (
            CharacterService.get_default_sheet_v5()
            if data.game_version == "v5"
            else CharacterService.get_default_sheet_v20()
        )

        # Merge with provided sheet data
        sheet = {**default_sheet, **(data.sheet or {})}

        character = Character(
            name=data.name,
            owner_id=owner_id,
            chronicle_id=data.chronicle_id,
            game_version=data.game_version,
            sheet=sheet,
        )
        db.add(character)
        await db.commit()
        await db.refresh(character)
        return character

    @staticmethod
    async def get_character(
        db: AsyncSession,
        character_id: str
    ) -> Optional[Character]:
        """Get character by ID"""
        result = await db.execute(
            select(Character).where(Character.id == character_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_characters(
        db: AsyncSession,
        user_id: str
    ) -> List[Character]:
        """Get all characters owned by a user"""
        result = await db.execute(
            select(Character)
            .where(Character.owner_id == user_id)
            .order_by(Character.updated_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_chronicle_characters(
        db: AsyncSession,
        chronicle_id: str
    ) -> List[Character]:
        """Get all characters in a chronicle"""
        result = await db.execute(
            select(Character)
            .where(Character.chronicle_id == chronicle_id)
            .order_by(Character.name)
        )
        return list(result.scalars().all())

    @staticmethod
    async def update_character(
        db: AsyncSession,
        character: Character,
        data: CharacterUpdate
    ) -> Character:
        """Update character"""
        if data.name is not None:
            character.name = data.name
        if data.sheet is not None:
            # Merge sheets to preserve structure
            character.sheet = {**character.sheet, **data.sheet}
        if data.chronicle_id is not None:
            character.chronicle_id = data.chronicle_id

        await db.commit()
        await db.refresh(character)
        return character

    @staticmethod
    async def delete_character(
        db: AsyncSession,
        character: Character
    ) -> None:
        """Delete character"""
        await db.delete(character)
        await db.commit()


character_service = CharacterService()
