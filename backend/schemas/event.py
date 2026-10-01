from datetime import datetime, timezone
from typing import Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator

EventType = Literal["view", "click", "like", "share", "skip", "bookmark"]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class EventCreate(BaseModel):
    user_id: str
    content_id: str
    event_type: EventType
    metadata: dict = Field(default_factory=dict)
    occurred_at: datetime = Field(default_factory=_utcnow)

    @field_validator("occurred_at")
    @classmethod
    def _to_naive_utc(cls, value: datetime) -> datetime:
        # Naive datetimes are treated as UTC; aware ones are converted to UTC.
        if value.tzinfo is not None:
            value = value.astimezone(timezone.utc).replace(tzinfo=None)
        return value


class EventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    content_id: str
    event_type: EventType
    weight: float
    # The ORM attribute is `event_metadata` ("metadata" is reserved on declarative models).
    metadata: dict | None = Field(
        default=None, validation_alias=AliasChoices("event_metadata", "metadata")
    )
    occurred_at: datetime


class EventBatch(BaseModel):
    events: list[EventCreate] = Field(min_length=1, max_length=50)
