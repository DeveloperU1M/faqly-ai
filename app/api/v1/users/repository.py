from sqlalchemy.orm import Session
from app.models.user import User
from app.api.v1.users.schemas  import UserCreate

def create_user(db: Session, user: UserCreate, hashed_password: str) -> User:
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()
