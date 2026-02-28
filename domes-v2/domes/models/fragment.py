"""
DOMES v2 — Fragment Model (Raw Ingested Data)

A Fragment is an atomic unit of data from a single external system.
Fragments are immutable once ingested — they represent the raw record
as received, before any normalization or enrichment.

The Fragment model is the input side of the DOMES pipeline:
  Source System → Fragment (raw) → Observation/Encounter/etc. (normalized)

Design principles:
- Immutable: raw_payload is never modified after creation
- Traceable: every normalized record traces back to a Fragment
- Consent-gated: every Fragment references a valid Consent
- Source-typed: FragmentSourceType drives the parser/normalizer pipeline
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import FragmentSourceType
from domes.models.base import (
    AuditMixin,
    DOMESBase,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from domes.models.consent import Consent
    from domes.models.person import Person


class Fragment(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    DOMESBase,
):
    """Raw data fragment from a single external source system.

    Immutable once created. Represents the exact payload received,
    before normalization. Every downstream record (Observation, Encounter,
    Condition, etc.) references the Fragment(s) that produced it.
    """

    __tablename__ = "fragment"
    __table_args__ = {
        "comment": (
            "Raw inbound data from external systems. Immutable once created. "
            "Every normalized record traces back to one or more Fragments."
        )
    }

    # ------------------------------------------------------------------
    # Core relations
    # ------------------------------------------------------------------

    person_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("person.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Person this fragment belongs to",
    )
    consent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("consent.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        comment=(
            "Consent under which this fragment was ingested. "
            "Ingestion is blocked if no valid consent exists."
        ),
    )

    # ------------------------------------------------------------------
    # Source metadata
    # ------------------------------------------------------------------

    source_type: Mapped[FragmentSourceType] = mapped_column(
        Enum(FragmentSourceType, name="fragment_source_type_enum"),
        nullable=False,
        comment="Type of source system (drives the normalizer pipeline)",
    )
    source_system_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Human-readable name of the source system",
    )
    source_system_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Identifier of the specific source system instance",
    )
    source_record_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        comment="The record ID in the source system (for deduplication)",
    )
    source_record_version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Version or ETag of the source record",
    )
    source_timestamp: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When the event/record occurred in the source system",
    )
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="When DOMES received this fragment",
    )

    # ------------------------------------------------------------------
    # Raw payload
    # ------------------------------------------------------------------

    raw_payload: Mapped[Any] = mapped_column(
        JSONB(),
        nullable=False,
        comment=(
            "The exact payload as received from the source system. "
            "Immutable — never modified after ingest."
        ),
    )
    payload_schema_version: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Schema version of the payload (for versioned normalizers)",
    )
    payload_size_bytes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Size of raw_payload in bytes (for monitoring)",
    )

    # ------------------------------------------------------------------
    # Processing status
    # ------------------------------------------------------------------

    is_processed: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        comment="True when the normalizer has processed this fragment",
    )
    processing_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Error message if processing failed",
    )
    processing_attempts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Number of normalizer processing attempts",
    )
    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When this fragment was successfully processed",
    )

    # ------------------------------------------------------------------
    # Deduplication
    # ------------------------------------------------------------------

    content_hash: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        index=True,
        comment=(
            "SHA-256 hash of raw_payload for deduplication. "
            "Fragments with identical content_hash are skipped."
        ),
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    person: Mapped["Person"] = relationship(
        "Person",
        back_populates="fragments",
        lazy="select",
    )
    consent: Mapped["Consent"] = relationship(
        "Consent",
        back_populates="fragments",
        lazy="select",
    )
