from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, func, JSON
from sqlalchemy.orm import relationship
import uuid

from ..database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Character(Base):
    __tablename__ = "characters"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    concept = Column(String(255), nullable=True)
    clan = Column(String(100), nullable=True)
    generation = Column(Integer, nullable=True)

    # V5 specific
    predator_type = Column(String(100), nullable=True)

    # V20 specific
    nature = Column(String(100), nullable=True)
    demeanor = Column(String(100), nullable=True)

    # Relations
    owner_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    chronicle_id = Column(String(36), ForeignKey("chronicles.id", ondelete="SET NULL"), nullable=True)

    # Game edition
    game_version = Column(String(10), nullable=False, default="v5")  # "v5" or "v20"

    # Full character sheet as JSON
    sheet = Column(JSON, nullable=False, default=dict)

    # Approval system
    approval_status = Column(String(20), default="draft")  # draft, pending, approved, rejected
    pending_sheet = Column(JSON, nullable=True)  # Proposed changes waiting for approval
    storyteller_notes = Column(Text, nullable=True)  # Notes from storyteller on approval/rejection

    # Meta
    is_npc = Column(Boolean, default=False)
    portrait_url = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="characters")
    chronicle = relationship("Chronicle", back_populates="characters")
    dice_rolls = relationship("DiceRoll", back_populates="character")
    xp_requests = relationship("XPRequest", back_populates="character", cascade="all, delete-orphan")
    xp_logs = relationship("XPLog", back_populates="character", cascade="all, delete-orphan")
    change_logs = relationship("SheetChangeLog", back_populates="character", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Character {self.name} ({self.clan})>"


# Default V5 character sheet structure
V5_SHEET_TEMPLATE = {
    "attributes": {
        "physical": {"strength": 1, "dexterity": 1, "stamina": 1},
        "social": {"charisma": 1, "manipulation": 1, "composure": 1},
        "mental": {"intelligence": 1, "wits": 1, "resolve": 1},
    },
    "skills": {
        "physical": {
            "athletics": 0, "brawl": 0, "craft": 0, "drive": 0, "firearms": 0,
            "larceny": 0, "melee": 0, "stealth": 0, "survival": 0,
        },
        "social": {
            "animal_ken": 0, "etiquette": 0, "insight": 0, "intimidation": 0,
            "leadership": 0, "performance": 0, "persuasion": 0, "streetwise": 0, "subterfuge": 0,
        },
        "mental": {
            "academics": 0, "awareness": 0, "finance": 0, "investigation": 0,
            "medicine": 0, "occult": 0, "politics": 0, "science": 0, "technology": 0,
        },
    },
    "specialties": [],
    "disciplines": {},
    "health": {"superficial": 0, "aggravated": 0},
    "willpower": {"superficial": 0, "aggravated": 0},
    "hunger": 1,
    "humanity": 7,
    "stains": 0,
    "blood_potency": 1,
    "advantages": [],
    "flaws": [],
    "touchstones": [],
    "convictions": [],
    "ambition": "",
    "desire": "",
    "experience": {"total": 0, "spent": 0},
}


# Default V20 character sheet structure
V20_SHEET_TEMPLATE = {
    "attributes": {
        "physical": {"strength": 1, "dexterity": 1, "stamina": 1},
        "social": {"charisma": 1, "manipulation": 1, "appearance": 1},
        "mental": {"perception": 1, "intelligence": 1, "wits": 1},
    },
    "abilities": {
        "talents": {
            "alertness": 0, "athletics": 0, "awareness": 0, "brawl": 0, "empathy": 0,
            "expression": 0, "intimidation": 0, "leadership": 0, "streetwise": 0, "subterfuge": 0,
        },
        "skills": {
            "animal_ken": 0, "crafts": 0, "drive": 0, "etiquette": 0, "firearms": 0,
            "larceny": 0, "melee": 0, "performance": 0, "stealth": 0, "survival": 0,
        },
        "knowledges": {
            "academics": 0, "computer": 0, "finance": 0, "investigation": 0, "law": 0,
            "medicine": 0, "occult": 0, "politics": 0, "science": 0, "technology": 0,
        },
    },
    "disciplines": {},
    "backgrounds": {},
    "virtues": {"conscience": 1, "self_control": 1, "courage": 1},
    "health": {"bashing": 0, "lethal": 0, "aggravated": 0},
    "willpower": {"permanent": 1, "temporary": 1},
    "blood_pool": {"current": 10, "max": 10},
    "humanity_or_path": {"name": "Humanity", "value": 7},
    "merits": [],
    "flaws": [],
    "experience": {"total": 0, "spent": 0},
}
