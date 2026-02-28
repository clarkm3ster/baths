"""
DOMES v2 — SQLAlchemy Declarative Base + Shared Mixins

All models inherit from DOMESBase. Mixins provide reusable column sets.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def _utcnow() -> datetime:
    """Return timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


class DOMESBase(DeclarativeBase):
    """Declarative base for all DOMES v2 models.

    Provides:
    - Type annotation support (SQLAlchemy 2.0 style)
    - Common __repr__ based on primary key
    - JSON serialization helper
    """

    type_annotation_map: dict[Any, Any] = {}  # Populated by subclasses

    def __repr__(self) -> str:
        pk_col = self.__class__.__table__.primary_key.columns
        pk_vals = {c.name: getattr(self, c.name, None) for c in pk_col}
        return f"<{self.__class__.__name__} {pk_vals}>"


# ---------------------------------------------------------------------------
# Mixins
# ---------------------------------------------------------------------------

class UUIDPrimaryKeyMixin:
    """UUID primary key — every core entity gets a UUID, never an integer."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="UUID primary key",
    )


class TimestampMixin:
    """created_at / updated_at timestamps — auto-managed by the database."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Row creation timestamp (UTC)",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Row last-updated timestamp (UTC)",
    )


class SoftDeleteMixin:
    """Soft-delete support — records are never hard-deleted, just flagged."""

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        comment="Soft-delete timestamp; NULL = active record",
    )
    deleted_reason: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        default=None,
        comment="Reason for soft-deletion (optional)",
    )

    @property
    def is_deleted(self) -> bool:
        """Return True if this record has been soft-deleted."""
        return self.deleted_at is not None


class PersonLinkedMixin:
    """Foreign key link to the Person table — used by almost every model."""

    # NOTE: The actual FK constraint is defined in each subclass using
    # ForeignKey("person.id") to avoid circular import issues. This mixin
    # documents the pattern; see person.py for FK definitions in models.
    pass


class FHIRMixin:
    """FHIR interoperability columns for models that map to FHIR resources."""

    fhir_resource_type: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        comment="FHIR resource type (e.g., 'Observation', 'Condition')",
    )
    fhir_resource_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        comment="FHIR resource ID in the originating system",
    )
    fhir_system: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
        comment="Base URL of the FHIR server this resource came from",
    )


class AuditMixin:
    """Who created / last modified a record — for audit trail compliance."""

    created_by: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="User / system that created this record",
    )
    updated_by: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="User / system that last updated this record",
    )
