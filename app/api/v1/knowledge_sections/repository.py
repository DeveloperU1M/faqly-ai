from sqlalchemy.orm import Session
from app.models.knowledge_section import KnowledgeSection
from app.models.document import Document
from sqlalchemy import func
import uuid
def create_section(db: Session, name: str, description: str, user_id: str) -> KnowledgeSection:
    new_section = KnowledgeSection(
        name=name,
        description=description,
        user_id=user_id
    )
    db.add(new_section)
    db.commit()
    db.refresh(new_section)
    return new_section

def get_sections(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 10):
    query = (
        db.query(
            KnowledgeSection,
            func.count(Document.document_id).label("document_count")
        )
        .outerjoin(Document, Document.section_id == KnowledgeSection.knowledge_section_id)
        .filter(KnowledgeSection.user_id == user_id)
        .group_by(KnowledgeSection.knowledge_section_id)
        .offset(skip)
        .limit(limit)
    )

    results = query.all()

    # Puedes retornar una lista de diccionarios más limpia si lo prefieres
    sections = [
        {
            "knowledge_section_id": section.knowledge_section_id,
            "name": section.name,
            "description": section.description,
            "created_at": section.created_at,
            "updated_at": section.updated_at,
            "document_count": document_count
        }
        for section, document_count in results
    ]

    return sections
