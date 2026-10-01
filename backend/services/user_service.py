from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from backend.exceptions import ConflictError, NotFoundError
from backend.models import User
from backend.schemas.user import UserCreate, UserUpdate


def _ensure_unique(
    db: Session, username: str | None, email: str | None, exclude_id: str | None = None
) -> None:
    conditions = []
    if username is not None:
        conditions.append(User.username == username)
    if email is not None:
        conditions.append(User.email == email)
    if not conditions:
        return
    stmt = select(User).where(or_(*conditions))
    if exclude_id is not None:
        stmt = stmt.where(User.id != exclude_id)
    existing = db.scalars(stmt).first()
    if existing is None:
        return
    if email is not None and existing.email == email:
        raise ConflictError("A user with this email already exists")
    raise ConflictError("A user with this username already exists")


def create_user(db: Session, data: UserCreate) -> User:
    _ensure_unique(db, data.username, data.email)
    user = User(username=data.username, email=data.email, preferences=data.preferences)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: str) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise NotFoundError(f"User {user_id} not found")
    return user


def list_users(db: Session, page: int, size: int) -> tuple[list[User], int]:
    total = db.scalar(select(func.count()).select_from(User)) or 0
    stmt = select(User).order_by(User.created_at, User.id).offset((page - 1) * size).limit(size)
    return list(db.scalars(stmt)), total


def update_user(db: Session, user_id: str, data: UserUpdate) -> User:
    user = get_user(db, user_id)
    changes = data.model_dump(exclude_unset=True)
    # Explicit nulls on non-nullable columns make no sense for a PATCH; ignore them.
    changes = {k: v for k, v in changes.items() if v is not None}
    _ensure_unique(
        db,
        changes.get("username") if changes.get("username") != user.username else None,
        changes.get("email") if changes.get("email") != user.email else None,
        exclude_id=user.id,
    )
    for field, value in changes.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user
