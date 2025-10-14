from pydantic import BaseModel
from typing import Optional

class AskRequest(BaseModel):
    prompt: str
    context: Optional[str] = None

class AskResponse(BaseModel):
    answer: str
