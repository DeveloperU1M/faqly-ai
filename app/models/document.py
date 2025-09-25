from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
class Document(Base):
    __tablename__ = "documents"

    document_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String, nullable=False)  # ruta en el servidor o bucket
    file_type = Column(String, nullable=False)  # pdf, docx, txt, etc.
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    section_id = Column(UUID(as_uuid=True), ForeignKey("knowledge_sections.knowledge_section_id"))
    section = relationship("KnowledgeSection", back_populates="documents")

    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    uploader = relationship("User", back_populates="documents")
