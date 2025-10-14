from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.api.v1.knowledge_sections.schemas import KnowledgeSectionCreate, KnowledgeSectionResponse
from app.api.v1.knowledge_sections.service import create_section_service, list_sections_service
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/knowledge_sections", tags=["Knowledge Sections"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=KnowledgeSectionResponse)
def create_knowledge_section(
    section: KnowledgeSectionCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    return create_section_service(db, section, current_user)

@router.get("/", response_model=list[KnowledgeSectionResponse])
def list_sections(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return list_sections_service(db, current_user, skip, limit)
