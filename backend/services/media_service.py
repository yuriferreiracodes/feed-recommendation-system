import logging
from collections.abc import Iterator

from fastapi import UploadFile
from minio import Minio
from minio.error import S3Error
from sqlalchemy.orm import Session

from backend.config import settings
from backend.exceptions import (
    BadRequestError,
    NotFoundError,
    PayloadTooLargeError,
    StorageUnavailableError,
    UnsupportedMediaTypeError,
)
from backend.models import Content
from backend.services import content_service
from backend.storage import images, media

logger = logging.getLogger(__name__)

READ_CHUNK_BYTES = 1024 * 1024

# S3 error codes that mean "the object is simply not there".
_MISSING_CODES = {"NoSuchKey", "NoSuchBucket", "NoSuchObject"}


def _read_upload(upload: UploadFile) -> bytes:
    """Read the upload, refusing anything over the configured size limit.

    Reads through the sync file handle: the media endpoints are sync defs, so
    FastAPI already runs them in a worker thread.
    """
    limit = settings.MEDIA_MAX_UPLOAD_BYTES
    chunks: list[bytes] = []
    size = 0
    while True:
        chunk = upload.file.read(READ_CHUNK_BYTES)
        if not chunk:
            break
        size += len(chunk)
        if size > limit:
            # Stop reading as soon as the limit is passed; never buffer the rest.
            raise PayloadTooLargeError(
                f"Image exceeds the maximum upload size of {limit} bytes"
            )
        chunks.append(chunk)
    return b"".join(chunks)


def attach_image(
    db: Session, client: Minio, content_id: str, upload: UploadFile
) -> Content:
    """Store an uploaded image (plus a thumbnail) and point the content row at it.

    Replaces any image the content already had. The old objects are deleted only
    after the row commits, so a failure never leaves a row pointing at nothing.
    """
    content = content_service.get_content(db, content_id)
    raw = _read_upload(upload)

    try:
        processed = images.process(raw)
    except images.UnsupportedImageFormatError as exc:
        raise UnsupportedMediaTypeError(str(exc)) from exc
    except images.InvalidImageError as exc:
        raise BadRequestError(str(exc)) from exc

    previous_keys = [k for k in (content.image_key, content.thumbnail_key) if k]
    image_key, thumbnail_key = media.build_keys(content.id, processed.extension)

    try:
        media.put_bytes(client, image_key, processed.data, processed.content_type)
        media.put_bytes(
            client, thumbnail_key, processed.thumbnail, images.THUMBNAIL_CONTENT_TYPE
        )
    except S3Error as exc:
        media.remove_keys(client, image_key, thumbnail_key)
        raise StorageUnavailableError(f"Could not store the image: {exc.code}") from exc
    except Exception as exc:  # connection refused, DNS, timeouts
        media.remove_keys(client, image_key, thumbnail_key)
        logger.exception("Upload to object storage failed for content %s", content.id)
        raise StorageUnavailableError("Object storage is unavailable") from exc

    content.image_key = image_key
    content.thumbnail_key = thumbnail_key
    content.image_width = processed.width
    content.image_height = processed.height
    content.image_content_type = processed.content_type
    content.image_bytes = len(processed.data)
    db.commit()
    db.refresh(content)

    media.remove_keys(client, *previous_keys)
    return content


def remove_image(db: Session, client: Minio, content_id: str) -> Content:
    """Detach and delete the content's image. No-op when there is none."""
    content = content_service.get_content(db, content_id)
    keys = [k for k in (content.image_key, content.thumbnail_key) if k]
    if not keys:
        return content

    content.image_key = None
    content.thumbnail_key = None
    content.image_width = None
    content.image_height = None
    content.image_content_type = None
    content.image_bytes = None
    db.commit()
    db.refresh(content)

    media.remove_keys(client, *keys)
    return content


def open_media(client: Minio, key: str) -> tuple[Iterator[bytes], str, int, str | None]:
    """Return (byte stream, content type, length, etag) for a stored object."""
    # Only keys this service generates are servable: the bucket may later hold
    # objects that are not meant to be public.
    if not media.is_valid_key(key):
        raise NotFoundError("Media object not found")

    try:
        info = media.stat(client, key)
    except S3Error as exc:
        if exc.code in _MISSING_CODES:
            raise NotFoundError("Media object not found") from exc
        raise StorageUnavailableError(f"Could not read the image: {exc.code}") from exc
    except Exception as exc:
        logger.exception("Object storage stat failed for %s", key)
        raise StorageUnavailableError("Object storage is unavailable") from exc

    content_type = info.content_type or "application/octet-stream"
    return media.stream(client, key), content_type, info.size or 0, info.etag
