from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid
# --- Schemas de entrada ---
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

# --- Schemas de salida ---
class UserOut(BaseModel):
    user_id: uuid.UUID
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
