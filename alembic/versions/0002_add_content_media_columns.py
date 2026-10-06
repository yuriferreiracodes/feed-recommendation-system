"""add media columns to content

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-05

The feed became image-first, so content carries an uploaded image: MinIO object
keys plus the metadata the UI needs before the bytes arrive (intrinsic size).

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("content", sa.Column("image_key", sa.String(length=512), nullable=True))
    op.add_column("content", sa.Column("thumbnail_key", sa.String(length=512), nullable=True))
    op.add_column("content", sa.Column("image_width", sa.Integer(), nullable=True))
    op.add_column("content", sa.Column("image_height", sa.Integer(), nullable=True))
    op.add_column(
        "content", sa.Column("image_content_type", sa.String(length=100), nullable=True)
    )
    op.add_column("content", sa.Column("image_bytes", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("content", "image_bytes")
    op.drop_column("content", "image_content_type")
    op.drop_column("content", "image_height")
    op.drop_column("content", "image_width")
    op.drop_column("content", "thumbnail_key")
    op.drop_column("content", "image_key")
