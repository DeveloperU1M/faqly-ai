from sqlalchemy.orm import Session
from app.api.v1.knowledge_sections.schemas import KnowledgeSectionCreate
from app.models.user import User
from app.api.v1.knowledge_sections import repository
from fastapi import HTTPException
def create_section_service(db: Session, section_in: KnowledgeSectionCreate, current_user: User):
    return repository.create_section(
        db=db,
        name=section_in.name,
        description=section_in.description,
        user_id=current_user.user_id
    )

def list_sections_service(db: Session, current_user: User, skip: int = 0, limit: int = 10):
    return repository.get_sections(db, user_id=current_user.user_id, skip=skip, limit=limit)

def deactivate_section(db, section_id: str):
    section = repository.get_section_by_id(db, section_id)

    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    if section.agents and len(section.agents) > 0:
        raise HTTPException(
            status_code=409,  # 409 Conflict → lo adecuado en este caso
            detail="Section is linked to one or more agents and cannot be deactivated"
        )
        
    if not section.is_active:
        raise HTTPException(status_code=400, detail="Section is already inactive")

    return repository.deactivate_section(db, section)