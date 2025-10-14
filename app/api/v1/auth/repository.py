from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.user_sessions import UserSession


def create_session(db: Session, user_id: str, refresh_token: str, refresh_expires_at: datetime,
                   user_agent: str = None, ip_address: str = None):
    session = UserSession(
        user_id=user_id,
        refresh_token=refresh_token,
        refresh_expires_at=refresh_expires_at,
        user_agent=user_agent,
        ip_address=ip_address
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def revoke_session(db: Session, refresh_token: str):
    session = db.query(UserSession).filter(UserSession.refresh_token == refresh_token).first()
    if session:
        session.is_revoked = True
        db.commit()
    return session


def validate_session(db: Session, refresh_token: str):
    session = db.query(UserSession).filter(
        UserSession.refresh_token == refresh_token,
        UserSession.is_revoked == False,
        UserSession.refresh_expires_at > datetime.now(timezone.utc)
    ).first()
    return session

