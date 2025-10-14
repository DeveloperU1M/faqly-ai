from datetime import timedelta
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from google.auth.transport import requests
from google.oauth2 import id_token

from app.core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from app.models.user import User
from datetime import datetime, timezone
from app.api.v1.auth.repository import create_session
from app.api.v1.users.repository import  get_user_by_email, create_user_from_google, get_user_by_google_id


import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
ALLOWED_DOMAIN = os.getenv("ALLOWED_DOMAIN")

def authenticate_user(form_data: OAuth2PasswordRequestForm, db: Session, user_agent: str = None, ip_address: str = None):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generar tokens
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(
        data={"sub": str(user.username), "user_id": str(user.user_id)},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.username), "user_id": str(user.user_id)},
        expires_delta=refresh_token_expires
    )

    # Guardar sesión en BD
    refresh_expires_at = datetime.now(timezone.utc) + refresh_token_expires
    create_session(
        db=db,
        user_id=user.user_id,
        refresh_token=refresh_token,
        refresh_expires_at=refresh_expires_at,
        user_agent=user_agent,
        ip_address=ip_address
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def create_refresh_token(data: dict):
    expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return create_access_token(data, expires)

def login_with_google_service(token: str, db: Session):
    try:
        # 1️⃣ Verificar token de Google
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        sub = idinfo["sub"]  # ID único de Google
        email = idinfo["email"]
        name = idinfo.get("name", "")

        # 2️⃣ Buscar usuario por Google ID
        user = get_user_by_google_id(db, sub)

        # 3️⃣ Si no existe, crear usuario
        if not user:
            user = create_user_from_google(db, email, sub, name)

        # 4️⃣ Generar token interno
        access_token_expires = timedelta(minutes=15)
        access_token = create_access_token(
            data={"sub": user.username, "user_id": str(user.user_id)},
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de Google inválido"
        )
