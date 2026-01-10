from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class CharacterBase(BaseModel):
    name: str
    game_version: str = "v5"
    chronicle_id: Optional[str] = None


class CharacterCreate(CharacterBase):
    sheet: Optional[Dict[str, Any]] = None


class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    sheet: Optional[Dict[str, Any]] = None
    chronicle_id: Optional[str] = None


class CharacterResponse(CharacterBase):
    id: str
    owner_id: str
    sheet: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CharacterListResponse(BaseModel):
    id: str
    name: str
    game_version: str
    chronicle_id: Optional[str] = None
    sheet: Dict[str, Any] = {}
    created_at: datetime

    class Config:
        from_attributes = True


# V5 Character Sheet Schema
class CharacterSheetV5(BaseModel):
    # Header
    concept: Optional[str] = None
    clan: Optional[str] = None
    sire: Optional[str] = None
    generation: int = 13
    predator_type: Optional[str] = None
    ambition: Optional[str] = None
    desire: Optional[str] = None

    # Attributes
    attributes: Dict[str, int] = {
        "strength": 1, "dexterity": 1, "stamina": 1,
        "charisma": 1, "manipulation": 1, "composure": 1,
        "intelligence": 1, "wits": 1, "resolve": 1,
    }

    # Skills
    skills: Dict[str, int] = {}

    # Disciplines
    disciplines: Dict[str, Dict[str, Any]] = {}

    # Trackers
    health: Dict[str, Any] = {"max": 3, "boxes": {}}
    willpower: Dict[str, Any] = {"max": 3, "boxes": {}}
    hunger: int = 1
    humanity: int = 7
    blood_potency: int = 1

    # Other
    merits: List[Dict[str, Any]] = []
    flaws: List[Dict[str, Any]] = []
    backgrounds: List[Dict[str, Any]] = []
    notes: Optional[str] = None


# V20 Character Sheet Schema
class CharacterSheetV20(BaseModel):
    # Header
    concept: Optional[str] = None
    clan: Optional[str] = None
    sire: Optional[str] = None
    nature: Optional[str] = None
    demeanor: Optional[str] = None
    generation: int = 13

    # Attributes
    attributes: Dict[str, int] = {
        "strength": 1, "dexterity": 1, "stamina": 1,
        "charisma": 1, "manipulation": 1, "appearance": 1,
        "perception": 1, "intelligence": 1, "wits": 1,
    }

    # Abilities
    abilities: Dict[str, int] = {}

    # Disciplines
    disciplines: Dict[str, Dict[str, Any]] = {}

    # Backgrounds
    backgrounds: Dict[str, Dict[str, Any]] = {}

    # Virtues
    virtues: Dict[str, int] = {
        "conscience": 1,
        "self_control": 1,
        "courage": 1,
    }

    # Trackers
    health: Dict[str, str] = {}
    willpower: Dict[str, int] = {"permanent": 3, "temporary": 3}
    blood_pool: Dict[str, int] = {"current": 10, "max": 10}
    humanity: int = 7

    # Experience
    experience: Dict[str, int] = {"total": 0, "current": 0}

    # Other
    merits: List[Dict[str, Any]] = []
    flaws: List[Dict[str, Any]] = []
    notes: Optional[str] = None
