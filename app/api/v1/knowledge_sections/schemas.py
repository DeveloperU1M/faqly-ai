from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class KnowledgeSectionBase(BaseModel):
    name: str
    description: Optional[str] = None

class KnowledgeSectionCreate(KnowledgeSectionBase):
    pass

class KnowledgeSectionResponse(KnowledgeSectionBase):
    knowledge_section_id: uuid.UUID
    document_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None 
    class Config:
        from_attributes = True

class CreateKnowledgeSectionResponse(KnowledgeSectionBase):
    knowledge_section_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True<