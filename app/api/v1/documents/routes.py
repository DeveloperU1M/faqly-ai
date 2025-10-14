from fastapi import UploadFile, File, APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.api.v1.documents.schemas import DocumentCreate, DocumentResponse
from app.api.v1.documents.service import create_document_service, list_documents_service, get_document_service, save_document_service
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.gemini.parser import generate_json_structure
router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    section_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    response = await save_document_service(db, file, section_id, current_user)
    background_tasks.add_task(generate_json_structure, response.file_path, current_user.user_id , response.document_id)
    return response

@router.get("/download/{doc_id}")
def download_document(
    doc_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doc = get_document_service(db, doc_id, current_user)
    return FileResponse(
        doc.file_path,
        filename=doc.title,   # nombre del archivo que verá el usuario
        media_type="application/octet-stream"
    )

@router.get("/", response_model=List[DocumentResponse])
def list_documents(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return list_documents_service(db, skip, limit)

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str, db: Session = Depends(get_db)):
    try:
        return get_document_service(db, document_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))