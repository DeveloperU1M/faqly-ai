from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.api.v1.users import repository
from app.api.v1.users.schemas  import UserCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_user_service(db: Session, user: UserCreate):
    existing = repository.get_user_by_email(db, user.email)
    if existing:
        raise ValueError("El email ya está registrado")

    hashed_pw = hash_password(user.password)

    try:
        return repository.create_user(db, user, hashed_pw)
    except IntegrityError:
        raise ValueError("El email o username ya están registrados")
