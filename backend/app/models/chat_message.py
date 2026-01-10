from sqlalchemy import Column, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
import uuid

from ..database import Base


def generate_uuid():
    return str(uuid.uuid4())


class ChatMessage(Base):
    """Mensagem de chat persistente"""
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    chronicle_id = Column(String(36), ForeignKey("chronicles.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(String(36), ForeignKey("game_sessions.id", ondelete="SET NULL"), nullable=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    character_id = Column(String(36), ForeignKey("characters.id", ondelete="SET NULL"), nullable=True)

    # Conteudo da mensagem
    message_type = Column(String(20), default="chat")  # "chat", "action", "whisper", "ooc", "system"
    content = Column(Text, nullable=False)

    # Para sussurros (whisper)
    recipient_id = Column(String(36), ForeignKey("users.id"), nullable=True)

    # Cache de nomes para exibicao (evita joins)
    sender_name = Column(String(255), nullable=True)
    character_name = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    chronicle = relationship("Chronicle", back_populates="chat_messages")
    session = relationship("GameSession", back_populates="chat_messages")
    user = relationship("User", foreign_keys=[user_id], backref="chat_messages_sent")
    character = relationship("Character", backref="chat_messages")
    recipient = relationship("User", foreign_keys=[recipient_id], backref="chat_messages_received")

    def __repr__(self):
        return f"<ChatMessage [{self.message_type}] {self.content[:30]}...>"
