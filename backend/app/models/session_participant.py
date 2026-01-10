from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
import uuid

from ..database import Base


def generate_uuid():
    return str(uuid.uuid4())


class SessionParticipant(Base):
    """Participante de uma sessao de jogo"""
    __tablename__ = "session_participants"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    session_id = Column(String(36), ForeignKey("game_sessions.id", ondelete="CASCADE"), nullable=False)
    character_id = Column(String(36), ForeignKey("characters.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    left_at = Column(DateTime(timezone=True), nullable=True)

    # XP individual recebido nesta sessao
    xp_received = Column(Integer, default=0)

    # Relationships
    session = relationship("GameSession", back_populates="participants")
    character = relationship("Character", backref="session_participations")
    user = relationship("User", backref="session_participations")

    def __repr__(self):
        return f"<SessionParticipant {self.character_id} in {self.session_id}>"
