from collections.abc import Generator
from typing import Annotated

import redis
from elasticsearch import Elasticsearch
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.config import settings
from backend.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis() -> redis.Redis:
    return redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_es() -> Elasticsearch:
    return Elasticsearch(settings.ELASTICSEARCH_URL)


DbSession = Annotated[Session, Depends(get_db)]
RedisClient = Annotated[redis.Redis, Depends(get_redis)]
EsClient = Annotated[Elasticsearch, Depends(get_es)]
