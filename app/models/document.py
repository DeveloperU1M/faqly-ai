import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.session import Base
from sqlalchemy import Enum

class Document(Base):
    __tablename__ = "documents"

    document_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(BigInteger, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Nueva columna
    status = Column(
        String,
        default="pending",
        nullable=False
    )
    # Si prefieres un Enum:
    # status = Column(Enum("pending", "processing", "ready", "failed", name="document_status"), default="pending", nullable=False)

    section_id = Column(UUID(as_uuid=True), ForeignKey("knowledge_sections.knowledge_section_id"))
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))

    section = relationship("KnowledgeSection", back_populates="documents")
    uploader = relationship("User", back_populates="documents")

