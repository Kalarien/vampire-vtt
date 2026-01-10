from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
import uuid

from ..database import Base


def generate_uuid():
    return str(uuid.uuid4())


class GameSession(Base):
    """Sessao de jogo formal com inicio e fim"""
    __tablename__ = "game_sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    chronicle_id = Column(String(36), ForeignKey("chronicles.id", ondelete="CASCADE"), nullable=False)

    # Informacoes da sessao
    name = Column(String(255), nullable=True)  # Titulo opcional (ex: "Sessao 15 - O Ritual")
    number = Column(Integer, nullable=True)  # Numero da sessao
    notes = Column(Text, nullable=True)  # Notas do Storyteller

    # Timing
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)

    # Estado atual
    active_scene_id = Column(String(36), ForeignKey("scenes.id", ondelete="SET NULL"), nullable=True)

    # XP concedido ao final
    xp_awarded = Column(Integer, default=0)

    # Quem iniciou
    started_by_id = Column(String(36), ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    chronicle = relationship("Chronicle", back_populates="game_sessions")
    active_scene = relationship("Scene", foreign_keys=[active_scene_id])
    started_by = relationship("User", backref="sessions_started")
    participants = relationship("SessionParticipant", back_populates="session", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    initiative_orders = relationship("InitiativeOrder", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        status = "Ativa" if self.is_active else "Encerrada"
        return f"<GameSession {self.name or 'Sem nome'} - {status}>"
