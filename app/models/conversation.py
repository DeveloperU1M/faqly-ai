from sqlalchemy import Column, String, DateTime, ForeignKey, UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.session import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    agent_id = Column(
        UUID(as_uuid=True),
        ForeignKey("agents.agent_id"),
        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    title = Column(String, nullable=False)

    agent = relationship("Agent", back_populates="conversations")
    messages = relationship(
        "ConversationMessage",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )