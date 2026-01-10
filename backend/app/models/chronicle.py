from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
import uuid
import secrets

from ..database import Base


def generate_uuid():
    return str(uuid.uuid4())


def generate_invite_code():
    return secrets.token_urlsafe(12)


class Chronicle(Base):
    __tablename__ = "chronicles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    game_version = Column(String(10), nullable=False, default="v5")  # "v5" or "v20"

    # Configuration
    starting_xp = Column(Integer, default=0)

    # Owner (Storyteller)
    storyteller_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Invite
    invite_code = Column(String(20), unique=True, default=generate_invite_code)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    storyteller = relationship("User", back_populates="owned_chronicles")
    members = relationship("ChronicleMember", back_populates="chronicle", cascade="all, delete-orphan")
    characters = relationship("Character", back_populates="chronicle")
    scenes = relationship("Scene", back_populates="chronicle", cascade="all, delete-orphan")
    dice_rolls = relationship("DiceRoll", back_populates="chronicle", cascade="all, delete-orphan")
    game_sessions = relationship("GameSession", back_populates="chronicle", cascade="all, delete-orphan")
    xp_requests = relationship("XPRequest", back_populates="chronicle", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="chronicle", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Chronicle {self.name} ({self.game_version})>"


class ChronicleMember(Base):
    __tablename__ = "chronicle_members"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    chronicle_id = Column(String(36), ForeignKey("chronicles.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False, default="player")  # "storyteller" or "player"

    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    chronicle = relationship("Chronicle", back_populates="members")
    user = relationship("User", back_populates="chronicle_memberships")

    def __repr__(self):
        return f"<ChronicleMember {self.user_id} in {self.chronicle_id} as {self.role}>"
