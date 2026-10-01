import uuid

from sqlalchemy import JSON, Column, DateTime, Float, String, Text

from backend.database import Base
from backend.models.base import TimestampMixin


class Content(Base, TimestampMixin):
    __tablename__ = "content"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    external_id = Column(String(255), unique=True)  # ID from the original source
    title = Column(String(500), nullable=False)
    body = Column(Text)
    url = Column(String(2048))
    source = Column(String(100))  # "techcrunch", "arxiv", etc.
    topics = Column(JSON)  # ["python", "ml", ...]
    author = Column(String(255))
    published_at = Column(DateTime)
    score = Column(Float, default=0.0)  # aggregated engagement score
