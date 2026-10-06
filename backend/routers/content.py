from typing import Annotated

from fastapi import APIRouter, File, Query, UploadFile, status

from backend.dependencies import DbSession, StorageClient
from backend.schemas.common import PaginatedResponse
from backend.schemas.content import ContentCreate, ContentRead, ContentUpdate
from backend.services import content_service, media_service

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


@router.put(
    "/{content_id}/image",
    response_model=ContentRead,
    summary="Upload or replace the content's image",
)
def upload_content_image(
    content_id: str,
    db: DbSession,
    storage: StorageClient,
    file: UploadFile = File(description="JPEG, PNG or WebP image"),
):
    """Store the image in MinIO, derive a thumbnail, and record its metadata.

    Idempotent by design: uploading again replaces the previous image, which is
    why this is PUT and not POST.
    """
    return media_service.attach_image(db, storage, content_id, file)


@router.delete("/{content_id}/image", response_model=ContentRead)
def delete_content_image(content_id: str, db: DbSession, storage: StorageClient):
    """Remove the content's image and its thumbnail from object storage."""
    return media_service.remove_image(db, storage, content_id)
