from sqlalchemy import Column, DateTime, func


class TimestampMixin:
    """Adds self-managing created_at / updated_at columns to a model."""

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
