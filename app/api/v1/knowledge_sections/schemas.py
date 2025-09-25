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
    created_at: datetime

    class Config:
        orm_mode = True
