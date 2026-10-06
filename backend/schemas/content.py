from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, computed_field

from backend.storage.media import media_url


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

    # --- Media ---------------------------------------------------------------
    # Intrinsic size lets the client reserve the slot before the image loads.
    image_width: int | None = None
    image_height: int | None = None
    image_content_type: str | None = None
    image_bytes: int | None = None

    # Object keys are an implementation detail: read off the ORM model, kept out
    # of the response, and exposed only through the derived URLs below.
    image_key: str | None = Field(default=None, exclude=True)
    thumbnail_key: str | None = Field(default=None, exclude=True)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def image_url(self) -> str | None:
        """Served by GET /api/v1/media/{key}; None until an image is uploaded."""
        return media_url(self.image_key)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def thumbnail_url(self) -> str | None:
        return media_url(self.thumbnail_key)
