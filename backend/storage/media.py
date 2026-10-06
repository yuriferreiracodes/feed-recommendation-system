import io
import logging
import re
import uuid
from collections.abc import Iterator

from minio import Minio
from minio.datatypes import Object

from backend.config import settings
from backend.storage.images import THUMBNAIL_EXTENSION

logger = logging.getLogger(__name__)

# Images are served by the backend, not straight from MinIO: the bucket stays
# private and the URL in the DB never expires. The frontend only sees this path.
MEDIA_URL_PREFIX = "/api/v1/media/"

# Keys this module generates: content/<content uuid>/<random hex>[_thumb].<ext>
# GET /media/{key} matches the request key against this before touching MinIO,
# so the endpoint can never be used to read an object it did not create.
KEY_PATTERN = re.compile(
    r"^content/[0-9a-f-]{36}/[0-9a-f]{32}(_thumb)?\.(jpg|png|webp)$"
)

STREAM_CHUNK_BYTES = 64 * 1024


def media_url(key: str | None) -> str | None:
    """Public URL for an object key, or None when there is no object."""
    return f"{MEDIA_URL_PREFIX}{key}" if key else None


def is_valid_key(key: str) -> bool:
    return KEY_PATTERN.fullmatch(key) is not None


def build_keys(content_id: str, extension: str) -> tuple[str, str]:
    """Return (image key, thumbnail key) for a new upload.

    The random stem means a re-upload never reuses a key, so stale copies cached
    by browsers or proxies are not served for the new image.
    """
    stem = uuid.uuid4().hex
    prefix = f"content/{content_id}/{stem}"
    return f"{prefix}.{extension}", f"{prefix}_thumb.{THUMBNAIL_EXTENSION}"


def put_bytes(client: Minio, key: str, data: bytes, content_type: str) -> None:
    client.put_object(
        settings.MINIO_BUCKET,
        key,
        io.BytesIO(data),
        length=len(data),
        content_type=content_type,
    )


def remove_keys(client: Minio, *keys: str) -> None:
    """Best-effort delete: a leftover object is cheap, a failed request is not."""
    for key in keys:
        try:
            client.remove_object(settings.MINIO_BUCKET, key)
        except Exception as exc:  # noqa: BLE001 - cleanup must not fail the request
            logger.warning("Could not delete object %s: %s", key, exc)


def stat(client: Minio, key: str) -> Object:
    return client.stat_object(settings.MINIO_BUCKET, key)


def stream(client: Minio, key: str) -> Iterator[bytes]:
    """Yield an object's bytes, releasing the HTTP connection when done."""
    response = client.get_object(settings.MINIO_BUCKET, key)
    try:
        yield from response.stream(STREAM_CHUNK_BYTES)
    finally:
        response.close()
        response.release_conn()
