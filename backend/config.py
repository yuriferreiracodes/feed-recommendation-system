from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, loaded from environment variables or a .env file."""

    APP_ENV: str = "development"
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/feedapp"
    REDIS_URL: str = "redis://localhost:6379/0"
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    # --- Object storage (MinIO / S3) -------------------------------------
    # Uploaded images live in MinIO; the DB only stores object keys.
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "feed-media"
    MINIO_SECURE: bool = False  # True once the endpoint is behind TLS

    # --- Image uploads ---------------------------------------------------
    MEDIA_MAX_UPLOAD_BYTES: int = 10 * 1024 * 1024  # 10 MiB
    MEDIA_THUMBNAIL_MAX_PX: int = 480  # longest side of the generated thumbnail

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance so the .env file is read only once."""
    return Settings()


settings = get_settings()
