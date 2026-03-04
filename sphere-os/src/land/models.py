"""SQLAlchemy models for the Land Intelligence Engine.

Defines ParcelRecord and ParcelCluster with PostGIS geometry columns.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime

from geoalchemy2 import Geometry
from sqlalchemy import (
    ARRAY,
    Boolean,
    Date,
    DateTime,
    Double,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.shared.database import Base


class ParcelCluster(Base):
    """A spatial cluster of adjacent vacant parcels identified by DBSCAN."""

    __tablename__ = "parcel_clusters"
    __table_args__ = {"schema": "land"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    geometry = mapped_column(Geometry("MULTIPOLYGON", srid=4326), nullable=False)
    total_area_sqft: Mapped[float] = mapped_column(Double, nullable=False, default=0)
    parcel_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    avg_viability_score: Mapped[float] = mapped_column(Double, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    parcels: Mapped[list[ParcelRecord]] = relationship(back_populates="cluster")


class ParcelRecord(Base):
    """An individual land parcel discovered from public data sources."""

    __tablename__ = "parcels"
    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_parcels_source_external"),
        {"schema": "land"},
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    source: Mapped[str] = mapped_column(String(64), nullable=False)
    external_id: Mapped[str] = mapped_column(String(128), nullable=False)

    # Geometry
    geometry = mapped_column(Geometry("POLYGON", srid=4326), nullable=True)
    centroid = mapped_column(Geometry("POINT", srid=4326), nullable=True, index=True)

    # Ownership
    ownership_type: Mapped[str | None] = mapped_column(String(64))
    owner_name: Mapped[str | None] = mapped_column(String(256))

    # Physical
    area_sqft: Mapped[float | None] = mapped_column(Double)
    street_frontage_ft: Mapped[float | None] = mapped_column(Double)

    # Zoning & Vacancy
    zoning: Mapped[str | None] = mapped_column(String(32))
    vacancy_score: Mapped[float | None] = mapped_column(Double)
    vacant_building_count: Mapped[int] = mapped_column(Integer, default=0)
    vacant_land_indicator: Mapped[bool] = mapped_column(Boolean, default=False)
    last_activity_date: Mapped[date | None] = mapped_column(Date)

    # Context
    census_block_group: Mapped[str | None] = mapped_column(String(32))
    transit_proximity_ft: Mapped[float | None] = mapped_column(Double)
    environmental_flags: Mapped[list[str]] = mapped_column(
        ARRAY(String), default=list, server_default="{}"
    )

    # Sphere viability (computed)
    sphere_viability_score: Mapped[float | None] = mapped_column(Double)
    sphere_viability_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Status
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="discovered")
    activated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Cluster relationship
    cluster_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("land.parcel_clusters.id"), nullable=True
    )
    cluster: Mapped[ParcelCluster | None] = relationship(back_populates="parcels")

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
