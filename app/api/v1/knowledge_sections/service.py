from sqlalchemy.orm import Session
from app.api.v1.knowledge_sections.schemas import KnowledgeSectionCreate
from app.models.user import User
from app.api.v1.knowledge_sections.repository import create_section as repo_create_section, get_sections

def create_section_service(db: Session, section_in: KnowledgeSectionCreate, current_user: User):
    return repo_create_section(
        db=db,
        name=section_in.name,
        description=section_in.description,
        user_id=current_user.user_id
    )

def list_sections_service(db: Session, current_user: User, skip: int = 0, limit: int = 10):
    return get_sections(db, user_id=current_user.user_id, skip=skip, limit=limit)
