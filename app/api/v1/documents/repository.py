from sqlalchemy.orm import Session
from app.models.document import Document
from app.api.v1.documents.schemas import DocumentCreate
from app.models.user import User

def create_document(db: Session, doc_in: DocumentCreate, current_user: User):
    new_doc = Document(
        title=doc_in.title,
        description=doc_in.description,
        file_path=doc_in.file_path,
        file_type=doc_in.file_type,
        file_size=doc_in.file_size,
        section_id=doc_in.section_id,
        uploaded_by=current_user.user_id
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc

def get_documents(current_user: User, db: Session, section_id: str, skip: int = 0, limit: int = 10):
    return db.query(Document).filter(Document.section_id == section_id).offset(skip).limit(limit).all()

def get_document(db: Session, document_id: str):
    return db.query(Document).filter(Document.document_id == document_id).first()

def get_section_by_id(db: Session, section_id: str):
    from app.models.knowledge_section import KnowledgeSection
    return db.query(KnowledgeSection).filter(
        KnowledgeSection.knowledge_section_id == section_id
    ).first()

def get_document_by_id(db: Session, doc_id: str) -> Document | None:
    return db.query(Document).filter(Document.document_id == doc_id).first()