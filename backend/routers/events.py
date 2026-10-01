from typing import Annotated

from fastapi import APIRouter, Query, status

from backend.dependencies import DbSession, RedisClient
from backend.schemas.common import PaginatedResponse
from backend.schemas.event import EventBatch, EventCreate, EventRead
from backend.services import event_service

router = APIRouter()


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(data: EventCreate, db: DbSession, redis: RedisClient):
    return event_service.record_event(db, redis, data)


@router.post("/batch", response_model=list[EventRead], status_code=status.HTTP_201_CREATED)
def create_events_batch(batch: EventBatch, db: DbSession, redis: RedisClient):
    return event_service.record_events_batch(db, redis, batch)


@router.get("", response_model=PaginatedResponse[EventRead])
def list_events(
    db: DbSession,
    user_id: str | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
):
    items, total = event_service.get_user_events(db, user_id, page, size)
    return PaginatedResponse[EventRead](items=items, total=total, page=page, size=size)
