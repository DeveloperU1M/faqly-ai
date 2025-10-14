from sqlalchemy.orm import Session
from app.models.knowledge_section import KnowledgeSection
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
    return (
        db.query(KnowledgeSection)
        .filter(KnowledgeSection.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )