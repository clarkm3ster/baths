"""SPHERE/OS Scheduling Models — Sphere, TimeSlice, Booking, MaterialConfiguration.

Defines the temporal operating system data layer for managing Sphere time slices,
bookings, and material configuration state.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime
from typing import Any, TypedDict

from sqlalchemy import (
    ARRAY,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.shared.database import Base


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class SphereStatus(str, enum.Enum):
    planning = "planning"
    construction = "construction"
    active_production = "active_production"
    legacy_soundstage = "legacy_soundstage"
    public_access = "public_access"
    dormant = "dormant"


class SphereMode(str, enum.Enum):
    production = "production"
    public = "public"
    community = "community"
    maintenance = "maintenance"


class TimeSliceMode(str, enum.Enum):
    production = "production"
    public = "public"
    community = "community"
    maintenance = "maintenance"
    transition = "transition"


class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


# ---------------------------------------------------------------------------
# MaterialConfiguration TypedDict (stored as JSONB)
# ---------------------------------------------------------------------------


class ScentProfile(TypedDict, total=False):
    primary: str | None
    secondary: str | None
    intensity: float  # 0-1


class ShapeMemoryElement(TypedDict):
    element_id: str
    target_curvature: float  # 0-1


class MaterialConfiguration(TypedDict, total=False):
    """Full material configuration stored as JSONB on Sphere.base_state and TimeSlice.material_config.

    All fields are optional (total=False) so partial configs are valid for updates.
    """

    acoustic_reverb_time_seconds: float  # 0.5-5.0
    acoustic_absorption_profile: list[float]  # 7 frequency bands
    wall_color_rgb: list[int]  # [r, g, b] — JSON doesn't support tuples
    wall_opacity: float  # 0-1
    light_color_temp_kelvin: int  # 2700-6500
    light_intensity_lux: int  # 50-1000
    floor_haptic_pattern: str  # off|gentle_rain|heartbeat|earthquake
    floor_haptic_intensity: float  # 0-1
    scent_profile: ScentProfile
    thermal_target_celsius: float  # 16-28
    shape_memory_elements: list[ShapeMemoryElement]


# ---------------------------------------------------------------------------
# Default / neutral MaterialConfiguration
# ---------------------------------------------------------------------------

NEUTRAL_MATERIAL_CONFIG: MaterialConfiguration = {
    "acoustic_reverb_time_seconds": 1.0,
    "acoustic_absorption_profile": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    "wall_color_rgb": [200, 200, 200],
    "wall_opacity": 1.0,
    "light_color_temp_kelvin": 4000,
    "light_intensity_lux": 300,
    "floor_haptic_pattern": "off",
    "floor_haptic_intensity": 0.0,
    "scent_profile": {"primary": None, "secondary": None, "intensity": 0.0},
    "thermal_target_celsius": 22.0,
    "shape_memory_elements": [],
}


# ---------------------------------------------------------------------------
# SQLAlchemy ORM Models
# ---------------------------------------------------------------------------


class Sphere(Base):
    """A programmable material environment on a specific land parcel."""

    __tablename__ = "spheres"
    __table_args__ = {"schema": "scheduling"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    parcel_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
        comment="FK to land.parcels.id — nullable during planning phase",
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[SphereStatus] = mapped_column(
        Enum(SphereStatus, name="sphere_status", schema="scheduling"),
        nullable=False,
        default=SphereStatus.planning,
    )
    material_inventory: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list,
        server_default="{}",
        comment="Available material systems: acoustic, electrochromic, projection, haptic, olfactory, thermal_pcm, shape_memory, deployable_4d",
    )
    current_mode: Mapped[SphereMode] = mapped_column(
        Enum(SphereMode, name="sphere_mode", schema="scheduling"),
        nullable=False,
        default=SphereMode.maintenance,
    )
    base_state: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: dict(NEUTRAL_MATERIAL_CONFIG),
        comment="Current MaterialConfiguration as JSONB",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.utcnow,
    )

    # Relationships
    time_slices: Mapped[list["TimeSlice"]] = relationship(
        back_populates="sphere",
        cascade="all, delete-orphan",
        order_by="TimeSlice.start_time",
    )


class TimeSlice(Base):
    """A discrete time window within a Sphere with specific material configuration."""

    __tablename__ = "time_slices"
    __table_args__ = {"schema": "scheduling"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    sphere_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scheduling.spheres.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    mode: Mapped[TimeSliceMode] = mapped_column(
        Enum(TimeSliceMode, name="time_slice_mode", schema="scheduling"),
        nullable=False,
        default=TimeSliceMode.public,
    )
    material_config: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=lambda: dict(NEUTRAL_MATERIAL_CONFIG),
        comment="Desired MaterialConfiguration for this slice",
    )
    transition_buffer_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Calculated transition time FROM previous slice (minutes, rounded up)",
    )
    booking_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scheduling.bookings.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    # Relationships
    sphere: Mapped["Sphere"] = relationship(back_populates="time_slices")
    booking: Mapped["Booking | None"] = relationship(back_populates="time_slices")


class Booking(Base):
    """A user's reservation of a Sphere time slice with material preferences."""

    __tablename__ = "bookings"
    __table_args__ = {"schema": "scheduling"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        comment="User requesting the booking (external identity system)",
    )
    sphere_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scheduling.spheres.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    material_request: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        comment="User-requested MaterialConfiguration",
    )
    material_actual: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="Actual MaterialConfiguration applied (may differ from request)",
    )
    pricing_usd: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )
    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus, name="booking_status", schema="scheduling"),
        nullable=False,
        default=BookingStatus.pending,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.utcnow,
    )

    # Relationships
    time_slices: Mapped[list["TimeSlice"]] = relationship(
        back_populates="booking",
        cascade="all, delete-orphan",
        order_by="TimeSlice.start_time",
    )
