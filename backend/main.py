from fastapi import FastAPI, HTTPException

from backend.config import settings

app = FastAPI(
    title="Feed Recommendation System",
    description="A personalized feed recommendation system.",
    version="0.1.0",
)


@app.get("/health")
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


@app.get("/health/ready")
def ready() -> dict[str, str]:
    checks = {
        "db": _check_db,
        "redis": _check_redis,
        "elasticsearch": _check_elasticsearch,
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
