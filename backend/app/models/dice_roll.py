from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
import uuid

from ..database import Base


def generate_uuid():
    return str(uuid.uuid4())


class DiceRoll(Base):
    __tablename__ = "dice_rolls"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    # Relations
    chronicle_id = Column(String(36), ForeignKey("chronicles.id", ondelete="CASCADE"), nullable=True)
    character_id = Column(String(36), ForeignKey("characters.id", ondelete="SET NULL"), nullable=True)
    roller_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Roll info
    game_version = Column(String(10), nullable=False)  # "v5" or "v20"
    roll_type = Column(String(50), nullable=True)  # "standard", "rouse", "frenzy", "remorse"
    description = Column(Text, nullable=True)

    # Dice data
    pool = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=True)
    hunger = Column(Integer, default=0)

    # Results stored as JSON
    result = Column(JSON, nullable=False, default=dict)

    # Computed results
    successes = Column(Integer, nullable=False, default=0)

    # V5 specific
    is_critical = Column(Boolean, default=False)
    is_messy_critical = Column(Boolean, default=False)
    is_bestial_failure = Column(Boolean, default=False)

    # V20 specific
    is_botch = Column(Boolean, default=False)

    # Meta
    is_secret = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    chronicle = relationship("Chronicle", back_populates="dice_rolls")
    character = relationship("Character", back_populates="dice_rolls")
    roller = relationship("User", back_populates="dice_rolls")

    def __repr__(self):
        return f"<DiceRoll {self.pool}d10 = {self.successes} successes>"
