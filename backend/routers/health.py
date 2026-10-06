from fastapi import APIRouter, HTTPException

from backend.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def _check_db() -> None:
    from sqlalchemy import create_engine, text

    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    finally:
        engine.dispose()


def _check_redis() -> None:
    import redis

    client = redis.from_url(settings.REDIS_URL, socket_connect_timeout=5)
    try:
        client.ping()
    finally:
        client.close()


def _check_elasticsearch() -> None:
    from elasticsearch import Elasticsearch

    client = Elasticsearch(settings.ELASTICSEARCH_URL, request_timeout=5)
    try:
        if not client.ping():
            raise RuntimeError("ping returned false")
    finally:
        client.close()


def _check_minio() -> None:
    from backend.storage import get_client

    if not get_client().bucket_exists(settings.MINIO_BUCKET):
        raise RuntimeError(f"bucket {settings.MINIO_BUCKET} does not exist")


@router.get("/health/ready")
def ready() -> dict[str, str]:
    checks = {
        "db": _check_db,
        "redis": _check_redis,
        "elasticsearch": _check_elasticsearch,
        "minio": _check_minio,
    }

    status: dict[str, str] = {}
    for name, check in checks.items():
        try:
            check()
            status[name] = "ok"
        except Exception as exc:  # noqa: BLE001 - report any failure as not-ready
            status[name] = f"error: {exc}"

    if any(value != "ok" for value in status.values()):
        raise HTTPException(status_code=503, detail=status)

    return status
