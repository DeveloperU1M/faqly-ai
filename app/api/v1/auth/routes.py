from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.v1.auth.service import authenticate_user, login_with_google_service, refresh_access_token
from app.core.dependencies import get_db
from app.api.v1.auth.schemas import Token, GoogleTokenRequest,TokenResponse, TokenRefreshRequest


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return authenticate_user(form_data, db)




@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    refresh_token: str = Cookie(None),  # Lee la cookie llamada 'refresh_token'
    db: Session = Depends(get_db)
):
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Missing refresh token cookie")

    # Llama a la función que maneja la lógica, pasando el refresh_token y la db
    return refresh_access_token(refresh_token, db)

@router.post("/login/google" , response_model=TokenResponse)
def login_with_google(payload: GoogleTokenRequest, response: Response, db: Session = Depends(get_db)):
    return login_with_google_service(payload.token, db, response=response)
