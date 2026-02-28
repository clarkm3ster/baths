"""
DOMES v2 — Fragment Model (Raw Ingested Data)

A Fragment is the smallest unit of input data in DOMES. Every record from
every government system — a FHIR Observation, an HMIS enrollment, an EHR
discharge summary, a wearable data packet — enters as a Fragment before
being normalized and assembled into the digital twin.

The Fragment model tracks the full lifecycle of data:
  ingested_at → validated_at → assembled_at

Key design:
- raw_payload: Original data exactly as received (JSONB) — immutable
- normalized_payload: FHIR-normalized version for standardized processing
- Every Fragment must reference a valid Consent that authorized its ingestion
- is_superseded flags when newer data has replaced a Fragment
- quality_score enables filtering low-quality data from dome assembly
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import DataDomain, FragmentSourceType
from domes.models.base import (
    AuditMixin,
    DOMESBase,
    FHIRMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from domes.models.consent import Consent
    from domes.models.person import Person
    from domes.models.system import GovernmentSystem


class Fragment(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    FHIRMixin,
    DOMESBase,
):
    """Raw data fragment from any source system.

    A Fragment is the input side of the DOMES pipeline. It captures a single
    atomic record from an external system — a FHIR resource, an HMIS row, a
    wearable telemetry packet, etc. — in its original form plus a normalized
    version for processing.

    The Fragment → Observation / Condition / Encounter pipeline:
    1. Fragment arrives (raw_payload stored unchanged)
    2. Validation runs (validated_at set; errors noted in validation_errors)
    3. Normalization transforms raw_payload → normalized_payload (FHIR-aligned)
    4. Assembly extracts typed records (Observation, Condition, etc.)
    5. assembled_at set; Fragment linked to assembled records

    Privacy: every Fragment must link to a Consent that authorized its ingestion.
    If consent is revoked, is_superseded = True.
    """

    __tablename__ = "fragment"
    __table_args__ = {
        "comment": (
            "Raw data fragments from all source systems. "
            "Every external data record enters DOMES as a Fragment before assembly. "
            "raw_payload is immutable — the original source record."
        )
    }

    # ------------------------------------------------------------------
    # Relations
    # ------------------------------------------------------------------

    person_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("person.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Person this fragment belongs to",
    )
    source_system_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("government_system.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Government / external system that originated this data",
    )
    consent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("consent.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment=(
            "Consent that authorized ingestion of this data. "
            "NULL allowed for non-consent-required data (environmental, census). "
            "Required for health and behavioral health data."
        ),
    )
    superseded_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("fragment.id", ondelete="SET NULL"),
        nullable=True,
        comment="ID of the newer Fragment that supersedes this one",
    )

    # ------------------------------------------------------------------
    # Source classification
    # ------------------------------------------------------------------

    source_type: Mapped[FragmentSourceType] = mapped_column(
        Enum(FragmentSourceType, name="fragment_source_type_enum"),
        nullable=False,
        comment="Type of source system that generated this fragment",
    )
    data_domain: Mapped[DataDomain] = mapped_column(
        Enum(DataDomain, name="fragment_data_domain_enum"),
        nullable=False,
        comment="Data sensitivity domain — drives consent requirements",
    )
    source_record_id: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
        index=True,
        comment="Original record ID in the source system (for deduplication and traceability)",
    )
    source_record_version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Version / etag of the source record (for change detection)",
    )
    source_record_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Resource type in the source system (e.g., FHIR 'Observation', HMIS 'Enrollment')",
    )

    # ------------------------------------------------------------------
    # Payload storage (the actual data)
    # ------------------------------------------------------------------

    raw_payload: Mapped[Any] = mapped_column(
        JSONB(),
        nullable=False,
        comment=(
            "The original data exactly as received from the source system. "
            "IMMUTABLE — never modify this after ingestion. "
            "Serves as the audit trail / source of truth."
        ),
    )
    normalized_payload: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment=(
            "FHIR R4-normalized version of the raw_payload. "
            "Produced by the normalization service. "
            "NULL until normalization is complete."
        ),
    )

    # ------------------------------------------------------------------
    # Lifecycle timestamps
    # ------------------------------------------------------------------

    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="When this fragment arrived at the DOMES ingest API",
    )
    validated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When validation completed (NULL = not yet validated)",
    )
    normalized_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When normalization to FHIR completed",
    )
    assembled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When assembly into typed records (Observation, Condition, etc.) completed",
    )

    # ------------------------------------------------------------------
    # Quality and status
    # ------------------------------------------------------------------

    quality_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment=(
            "Data quality score 0.0–1.0. "
            "Computed from: completeness, consistency, timeliness, accuracy. "
            "Fragments with score < 0.3 are excluded from dome assembly by default."
        ),
    )
    validation_errors: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment="Array of validation error objects from the validation service",
    )
    is_superseded: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment=(
            "True when a newer Fragment has replaced this one. "
            "Superseded fragments are excluded from dome assembly. "
            "They are NEVER deleted — maintained for audit trail."
        ),
    )
    processing_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Human-readable notes from the ingestion/normalization pipeline",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    person: Mapped["Person"] = relationship(
        "Person",
        back_populates="fragments",
        lazy="select",
    )
    source_system: Mapped["GovernmentSystem | None"] = relationship(
        "GovernmentSystem",
        back_populates="fragments",
        lazy="select",
    )
    consent: Mapped["Consent | None"] = relationship(
        "Consent",
        back_populates="fragments",
        lazy="select",
    )
    superseded_by: Mapped["Fragment | None"] = relationship(
        "Fragment",
        remote_side="Fragment.id",
        lazy="select",
    )
