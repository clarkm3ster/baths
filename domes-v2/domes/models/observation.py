"""
DOMES v2 — Observation Model (FHIR-aligned)

Observations are normalized, structured data points derived from Fragments.
They follow the FHIR Observation resource structure:
- A coded observation type (LOINC, SNOMED, custom)
- A value (quantity, string, boolean, or coded)
- A time window (effective_start / effective_end)
- A category (vital-signs, laboratory, social-history, survey, sdoh, etc.)

Observations are the workhorse of the DOMES pipeline — they represent
the normalized, queryable form of data after ingestion.

FHIR alignment: https://hl7.org/fhir/R4/observation.html
US Core Observation profiles: https://hl7.org/fhir/us/core/
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import (
    CodeSystem,
    ObservationCategory,
    ObservationStatus,
)
from domes.models.base import (
    AuditMixin,
    DOMESBase,
    FHIRMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from domes.models.person import Person


class Observation(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    FHIRMixin,
    DOMESBase,
):
    """A single normalized observation — the FHIR Observation equivalent.

    Created by the normalizer pipeline from raw Fragments. Each Observation
    represents a single data point about a person at a specific time.
    """

    __tablename__ = "observation"
    __table_args__ = {
        "comment": (
            "Normalized, structured observations derived from Fragment ingestion. "
            "Follows FHIR Observation R4 structure. Primary queryable data store."
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
        comment="Person this observation belongs to",
    )

    # ------------------------------------------------------------------
    # FHIR Observation.code — what was observed
    # ------------------------------------------------------------------

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="The observation code (LOINC code, SNOMED code, or custom code)",
    )
    code_system: Mapped[CodeSystem] = mapped_column(
        Enum(CodeSystem, name="code_system_enum"),
        nullable=False,
        default=CodeSystem.LOINC,
        comment="Coding system for the observation code",
    )
    code_display: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Human-readable display name for the code",
    )

    # ------------------------------------------------------------------
    # FHIR Observation.category
    # ------------------------------------------------------------------

    category: Mapped[ObservationCategory] = mapped_column(
        Enum(ObservationCategory, name="observation_category_enum"),
        nullable=False,
        comment="FHIR observation category — drives UI display and querying",
    )

    # ------------------------------------------------------------------
    # FHIR Observation.status
    # ------------------------------------------------------------------

    status: Mapped[ObservationStatus] = mapped_column(
        Enum(ObservationStatus, name="observation_status_enum"),
        nullable=False,
        default=ObservationStatus.FINAL,
        comment="FHIR Observation.status",
    )

    # ------------------------------------------------------------------
    # FHIR Observation.effective[x] — time window
    # ------------------------------------------------------------------

    effective_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="When this observation started (FHIR effectiveDateTime or effectivePeriod.start)",
    )
    effective_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When this observation ended (FHIR effectivePeriod.end; NULL for point-in-time)",
    )

    # ------------------------------------------------------------------
    # FHIR Observation.value[x] — the actual value
    # ------------------------------------------------------------------

    value_quantity: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Numeric value (for valueQuantity)",
    )
    value_unit: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Unit of the numeric value (UCUM units, e.g., 'mg/dL', 'kg', '%')",
    )
    value_string: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="String value (for valueString)",
    )
    value_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Coded value (for valueCodeableConcept.coding.code)",
    )
    value_boolean: Mapped[bool | None] = mapped_column(
        nullable=True,
        comment="Boolean value (for valueBoolean)",
    )
    value_json: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment="Full FHIR Observation.value[x] as JSON for complex value types",
    )

    # ------------------------------------------------------------------
    # Interpretation / Reference range
    # ------------------------------------------------------------------

    interpretation_code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="FHIR Observation.interpretation (H, L, N, A, etc.)",
    )
    reference_range_low: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Reference range lower bound",
    )
    reference_range_high: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Reference range upper bound",
    )

    # ------------------------------------------------------------------
    # Source provenance
    # ------------------------------------------------------------------

    source_fragment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        comment="Fragment that produced this observation (for traceability)",
    )
    source_system_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="System that produced this observation",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    person: Mapped["Person"] = relationship(
        "Person",
        back_populates="observations",
        lazy="select",
    )
