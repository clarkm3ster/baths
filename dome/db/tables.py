"""DOME ORM table definitions.

All tables use SQLAlchemy 2.0 ``DeclarativeBase`` with ``mapped_column``.
Complex nested data is stored in JSON columns so the relational layer stays
simple while the domain model remains rich.
"""

from __future__ import annotations

import datetime
from typing import Optional

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------


class Base(DeclarativeBase):
    """Shared declarative base for every DOME table."""

    pass


# ---------------------------------------------------------------------------
# PersonTable
# ---------------------------------------------------------------------------


class PersonTable(Base):
    """Core person record — the single source of truth for an individual
    inside THE DOME.

    All deeply nested profile, state, metrics, and budget data live in JSON
    columns so the schema can evolve without constant migrations.
    """

    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    person_uid: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )

    # --- JSON blobs ---
    identity_spine_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    static_profile_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    dynamic_state_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    dome_metrics_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    budget_key_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    budget_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    trajectory_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # --- Timestamps ---
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # --- Relationships ---
    fiscal_events: Mapped[list["FiscalEventTable"]] = relationship(
        back_populates="person", cascade="all, delete-orphan"
    )
    cascade_alerts: Mapped[list["CascadeAlertTable"]] = relationship(
        back_populates="person", cascade="all, delete-orphan"
    )
    intervention_plans: Mapped[list["InterventionPlanTable"]] = relationship(
        back_populates="person", cascade="all, delete-orphan"
    )
    simulation_results: Mapped[list["SimulationResultTable"]] = relationship(
        back_populates="person", cascade="all, delete-orphan"
    )
    settlement_matrices: Mapped[list["SettlementMatrixTable"]] = relationship(
        back_populates="person", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Person uid={self.person_uid!r}>"


# ---------------------------------------------------------------------------
# FiscalEventTable
# ---------------------------------------------------------------------------


class FiscalEventTable(Base):
    """A single fiscal event — one payment, one claim line, one transaction.

    Captures *who paid*, *how much*, *for what*, and *at what confidence*.
    """

    __tablename__ = "fiscal_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(
        String(128), unique=True, nullable=False, index=True
    )
    person_uid: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("persons.person_uid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event_date: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # --- Payer / program ---
    payer_level: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    payer_entity: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    program_or_fund: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    # --- Service classification ---
    domain: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    mechanism: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    service_category: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    # --- Quantity / amount ---
    utilization_unit: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    quantity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    amount_paid: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    amount_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    # --- Provenance ---
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    data_source_system: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True
    )
    attribution_tags_json: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True
    )

    # --- Timestamps ---
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # --- Relationships ---
    person: Mapped["PersonTable"] = relationship(back_populates="fiscal_events")

    __table_args__ = (
        Index("ix_fiscal_events_person_date", "person_uid", "event_date"),
    )

    def __repr__(self) -> str:
        return f"<FiscalEvent id={self.event_id!r} person={self.person_uid!r}>"


# ---------------------------------------------------------------------------
# CascadeAlertTable
# ---------------------------------------------------------------------------


class CascadeAlertTable(Base):
    """An alert raised when a cascade failure pattern is detected for a person.

    Contains the projected costs for path-A (status quo) vs path-B
    (intervention) and the recommended actions.
    """

    __tablename__ = "cascade_alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    alert_id: Mapped[str] = mapped_column(
        String(128), unique=True, nullable=False, index=True
    )
    person_uid: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("persons.person_uid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    cascade_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    current_link_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    detected_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # --- Projections ---
    path_a_projected_cost: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True
    )
    path_b_projected_cost: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True
    )

    recommended_interventions_json: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True
    )

    # --- Timestamps ---
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # --- Relationships ---
    person: Mapped["PersonTable"] = relationship(back_populates="cascade_alerts")
    intervention_plans: Mapped[list["InterventionPlanTable"]] = relationship(
        back_populates="cascade_alert", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_cascade_alerts_person_cascade", "person_uid", "cascade_id"),
    )

    def __repr__(self) -> str:
        return f"<CascadeAlert id={self.alert_id!r} person={self.person_uid!r}>"


# ---------------------------------------------------------------------------
# InterventionPlanTable
# ---------------------------------------------------------------------------


class InterventionPlanTable(Base):
    """A concrete intervention plan generated in response to a cascade alert.

    Stores the list of interventions, their combined cost, expected savings,
    and computed ROI.
    """

    __tablename__ = "intervention_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plan_id: Mapped[str] = mapped_column(
        String(128), unique=True, nullable=False, index=True
    )
    person_uid: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("persons.person_uid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    cascade_alert_id: Mapped[Optional[str]] = mapped_column(
        String(128),
        ForeignKey("cascade_alerts.alert_id", ondelete="SET NULL"),
        nullable=True,
    )

    interventions_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    total_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    expected_savings: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    expected_roi: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # --- Timestamps ---
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # --- Relationships ---
    person: Mapped["PersonTable"] = relationship(back_populates="intervention_plans")
    cascade_alert: Mapped[Optional["CascadeAlertTable"]] = relationship(
        back_populates="intervention_plans"
    )

    def __repr__(self) -> str:
        return f"<InterventionPlan id={self.plan_id!r} person={self.person_uid!r}>"


# ---------------------------------------------------------------------------
# SimulationResultTable
# ---------------------------------------------------------------------------


class SimulationResultTable(Base):
    """Persisted output from a Monte Carlo or deterministic simulation run.

    Stores median outcomes for both paths, the net DOME cost, ROI, and the
    full results blob for drill-down.
    """

    __tablename__ = "simulation_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    person_uid: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("persons.person_uid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    simulation_type: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    path_a_median: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    path_b_median: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    dome_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    dome_roi: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    results_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # --- Timestamps ---
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # --- Relationships ---
    person: Mapped["PersonTable"] = relationship(back_populates="simulation_results")

    __table_args__ = (
        Index("ix_simulation_results_person_type", "person_uid", "simulation_type"),
    )

    def __repr__(self) -> str:
        return (
            f"<SimulationResult person={self.person_uid!r} "
            f"type={self.simulation_type!r}>"
        )


# ---------------------------------------------------------------------------
# SettlementMatrixTable
# ---------------------------------------------------------------------------


class SettlementMatrixTable(Base):
    """A settlement-matrix snapshot — who pays, who saves, and the transfers
    required to realign incentives across payers for a given person and
    scenario.
    """

    __tablename__ = "settlement_matrices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    person_uid: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("persons.person_uid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    scenario_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    horizon_label: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    payers_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    transfers_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    assumptions_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    generated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    model_version: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    # --- Timestamps ---
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # --- Relationships ---
    person: Mapped["PersonTable"] = relationship(back_populates="settlement_matrices")

    __table_args__ = (
        Index("ix_settlement_matrices_person_scenario", "person_uid", "scenario_id"),
    )

    def __repr__(self) -> str:
        return (
            f"<SettlementMatrix person={self.person_uid!r} "
            f"scenario={self.scenario_id!r}>"
        )
