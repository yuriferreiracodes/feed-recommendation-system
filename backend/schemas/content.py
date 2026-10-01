from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ContentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    body: str | None = None
    url: str | None = Field(default=None, max_length=2048)
    source: str | None = Field(default=None, max_length=100)
    topics: list[str] = Field(default_factory=list)
    author: str | None = Field(default=None, max_length=255)
    published_at: datetime | None = None
    external_id: str | None = Field(default=None, max_length=255)


class ContentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=500)
    body: str | None = None
    url: str | None = Field(default=None, max_length=2048)
    source: str | None = Field(default=None, max_length=100)
    topics: list[str] | None = None
    author: str | None = Field(default=None, max_length=255)
    published_at: datetime | None = None
    external_id: str | None = Field(default=None, max_length=255)


class ContentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    external_id: str | None
    title: str
    body: str | None
    url: str | None
    source: str | None
    topics: list[str] | None
    author: str | None
    published_at: datetime | None
    score: float
    created_at: datetime
    updated_at: datetime
