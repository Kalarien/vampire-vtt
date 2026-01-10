from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
import uuid

from ..database import Base


def generate_uuid():
    return str(uuid.uuid4())


class XPLog(Base):
    """Historico de todas as alteracoes de XP de um personagem"""
    __tablename__ = "xp_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    character_id = Column(String(36), ForeignKey("characters.id", ondelete="CASCADE"), nullable=False)
    chronicle_id = Column(String(36), ForeignKey("chronicles.id", ondelete="SET NULL"), nullable=True)
    session_id = Column(String(36), ForeignKey("game_sessions.id", ondelete="SET NULL"), nullable=True)

    # Tipo de alteracao
    change_type = Column(String(20), nullable=False)  # "award", "spend", "refund", "adjustment"
    amount = Column(Integer, nullable=False)  # positivo = ganho, negativo = gasto
    previous_total = Column(Integer, nullable=False)
    new_total = Column(Integer, nullable=False)

    # Detalhes
    description = Column(Text, nullable=False)
    trait_affected = Column(String(100), nullable=True)  # O que foi melhorado
    xp_request_id = Column(String(36), ForeignKey("xp_requests.id", ondelete="SET NULL"), nullable=True)

    performed_by_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    character = relationship("Character", back_populates="xp_logs")
    chronicle = relationship("Chronicle", backref="xp_logs")
    session = relationship("GameSession", backref="xp_logs")
    xp_request = relationship("XPRequest", backref="xp_log")
    performed_by = relationship("User", backref="xp_actions")

    def __repr__(self):
        return f"<XPLog {self.change_type} {self.amount:+d} XP>"
