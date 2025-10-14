from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    description: Optional[str] = None

class DocumentCreate(DocumentBase):
    file_path: str
    file_type: str
    file_size: Optional[int] = None
    section_id: UUID

class DocumentResponse(DocumentBase):
    document_id: UUID
    file_path: str
    file_type: str
    file_size: Optional[int]
    uploaded_at: datetime
    is_active: bool
    section_id: UUID
    uploaded_by: UUID

    class Config:
        from_attributes = True
