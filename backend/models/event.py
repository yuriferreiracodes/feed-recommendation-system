import uuid

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    String,
    func,
)

from backend.database import Base

# Event.weight is pre-computed from the event type at insert time using this map.
EVENT_WEIGHTS: dict[str, float] = {
    "view": 1.0,
    "click": 2.0,
    "like": 3.0,
    "bookmark": 3.0,
    "share": 4.0,
    "skip": -1.0,
}


class Event(Base):
    __tablename__ = "events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    content_id = Column(
        String(36), ForeignKey("content.id"), nullable=False, index=True
    )
    event_type = Column(
        Enum("view", "click", "like", "share", "skip", "bookmark", name="event_type"),
        nullable=False,
        index=True,
    )
    weight = Column(Float, nullable=False)  # numeric importance; see EVENT_WEIGHTS
    # "metadata" is reserved on the declarative Base, so the attribute is renamed
    # while the DB column stays "metadata". e.g. {"duration_seconds": 45, "source": "feed"}
    event_metadata = Column("metadata", JSON)
    occurred_at = Column(
        DateTime, server_default=func.now(), nullable=False, index=True
    )

    __table_args__ = (
        Index("ix_events_user_content_type", "user_id", "content_id", "event_type"),
    )
