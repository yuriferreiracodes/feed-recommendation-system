from typing import Annotated

from fastapi import APIRouter, Query, status

from backend.dependencies import DbSession
from backend.schemas.common import PaginatedResponse
from backend.schemas.user import UserCreate, UserRead, UserUpdate
from backend.services import user_service

router = APIRouter()


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: DbSession):
    return user_service.create_user(db, data)


@router.get("", response_model=PaginatedResponse[UserRead])
def list_users(
    db: DbSession,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
):
    items, total = user_service.list_users(db, page, size)
    return PaginatedResponse[UserRead](items=items, total=total, page=page, size=size)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: str, db: DbSession):
    return user_service.get_user(db, user_id)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: str, data: UserUpdate, db: DbSession):
    return user_service.update_user(db, user_id, data)
