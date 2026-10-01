import logging
from contextlib import asynccontextmanager

import redis
from elasticsearch import Elasticsearch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.database import engine
from backend.exceptions import register_exception_handlers
from backend.routers.content import router as content_router
from backend.routers.health import router as health_router
from backend.routers.users import router as users_router

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: verify the DB connection pool is reachable.
    with engine.connect():
        logger.info("Database connection established")
    # Ping Redis and Elasticsearch so startup surfaces connectivity issues.
    # These are logged, not fatal — readiness is enforced by /health/ready.
    try:
        redis.from_url(settings.REDIS_URL, socket_connect_timeout=5).ping()
        logger.info("Redis connection established")
    except Exception as exc:  # noqa: BLE001 - startup connectivity is best-effort
        logger.warning("Redis ping failed at startup: %s", exc)
    try:
        Elasticsearch(settings.ELASTICSEARCH_URL, request_timeout=5).info()
        logger.info("Elasticsearch connection established")
    except Exception as exc:  # noqa: BLE001 - startup connectivity is best-effort
        logger.warning("Elasticsearch ping failed at startup: %s", exc)
    yield
    # Shutdown: release the connection pool.
    engine.dispose()
    logger.info("Database connection pool disposed")


app = FastAPI(
    title="Feed Recommendation System",
    description="A personalized feed recommendation system.",
    version="0.1.0",
    lifespan=lifespan,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(health_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(content_router, prefix="/api/v1/content", tags=["content"])
