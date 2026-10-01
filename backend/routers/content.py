from typing import Annotated

from fastapi import APIRouter, Query, status

from backend.dependencies import DbSession
from backend.schemas.common import PaginatedResponse
from backend.schemas.content import ContentCreate, ContentRead, ContentUpdate
from backend.services import content_service

router = APIRouter()


@router.post("", response_model=ContentRead, status_code=status.HTTP_201_CREATED)
def create_content(data: ContentCreate, db: DbSession):
    return content_service.create_content(db, data)


@router.get("", response_model=PaginatedResponse[ContentRead])
def list_content(
    db: DbSession,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
    source: str | None = None,
    topic: str | None = None,
):
    items, total = content_service.list_content(db, page, size, source=source, topic=topic)
    return PaginatedResponse[ContentRead](items=items, total=total, page=page, size=size)


@router.get("/{content_id}", response_model=ContentRead)
def get_content(content_id: str, db: DbSession):
    return content_service.get_content(db, content_id)


@router.patch("/{content_id}", response_model=ContentRead)
def update_content(content_id: str, data: ContentUpdate, db: DbSession):
    return content_service.update_content(db, content_id, data)
