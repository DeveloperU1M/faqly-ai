from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime
import uuid


class AgentBase(BaseModel):
    name: str = Field(..., example="Agente de soporte técnico")
    instructions: Optional[str] = Field(None, example="Responde de manera amable y profesional")
    config: Optional[Any] = Field(None, example={"model": "gpt-4", "temperature": 0.7})


class AgentCreate(AgentBase):
    section_ids: Optional[List[uuid.UUID]] = Field(default_factory=list)
    color: str


class AgentResponse(AgentBase):
    agent_id: uuid.UUID
    name: str
    created_at: Optional[datetime] 
    welcome_message: str | None = None
    class Config:
        from_attributes = True

class AgentListResponse(BaseModel):
    total: int
    agents: List[AgentResponse]


class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    
    
class ConversationCreate(BaseModel):
    agent_id: str
    title: str | None = "Nueva Conversación"

class ConversationResponse(BaseModel):
    id: uuid.UUID
    agent_id: uuid.UUID
    title: str
    created_at: datetime
    class Config:
        from_attributes = True