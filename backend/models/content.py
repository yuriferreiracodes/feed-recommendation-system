import uuid

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, Text

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

    # --- Media ---------------------------------------------------------------
    # The feed is image-first: these columns hold MinIO object keys, never URLs,
    # so the storage endpoint can move without rewriting rows. The public URL is
    # derived at serialization time (see schemas.content / storage.media).
    image_key = Column(String(512))
    thumbnail_key = Column(String(512))
    # Intrinsic dimensions of the stored image. Not decorative: the feed reserves
    # each slot's space from the ratio before the image loads, to avoid reflow.
    image_width = Column(Integer)
    image_height = Column(Integer)
    image_content_type = Column(String(100))
    image_bytes = Column(Integer)  # size of the stored original
