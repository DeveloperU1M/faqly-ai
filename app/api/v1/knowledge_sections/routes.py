from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.api.v1.knowledge_sections.schemas import KnowledgeSectionCreate, KnowledgeSectionResponse
from app.api.v1.knowledge_sections.service import create_section
from app.core.dependencies import get_current_user

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
    current_user: dict = Depends(get_current_user)
):
    return create_section(db, section)
