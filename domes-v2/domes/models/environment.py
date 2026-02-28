"""
DOMES v2 — EnvironmentReading Model

Environmental monitoring data linked to person-location-time.
Tracks air quality, noise, weather, and other environmental exposures
that directly affect health outcomes for vulnerable populations.

Environmental context matters enormously for DOMES characters:
- Robert Jackson (unsheltered): PM2.5 exposure from street sleeping
- Marcus Thompson (reentry): Noise levels in temporary housing
- Maria Rodriguez (foster care): Lead / indoor air quality in placement homes

Data sources:
- PurpleAir: Hyperlocal PM2.5 / PM10 sensors
- EPA AQS: Official air quality monitoring stations  
- OpenWeatherMap / Tomorrow.io: Temperature, humidity, UV, wind
- Direct sensors: On-device (phone) or placement-site sensors
- NOAA: Official weather data for climate analysis

SDOH connection:
Environmental readings feed into the EnvironmentalHarmony flourishing domain
and can trigger environmental health risk flags in the Dome snapshot.
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
    DataDomain,
    EnvironmentMetric,
    EnvironmentSource,
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


class EnvironmentReading(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    AuditMixin,
    DOMESBase,
):
    """
    A single environmental measurement at a person's location and time.

    This table is TimescaleDB hypertable-compatible. Run after table creation:

        SELECT create_hypertable(
            'environment_reading', 'timestamp',
            partitioning_column => 'person_id',
            number_partitions => 4,
            chunk_time_interval => INTERVAL '1 week',
            if_not_exists => TRUE
        );

    Location is captured as lat/lon text (not PostGIS Point) to avoid the
    PostGIS dependency in the base schema. Future versions may add a geometry
    column for spatial queries.

    AQI thresholds (EPA):
        0-50    Good
        51-100  Moderate
        101-150 Unhealthy for Sensitive Groups
        151-200 Unhealthy
        201-300 Very Unhealthy
        301-500 Hazardous
    """

    __tablename__ = "environment_reading"
    __table_args__ = (
        Index(
            "idx_env_person_metric_time",
            "person_id",
            "metric",
            "timestamp",
            postgresql_ops={"timestamp": "DESC"},
        ),
        Index(
            "idx_env_aqi_alert",
            "person_id",
            "aqi_category",
            postgresql_where="aqi_category IS NOT NULL",
        ),
        Index("idx_env_source_time", "source", "timestamp"),
        {
            "comment": (
                "TimescaleDB hypertable — environmental readings linked to person-location-time."
            )
        },
    )

    # ------------------------------------------------------------------
    # Core: who, what, when, where
    # ------------------------------------------------------------------

    person_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("person.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Person this environmental reading is associated with",
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="UTC timestamp of the environmental measurement",
    )

    metric: Mapped[EnvironmentMetric] = mapped_column(
        Enum(EnvironmentMetric, name="environment_metric_enum", create_type=False),
        nullable=False,
        comment="Type of environmental measurement",
    )

    # ------------------------------------------------------------------
    # Measurement value
    # ------------------------------------------------------------------

    value: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=4),
        nullable=False,
        comment="Numeric value of the environmental measurement",
    )

    unit: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="",
        comment="UCUM unit string (e.g., 'µg/m³', '°F', '%', 'dB', 'lux', 'mph')",
    )

    # ------------------------------------------------------------------
    # Air quality specific
    # ------------------------------------------------------------------

    aqi_category: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        comment=(
            "EPA AQI category when metric=aqi: "
            "'good', 'moderate', 'unhealthy_sensitive', 'unhealthy', "
            "'very_unhealthy', 'hazardous'"
        ),
    )

    pollutant: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
        comment="Primary pollutant (e.g., 'PM2.5', 'PM10', 'O3', 'NO2', 'CO', 'SO2')",
    )

    # ------------------------------------------------------------------
    # Location context
    # ------------------------------------------------------------------

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Decimal degrees latitude of measurement location",
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Decimal degrees longitude of measurement location",
    )

    location_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Human-readable location description (e.g., 'Grant Park, Chicago, IL')",
    )

    location_type: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        comment=(
            "Type of location: 'street', 'shelter', 'home', 'workplace', "
            "'transit', 'healthcare_facility', 'unknown'"
        ),
    )

    census_tract: Mapped[str | None] = mapped_column(
        String(16),
        nullable=True,
        comment="FIPS census tract code — enables SDOH neighborhood analysis",
    )

    zip_code: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
        comment="US ZIP code for the measurement location",
    )

    # ------------------------------------------------------------------
    # Data source
    # ------------------------------------------------------------------

    source: Mapped[EnvironmentSource] = mapped_column(
        Enum(EnvironmentSource, name="environment_source_enum", create_type=False),
        nullable=False,
        default=EnvironmentSource.MANUAL,
        comment="Data source for this reading",
    )

    sensor_id: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        comment="External sensor ID (e.g., PurpleAir sensor ID, EPA station code)",
    )

    # ------------------------------------------------------------------
    # Quality / confidence
    # ------------------------------------------------------------------

    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Data quality confidence 0.0–1.0 (1.0 = validated official reading)",
    )

    is_estimated: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment=(
            "True if this value was estimated/interpolated rather than directly measured. "
            "Estimated values are less reliable for clinical decision support."
        ),
    )

    # ------------------------------------------------------------------
    # Health relevance flags
    # ------------------------------------------------------------------

    exceeds_who_guideline: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
        comment=(
            "True if this reading exceeds the WHO guideline threshold for this metric. "
            "WHO PM2.5 annual: 5 µg/m³; WHO PM2.5 24h: 15 µg/m³."
        ),
    )

    exceeds_epa_standard: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
        comment=(
            "True if this reading exceeds EPA NAAQS standards. "
            "EPA PM2.5 annual: 12 µg/m³; EPA PM2.5 24h: 35 µg/m³."
        ),
    )

    # ------------------------------------------------------------------
    # Source linkage
    # ------------------------------------------------------------------

    source_fragment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("fragment.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Raw data fragment this reading was parsed from",
    )

    # ------------------------------------------------------------------
    # Extended metadata
    # ------------------------------------------------------------------

    metadata_: Mapped[Any | None] = mapped_column(
        "metadata",
        JSONB(),
        nullable=True,
        comment=(
            "Source-specific extended fields. Examples: "
            "PurpleAir: {confidence_pct, channel_a_pm25, channel_b_pm25}, "
            "OpenWeatherMap: {weather_id, description, icon}, "
            "NOAA: {station_id, observation_type}"
        ),
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Clinical or contextual notes about this environmental reading",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    person: Mapped[Person] = relationship(
        "Person",
        back_populates="environment_readings",
        lazy="select",
    )

    source_fragment: Mapped[Fragment | None] = relationship(
        "Fragment",
        foreign_keys=[source_fragment_id],
        lazy="select",
    )

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def is_hazardous_aqi(self) -> bool:
        """Return True if AQI reading is in the hazardous range (>300)."""
        if self.metric != EnvironmentMetric.AQI:
            return False
        return self.value is not None and float(self.value) > 300

    @property
    def is_health_risk(self) -> bool:
        """Return True if this reading poses a health risk based on EPA/WHO thresholds."""
        return bool(self.exceeds_who_guideline or self.exceeds_epa_standard or self.is_hazardous_aqi)
