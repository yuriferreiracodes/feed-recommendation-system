import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.database import engine
from backend.exceptions import register_exception_handlers
from backend.routers.health import router as health_router

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: verify the DB connection pool is reachable.
    with engine.connect():
        logger.info("Database connection established")
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
