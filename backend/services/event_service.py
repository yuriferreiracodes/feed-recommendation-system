import json
import logging

import redis as redis_lib
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.exceptions import NotFoundError
from backend.models import EVENT_WEIGHTS, Content, Event, User
from backend.schemas.event import EventBatch, EventCreate

logger = logging.getLogger(__name__)

USER_EVENTS_MAX = 500


def _ensure_exist(db: Session, model, ids: set[str], label: str) -> None:
    found = set(db.scalars(select(model.id).where(model.id.in_(ids))))
    missing = sorted(ids - found)
    if missing:
        raise NotFoundError(f"{label} {missing[0]} not found")


def _push_to_redis(client: redis_lib.Redis, events: list[Event]) -> None:
    # Redis is the performance layer; the DB stays the source of truth, so a
    # Redis failure only logs a warning and never rolls back the saved events.
    try:
        pipe = client.pipeline()
        for event in events:
            key = f"user:{event.user_id}:events"
            payload = json.dumps(
                {
                    "id": event.id,
                    "content_id": event.content_id,
                    "event_type": event.event_type,
                    "weight": event.weight,
                    "occurred_at": event.occurred_at.isoformat(),
                }
            )
            pipe.lpush(key, payload)
            pipe.ltrim(key, 0, USER_EVENTS_MAX - 1)
            pipe.zincrby("global:content:scores", event.weight, event.content_id)
        pipe.execute()
    except redis_lib.RedisError as exc:
        logger.warning("Failed to write events to Redis: %s", exc)


def record_events(db: Session, client: redis_lib.Redis, items: list[EventCreate]) -> list[Event]:
    # Validate everything up front so a bad item doesn't leave a half-saved batch.
    _ensure_exist(db, User, {i.user_id for i in items}, "User")
    _ensure_exist(db, Content, {i.content_id for i in items}, "Content")
    events = [
        Event(
            user_id=i.user_id,
            content_id=i.content_id,
            event_type=i.event_type,
            weight=EVENT_WEIGHTS[i.event_type],
            event_metadata=i.metadata,
            occurred_at=i.occurred_at,
        )
        for i in items
    ]
    db.add_all(events)
    db.commit()
    for event in events:
        db.refresh(event)
    _push_to_redis(client, events)
    return events


def record_event(db: Session, client: redis_lib.Redis, data: EventCreate) -> Event:
    return record_events(db, client, [data])[0]


def record_events_batch(db: Session, client: redis_lib.Redis, batch: EventBatch) -> list[Event]:
    return record_events(db, client, batch.events)


def get_user_events(
    db: Session, user_id: str | None, page: int, size: int
) -> tuple[list[Event], int]:
    conditions = [Event.user_id == user_id] if user_id is not None else []
    total = db.scalar(select(func.count()).select_from(Event).where(*conditions)) or 0
    stmt = (
        select(Event)
        .where(*conditions)
        .order_by(Event.occurred_at.desc(), Event.id)
        .offset((page - 1) * size)
        .limit(size)
    )
    return list(db.scalars(stmt)), total
