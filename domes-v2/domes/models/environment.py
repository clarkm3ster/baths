"""
DOMES v2 — EnvironmentReading Model

Environmental monitoring data linked to person-location-time.
Captures ambient conditions that affect health outcomes.

Data sources:
- EPA AQI API (air quality)
- OpenWeatherMap (temperature, humidity, pressure)
- CDC SVI / USALEEP (neighborhood life expectancy)
- Custom IoT sensors (shelter air quality monitors)
- NOAA (extreme weather events)

Key LOINC codes:
    89765-0: Air quality index observable
    60832-3: PM2.5 respirable particulate [Mass/volume] in Air
    59408-5: Oxygen saturation by pulse oximetry (for indoor O2)
    8310-5:  Body temperature (ambient temp context)
    75860-7: Blood lead level (for lead exposure)

CDC Social Vulnerability Index dimensions stored in metadata_:
    {svi_overall, svi_socioeconomic, svi_household, svi_minority, svi_housing}
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

from domes.enums import DataDomain, EnvironmentMetric
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
    A single environmental measurement at a location and time.

    Environmental data is linked to persons via their location at time of reading.
    This enables correlation of air quality, temperature, and neighborhood conditions
    with health outcomes in the DOMES flourishing score.

    TimescaleDB hypertable candidate (like biometric_reading).
    """

    __tablename__ = "environment_reading"
    __table_args__ = (
        Index(
            "idx_env_person_metric_time",
            "person_id",
            "metric",
            "timestamp",
        ),
        Index("idx_env_location", "latitude", "longitude"),
        {
            "comment": (
                "Environmental readings linked to person-location-time. "
                "Air quality, temperature, neighborhood conditions."
            )
        },
    )

    # ------------------------------------------------------------------
    # Core
    # ------------------------------------------------------------------

    person_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("person.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )
    metric: Mapped[EnvironmentMetric] = mapped_column(
        Enum(EnvironmentMetric, name="environment_metric_enum", create_type=False),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Value
    # ------------------------------------------------------------------

    value: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=12, scale=4),
        nullable=True,
    )
    value_string: Mapped[str | None] = mapped_column(String(64), nullable=True)
    unit: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    loinc_code: Mapped[str | None] = mapped_column(String(16), nullable=True)

    # ------------------------------------------------------------------
    # Location
    # ------------------------------------------------------------------

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="WGS84 latitude",
    )
    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="WGS84 longitude",
    )
    census_tract: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="11-digit FIPS census tract code",
    )
    zip_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    neighborhood: Mapped[str | None] = mapped_column(String(100), nullable=True)
    county_fips: Mapped[str | None] = mapped_column(String(10), nullable=True)

    # ------------------------------------------------------------------
    # Source
    # ------------------------------------------------------------------

    data_source: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Data source (e.g., 'EPA AirNow', 'OpenWeatherMap', 'NOAA')",
    )
    data_domain: Mapped[DataDomain] = mapped_column(
        Enum(DataDomain, name="data_domain_enum", create_type=False),
        nullable=False,
        default=DataDomain.ENVIRONMENTAL,
    )
    source_fragment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("fragment.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Quality / alerts
    # ------------------------------------------------------------------

    quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_anomaly: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    exceeds_who_guideline: Mapped[bool | None] = mapped_column(
        nullable=True,
        comment="True if value exceeds WHO guideline (stricter than EPA)",
    )
    exceeds_epa_standard: Mapped[bool | None] = mapped_column(
        nullable=True,
        comment="True if value exceeds EPA NAAQS standard",
    )
    is_hazardous_aqi: Mapped[bool | None] = mapped_column(
        nullable=True,
        comment="True if AQI >= 301 (Hazardous category)",
    )

    # ------------------------------------------------------------------
    # AQI-specific
    # ------------------------------------------------------------------

    aqi_category: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="AQI category: Good/Moderate/USG/Unhealthy/Very Unhealthy/Hazardous",
    )
    aqi_pollutant: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="Determining pollutant for AQI (PM2.5, PM10, O3, NO2, SO2, CO)",
    )

    # ------------------------------------------------------------------
    # SVI neighborhood data
    # ------------------------------------------------------------------

    svi_overall: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="CDC SVI overall percentile rank (0=lowest vulnerability, 1=highest)",
    )
    life_expectancy_years: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Neighborhood life expectancy from CDC USALEEP",
    )

    # ------------------------------------------------------------------
    # Extended
    # ------------------------------------------------------------------

    metadata_: Mapped[Any | None] = mapped_column("metadata", JSONB(), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    person: Mapped[Person] = relationship(
        "Person", back_populates="environment_readings", lazy="select"
    )
    source_fragment: Mapped[Fragment | None] = relationship(
        "Fragment", foreign_keys=[source_fragment_id], lazy="select"
    )

    @property
    def is_air_quality_hazard(self) -> bool:
        """True if any air quality threshold is exceeded."""
        return bool(self.exceeds_who_guideline or self.exceeds_epa_standard or self.is_hazardous_aqi)
