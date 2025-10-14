from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.v1.auth.service import authenticate_user, login_with_google_service
from app.core.dependencies import get_db
from app.api.v1.auth.schemas import Token, GoogleTokenRequest
from app.core.security import create_access_token, decode_token
from app.models.user import User
from datetime import timedelta
from fastapi import  status

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return authenticate_user(form_data, db)



@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = decode_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

    user = db.query(User).filter(User.user_id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    access_token_expires = timedelta(minutes=15)
    new_access_token = create_access_token(
        data={"sub": user.username, "user_id": str(user.user_id)},
        expires_delta=access_token_expires
    )

    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post("/login/google")
def login_with_google(payload: GoogleTokenRequest, db: Session = Depends(get_db)):
    return login_with_google_service(payload.token, db)