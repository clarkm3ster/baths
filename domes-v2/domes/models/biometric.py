"""
DOMES v2 — BiometricReading Model

TimescaleDB hypertable-ready time-series model for continuous biometric data.
Designed for high-throughput ingestion from wearables and clinical devices.

TimescaleDB setup (run after table creation):
    SELECT create_hypertable(
        'biometric_reading', 'timestamp',
        partitioning_column => 'person_id',
        number_partitions => 4,
        chunk_time_interval => INTERVAL '1 week',
        if_not_exists => TRUE
    );

Design notes:
- (person_id, metric, timestamp) is the effective composite key for lookups
- value is NUMERIC for precision; raw_value stores string for non-numeric metrics
  (e.g., sleep_stage = 'rem')
- All timestamps are UTC with timezone
- metadata_ JSONB holds device-specific fields (CGM trend, confidence, etc.)
- source_fragment_id links back to the raw data fragment it was derived from
- is_anomaly flag set by real-time anomaly detection pipeline
- quality_score 0.0-1.0 (1.0 = perfect signal; <0.5 = unreliable)

LOINC codes for common biometric metrics:
    heart_rate       → 8867-4
    hrv_rmssd        → 80404-7
    blood_glucose    → 2339-0 (fasting) / 2345-7 (random)
    spo2             → 59408-5
    respiratory_rate → 9279-1
    bp_systolic      → 8480-6
    bp_diastolic     → 8462-4
    temperature_body → 8310-5
    steps            → 55423-8
    weight           → 29463-7
    bmi              → 39156-5
    vo2_max          → 80494-9
"""
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domes.enums import (
    BiometricDevice,
    BiometricMetric,
    CGMTrend,
    DataDomain,
)
from domes.models.base import (
    AuditMixin,
    DOMESBase,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)

if TYPE_CHECKING:
    from domes.models.fragment import Fragment
    from domes.models.person import Person


class BiometricReading(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    DOMESBase,
):
    """
    A single biometric measurement for a person at a point in time.

    This is the core time-series entity in DOMES. Converted to a TimescaleDB
    hypertable partitioned by timestamp (weekly chunks) and person_id (4 partitions).

    Indexes (beyond the hypertable auto-index):
        - idx_biometric_person_metric_time: (person_id, metric, timestamp DESC)
          — the primary access pattern: "give me all heart_rate for person X in last 7 days"
        - idx_biometric_anomaly: (person_id, is_anomaly) WHERE is_anomaly = true
          — fast anomaly dashboard queries
        - idx_biometric_device: (device, timestamp DESC)
          — device-level aggregation queries
    """

    __tablename__ = "biometric_reading"
    __table_args__ = (
        Index(
            "idx_biometric_person_metric_time",
            "person_id",
            "metric",
            "timestamp",
            postgresql_ops={"timestamp": "DESC"},
        ),
        Index(
            "idx_biometric_anomaly",
            "person_id",
            "is_anomaly",
            postgresql_where="is_anomaly = true",
        ),
        Index("idx_biometric_device_time", "device", "timestamp"),
        {
            "comment": (
                "TimescaleDB hypertable — biometric time-series readings. "
                "Run create_hypertable() after CREATE TABLE."
            )
        },
    )

    person_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("person.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Person this reading belongs to",
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="UTC timestamp of the measurement (hypertable partition key)",
    )
    metric: Mapped[BiometricMetric] = mapped_column(
        Enum(BiometricMetric, name="biometric_metric_enum", create_type=False),
        nullable=False,
        comment="Type of biometric measurement (BiometricMetric enum)",
    )
    value: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=12, scale=4),
        nullable=True,
        comment="Numeric measurement value. NULL for categorical metrics (e.g., sleep_stage).",
    )
    value_string: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        comment="String value for categorical metrics (e.g., sleep_stage='rem').",
    )
    unit: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="",
        comment="UCUM unit string (e.g., 'bpm', 'mg/dL', '%', 'ms', 'kcal', 'kg')",
    )
    loinc_code: Mapped[str | None] = mapped_column(
        String(16),
        nullable=True,
        comment="LOINC code for this metric (e.g., '8867-4' for heart rate)",
    )
    device: Mapped[BiometricDevice] = mapped_column(
        Enum(BiometricDevice, name="biometric_device_enum", create_type=False),
        nullable=False,
        default=BiometricDevice.UNKNOWN,
    )
    device_serial: Mapped[str | None] = mapped_column(String(128), nullable=True)
    data_domain: Mapped[DataDomain] = mapped_column(
        Enum(DataDomain, name="data_domain_enum", create_type=False),
        nullable=False,
        default=DataDomain.BIOMETRIC,
    )
    quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_anomaly: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    anomaly_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cgm_trend: Mapped[CGMTrend | None] = mapped_column(
        Enum(CGMTrend, name="cgm_trend_enum", create_type=False),
        nullable=True,
    )
    cgm_transmitter_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    interval_seconds: Mapped[int | None] = mapped_column(nullable=True)
    source_fragment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("fragment.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    metadata_: Mapped[Any | None] = mapped_column("metadata", JSONB(), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    person: Mapped[Person] = relationship("Person", back_populates="biometric_readings", lazy="select")
    source_fragment: Mapped[Fragment | None] = relationship(
        "Fragment", foreign_keys=[source_fragment_id], lazy="select"
    )

    @property
    def is_critical_glucose(self) -> bool:
        """True if blood glucose is critically low (<54 mg/dL Level 2 hypo) or >300 mg/dL"""
        if self.metric.value != "blood_glucose" or self.value is None:
            return False
        return float(self.value) < 54.0 or float(self.value) > 300.0
