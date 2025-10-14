from sqlalchemy.orm import Session
from app.models.user import User
from app.api.v1.users.schemas  import UserCreate

def create_user(db: Session, user: UserCreate, hashed_password: str) -> User:
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.user_id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_google_id(db: Session, google_id: str) -> User | None:
    return db.query(User).filter(User.google_id == google_id).first()

def create_user_from_google(db: Session, email: str, sub: str, name: str) -> User:
    user = User(
        username=email.split("@")[0],
        email=email,
        google_id=sub,
        full_name=name,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
