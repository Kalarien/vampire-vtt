from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship
import uuid

from ..database import Base


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    discord_id = Column(String(100), unique=True, nullable=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=True)  # For email/password login
    avatar = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    owned_chronicles = relationship("Chronicle", back_populates="storyteller", cascade="all, delete-orphan")
    chronicle_memberships = relationship("ChronicleMember", back_populates="user", cascade="all, delete-orphan")
    characters = relationship("Character", back_populates="owner", cascade="all, delete-orphan")
    dice_rolls = relationship("DiceRoll", back_populates="roller", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"
