import os
from sqlalchemy.orm import Session
from app.api.v1.documents.repository import create_document, get_documents, get_document, get_section_by_id, get_document_by_id
from app.api.v1.documents.schemas import DocumentCreate
from app.models.user import User
from app.models.document import Document
from fastapi import HTTPException, status, UploadFile

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")

def create_document_service(db: Session, doc_in: DocumentCreate, current_user: User):
    # 1. Validar que la sección exista
    section = get_section_by_id(db, doc_in.section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La sección especificada no existe"
        )

    # 2. Validación opcional de tamaño
    if hasattr(doc_in, "file_size") and doc_in.file_size > 10_000_000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo excede el tamaño máximo permitido"
        )

    # 3. Crear objeto Document
    new_doc = Document(
        title=doc_in.title,
        description=doc_in.description,
        file_path=doc_in.file_path,
        file_type=doc_in.file_type,
        uploaded_by=current_user.user_id,
        section_id=doc_in.section_id,
        is_active=True
    )

    # 4. Persistir en la BD
    return create_document(db, new_doc)

async def save_document_service(db: Session, file: UploadFile, section_id: str, current_user: User):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    file_size = os.path.getsize(file_path)

    new_doc = Document(
        title=file.filename,
        description=None,
        file_path=file_path,
        file_type=file.content_type,
        uploaded_by=current_user.user_id,
        section_id=section_id,
        file_size=file_size,
        is_active=True
    )

    return create_document(db, new_doc, current_user)
def list_documents_service(db: Session, skip: int = 0, limit: int = 10):
    return get_documents(db, skip, limit)

def get_document_service(db: Session, document_id: str):
    doc = get_document(db, document_id)
    if not doc:
        raise ValueError("Documento no encontrado")
    return doc

def get_document_service(db: Session, doc_id: str, current_user: User):
    doc = get_document_by_id(db, doc_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    # regla de negocio: validar acceso
    if doc.uploaded_by != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No access to this document")

    return doc