import json

from sqlalchemy import String, cast, func, select
from sqlalchemy.orm import Session

from backend.exceptions import ConflictError, NotFoundError
from backend.models import Content
from backend.schemas.content import ContentCreate, ContentUpdate


def _topic_filter(db: Session, topic: str):
    # MySQL has native JSON_CONTAINS; fall back to a text match elsewhere (e.g. SQLite in tests).
    if db.get_bind().dialect.name == "mysql":
        return func.json_contains(Content.topics, json.dumps(topic)) == 1
    return cast(Content.topics, String).like(f"%{json.dumps(topic)}%")


def _ensure_external_id_free(db: Session, external_id: str | None, exclude_id: str | None = None):
    if external_id is None:
        return
    stmt = select(Content.id).where(Content.external_id == external_id)
    if exclude_id is not None:
        stmt = stmt.where(Content.id != exclude_id)
    if db.scalars(stmt).first() is not None:
        raise ConflictError("Content with this external_id already exists")


def create_content(db: Session, data: ContentCreate) -> Content:
    _ensure_external_id_free(db, data.external_id)
    content = Content(**data.model_dump())
    db.add(content)
    db.commit()
    db.refresh(content)
    return content


def get_content(db: Session, content_id: str) -> Content:
    content = db.get(Content, content_id)
    if content is None:
        raise NotFoundError(f"Content {content_id} not found")
    return content


def list_content(
    db: Session,
    page: int,
    size: int,
    source: str | None = None,
    topic: str | None = None,
) -> tuple[list[Content], int]:
    conditions = []
    if source is not None:
        conditions.append(Content.source == source)
    if topic is not None:
        conditions.append(_topic_filter(db, topic))
    total = db.scalar(select(func.count()).select_from(Content).where(*conditions)) or 0
    stmt = (
        select(Content)
        .where(*conditions)
        .order_by(Content.created_at.desc(), Content.id)
        .offset((page - 1) * size)
        .limit(size)
    )
    return list(db.scalars(stmt)), total


def update_content(db: Session, content_id: str, data: ContentUpdate) -> Content:
    content = get_content(db, content_id)
    changes = data.model_dump(exclude_unset=True)
    if "title" in changes and changes["title"] is None:
        del changes["title"]  # title is NOT NULL
    if "external_id" in changes and changes["external_id"] != content.external_id:
        _ensure_external_id_free(db, changes["external_id"], exclude_id=content.id)
    for field, value in changes.items():
        setattr(content, field, value)
    db.commit()
    db.refresh(content)
    return content
