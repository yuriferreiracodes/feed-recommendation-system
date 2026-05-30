from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, loaded from environment variables or a .env file."""

    APP_ENV: str = "development"
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/feedapp"
    REDIS_URL: str = "redis://localhost:6379/0"
    ELASTICSEARCH_URL: str = "http://localhost:9200"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
