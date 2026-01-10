from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
import uuid

from ..database import Base


def generate_uuid():
    return str(uuid.uuid4())


class XPRequest(Base):
    """Solicitacao de gasto de XP - requer aprovacao do Storyteller"""
    __tablename__ = "xp_requests"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    chronicle_id = Column(String(36), ForeignKey("chronicles.id", ondelete="CASCADE"), nullable=False)
    character_id = Column(String(36), ForeignKey("characters.id", ondelete="CASCADE"), nullable=False)
    requester_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # O que o jogador quer comprar
    trait_type = Column(String(50), nullable=False)  # "attribute", "skill", "discipline", "merit", etc.
    trait_name = Column(String(100), nullable=False)  # Nome do trait (ex: "Forca", "Briga")
    trait_category = Column(String(50), nullable=True)  # Categoria opcional (ex: "physical", "clan")
    current_value = Column(Integer, default=0)
    requested_value = Column(Integer, nullable=False)
    xp_cost = Column(Integer, nullable=False)

    # Justificativa do jogador
    justification = Column(Text, nullable=True)

    # Status da solicitacao
    status = Column(String(20), default="pending")  # "pending", "approved", "rejected"
    storyteller_message = Column(Text, nullable=True)
    reviewed_by_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    chronicle = relationship("Chronicle", back_populates="xp_requests")
    character = relationship("Character", back_populates="xp_requests")
    requester = relationship("User", foreign_keys=[requester_id], backref="xp_requests_made")
    reviewer = relationship("User", foreign_keys=[reviewed_by_id], backref="xp_requests_reviewed")

    def __repr__(self):
        return f"<XPRequest {self.trait_name} ({self.current_value}->{self.requested_value}) - {self.status}>"
