from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.api.v1.knowledge_sections.schemas import KnowledgeSectionCreate, KnowledgeSectionResponse, CreateKnowledgeSectionResponse, DesactivateSectionResponse 
from app.api.v1.knowledge_sections  import service
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/knowledge_sections", tags=["Knowledge Sections"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CreateKnowledgeSectionResponse)
def create_knowledge_section(
    section: KnowledgeSectionCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    return service.create_section_service(db, section, current_user)

@router.get("/", response_model=list[KnowledgeSectionResponse])
def list_sections(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return service.list_sections_service(db, current_user, skip, limit)

@router.patch("/{section_id}/deactivate", response_model=DesactivateSectionResponse)
def deactivate_section(section_id: str, db: Session = Depends(get_db)):
    return service.deactivate_section(db, section_id)