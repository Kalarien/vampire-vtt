from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..database import Base


class SheetChangeLog(Base):
    """Log de alteracoes na ficha feitas pelo Narrador"""
    __tablename__ = "sheet_change_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    character_id = Column(String, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False)
    storyteller_id = Column(String, ForeignKey("users.id"), nullable=False)
    changes = Column(JSON, nullable=False)  # Dict com as mudancas feitas
    reason = Column(Text, nullable=True)  # Motivo da alteracao
    seen = Column(Boolean, default=False)  # Se o jogador ja viu
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    character = relationship("Character", back_populates="change_logs")
    storyteller = relationship("User")
