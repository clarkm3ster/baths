"""Safety event models — tracking violations and reports."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field
from sqlalchemy import DateTime, Float, String, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.database import Base


class SafetyEvent(Base):
    """A recorded safety threshold violation or alert."""

    __tablename__ = "safety_events"
    __table_args__ = {"schema": "safety"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    sphere_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    system_type: Mapped[str] = mapped_column(String(64), nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)  # warning|critical|emergency
    parameter: Mapped[str] = mapped_column(String(64), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    threshold: Mapped[float] = mapped_column(Float, nullable=False)
    resolved: Mapped[bool] = mapped_column(default=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    acknowledged: Mapped[bool] = mapped_column(default=False)


# Pydantic schemas

class SafetyViolation(BaseModel):
    system_type: str
    parameter: str
    value: float
    threshold: float
    severity: str
    description: str = ""


class SafetyReport(BaseModel):
    sphere_id: str
    timestamp: str
    all_clear: bool
    violations: list[SafetyViolation] = Field(default_factory=list)
    system_states: dict[str, Any] = Field(default_factory=dict)


class SafetyEventResponse(BaseModel):
    id: str
    sphere_id: str
    timestamp: str
    system_type: str
    severity: str
    parameter: str
    value: float
    threshold: float
    resolved: bool
    acknowledged: bool

    model_config = {"from_attributes": True}
