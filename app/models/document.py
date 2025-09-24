from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class Document(Base):
    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String, nullable=False)  # ruta en el servidor o bucket
    file_type = Column(String, nullable=False)  # pdf, docx, txt, etc.
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # relaciones
    section_id = Column(Integer, ForeignKey("knowledge_sections.knowledge_section_id"))
    section = relationship("KnowledgeSection", back_populates="documents")

    uploaded_by = Column(Integer, ForeignKey("users.id"))
    uploader = relationship("User", back_populates="documents")
