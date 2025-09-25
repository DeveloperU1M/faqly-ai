from sqlalchemy.orm import Session
from app.models.knowledge_section import KnowledgeSection
from app.api.v1.knowledge_sections.schemas import KnowledgeSectionCreate

def create_section(db: Session, section_in: KnowledgeSectionCreate):
    new_section = KnowledgeSection(
        name=section_in.name,
        description=section_in.description
    )
    db.add(new_section)
    db.commit()
    db.refresh(new_section)
    return new_section
