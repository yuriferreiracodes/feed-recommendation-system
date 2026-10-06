import logging
from functools import lru_cache

from minio import Minio

from backend.config import settings

logger = logging.getLogger(__name__)


@lru_cache
def get_client() -> Minio:
    """Return a cached MinIO client (the SDK pools connections and is thread-safe)."""
    return Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE,
    )


def ensure_bucket(client: Minio | None = None) -> None:
    """Create the media bucket if it does not exist yet. Idempotent.

    The bucket stays private: images are served through GET /api/v1/media/{key},
    so there is no public bucket policy and no presigned-URL expiry to manage.
    """
    client = client or get_client()
    if not client.bucket_exists(settings.MINIO_BUCKET):
        client.make_bucket(settings.MINIO_BUCKET)
        logger.info("Created MinIO bucket %s", settings.MINIO_BUCKET)
