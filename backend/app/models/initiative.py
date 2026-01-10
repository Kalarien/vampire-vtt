from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
import uuid

from ..database import Base


def generate_uuid():
    return str(uuid.uuid4())


class InitiativeOrder(Base):
    """Ordem de iniciativa/combate"""
    __tablename__ = "initiative_orders"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    session_id = Column(String(36), ForeignKey("game_sessions.id", ondelete="CASCADE"), nullable=False)

    # Estado do combate
    is_active = Column(Boolean, default=True)
    current_round = Column(Integer, default=1)
    current_turn_index = Column(Integer, default=0)

    # Nome do combate (opcional)
    name = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    session = relationship("GameSession", back_populates="initiative_orders")
    entries = relationship(
        "InitiativeEntry",
        back_populates="order",
        cascade="all, delete-orphan",
        order_by="desc(InitiativeEntry.initiative_value)"
    )

    def __repr__(self):
        status = "Ativo" if self.is_active else "Encerrado"
        return f"<InitiativeOrder Round {self.current_round} - {status}>"


class InitiativeEntry(Base):
    """Entrada individual na ordem de iniciativa"""
    __tablename__ = "initiative_entries"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    order_id = Column(String(36), ForeignKey("initiative_orders.id", ondelete="CASCADE"), nullable=False)

    # Personagem ou NPC
    character_id = Column(String(36), ForeignKey("characters.id", ondelete="SET NULL"), nullable=True)
    character_name = Column(String(255), nullable=False)  # Cache para NPCs

    # Valor de iniciativa
    initiative_value = Column(Integer, default=0)
    initiative_modifier = Column(Integer, default=0)  # Bonus permanente

    # Estado
    is_npc = Column(Boolean, default=False)
    has_acted = Column(Boolean, default=False)
    is_delayed = Column(Boolean, default=False)  # Segurou a acao

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    order = relationship("InitiativeOrder", back_populates="entries")
    character = relationship("Character", backref="initiative_entries")

    def __repr__(self):
        return f"<InitiativeEntry {self.character_name}: {self.initiative_value}>"
