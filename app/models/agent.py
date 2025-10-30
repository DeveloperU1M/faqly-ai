from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Table, JSON, UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database.session import Base

agent_sections = Table(
    "agent_sections",
    Base.metadata,
    Column("agent_id", UUID(as_uuid=True), ForeignKey("agents.agent_id"), primary_key=True),
    Column("section_id", UUID(as_uuid=True), ForeignKey("knowledge_sections.knowledge_section_id"), primary_key=True)
)

class Agent(Base):
    __tablename__ = "agents"

    agent_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    instructions = Column(String, nullable=True)  # prompt base o contexto del agente
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    icon_agent = Column(String, nullable=True)
    # Configuración del modelo (ej. temperatura, modelo LLM, etc.)
    config = Column(JSON, nullable=True)

    # Relación con usuario
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))

    # Relaciones con documentos y secciones
    sections = relationship("KnowledgeSection", secondary=agent_sections, back_populates="agents")
    user = relationship("User", back_populates="agents")

    creator = relationship("User", back_populates="agents")

# Y en Document y KnowledgeSection deberás agregar el back_populates:

# En Document:
#   agents = relationship("Agent", secondary=agent_documents, back_populates="documents")

# En KnowledgeSection:
# agents = relationship("Agent", secondary=agent_sections, back_populates="sections")
