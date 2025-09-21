from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# --- Schemas de entrada ---
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

# --- Schemas de salida ---
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # permite convertir desde SQLAlchemy
