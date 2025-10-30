from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.database.session import Base
import uuid
from app.models.agent import agent_sections

class KnowledgeSection(Base):
    __tablename__ = "knowledge_sections"

    knowledge_section_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)

    user = relationship("User", back_populates="knowledge_sections")

    # relación con documentos
    documents = relationship("Document", back_populates="section")
    agents = relationship("Agent", secondary=agent_sections, back_populates="sections")