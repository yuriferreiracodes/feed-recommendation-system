import uuid

from sqlalchemy import JSON, Boolean, Column, String

from backend.database import Base
from backend.models.base import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    # MySQL has no native UUID type; store as CHAR(36) with a Python-side
    # default so Alembic autogenerate can see it.
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    # Native MySQL JSON, e.g. {"topics": [...], "sources": [...]}.
    preferences = Column(JSON, nullable=False, default=dict)
    is_active = Column(Boolean, nullable=False, default=True)
