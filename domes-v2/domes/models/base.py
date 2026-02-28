"""
DOMES v2 — SQLAlchemy Declarative Base + Shared Mixins

All models inherit from DOMESBase. Mixins provide reusable columns.

Usage:
    from domes.models.base import Base, DOMESBase, TimestampMixin

    class MyModel(DOMESBase):
        __tablename__ = "my_table"
        ...
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    SQLAlchemy 2.0 declarative base.

    All DOMES v2 models inherit from this class.
    Alembic uses Base.metadata to detect schema changes.
    """
    pass


class TimestampMixin:
    """
    Adds created_at and updated_at columns to a model.

    Uses PostgreSQL server-side now() for created_at and a trigger-updated
    updated_at column. The updated_at default ensures Python-side inserts
    also work without a database trigger.
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Timestamp when the record was created (UTC)",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Timestamp when the record was last updated (UTC)",
    )


class SoftDeleteMixin:
    """
    Adds soft-delete support via a deleted_at timestamp.

    Records are never physically deleted — instead deleted_at is set.
    All queries should filter WHERE deleted_at IS NULL.
    """
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        doc="If set, the record is soft-deleted (not physically removed)",
    )

    @property
    def is_deleted(self) -> bool:
        """Return True if this record has been soft-deleted."""
        return self.deleted_at is not None

    def soft_delete(self) -> None:
        """Mark this record as deleted."""
        self.deleted_at = datetime.now(timezone.utc)


class DOMESBase(Base, TimestampMixin):
    """
    Abstract base class for all DOMES v2 models.

    Provides:
    - UUID primary key (PostgreSQL gen_random_uuid())
    - created_at / updated_at timestamps
    - __repr__ for debugging
    """
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        doc="Primary key — PostgreSQL gen_random_uuid() UUID v4",
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"

    def to_dict(self) -> dict[str, Any]:
        """Return a dict of column values. Useful for debugging and testing."""
        return {
            c.key: getattr(self, c.key)
            for c in self.__table__.columns  # type: ignore[attr-defined]
        }
