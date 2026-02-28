"""
DOMES v2 — Observation Model (FHIR-aligned)

Observations capture structured measurements, assessments, and social history.
Aligned with FHIR R4 Observation resource and US Core profiles.

Covers:
- Vital signs (blood pressure, heart rate, temperature, SpO2, weight, BMI)
- Laboratory results (glucose, HbA1c, CBC, metabolic panels)
- Social history (housing status, smoking, substance use)
- Survey results (PHQ-9 total, GAD-7 total, VI-SPDAT scores)
- SDOH conditions (Z-codes: Z59.0 homelessness, Z59.4 food insecurity)

Key LOINC codes for DOMES:
- 85354-9: Blood pressure panel
- 2339-0: Blood glucose
- 4548-4: HbA1c
- 44261-6: PHQ-9 panel
- 71802-3: Housing status (LOINC)
- 98968-2: VI-SPDAT score
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
    from domes.models.fragment import Fragment
    from domes.models.person import Person
    from domes.models.system import GovernmentSystem


class Observation(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    FHIRMixin,
    DOMESBase,
):
    """A structured measurement, assessment result, or social observation.

    FHIR resource type: Observation
    US Core profiles supported:
    - us-core-vital-signs
    - us-core-observation-lab
    - us-core-observation-screening-assessment
    - us-core-observation-social-history
    - SDOHCC-Observation (Gravity Project)

    Value types supported (FHIR value[x]):
    - valueQuantity: numeric with unit (most vitals and labs)
    - valueString: free text
    - valueCodeableConcept: coded value (housing status, etc.)
    - component[]: multi-component observations (blood pressure = systolic + diastolic)
    """

    __tablename__ = "observation"
    __table_args__ = {
        "comment": (
            "Structured clinical and social observations (FHIR Observation). "
            "Covers vitals, labs, assessments, and social history."
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
    )
    fragment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("fragment.id", ondelete="SET NULL"),
        nullable=True,
        comment="Source fragment this observation was assembled from",
    )
    performer_system_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("government_system.id", ondelete="SET NULL"),
        nullable=True,
        comment="System / organization that performed this observation",
    )

    # ------------------------------------------------------------------
    # FHIR Observation fields
    # ------------------------------------------------------------------

    status: Mapped[ObservationStatus] = mapped_column(
        Enum(ObservationStatus, name="observation_status_enum"),
        nullable=False,
        default=ObservationStatus.FINAL,
        comment="FHIR Observation.status",
    )
    category: Mapped[ObservationCategory] = mapped_column(
        Enum(ObservationCategory, name="observation_category_enum"),
        nullable=False,
        comment="FHIR observation-category code",
    )

    # ------------------------------------------------------------------
    # Code (what was observed)
    # ------------------------------------------------------------------

    code_system: Mapped[CodeSystem] = mapped_column(
        Enum(CodeSystem, name="obs_code_system_enum"),
        nullable=False,
        default=CodeSystem.LOINC,
        comment="Coding system (LOINC, SNOMED CT, ICD-10-CM, etc.)",
    )
    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="The observation code (e.g., '8480-6' for systolic BP in LOINC)",
    )
    code_display: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Human-readable code description",
    )

    # ------------------------------------------------------------------
    # Value (what was found) — FHIR value[x] pattern
    # ------------------------------------------------------------------

    value_quantity: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Numeric observation value (for valueQuantity)",
    )
    value_unit: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="UCUM unit code (e.g., 'mmHg', 'mg/dL', '%', 'kg')",
    )
    value_unit_display: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Human-readable unit",
    )
    value_string: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Free-text value (for valueString)",
    )
    value_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Coded value (for valueCodeableConcept.coding.code)",
    )
    value_code_display: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Human-readable coded value",
    )
    value_boolean: Mapped[bool | None] = mapped_column(
        nullable=True,
        comment="Boolean value (for valueBoolean)",
    )
    value_integer: Mapped[int | None] = mapped_column(
        nullable=True,
        comment="Integer value (for survey scores like PHQ-9)",
    )

    # ------------------------------------------------------------------
    # Interpretation and reference range
    # ------------------------------------------------------------------

    interpretation_code: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
        comment="HL7 ObservationInterpretation code: H=High, L=Low, N=Normal, A=Abnormal",
    )
    interpretation_display: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Human-readable interpretation",
    )
    reference_range_low: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Lower bound of reference range",
    )
    reference_range_high: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Upper bound of reference range",
    )

    # ------------------------------------------------------------------
    # Multi-component support (blood pressure, PHQ-9 items)
    # ------------------------------------------------------------------

    components: Mapped[Any | None] = mapped_column(
        JSONB(),
        nullable=True,
        comment=(
            "For multi-component observations (e.g., blood pressure). "
            "Array of {code, code_display, value_quantity, value_unit, value_string}"
        ),
    )

    # ------------------------------------------------------------------
    # Effective time
    # ------------------------------------------------------------------

    effective_datetime: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        comment="When this observation was made (point in time)",
    )
    effective_period_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Start of observation period (for period observations)",
    )
    effective_period_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="End of observation period",
    )

    # ------------------------------------------------------------------
    # Data sensitivity (DS4P security labels)
    # ------------------------------------------------------------------

    sensitivity_label: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment=(
            "DS4P security label for sensitive data: "
            "'ETHUD' (alcohol), 'OPIOIDUD', 'SBUD' (substance use), 'PSY' (psychiatric), "
            "'HIV'. NULL = normal sensitivity."
        ),
    )
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Clinical notes associated with this observation",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    person: Mapped["Person"] = relationship(
        "Person",
        back_populates="observations",
        lazy="select",
    )
    fragment: Mapped["Fragment | None"] = relationship(
        "Fragment",
        lazy="select",
    )
    performer_system: Mapped["GovernmentSystem | None"] = relationship(
        "GovernmentSystem",
        lazy="select",
    )
