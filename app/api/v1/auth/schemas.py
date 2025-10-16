import uuid
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str | None = None  # user_id en el JWT

class GoogleTokenRequest(BaseModel):
    token: str


class UserResponse(BaseModel):
    user_id: uuid.UUID
    email: str
    name: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenRefreshRequest(BaseModel):
    refresh_token: str
