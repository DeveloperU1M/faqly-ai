import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.session import Base

class UserSession(Base):
    __tablename__ = "user_sessions"

    session_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))

    refresh_token = Column(String, nullable=False)
    refresh_expires_at = Column(DateTime, nullable=False)

    # opcional — solo si quieres auditar o invalidar access tokens
    last_access_token = Column(String, nullable=True)
    last_access_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user_agent = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="sessions")
