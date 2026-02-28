"""
DOMES v2 — Unified API Gateway
================================

This is the front door of the DOMES v2 system. A FastAPI application that
exposes every capability of the Directed Outcome Modeling & Engineering
System through a single, versioned REST API.

Architecture
------------
All endpoints are async and return JSON. Response models are defined here
using Pydantic v2. Because the service layer (prediction.py, flourishing.py,
fragment.py, cosm.py) is being assembled in parallel, this module defines
*placeholder* functions that return realistic mock data for the primary
subject: **Robert Jackson**.

When the service layer is ready, replace the placeholder calls in each
endpoint with::

    from domes.services.prediction import PredictionService
    from domes.services.flourishing import FlourishingService
    # etc.

Authentication
--------------
Endpoints are currently unauthenticated for internal development. In
production, add a dependency on ``verify_api_key`` or an OAuth2 provider.

Running
-------
::

    uvicorn domes.services.api:app --reload --port 8000

OpenAPI docs:
    http://localhost:8000/docs    (Swagger UI)
    http://localhost:8000/redoc  (ReDoc)

Endpoints summary
-----------------
Person      GET /api/v2/persons/{person_id}
                /timeline  /systems
Dome        GET /api/v2/domes/{person_id}
                /knowledge-graph  /confidence  /state
Prediction  GET /api/v2/predictions/{person_id}/risks
                /interventions  /forecast  /causal
Flourishing GET /api/v2/flourishing/{person_id}
                /traditions  /trajectory  /what-if  /cost-of-suffering
Fragment    POST /api/v2/fragments/
            GET /api/v2/fragments/{person_id}/recent
                /sources  /quality
Compute     GET /api/v2/compute/budget
                /allocation/{person_id}  /information-gain
System-wide GET /api/v2/systems  /gaps  /provisions
Health      GET /health  /api/v2/health
"""
from __future__ import annotations

import uuid
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Query, Path, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from domes.services.compute import (
    COMPUTE_BUDGET,
    ServiceName,
    TOTAL_FLOPS,
    TOTAL_BUDGET_USD_LOW,
    TOTAL_BUDGET_USD_HIGH,
    BUDGET_YEARS,
    SUSTAINED_FLOPS_PER_SECOND,
    COST_PER_FLOP,
)

# ---------------------------------------------------------------------------
# ASCII art banner
# ---------------------------------------------------------------------------

DOMES_BANNER = r"""
╬════════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║    ██████╗  ██████╗ ███╗   ███╗███████╗███████╗    ██╗   ██╗██████╗     ║
║    ██╔══██╗██╔═══██╗████╗ ████║██╔════╝██╔════╝    ██║   ██║╔════██╗    ║
║    ██║  ██║██║   ██║██╔████╔██║█████╗  ███████╗    ██║   ██║ █████╔╝    ║
║    ██║  ██║██║   ██║██║╚██╔╝██║██╔══╝  ╚════██║    ╚██╗ ██╔╝██╔═══╝     ║
║    ██████╔╝╚██████╔╝██║ ╚═╝ ██║███████╗███████║     ╚████╔╝ ███████╗    ║
║    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚══════╝╚══════╝      ╚═══╝  ╚══════╝    ║
║                                                                          ║
║  Directed Outcome Modeling & Engineering System  ·  Version 2.0.0       ║
║  3×10²¹ FLOPs  ·  $33–50B  ·  5 years  ·  One person: Robert Jackson   ║
║                                                                          ║
║  "The most compute ever directed at modeling a single human life."       ║
║                                                                          ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

# ---------------------------------------------------------------------------
# Mock data — Robert Jackson
# ---------------------------------------------------------------------------

#: The primary subject UUID — Robert Jackson.
ROBERT_JACKSON_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
ROBERT_JACKSON_ID_STR = str(ROBERT_JACKSON_ID)

_NOW = datetime.now(tz=timezone.utc)
_NOW_ISO = _NOW.isoformat()


def _rj_person_record() -> dict[str, Any]:
    """Return a realistic mock person record for Robert Jackson."""
    return {
        "id": ROBERT_JACKSON_ID_STR,
        "first_name": "Robert",
        "middle_name": "Earl",
        "last_name": "Jackson",
        "preferred_name": "Rob",
        "date_of_birth": "1979-03-14",
        "age": 46,
        "gender": "man",
        "race": "black_african_american",
        "ethnicity": "not_hispanic_or_latino",
        "primary_language": "en",
        "city": "Detroit",
        "state": "MI",
        "county": "Wayne",
        "zip_code": "48207",
        "census_tract": "26163519700",
        "housing_status": "sheltered",
        "employment_status": "unemployed",
        "immigration_status": "us_citizen",
        "veteran": False,
        "chronic_homelessness": True,
        "medicaid_id": "MI-20391847",
        "medicare_id": None,
        "snap_case_number": "SNAP-DET-998821",
        "va_patient_id": None,
        "hmis_client_id": "HMIS-48827",
        "probation_case_number": None,
        "fhir_resource_type": "Patient",
        "fhir_resource_id": "Patient/rj-fhir-001",
        "created_at": "2023-01-15T08:30:00Z",
        "updated_at": _NOW_ISO,
        "deleted_at": None,
    }


def _rj_12_domain_scores() -> dict[str, Any]:
    """Return mock 12-domain flourishing scores for Robert Jackson."""
    return {
        "health_vitality":        {"score": 34.2, "trend": "declining",  "risk_level": "high"},
        "economic_prosperity":    {"score": 12.1, "trend": "stable",     "risk_level": "critical"},
        "community_belonging":    {"score": 41.0, "trend": "improving",  "risk_level": "moderate"},
        "environmental_harmony":  {"score": 28.7, "trend": "stable",     "risk_level": "high"},
        "creative_expression":    {"score": 55.3, "trend": "improving",  "risk_level": "moderate"},
        "intellectual_growth":    {"score": 48.9, "trend": "stable",     "risk_level": "moderate"},
        "physical_space_beauty":  {"score": 19.4, "trend": "declining",  "risk_level": "high"},
        "play_joy":               {"score": 31.6, "trend": "stable",     "risk_level": "high"},
        "spiritual_depth":        {"score": 62.1, "trend": "improving",  "risk_level": "low"},
        "love_relationships":     {"score": 44.8, "trend": "stable",     "risk_level": "moderate"},
        "purpose_meaning":        {"score": 52.0, "trend": "improving",  "risk_level": "moderate"},
        "legacy_contribution":    {"score": 38.5, "trend": "stable",     "risk_level": "high"},
    }


# ---------------------------------------------------------------------------
# Pydantic response models
# ---------------------------------------------------------------------------

class HealthResponse(BaseModel):
    status: Literal["ok", "degraded", "down"] = "ok"
    version: str = "2.0.0"
    timestamp: str
    compute_budget_consumed_fraction: float
    uptime_seconds: float


class PersonResponse(BaseModel):
    id: str
    first_name: str | None
    last_name: str | None
    preferred_name: str | None
    date_of_birth: str | None
    age: int | None
    gender: str | None
    race: str | None
    ethnicity: str | None
    primary_language: str | None
    city: str | None
    state: str | None
    county: str | None
    zip_code: str | None
    census_tract: str | None
    housing_status: str | None
    employment_status: str | None
    immigration_status: str | None
    veteran: bool | None
    chronic_homelessness: bool | None
    medicaid_id: str | None
    medicare_id: str | None
    snap_case_number: str | None
    va_patient_id: str | None
    hmis_client_id: str | None
    probation_case_number: str | None
    fhir_resource_type: str | None
    fhir_resource_id: str | None
    created_at: str
    updated_at: str
    deleted_at: str | None


class TimelineEvent(BaseModel):
    event_id: str
    event_type: str
    event_class: str
    timestamp: str
    description: str
    system: str | None
    risk_flag: bool = False
    domain: str | None


class TimelineResponse(BaseModel):
    person_id: str
    total_events: int
    date_range: dict[str, str]
    events: list[TimelineEvent]


class SystemTouchpoint(BaseModel):
    system_id: str
    system_name: str
    domain: str
    first_contact: str
    last_contact: str
    active: bool
    enrollment_status: str | None


class PersonSystemsResponse(BaseModel):
    person_id: str
    total_systems: int
    active_enrollments: int
    systems: list[SystemTouchpoint]


class DomeStateResponse(BaseModel):
    dome_id: str
    person_id: str
    assembled_at: str
    is_current: bool
    trigger: str
    assembly_version: str
    cosm_score: float | None
    cosm_label: str | None
    cosm_delta: float | None
    overall_risk_level: str
    crisis_flags: list[str]
    fragment_count: int
    systems_represented: list[str]
    fragmented_annual_cost: float | None
    coordinated_annual_cost: float | None
    delta: float | None
    lifetime_cost_estimate: float | None
    recommendations: list[dict[str, Any]]
    narrative_summary: str | None
    assembly_duration_ms: int | None


class KnowledgeGraphNode(BaseModel):
    node_id: str
    node_type: str
    label: str
    domain: str | None
    properties: dict[str, Any]


class KnowledgeGraphEdge(BaseModel):
    edge_id: str
    source_id: str
    target_id: str
    relationship: str
    weight: float
    evidence: str | None


class KnowledgeGraphResponse(BaseModel):
    person_id: str
    generated_at: str
    node_count: int
    edge_count: int
    nodes: list[KnowledgeGraphNode]
    edges: list[KnowledgeGraphEdge]


class ConfidenceResponse(BaseModel):
    person_id: str
    overall_confidence: float
    last_updated: str
    domains: dict[str, dict[str, Any]]


class TwinStateResponse(BaseModel):
    person_id: str
    dome_id: str
    state: str
    state_description: str
    last_transition: str
    pending_triggers: list[str]
    next_scheduled_assembly: str | None
    fragment_buffer_size: int


class RiskDashboardResponse(BaseModel):
    person_id: str
    computed_at: str
    overall_risk_level: str
    risks: dict[str, dict[str, Any]]
    top_risk_factors: list[str]
    protective_factors: list[str]
    crisis_flags: list[str]


class InterventionResponse(BaseModel):
    person_id: str
    computed_at: str
    interventions: list[dict[str, Any]]
    total_estimated_annual_savings: float


class ForecastPoint(BaseModel):
    date: str
    predicted_value: float
    lower_ci: float
    upper_ci: float
    confidence: float


class ForecastResponse(BaseModel):
    person_id: str
    metric: str
    horizon: str
    forecast_generated_at: str
    model_version: str
    points: list[ForecastPoint]
    trend_direction: str
    summary: str


class CausalModelResponse(BaseModel):
    person_id: str
    generated_at: str
    causal_factors: list[dict[str, Any]]
    causal_graph_summary: str
    total_causal_pathways: int


class FlourishingResponse(BaseModel):
    person_id: str
    scored_at: str
    cosm_score: float
    cosm_label: str
    foundation_layer_met: bool
    scores: dict[str, dict[str, Any]]


class TraditionView(BaseModel):
    tradition: str
    tradition_full_name: str
    overall_assessment: str
    domain_weights: dict[str, float]
    weighted_score: float
    key_observations: list[str]
    recommendations: list[str]


class TraditionsResponse(BaseModel):
    person_id: str
    generated_at: str
    traditions: list[TraditionView]


class TrajectoryPoint(BaseModel):
    date: str
    cosm_score: float
    domain_scores: dict[str, float]


class TrajectoryResponse(BaseModel):
    person_id: str
    data_points: list[TrajectoryPoint]
    cosm_trend: str
    inflection_points: list[str]


class WhatIfResponse(BaseModel):
    person_id: str
    domain: str
    current_score: float
    target_score: float
    feasibility: str
    estimated_time_to_target: str
    required_interventions: list[dict[str, Any]]
    cascading_effects: dict[str, float]
    annual_cost_reduction: float


class CostOfSufferingResponse(BaseModel):
    person_id: str
    computed_at: str
    annual_system_cost_fragmented: float
    annual_system_cost_coordinated: float
    annual_savings_potential: float
    lifetime_cost_estimate: float
    cost_per_domain: dict[str, float]
    methodology: str


class FragmentIngestRequest(BaseModel):
    person_id: str
    source_type: str
    data_domain: str
    raw_payload: dict[str, Any]
    source_format: str | None = None
    external_id: str | None = None
    is_42cfr_protected: bool = False
    is_pii: bool = True
    consent_id: str | None = None


class FragmentIngestResponse(BaseModel):
    fragment_id: str
    person_id: str
    ingested_at: str
    validation_status: str
    normalization_queued: bool
    dome_reassembly_triggered: bool


class FragmentSummary(BaseModel):
    fragment_id: str
    source_type: str
    data_domain: str
    ingested_at: str
    validation_status: str
    is_superseded: bool
    is_42cfr_protected: bool


class RecentFragmentsResponse(BaseModel):
    person_id: str
    total_fragments: int
    page: int
    page_size: int
    fragments: list[FragmentSummary]


class DataSourceStatus(BaseModel):
    source_type: str
    last_fragment_at: str | None
    fragment_count_30d: int
    avg_quality_score: float
    is_active: bool
    gap_days: int | None


class DataSourcesResponse(BaseModel):
    person_id: str
    total_sources: int
    active_sources: int
    sources: list[DataSourceStatus]


class FragmentQualityResponse(BaseModel):
    person_id: str
    overall_quality_score: float
    total_fragments: int
    validation_pass_rate: float
    normalization_success_rate: float
    completeness_by_domain: dict[str, float]
    freshness_by_source: dict[str, str]
    data_quality_issues: list[str]


class ComputeBudgetResponse(BaseModel):
    total_flops: float
    budget_years: int
    budget_usd_low: float
    budget_usd_high: float
    sustained_flops_per_second: float
    cost_per_flop: float
    program_elapsed_fraction: float
    total_flops_consumed: float
    budget_fraction_consumed: float
    total_cost_consumed_usd: float
    overall_utilization: float
    energy_consumed_kwh: float
    energy_cost_usd: float
    services: dict[str, Any]
    compute_pressure: dict[str, Any]
    next_flop_goes_to: str


class ComputeAllocationResponse(BaseModel):
    person_id: str
    note: str
    services: dict[str, Any]
    total_flops_consumed: float
    total_cost_consumed_usd: float


class InfoGainResponse(BaseModel):
    services: dict[str, dict[str, Any]]
    highest_marginal_value_service: str
    recommendation: str | None


class GovernmentSystem(BaseModel):
    system_id: str
    name: str
    domain: str
    privacy_law: str | None
    api_availability: str
    description: str


class GovernmentSystemsResponse(BaseModel):
    total_systems: int
    systems: list[GovernmentSystem]


class DataGap(BaseModel):
    gap_id: str
    system_a: str
    system_b: str
    gap_type: str
    severity: str
    description: str
    blocking_statute: str | None
    workaround: str | None


class DataGapsResponse(BaseModel):
    total_gaps: int
    critical_gaps: int
    gaps: list[DataGap]


class LegalProvision(BaseModel):
    provision_id: str
    name: str
    provision_type: str
    domain: str
    description: str
    enables: list[str]
    blocks: list[str]
    citation: str | None


class ProvisionsResponse(BaseModel):
    total_provisions: int
    provisions: list[LegalProvision]


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="DOMES v2 API",
    description=(
        "**Directed Outcome Modeling & Engineering System — Version 2.0**\n\n"
        "The unified API gateway for DOMES v2. This system models 3×10²¹ FLOPs over "
        "5 years directed at a single person, Robert Jackson, to achieve the most "
        "comprehensive computational understanding of a human life ever attempted.\n\n"
        "## Architecture\n"
        "- **17 tables, 505 columns** of structured data\n"
        "- **12 flourishing domains** scored continuously\n"
        "- **30 government systems** integrated\n"
        "- **8 philosophical traditions** for flourishing evaluation\n"
        "- **$33–50B compute budget** tracked to the FLOP\n\n"
        "## Authentication\n"
        "Internal development mode — no authentication required. "
        "Production will require `X-DOMES-API-Key` header.\n\n"
        "## Subject\n"
        "All endpoints accept `{person_id}`. The primary subject is Robert Jackson "
        f"(`{ROBERT_JACKSON_ID_STR}`).\n\n"
        "---\n"
        "*The most compute ever directed at modeling a single human life.*"
    ),
    version="2.0.0",
    contact={
        "name":  "DOMES Engineering",
        "email": "eng@domes.example.com",
    },
    license_info={
        "name": "Proprietary — DOMES v2",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Lock down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Application lifecycle
# ---------------------------------------------------------------------------

@app.on_event("startup")
async def startup_event() -> None:
    """Print the DOMES ASCII art banner and validate compute budget on startup."""
    print(DOMES_BANNER)
    print(f"  API Gateway online — {datetime.now(tz=timezone.utc).isoformat()}")
    print(f"  Compute budget: {TOTAL_FLOPS:.1e} FLOPs | "
          f"${TOTAL_BUDGET_USD_LOW/1e9:.0f}–${TOTAL_BUDGET_USD_HIGH/1e9:.0f}B | "
          f"{BUDGET_YEARS} years\n")


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def _require_robert_jackson(person_id: str) -> None:
    """Validate that person_id is known. Mock: only Robert Jackson exists."""
    try:
        uid = uuid.UUID(person_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid UUID: {person_id!r}",
        )
    if uid != ROBERT_JACKSON_ID:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Person '{person_id}' not found. "
                "In this installation, only Robert Jackson is enrolled. "
                f"Use person_id={ROBERT_JACKSON_ID_STR}"
            ),
        )


# ---------------------------------------------------------------------------
# Health endpoints
# ---------------------------------------------------------------------------

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="System health check",
    description=(
        "Returns the operational status of the DOMES API gateway, "
        "current compute budget utilization, and uptime. "
        "Used by load balancers and monitoring systems."
    ),
)
async def health_check() -> HealthResponse:
    """Lightweight health probe. Returns 200 when the system is operational."""
    return HealthResponse(
        status="ok",
        version="2.0.0",
        timestamp=datetime.now(tz=timezone.utc).isoformat(),
        compute_budget_consumed_fraction=COMPUTE_BUDGET.budget_fraction_consumed,
        uptime_seconds=round(COMPUTE_BUDGET.elapsed_seconds, 1),
    )


@app.get(
    "/api/v2/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Versioned health check",
    description="Versioned health check endpoint. Identical to `/health`.",
)
async def health_check_versioned() -> HealthResponse:
    """Versioned health probe — same as /health."""
    return await health_check()


# ===========================================================================
# Person Endpoints
# ===========================================================================

@app.get(
    "/api/v2/persons/{person_id}",
    response_model=PersonResponse,
    tags=["Person"],
    summary="Full person record",
    description=(
        "Returns the complete person record for the given person UUID, "
        "including all demographic fields, current housing/employment status, "
        "and cross-system government identifiers (HMIS, Medicaid, SNAP, etc.).\n\n"
        "**SSN is never returned.** Only the last-4 and a SHA-256 hash are stored.\n\n"
        "This endpoint is FHIR Patient-aligned (US Core profile)."
    ),
)
async def get_person(
    person_id: str = Path(..., description="Person UUID", examples=[ROBERT_JACKSON_ID_STR]),
) -> PersonResponse:
    """Retrieve the full person record for `person_id`."""
    _require_robert_jackson(person_id)
    return PersonResponse(**_rj_person_record())


@app.get(
    "/api/v2/persons/{person_id}/timeline",
    response_model=TimelineResponse,
    tags=["Person"],
    summary="Chronological event timeline",
    description=(
        "Returns a reverse-chronological timeline of all recorded events "
        "for this person across all integrated government systems.\n\n"
        "Event types include: encounters (ER, shelter, outreach), "
        "enrollment changes, assessment completions, medication starts/stops, "
        "biometric alerts, crisis flags, and data fragment arrivals.\n\n"
        "The timeline is the raw source material for the digital twin assembly."
    ),
)
async def get_person_timeline(
    person_id: str = Path(..., description="Person UUID"),
    limit: int = Query(50, ge=1, le=500, description="Maximum events to return"),
    after: str | None = Query(None, description="Return events after this ISO timestamp"),
) -> TimelineResponse:
    """Return a chronological event timeline for `person_id`."""
    _require_robert_jackson(person_id)

    events = [
        TimelineEvent(
            event_id="evt-001",
            event_type="encounter",
            event_class="er_visit",
            timestamp="2025-11-03T02:14:00Z",
            description="Emergency department visit — Henry Ford Hospital. Chief complaint: hypertensive crisis.",
            system="medicaid",
            risk_flag=True,
            domain="health_vitality",
        ),
        TimelineEvent(
            event_id="evt-002",
            event_type="enrollment",
            event_class="enrollment_change",
            timestamp="2025-10-12T09:00:00Z",
            description="Enrolled in Permanent Supportive Housing waitlist — SER Metro Detroit.",
            system="hmis",
            risk_flag=False,
            domain="economic_prosperity",
        ),
        TimelineEvent(
            event_id="evt-003",
            event_type="assessment",
            event_class="assessment_completed",
            timestamp="2025-10-01T14:30:00Z",
            description="PHQ-9 scored 19/27 (severe depression). Referred to psychiatrist.",
            system="behavioral_health",
            risk_flag=True,
            domain="health_vitality",
        ),
        TimelineEvent(
            event_id="evt-004",
            event_type="fragment",
            event_class="biometric_alert",
            timestamp="2025-09-18T22:47:00Z",
            description="Wearable alert: HRV drop below threshold (RMSSD < 12ms). Stress event detected.",
            system="wearable",
            risk_flag=True,
            domain="health_vitality",
        ),
        TimelineEvent(
            event_id="evt-005",
            event_type="encounter",
            event_class="shelter_stay",
            timestamp="2025-08-22T18:00:00Z",
            description="Shelter intake — Detroit Rescue Mission. Stayed 14 nights.",
            system="hmis",
            risk_flag=False,
            domain="environmental_harmony",
        ),
        TimelineEvent(
            event_id="evt-006",
            event_type="medication",
            event_class="medication_change",
            timestamp="2025-07-11T11:00:00Z",
            description="Lisinopril 10mg started for hypertension management.",
            system="fhir",
            risk_flag=False,
            domain="health_vitality",
        ),
    ]

    return TimelineResponse(
        person_id=person_id,
        total_events=142,
        date_range={"earliest": "2018-03-01T00:00:00Z", "latest": _NOW_ISO},
        events=events[:limit],
    )


@app.get(
    "/api/v2/persons/{person_id}/systems",
    response_model=PersonSystemsResponse,
    tags=["Person"],
    summary="Government systems touchpoints",
    description=(
        "Returns all government systems this person has interacted with, "
        "including enrollment status, first/last contact dates, and whether "
        "the enrollment is currently active.\n\n"
        "Used to understand the multi-system footprint and identify "
        "coordination gaps between agencies."
    ),
)
async def get_person_systems(
    person_id: str = Path(..., description="Person UUID"),
) -> PersonSystemsResponse:
    """Return all government systems touching `person_id`."""
    _require_robert_jackson(person_id)

    systems = [
        SystemTouchpoint(system_id="sys-medicaid-mi",  system_name="Michigan Medicaid",        domain="health",            first_contact="2019-01-15", last_contact="2025-11-03", active=True,  enrollment_status="active"),
        SystemTouchpoint(system_id="sys-hmis-detroit", system_name="Detroit HMIS",              domain="housing",           first_contact="2020-06-01", last_contact="2025-10-12", active=True,  enrollment_status="active"),
        SystemTouchpoint(system_id="sys-snap-mi",      system_name="Michigan SNAP / EBT",       domain="income",            first_contact="2019-03-01", last_contact="2025-09-01", active=True,  enrollment_status="active"),
        SystemTouchpoint(system_id="sys-cmhc-detroit", system_name="Detroit CMHC",              domain="behavioral_health", first_contact="2021-02-14", last_contact="2025-10-01", active=True,  enrollment_status="active"),
        SystemTouchpoint(system_id="sys-liheap-mi",    system_name="Michigan LIHEAP",           domain="income",            first_contact="2022-11-01", last_contact="2024-11-01", active=False, enrollment_status="disenrolled"),
        SystemTouchpoint(system_id="sys-ssa",          system_name="Social Security (SSI/SSDI)", domain="income",         first_contact="2023-06-01", last_contact="2025-08-01", active=False, enrollment_status="pending"),
    ]

    return PersonSystemsResponse(
        person_id=person_id,
        total_systems=len(systems),
        active_enrollments=sum(1 for s in systems if s.active),
        systems=systems,
    )


# ===========================================================================
# Dome Endpoints (Digital Twin)
# ===========================================================================

@app.get(
    "/api/v2/domes/{person_id}",
    response_model=DomeStateResponse,
    tags=["Dome (Digital Twin)"],
    summary="Current dome state",
    description=(
        "Returns the current assembled digital twin (dome) for this person.\n\n"
        "The dome is DOMES v2's primary deliverable — a snapshot of the person's "
        "complete state synthesized from all available data fragments across all "
        "integrated systems. It includes:\n\n"
        "- **COSM score** (Composite Outcome Scoring Model, 0–100)\n"
        "- **Risk scores** by domain\n"
        "- **12-domain flourishing scores**\n"
        "- **Cost analysis** (fragmented vs. coordinated care)\n"
        "- **Prioritized recommendations**\n"
        "- **Narrative summary**\n\n"
        "Assembled by the dome assembly pipeline, triggered by new fragments, "
        "consent changes, or the daily scheduled run."
    ),
)
async def get_dome(
    person_id: str = Path(..., description="Person UUID"),
) -> DomeStateResponse:
    """Return the current assembled digital twin for `person_id`."""
    _require_robert_jackson(person_id)

    return DomeStateResponse(
        dome_id="dome-rj-20260227",
        person_id=person_id,
        assembled_at=_NOW_ISO,
        is_current=True,
        trigger="scheduled",
        assembly_version="2.0.0",
        cosm_score=38.2,
        cosm_label="Critical — Foundation Unmet",
        cosm_delta=-1.4,
        overall_risk_level="high",
        crisis_flags=["hypertensive_crisis_risk", "housing_instability_critical"],
        fragment_count=847,
        systems_represented=["medicaid", "hmis", "snap", "cmhc", "wearable", "fhir"],
        fragmented_annual_cost=284000.0,
        coordinated_annual_cost=97000.0,
        delta=187000.0,
        lifetime_cost_estimate=4200000.0,
        recommendations=[
            {
                "priority": 1,
                "domain": "economic_prosperity",
                "action": "Expedite PSH application — current waitlist position: 14. "
                           "Estimate 3–6 months to placement. Assign housing specialist.",
                "rationale": "Chronic homelessness is the single highest-leverage intervention: "
                             "housing stability correlates with 60% reduction in ER utilization.",
                "estimated_impact": "$112,000/year reduction in ER and shelter costs",
            },
            {
                "priority": 2,
                "domain": "health_vitality",
                "action": "Enroll in Wayne County CMHC ACT team. Assign psychiatrist for "
                           "medication management. Target PHQ-9 < 10 within 90 days.",
                "rationale": "ACT team reduces psychiatric hospitalization by 50% and "
                             "ER utilization by 35% for high-need individuals.",
                "estimated_impact": "$48,000/year reduction in psychiatric hospitalization costs",
            },
            {
                "priority": 3,
                "domain": "economic_prosperity",
                "action": "File SSI/SSDI application. Assign benefits counselor. "
                           "Eligibility probability: 62% (depression + hypertension combined).",
                "rationale": "SSI approval ($943/month) restores economic foundation layer "
                             "and reduces SNAP dependency.",
                "estimated_impact": "$11,316/year in direct income + program cost reduction",
            },
        ],
        narrative_summary=(
            "Robert Jackson is a 46-year-old Black man from Detroit experiencing chronic homelessness "
            "for 4.2 years. His COSM score of 38.2 places him in the Critical category with the "
            "foundation layer unmet. The primary driver is economic deprivation (score: 12.1/100) "
            "compounded by uncontrolled hypertension and severe depression (PHQ-9=19). "
            "Without intervention, his score is projected to decline to 35.8 in 30 days. "
            "The highest-value intervention is PSH placement, which would generate $112,000/year "
            "in system cost reduction and improve his COSM score by an estimated +14.2 points."
        ),
        assembly_duration_ms=847,
    )


@app.get(
    "/api/v2/domes/{person_id}/knowledge-graph",
    response_model=KnowledgeGraphResponse,
    tags=["Dome (Digital Twin)"],
    summary="Knowledge graph embedded in dome",
    description=(
        "Returns the semantic knowledge graph embedded in this person's dome. "
        "Nodes represent entities (diagnoses, encounters, programs, locations, events). "
        "Edges represent relationships (caused-by, co-occurs-with, leads-to, etc.).\n\n"
        "Used for causal analysis, intervention modeling, and narrative generation."
    ),
)
async def get_dome_knowledge_graph(
    person_id: str = Path(..., description="Person UUID"),
) -> KnowledgeGraphResponse:
    """Return the knowledge graph embedded in the current dome."""
    _require_robert_jackson(person_id)

    nodes = [
        KnowledgeGraphNode(node_id="n-001", node_type="condition",  label="Hypertension (I10)",        domain="health_vitality",     properties={"icd10": "I10",     "onset": "2021", "severity": "moderate"}),
        KnowledgeGraphNode(node_id="n-002", node_type="condition",  label="Major Depressive Disorder",  domain="health_vitality",     properties={"icd10": "F33.1",   "onset": "2020", "severity": "severe"}),
        KnowledgeGraphNode(node_id="n-003", node_type="status",     label="Chronic Homelessness",       domain="environmental_harmony", properties={"years": 4.2,     "hud_definition": True}),
        KnowledgeGraphNode(node_id="n-004", node_type="encounter",  label="ER Visit 2025-11-03",        domain="health_vitality",     properties={"system": "medicaid", "cost": 8400}),
        KnowledgeGraphNode(node_id="n-005", node_type="program",    label="Detroit HMIS PSH Waitlist",  domain="economic_prosperity", properties={"position": 14,     "est_wait": "3-6mo"}),
        KnowledgeGraphNode(node_id="n-006", node_type="assessment", label="PHQ-9 Score 19",             domain="health_vitality",     properties={"score": 19,        "date": "2025-10-01"}),
        KnowledgeGraphNode(node_id="n-007", node_type="stressor",   label="No Fixed Income",            domain="economic_prosperity", properties={"monthly_income": 0}),
        KnowledgeGraphNode(node_id="n-008", node_type="protective", label="Spiritual Community",        domain="spiritual_depth",     properties={"frequency": "weekly"}),
    ]

    edges = [
        KnowledgeGraphEdge(edge_id="e-001", source_id="n-003", target_id="n-002", relationship="exacerbates",      weight=0.82, evidence="Literature: homelessness doubles depression recurrence"),
        KnowledgeGraphEdge(edge_id="e-002", source_id="n-002", target_id="n-001", relationship="complicates",      weight=0.61, evidence="Medication non-adherence in depression → BP dyscontrol"),
        KnowledgeGraphEdge(edge_id="e-003", source_id="n-001", target_id="n-004", relationship="caused",           weight=0.74, evidence="Hypertensive crisis → ER admission"),
        KnowledgeGraphEdge(edge_id="e-004", source_id="n-007", target_id="n-003", relationship="perpetuates",      weight=0.91, evidence="No income → cannot exit homelessness"),
        KnowledgeGraphEdge(edge_id="e-005", source_id="n-008", target_id="n-002", relationship="protective_for",   weight=0.45, evidence="Faith community → reduced depression severity"),
        KnowledgeGraphEdge(edge_id="e-006", source_id="n-005", target_id="n-003", relationship="resolves",         weight=0.88, evidence="PSH placement → exits chronic homelessness"),
    ]

    return KnowledgeGraphResponse(
        person_id=person_id,
        generated_at=_NOW_ISO,
        node_count=len(nodes),
        edge_count=len(edges),
        nodes=nodes,
        edges=edges,
    )


@app.get(
    "/api/v2/domes/{person_id}/confidence",
    response_model=ConfidenceResponse,
    tags=["Dome (Digital Twin)"],
    summary="Per-domain confidence levels",
    description=(
        "Returns the DOMES system's confidence level in its data for each "
        "of the 12 flourishing domains and key risk categories.\n\n"
        "Confidence is derived from: data recency, fragment source count, "
        "inter-system corroboration, and known data gaps.\n\n"
        "Low confidence domains are candidates for targeted data collection."
    ),
)
async def get_dome_confidence(
    person_id: str = Path(..., description="Person UUID"),
) -> ConfidenceResponse:
    """Return per-domain confidence levels for the current dome."""
    _require_robert_jackson(person_id)

    return ConfidenceResponse(
        person_id=person_id,
        overall_confidence=0.61,
        last_updated=_NOW_ISO,
        domains={
            "health_vitality":        {"confidence": 0.78, "primary_source": "medicaid",   "last_data": "2025-11-03", "gaps": []},
            "economic_prosperity":    {"confidence": 0.52, "primary_source": "snap",        "last_data": "2025-09-01", "gaps": ["ssdi_determination", "wage_history"]},
            "community_belonging":    {"confidence": 0.44, "primary_source": "hmis",        "last_data": "2025-10-12", "gaps": ["social_network_data", "peer_relationships"]},
            "environmental_harmony":  {"confidence": 0.67, "primary_source": "purpleair",   "last_data": "2025-11-01", "gaps": []},
            "creative_expression":    {"confidence": 0.31, "primary_source": "self_report", "last_data": "2025-08-15", "gaps": ["structured_assessment"]},
            "intellectual_growth":    {"confidence": 0.38, "primary_source": "self_report", "last_data": "2025-08-15", "gaps": ["education_records_ferpa"]},
            "physical_space_beauty":  {"confidence": 0.72, "primary_source": "hmis",        "last_data": "2025-10-12", "gaps": []},
            "play_joy":               {"confidence": 0.29, "primary_source": "self_report", "last_data": "2025-08-15", "gaps": ["structured_assessment"]},
            "spiritual_depth":        {"confidence": 0.55, "primary_source": "self_report", "last_data": "2025-10-01", "gaps": ["corroborating_data"]},
            "love_relationships":     {"confidence": 0.41, "primary_source": "hmis",        "last_data": "2025-10-12", "gaps": ["family_network_data"]},
            "purpose_meaning":        {"confidence": 0.47, "primary_source": "self_report", "last_data": "2025-10-01", "gaps": ["structured_assessment"]},
            "legacy_contribution":    {"confidence": 0.33, "primary_source": "self_report", "last_data": "2025-08-15", "gaps": ["structured_assessment"]},
        },
    )


@app.get(
    "/api/v2/domes/{person_id}/state",
    response_model=TwinStateResponse,
    tags=["Dome (Digital Twin)"],
    summary="Digital twin state machine",
    description=(
        "Returns the current state of the digital twin's state machine.\n\n"
        "States: `current` → `stale` → `assembling` → `error` → `current`\n\n"
        "Also returns pending triggers (new fragments awaiting assembly), "
        "the next scheduled assembly time, and the size of the fragment buffer."
    ),
)
async def get_dome_state(
    person_id: str = Path(..., description="Person UUID"),
) -> TwinStateResponse:
    """Return the digital twin state machine status."""
    _require_robert_jackson(person_id)

    return TwinStateResponse(
        person_id=person_id,
        dome_id="dome-rj-20260227",
        state="current",
        state_description="Dome is fully assembled and up to date. All fragments processed.",
        last_transition=_NOW_ISO,
        pending_triggers=[],
        next_scheduled_assembly="2026-02-28T00:00:00Z",
        fragment_buffer_size=0,
    )


# ===========================================================================
# Prediction Endpoints
# ===========================================================================

@app.get(
    "/api/v2/predictions/{person_id}/risks",
    response_model=RiskDashboardResponse,
    tags=["Prediction"],
    summary="Current risk dashboard",
    description=(
        "Returns the current risk dashboard — probability scores across all "
        "major risk domains computed by the DOMES prediction service.\n\n"
        "Risk domains include: psychiatric hospitalization, ER utilization, "
        "housing loss, medication non-adherence, overdose, self-harm, "
        "incarceration, and mortality.\n\n"
        "Each risk score is a probability (0.0–1.0) with level classification "
        "and top contributing factors."
    ),
)
async def get_risks(
    person_id: str = Path(..., description="Person UUID"),
) -> RiskDashboardResponse:
    """Return the current risk dashboard for `person_id`."""
    _require_robert_jackson(person_id)
    COMPUTE_BUDGET.consume(ServiceName.PREDICTION, flops=1.2e9)

    return RiskDashboardResponse(
        person_id=person_id,
        computed_at=_NOW_ISO,
        overall_risk_level="high",
        risks={
            "psychiatric_hospitalization_30d": {
                "probability": 0.41,
                "level": "high",
                "model": "DOMES-PsychHosp-v2.1",
                "drivers": ["PHQ-9=19", "medication_non_adherence", "housing_instability"],
            },
            "er_visit_30d": {
                "probability": 0.58,
                "level": "high",
                "model": "DOMES-ER-v2.0",
                "drivers": ["hypertensive_crisis_history", "no_primary_care", "stress_hrv"],
            },
            "housing_loss_90d": {
                "probability": 0.72,
                "level": "critical",
                "model": "DOMES-Housing-v2.0",
                "drivers": ["no_income", "psh_waitlist", "chronic_homelessness"],
            },
            "medication_nonadherence": {
                "probability": 0.64,
                "level": "high",
                "model": "DOMES-MedAdh-v1.3",
                "drivers": ["unstable_housing", "depression_severity", "cost_barriers"],
            },
            "mortality_1yr": {
                "probability": 0.04,
                "level": "moderate",
                "model": "DOMES-Mort-v1.1",
                "drivers": ["hypertension_uncontrolled", "age_46", "social_isolation"],
            },
        },
        top_risk_factors=[
            "Chronic homelessness (4.2 years)",
            "Severe depression (PHQ-9=19)",
            "No fixed income",
            "Uncontrolled hypertension",
            "Medication non-adherence",
        ],
        protective_factors=[
            "Spiritual community engagement (weekly)",
            "SNAP benefits active",
            "Medicaid coverage active",
            "Engaged with HMIS case manager",
        ],
        crisis_flags=["hypertensive_crisis_risk", "housing_instability_critical"],
    )


@app.get(
    "/api/v2/predictions/{person_id}/interventions",
    response_model=InterventionResponse,
    tags=["Prediction"],
    summary="Ranked intervention recommendations",
    description=(
        "Returns interventions ranked by expected value — combining "
        "probability of success, cost reduction, and flourishing impact.\n\n"
        "Each intervention includes: action, target system, cost estimate, "
        "probability of success, and expected annual savings."
    ),
)
async def get_interventions(
    person_id: str = Path(..., description="Person UUID"),
) -> InterventionResponse:
    """Return ranked interventions for `person_id`."""
    _require_robert_jackson(person_id)
    COMPUTE_BUDGET.consume(ServiceName.PREDICTION, flops=8.4e8)

    return InterventionResponse(
        person_id=person_id,
        computed_at=_NOW_ISO,
        total_estimated_annual_savings=187000.0,
        interventions=[
            {
                "rank":                      1,
                "action":                    "PSH placement — Detroit Housing Commission",
                "domain":                    "economic_prosperity",
                "expected_value_score":      0.91,
                "probability_of_success":    0.74,
                "annual_cost_reduction":     112000.0,
                "cosm_score_delta":          +14.2,
                "implementation_cost":       18000.0,
                "urgency":                   "immediate",
            },
            {
                "rank":                      2,
                "action":                    "ACT team enrollment — Wayne County CMHC",
                "domain":                    "health_vitality",
                "expected_value_score":      0.78,
                "probability_of_success":    0.81,
                "annual_cost_reduction":     48000.0,
                "cosm_score_delta":          +8.7,
                "implementation_cost":       4200.0,
                "urgency":                   "soon",
            },
            {
                "rank":                      3,
                "action":                    "SSI/SSDI application filing",
                "domain":                    "economic_prosperity",
                "expected_value_score":      0.65,
                "probability_of_success":    0.62,
                "annual_cost_reduction":     27000.0,
                "cosm_score_delta":          +6.1,
                "implementation_cost":       600.0,
                "urgency":                   "soon",
            },
        ],
    )


@app.get(
    "/api/v2/predictions/{person_id}/forecast",
    response_model=ForecastResponse,
    tags=["Prediction"],
    summary="Time-series forecast",
    description=(
        "Returns a time-series forecast for a specified metric over a "
        "configurable horizon.\n\n"
        "Supported metrics: `cosm_score`, `health_vitality`, `economic_prosperity`, "
        "and all other 12 flourishing domains, plus risk probabilities.\n\n"
        "Horizons: `7d`, `30d`, `90d`, `180d`, `365d`."
    ),
)
async def get_forecast(
    person_id: str = Path(..., description="Person UUID"),
    horizon: str = Query("30d", description="Forecast horizon (7d, 30d, 90d, 180d, 365d)"),
    metric: str = Query("cosm_score", description="Metric to forecast"),
) -> ForecastResponse:
    """Return a time-series forecast for `person_id`."""
    _require_robert_jackson(person_id)
    COMPUTE_BUDGET.consume(ServiceName.PREDICTION, flops=2.1e10)

    # Generate synthetic daily forecast points (30-day default)
    horizon_days = {"7d": 7, "30d": 30, "90d": 90, "180d": 180, "365d": 365}.get(horizon, 30)
    from datetime import timedelta

    base_score = 38.2
    points: list[ForecastPoint] = []
    for i in range(1, horizon_days + 1):
        # Modest downward trend without intervention
        proj = base_score - (0.08 * i) + (0.5 * math.sin(i / 7))
        lower = proj - 4.2
        upper = proj + 3.8
        points.append(ForecastPoint(
            date=(date.today() + timedelta(days=i)).isoformat(),
            predicted_value=round(max(proj, 5.0), 2),
            lower_ci=round(max(lower, 0.0), 2),
            upper_ci=round(min(upper, 100.0), 2),
            confidence=round(max(0.9 - (i * 0.008), 0.4), 3),
        ))

    return ForecastResponse(
        person_id=person_id,
        metric=metric,
        horizon=horizon,
        forecast_generated_at=_NOW_ISO,
        model_version="DOMES-Forecast-v2.0",
        points=points,
        trend_direction="declining",
        summary=(
            f"Without intervention, COSM score is projected to decline from 38.2 to "
            f"{points[-1].predicted_value:.1f} over {horizon_days} days. "
            "Primary driver: housing instability compounding with untreated depression. "
            "PSH placement would reverse trajectory to +14.2 COSM improvement."
        ),
    )


@app.get(
    "/api/v2/predictions/{person_id}/causal",
    response_model=CausalModelResponse,
    tags=["Prediction"],
    summary="Causal model view",
    description=(
        "Returns the causal model underlying DOMES predictions for this person — "
        "a directed acyclic graph (DAG) of causal pathways with estimated "
        "effect sizes.\n\n"
        "The causal model distinguishes correlation from causation, enabling "
        "intervention design that targets root causes rather than downstream symptoms."
    ),
)
async def get_causal_model(
    person_id: str = Path(..., description="Person UUID"),
) -> CausalModelResponse:
    """Return the causal model view for `person_id`."""
    _require_robert_jackson(person_id)
    COMPUTE_BUDGET.consume(ServiceName.PREDICTION, flops=4.8e10)

    return CausalModelResponse(
        person_id=person_id,
        generated_at=_NOW_ISO,
        total_causal_pathways=11,
        causal_graph_summary=(
            "Root cause: no income (causal ancestor of 9/11 pathways). "
            "Primary mediator: chronic homelessness (4.2 years). "
            "Key effect modifier: depression (amplifies all housing→health pathways by 1.8×)."
        ),
        causal_factors=[
            {"factor": "no_fixed_income",       "is_root_cause": True,  "effect_size": 0.91, "downstream_count": 9,  "intervention_point": True,  "pathway": "income→housing→health"},
            {"factor": "chronic_homelessness",  "is_root_cause": False, "effect_size": 0.84, "downstream_count": 7,  "intervention_point": True,  "pathway": "housing→health→er_utilization"},
            {"factor": "depression_severity",   "is_root_cause": False, "effect_size": 0.71, "downstream_count": 5,  "intervention_point": True,  "pathway": "mental_health→medication_adherence→bp_control"},
            {"factor": "hypertension",          "is_root_cause": False, "effect_size": 0.62, "downstream_count": 3,  "intervention_point": True,  "pathway": "hypertension→er_visit→cost"},
            {"factor": "social_isolation",      "is_root_cause": False, "effect_size": 0.48, "downstream_count": 2,  "intervention_point": False, "pathway": "isolation→depression_persistence"},
            {"factor": "spiritual_community",   "is_root_cause": False, "effect_size": -0.31, "downstream_count": 2, "intervention_point": False, "pathway": "protective→depression_buffer"},
        ],
    )


# ===========================================================================
# Flourishing Endpoints
# ===========================================================================

@app.get(
    "/api/v2/flourishing/{person_id}",
    response_model=FlourishingResponse,
    tags=["Flourishing"],
    summary="Current 12-domain flourishing scores",
    description=(
        "Returns the current flourishing profile — scores for all 12 domains "
        "organized in three layers:\n\n"
        "**Layer 1 — Foundation:** health_vitality, economic_prosperity, "
        "community_belonging, environmental_harmony\n\n"
        "**Layer 2 — Aspiration:** creative_expression, intellectual_growth, "
        "physical_space_beauty, play_joy\n\n"
        "**Layer 3 — Transcendence:** spiritual_depth, love_relationships, "
        "purpose_meaning, legacy_contribution\n\n"
        "The COSM score is the composite mean across all 12 domains. "
        "`foundation_layer_met` is true only when all Layer 1 scores ≥ 50."
    ),
)
async def get_flourishing(
    person_id: str = Path(..., description="Person UUID"),
) -> FlourishingResponse:
    """Return current 12-domain flourishing scores for `person_id`."""
    _require_robert_jackson(person_id)
    COMPUTE_BUDGET.consume(ServiceName.FLOURISHING, flops=6.2e8)

    scores = _rj_12_domain_scores()
    cosm = round(sum(v["score"] for v in scores.values()) / 12, 2)
    foundation_met = all(
        scores[d]["score"] >= 50
        for d in ["health_vitality", "economic_prosperity", "community_belonging", "environmental_harmony"]
    )

    return FlourishingResponse(
        person_id=person_id,
        scored_at=_NOW_ISO,
        cosm_score=cosm,
        cosm_label="Critical — Foundation Unmet",
        foundation_layer_met=foundation_met,
        scores=scores,
    )


@app.get(
    "/api/v2/flourishing/{person_id}/traditions",
    response_model=TraditionsResponse,
    tags=["Flourishing"],
    summary="8 philosophical tradition views",
    description=(
        "Returns flourishing evaluation through 8 philosophical and cultural traditions:\n\n"
        "1. **Aristotelian** — Eudaimonia / virtue ethics\n"
        "2. **Utilitarian** — Maximizing welfare and reducing suffering\n"
        "3. **Capabilities** — Sen & Nussbaum central human capabilities\n"
        "4. **Ubuntu** — 'I am because we are' — communal flourishing\n"
        "5. **Buddhist** — Freedom from suffering, the Eightfold Path\n"
        "6. **Indigenous** — Seven Grandfather Teachings / balance with nature\n"
        "7. **Positive Psychology** — PERMA model (Seligman)\n"
        "8. **Liberation Theology** — Structural justice, preferential option for the poor\n\n"
        "Each tradition applies different domain weights and yields a different "
        "assessment of the same underlying scores — revealing blind spots in any "
        "single framework."
    ),
)
async def get_flourishing_traditions(
    person_id: str = Path(..., description="Person UUID"),
) -> TraditionsResponse:
    """Return 8 philosophical tradition views on flourishing for `person_id`."""
    _require_robert_jackson(person_id)
    COMPUTE_BUDGET.consume(ServiceName.FLOURISHING, flops=1.8e9)

    scores = _rj_12_domain_scores()

    traditions = [
        TraditionView(
            tradition="aristotelian",
            tradition_full_name="Aristotelian Eudaimonia",
            overall_assessment="Severely impaired — eudaimonia requires stable conditions for virtue expression",
            domain_weights={"health_vitality": 0.15, "economic_prosperity": 0.12, "community_belonging": 0.15, "intellectual_growth": 0.13, "purpose_meaning": 0.18, "love_relationships": 0.14, "legacy_contribution": 0.13},
            weighted_score=round(0.15*34.2 + 0.12*12.1 + 0.15*41.0 + 0.13*48.9 + 0.18*52.0 + 0.14*44.8 + 0.13*38.5, 2),
            key_observations=["Economic destitution prevents development of practical wisdom", "Community engagement is a genuine strength"],
            recommendations=["Restore material conditions as precondition for eudaimonia", "Leverage existing community ties as scaffold for growth"],
        ),
        TraditionView(
            tradition="utilitarian",
            tradition_full_name="Utilitarian Welfare Maximization",
            overall_assessment="High suffering load — economic and health domains dominate welfare calculation",
            domain_weights={"health_vitality": 0.20, "economic_prosperity": 0.20, "environmental_harmony": 0.15, "play_joy": 0.15, "love_relationships": 0.15, "purpose_meaning": 0.15},
            weighted_score=round(0.20*34.2 + 0.20*12.1 + 0.15*28.7 + 0.15*31.6 + 0.15*44.8 + 0.15*52.0, 2),
            key_observations=["Economic poverty generates the highest marginal disutility", "Spiritual depth is an underweighted source of positive utility"],
            recommendations=["Maximum welfare gain from income stabilization + housing", "Spiritual community is an untapped welfare multiplier"],
        ),
        TraditionView(
            tradition="capabilities",
            tradition_full_name="Capabilities Approach (Sen & Nussbaum)",
            overall_assessment="Multiple central capabilities below threshold — human dignity compromised",
            domain_weights={"health_vitality": 0.15, "economic_prosperity": 0.15, "community_belonging": 0.12, "intellectual_growth": 0.12, "creative_expression": 0.10, "environmental_harmony": 0.12, "love_relationships": 0.12, "purpose_meaning": 0.12},
            weighted_score=round(0.15*34.2 + 0.15*12.1 + 0.12*41.0 + 0.12*48.9 + 0.10*55.3 + 0.12*28.7 + 0.12*44.8 + 0.12*52.0, 2),
            key_observations=["Bodily health and bodily integrity capabilities severely constrained by homelessness", "Senses, imagination, thought capabilities preserved — a resilience signal"],
            recommendations=["Capabilities approach demands structural intervention — individual willpower is insufficient", "Housing as precondition for 7 of 10 central capabilities"],
        ),
        TraditionView(
            tradition="ubuntu",
            tradition_full_name="Ubuntu — 'I am because we are'",
            overall_assessment="Partially intact — communal bonds survive despite material deprivation",
            domain_weights={"community_belonging": 0.30, "love_relationships": 0.25, "legacy_contribution": 0.20, "spiritual_depth": 0.15, "purpose_meaning": 0.10},
            weighted_score=round(0.30*41.0 + 0.25*44.8 + 0.20*38.5 + 0.15*62.1 + 0.10*52.0, 2),
            key_observations=["Community belonging (41) and love relationships (44.8) represent genuine Ubuntu-aligned strengths", "Individual suffering is a community failure, not only personal failure"],
            recommendations=["Engage extended community as resource mobilization network", "Reframe intervention as collective obligation, not individual charity"],
        ),
        TraditionView(
            tradition="buddhist",
            tradition_full_name="Buddhist — Cessation of Suffering",
            overall_assessment="High dukkha (suffering) load; noble eightfold path partially traversed",
            domain_weights={"health_vitality": 0.18, "play_joy": 0.18, "spiritual_depth": 0.20, "community_belonging": 0.16, "purpose_meaning": 0.14, "love_relationships": 0.14},
            weighted_score=round(0.18*34.2 + 0.18*31.6 + 0.20*62.1 + 0.16*41.0 + 0.14*52.0 + 0.14*44.8, 2),
            key_observations=["Spiritual depth (62.1) is the strongest signal — indicates capacity for liberation", "Material craving cycle (no income → suffering → impulsive coping) is key dukkha driver"],
            recommendations=["Mindfulness-based stress reduction as adjunct to housing + health interventions", "Spiritual community is already on the path — formalize as resource"],
        ),
        TraditionView(
            tradition="positive_psychology",
            tradition_full_name="Positive Psychology — PERMA Model",
            overall_assessment="Below PERMA threshold; engagement and meaning are genuine strengths",
            domain_weights={"play_joy": 0.20, "love_relationships": 0.20, "purpose_meaning": 0.20, "creative_expression": 0.20, "legacy_contribution": 0.20},
            weighted_score=round(0.20*31.6 + 0.20*44.8 + 0.20*52.0 + 0.20*55.3 + 0.20*38.5, 2),
            key_observations=["Creative expression (55.3) and purpose/meaning (52.0) are PERMA strengths", "Relationships (44.8) present — not isolated"],
            recommendations=["Leverage engagement and meaning as scaffolding for recovery", "Creative expression programs within shelter/PSH settings"],
        ),
        TraditionView(
            tradition="indigenous",
            tradition_full_name="Indigenous Wisdom — Balance & Harmony",
            overall_assessment="Out of balance — physical and material worlds severely disrupted",
            domain_weights={"environmental_harmony": 0.20, "spiritual_depth": 0.20, "community_belonging": 0.20, "health_vitality": 0.20, "purpose_meaning": 0.20},
            weighted_score=round(0.20*28.7 + 0.20*62.1 + 0.20*41.0 + 0.20*34.2 + 0.20*52.0, 2),
            key_observations=["Spiritual depth and community belonging are relatively balanced", "Environmental harmony disrupted by homelessness and urban poverty"],
            recommendations=["Land connection / nature access programs within housing plan", "Ceremonial and community practice support"],
        ),
        TraditionView(
            tradition="liberation_theology",
            tradition_full_name="Liberation Theology — Structural Justice",
            overall_assessment="Victim of structural sin — poverty and homelessness are systemic, not personal failures",
            domain_weights={"economic_prosperity": 0.25, "community_belonging": 0.20, "environmental_harmony": 0.20, "love_relationships": 0.15, "legacy_contribution": 0.20},
            weighted_score=round(0.25*12.1 + 0.20*41.0 + 0.20*28.7 + 0.15*44.8 + 0.20*38.5, 2),
            key_observations=["Economic deprivation is the defining structural injustice", "Resilience under structural oppression is itself a form of dignity"],
            recommendations=["Advocacy for policy change alongside individual intervention", "Framing: Robert's suffering is a policy failure, not a personal one"],
        ),
    ]

    return TraditionsResponse(
        person_id=person_id,
        generated_at=_NOW_ISO,
        traditions=traditions,
    )


@app.get(
    "/api/v2/flourishing/{person_id}/trajectory",
    response_model=TrajectoryResponse,
    tags=["Flourishing"],
    summary="Temporal flourishing trajectory",
    description=(
        "Returns the historical trajectory of COSM score and all 12 domain "
        "scores over time. Used to identify inflection points — "
        "moments when conditions changed significantly."
    ),
)
async def get_flourishing_trajectory(
    person_id: str = Path(..., description="Person UUID"),
) -> TrajectoryResponse:
    """Return the temporal flourishing trajectory for `person_id`."""
    _require_robert_jackson(person_id)
    COMPUTE_BUDGET.consume(ServiceName.FLOURISHING, flops=4.1e8)

    data_points = [
        TrajectoryPoint(date="2023-01-15", cosm_score=52.1, domain_scores={"health_vitality": 48.0, "economic_prosperity": 38.0, "community_belonging": 55.0, "environmental_harmony": 42.0}),
        TrajectoryPoint(date="2023-07-01", cosm_score=47.3, domain_scores={"health_vitality": 44.0, "economic_prosperity": 28.0, "community_belonging": 52.0, "environmental_harmony": 38.0}),
        TrajectoryPoint(date="2024-01-01", cosm_score=44.8, domain_scores={"health_vitality": 41.0, "economic_prosperity": 20.0, "community_belonging": 48.0, "environmental_harmony": 35.0}),
        TrajectoryPoint(date="2024-07-01", cosm_score=41.2, domain_scores={"health_vitality": 38.0, "economic_prosperity": 16.0, "community_belonging": 44.0, "environmental_harmony": 31.0}),
        TrajectoryPoint(date="2025-01-01", cosm_score=39.6, domain_scores={"health_vitality": 36.0, "economic_prosperity": 13.0, "community_belonging": 43.0, "environmental_harmony": 30.0}),
        TrajectoryPoint(date="2025-07-01", cosm_score=38.8, domain_scores={"health_vitality": 35.0, "economic_prosperity": 12.5, "community_belonging": 41.5, "environmental_harmony": 29.0}),
        TrajectoryPoint(date="2026-02-27", cosm_score=38.2, domain_scores={"health_vitality": 34.2, "economic_prosperity": 12.1, "community_belonging": 41.0, "environmental_harmony": 28.7}),
    ]

    return TrajectoryResponse(
        person_id=person_id,
        data_points=data_points,
        cosm_trend="declining",
        inflection_points=[
            "2023-07-01: Lost permanent housing — COSM dropped 4.8 points",
            "2024-01-01: SNAP recertification gap — economic domain dropped 8 points",
            "2025-11-03: Hypertensive crisis ER visit — health domain accelerated decline",
        ],
    )


@app.get(
    "/api/v2/flourishing/{person_id}/what-if",
    response_model=WhatIfResponse,
    tags=["Flourishing"],
    summary="What-if intervention modeling",
    description=(
        "Models the cascading effect of improving a single flourishing domain "
        "to a target score.\n\n"
        "For example: 'What if economic_prosperity reached 50? How would that "
        "cascade to other domains, and what interventions would achieve it?'\n\n"
        "Powered by the DOMES causal graph — changes propagate through known "
        "causal pathways, not just correlations."
    ),
)
async def get_flourishing_what_if(
    person_id: str = Path(..., description="Person UUID"),
    domain: str = Query("economic_prosperity", description="Flourishing domain to improve"),
    target: float = Query(50.0, ge=0.0, le=100.0, description="Target score (0–100)"),
) -> WhatIfResponse:
    """Return what-if intervention modeling for `person_id`."""
    _require_robert_jackson(person_id)
    COMPUTE_BUDGET.consume(ServiceName.FLOURISHING, flops=2.9e9)

    scores = _rj_12_domain_scores()
    current = scores.get(domain, {}).get("score", 20.0)

    return WhatIfResponse(
        person_id=person_id,
        domain=domain,
        current_score=current,
        target_score=target,
        feasibility="achievable_with_intervention",
        estimated_time_to_target="6–12 months with PSH placement + SSI/SSDI",
        required_interventions=[
            {"intervention": "PSH placement",     "contribution": 0.55, "cost": 18000, "system": "Detroit Housing Commission"},
            {"intervention": "SSI/SSDI approval", "contribution": 0.35, "cost": 600,   "system": "Social Security Administration"},
            {"intervention": "ACT team support",  "contribution": 0.10, "cost": 4200,  "system": "Wayne County CMHC"},
        ],
        cascading_effects={
            "health_vitality":        +8.2,
            "environmental_harmony":  +11.4,
            "community_belonging":    +5.1,
            "physical_space_beauty":  +12.8,
            "play_joy":               +4.3,
            "love_relationships":     +3.2,
            "purpose_meaning":        +2.8,
        },
        annual_cost_reduction=187000.0,
    )


@app.get(
    "/api/v2/flourishing/{person_id}/cost-of-suffering",
    response_model=CostOfSufferingResponse,
    tags=["Flourishing"],
    summary="Dollar cost of suffering analysis",
    description=(
        "Returns the financial cost analysis of this person's current "
        "low flourishing state — comparing actual fragmented system costs "
        "to what coordinated care would cost.\n\n"
        "This is DOMES' most powerful policy argument: the difference between "
        "fragmented and coordinated care represents preventable waste.\n\n"
        "Costs are broken down by domain (housing system, health system, "
        "justice system, etc.) and include a lifetime cost projection."
    ),
)
async def get_cost_of_suffering(
    person_id: str = Path(..., description="Person UUID"),
) -> CostOfSufferingResponse:
    """Return cost-of-suffering analysis for `person_id`."""
    _require_robert_jackson(person_id)
    COMPUTE_BUDGET.consume(ServiceName.FLOURISHING, flops=3.4e8)

    return CostOfSufferingResponse(
        person_id=person_id,
        computed_at=_NOW_ISO,
        annual_system_cost_fragmented=284000.0,
        annual_system_cost_coordinated=97000.0,
        annual_savings_potential=187000.0,
        lifetime_cost_estimate=4200000.0,
        cost_per_domain={
            "health_system":          142000.0,
            "housing_system":         68000.0,
            "behavioral_health":      41000.0,
            "justice_system":         18000.0,
            "income_support":         15000.0,
        },
        methodology=(
            "Costs computed from actual claims data (Medicaid), HMIS bed-night costs "
            "($89/night emergency shelter), psychiatric hospitalization rates "
            "($1,400/day average), and ER utilization (2.3 visits/year average). "
            "Coordinated care cost modeled from ACT team literature ($18,000/year) "
            "plus PSH unit cost ($28,000/year including support services). "
            "Lifetime estimate uses actuarial life expectancy of 71.4 years "
            "(Black male, chronically homeless, current health status)."
        ),
    )


# ===========================================================================
# Fragment Endpoints
# ===========================================================================

@app.post(
    "/api/v2/fragments/",
    response_model=FragmentIngestResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Fragment (Ingest)"],
    summary="Ingest a new data fragment",
    description=(
        "Ingests a raw data fragment from any integrated government system. "
        "The fragment is the atomic unit of data in DOMES — an immutable "
        "snapshot of data from one source system at one point in time.\n\n"
        "**Fragment lifecycle:**\n"
        "`ingested_at → validated_at → normalized_at → dome_assembled_at`\n\n"
        "After ingest, the fragment is queued for:\n"
        "1. Schema validation\n"
        "2. Normalization (FHIR, HMIS → DOMES internal model)\n"
        "3. Dome re-assembly (if fragment changes key state)\n\n"
        "**42 CFR Part 2 warning:** Set `is_42cfr_protected=true` for any "
        "fragment containing substance use disorder data. These fragments "
        "require specific consent and are subject to stricter access controls."
    ),
)
async def ingest_fragment(
    fragment: FragmentIngestRequest,
) -> FragmentIngestResponse:
    """Ingest a new raw data fragment."""
    COMPUTE_BUDGET.consume(ServiceName.FRAGMENT, flops=2.4e8)
    new_id = str(uuid.uuid4())
    return FragmentIngestResponse(
        fragment_id=new_id,
        person_id=fragment.person_id,
        ingested_at=_NOW_ISO,
        validation_status="queued",
        normalization_queued=True,
        dome_reassembly_triggered=True,
    )


@app.get(
    "/api/v2/fragments/{person_id}/recent",
    response_model=RecentFragmentsResponse,
    tags=["Fragment (Ingest)"],
    summary="Recent fragments",
    description=(
        "Returns the most recent data fragments for this person, "
        "paginated in reverse-chronological order by ingested_at.\n\n"
        "Useful for monitoring data flow and diagnosing ingest issues."
    ),
)
async def get_recent_fragments(
    person_id: str = Path(..., description="Person UUID"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Fragments per page"),
) -> RecentFragmentsResponse:
    """Return recent fragments for `person_id`."""
    _require_robert_jackson(person_id)
    COMPUTE_BUDGET.consume(ServiceName.FRAGMENT, flops=1.1e7)

    fragments = [
        FragmentSummary(fragment_id="frag-001", source_type="fhir",         data_domain="health",           ingested_at="2025-11-03T04:21:00Z", validation_status="valid",   is_superseded=False, is_42cfr_protected=False),
        FragmentSummary(fragment_id="frag-002", source_type="wearable",     data_domain="biometric",        ingested_at="2025-11-02T23:00:00Z", validation_status="valid",   is_superseded=False, is_42cfr_protected=False),
        FragmentSummary(fragment_id="frag-003", source_type="hmis",         data_domain="housing",          ingested_at="2025-10-12T10:15:00Z", validation_status="valid",   is_superseded=False, is_42cfr_protected=False),
        FragmentSummary(fragment_id="frag-004", source_type="claims",       data_domain="health",           ingested_at="2025-10-01T14:30:00Z", validation_status="valid",   is_superseded=False, is_42cfr_protected=False),
        FragmentSummary(fragment_id="frag-005", source_type="benefits",     data_domain="financial",        ingested_at="2025-09-01T08:00:00Z", validation_status="valid",   is_superseded=False, is_42cfr_protected=False),
    ]

    return RecentFragmentsResponse(
        person_id=person_id,
        total_fragments=847,
        page=page,
        page_size=page_size,
        fragments=fragments,
    )


@app.get(
    "/api/v2/fragments/{person_id}/sources",
    response_model=DataSourcesResponse,
    tags=["Fragment (Ingest)"],
    summary="Data source status",
    description=(
        "Returns the status of all data sources contributing fragments for "
        "this person — last fragment date, 30-day count, average quality, "
        "and whether the source is currently active (feeding data).\n\n"
        "A `gap_days` value > 30 indicates a source that has gone silent — "
        "a data gap that may degrade prediction confidence."
    ),
)
async def get_fragment_sources(
    person_id: str = Path(..., description="Person UUID"),
) -> DataSourcesResponse:
    """Return data source status for `person_id`."""
    _require_robert_jackson(person_id)

    sources = [
        DataSourceStatus(source_type="fhir",         last_fragment_at="2025-11-03T04:21:00Z", fragment_count_30d=14,  avg_quality_score=0.92, is_active=True,  gap_days=None),
        DataSourceStatus(source_type="wearable",     last_fragment_at="2025-11-02T23:00:00Z", fragment_count_30d=720, avg_quality_score=0.97, is_active=True,  gap_days=None),
        DataSourceStatus(source_type="hmis",         last_fragment_at="2025-10-12T10:15:00Z", fragment_count_30d=3,   avg_quality_score=0.84, is_active=True,  gap_days=None),
        DataSourceStatus(source_type="claims",       last_fragment_at="2025-10-01T14:30:00Z", fragment_count_30d=8,   avg_quality_score=0.89, is_active=True,  gap_days=None),
        DataSourceStatus(source_type="benefits",     last_fragment_at="2025-09-01T08:00:00Z", fragment_count_30d=1,   avg_quality_score=0.78, is_active=True,  gap_days=None),
        DataSourceStatus(source_type="criminal_justice", last_fragment_at=None,               fragment_count_30d=0,   avg_quality_score=0.0,  is_active=False, gap_days=None),
        DataSourceStatus(source_type="environmental", last_fragment_at="2025-11-01T00:00:00Z", fragment_count_30d=30, avg_quality_score=0.95, is_active=True,  gap_days=None),
    ]

    return DataSourcesResponse(
        person_id=person_id,
        total_sources=len(sources),
        active_sources=sum(1 for s in sources if s.is_active),
        sources=sources,
    )


@app.get(
    "/api/v2/fragments/{person_id}/quality",
    response_model=FragmentQualityResponse,
    tags=["Fragment (Ingest)"],
    summary="Fragment quality metrics",
    description=(
        "Returns quality metrics for the full fragment corpus for this person.\n\n"
        "Metrics include:\n"
        "- Overall quality score (0.0–1.0)\n"
        "- Validation pass rate (schema + content validation)\n"
        "- Normalization success rate (FHIR/HMIS → DOMES translation)\n"
        "- Completeness by flourishing domain\n"
        "- Data freshness by source\n"
        "- Known quality issues flagged by the pipeline"
    ),
)
async def get_fragment_quality(
    person_id: str = Path(..., description="Person UUID"),
) -> FragmentQualityResponse:
    """Return fragment quality metrics for `person_id`."""
    _require_robert_jackson(person_id)

    return FragmentQualityResponse(
        person_id=person_id,
        overall_quality_score=0.81,
        total_fragments=847,
        validation_pass_rate=0.94,
        normalization_success_rate=0.89,
        completeness_by_domain={
            "health":           0.92,
            "housing":          0.88,
            "biometric":        0.97,
            "financial":        0.71,
            "behavioral_health": 0.76,
            "criminal_justice": 0.12,
            "environmental":    0.95,
        },
        freshness_by_source={
            "fhir":       "2025-11-03 (current)",
            "wearable":   "2025-11-02 (current)",
            "hmis":       "2025-10-12 (26 days old)",
            "claims":     "2025-10-01 (37 days old — approaching stale)",
            "benefits":   "2025-09-01 (87 days old — stale)",
        },
        data_quality_issues=[
            "Criminal justice source not connected — 0 fragments (gap_type: political/legal)",
            "SNAP benefits last updated 87 days ago — recertification status unknown",
            "5 FHIR fragments failed normalization (LOINC code not in reference table)",
        ],
    )


# ===========================================================================
# Compute Endpoints
# ===========================================================================

@app.get(
    "/api/v2/compute/budget",
    response_model=ComputeBudgetResponse,
    tags=["Compute Budget"],
    summary="Total compute budget status",
    description=(
        "Returns the full status of the DOMES compute budget — "
        "3×10²¹ FLOPs over 5 years directed at Robert Jackson.\n\n"
        "This is the most compute ever directed at modeling a single human life. "
        "For reference: 3×10²¹ FLOPs ≈ 100× GPT-4 training, sustained continuously "
        "for 5 years.\n\n"
        "Includes:\n"
        "- Total budget and consumption to date\n"
        "- Per-service allocation and utilization\n"
        "- Marginal information gain analysis\n"
        "- Compute pressure (should we shift allocation?)\n"
        "- Infrastructure cost and energy estimates"
    ),
)
async def get_compute_budget() -> ComputeBudgetResponse:
    """Return the full compute budget status."""
    report = COMPUTE_BUDGET.status_report()
    return ComputeBudgetResponse(
        total_flops=TOTAL_FLOPS,
        budget_years=BUDGET_YEARS,
        budget_usd_low=TOTAL_BUDGET_USD_LOW,
        budget_usd_high=TOTAL_BUDGET_USD_HIGH,
        sustained_flops_per_second=SUSTAINED_FLOPS_PER_SECOND,
        cost_per_flop=COST_PER_FLOP,
        program_elapsed_fraction=report["program"]["program_elapsed_fraction"],
        total_flops_consumed=report["consumption"]["total_flops_consumed"],
        budget_fraction_consumed=report["consumption"]["budget_fraction_consumed"],
        total_cost_consumed_usd=report["consumption"]["total_cost_usd"],
        overall_utilization=report["consumption"]["overall_utilization"],
        energy_consumed_kwh=report["consumption"]["energy_consumed_kwh"],
        energy_cost_usd=report["consumption"]["energy_cost_usd"],
        services=report["services"],
        compute_pressure=report["pressure"],
        next_flop_goes_to=report["next_flop_goes_to"],
    )


@app.get(
    "/api/v2/compute/allocation/{person_id}",
    response_model=ComputeAllocationResponse,
    tags=["Compute Budget"],
    summary="Per-person compute allocation",
    description=(
        "Returns the compute allocation breakdown for a specific person. "
        "In DOMES v2, all compute is directed at Robert Jackson — so this "
        "endpoint returns the full global allocation, annotated with the "
        "person ID.\n\n"
        "In a future multi-person deployment, this would return only the "
        "slice of compute allocated to this individual."
    ),
)
async def get_compute_allocation(
    person_id: str = Path(..., description="Person UUID"),
) -> ComputeAllocationResponse:
    """Return compute allocation for `person_id`."""
    _require_robert_jackson(person_id)
    report = COMPUTE_BUDGET.allocation_report(person_id)
    return ComputeAllocationResponse(
        person_id=person_id,
        note=report["note"],
        services=report["services"],
        total_flops_consumed=COMPUTE_BUDGET.total_flops_consumed,
        total_cost_consumed_usd=COMPUTE_BUDGET.total_cost_consumed_usd,
    )


@app.get(
    "/api/v2/compute/information-gain",
    response_model=InfoGainResponse,
    tags=["Compute Budget"],
    summary="Marginal information gain analysis",
    description=(
        "Returns the marginal information gain curves for all four compute-consuming "
        "services — prediction, flourishing, fragment, and cosm.\n\n"
        "Each service follows a diminishing returns curve: IG(n) = n^α, "
        "where α < 1 (concave). The marginal gain dIG/dn tells us which "
        "service would benefit most from the next FLOP.\n\n"
        "This drives the DOMES compute allocation engine: compute pressure "
        "is high when marginal values are unequal, suggesting a rebalance."
    ),
)
async def get_information_gain() -> InfoGainResponse:
    """Return marginal information gain analysis."""
    best = COMPUTE_BUDGET.highest_marginal_value()
    pressure = COMPUTE_BUDGET.compute_pressure()

    service_curves: dict[str, dict[str, Any]] = {}
    for svc in ServiceName:
        alloc = COMPUTE_BUDGET.services[svc]
        service_curves[svc.value] = {
            "allocated_fraction":        alloc.allocated_fraction,
            "flops_consumed":            alloc.flops_consumed,
            "information_gain":          alloc.information_gain,
            "marginal_information_gain": alloc.marginal_information_gain,
            "alpha":                     alloc.info_gain_alpha,
            "utilization":               alloc.utilization,
        }

    return InfoGainResponse(
        services=service_curves,
        highest_marginal_value_service=best.value,
        recommendation=pressure.get("recommendation"),
    )


# ===========================================================================
# System-Wide Endpoints
# ===========================================================================

@app.get(
    "/api/v2/systems",
    response_model=GovernmentSystemsResponse,
    tags=["System-Wide"],
    summary="All 30 government systems",
    description=(
        "Returns the full catalog of 30 government data systems integrated "
        "with DOMES v2, including their data domain, governing privacy law, "
        "API availability, and a description.\n\n"
        "Systems span: health (Medicaid, Medicare, VA), behavioral health "
        "(CMHC, SUD), housing (HMIS, HCV, PSH), income (SNAP, SSI, SSDI, "
        "TANF), justice (probation, DOC), child welfare, and veterans services."
    ),
)
async def get_systems() -> GovernmentSystemsResponse:
    """Return the full catalog of integrated government systems."""
    systems = [
        GovernmentSystem(system_id="sys-medicaid",     name="State Medicaid",                    domain="health",            privacy_law="HIPAA",           api_availability="partner_only", description="State Medicaid claims, enrollment, and encounter data"),
        GovernmentSystem(system_id="sys-medicare",     name="Medicare (CMS)",                    domain="health",            privacy_law="HIPAA",           api_availability="partner_only", description="Federal Medicare claims and enrollment"),
        GovernmentSystem(system_id="sys-va-health",    name="VA Health System",                  domain="health",            privacy_law="38_USC_5705",     api_availability="partner_only", description="Veterans Affairs electronic health records"),
        GovernmentSystem(system_id="sys-fhir-ehr",     name="EHR (FHIR R4)",                     domain="health",            privacy_law="HIPAA",           api_availability="limited",      description="Hospital and clinic EHR via FHIR R4 API"),
        GovernmentSystem(system_id="sys-cmhc",         name="Community Mental Health Centers",   domain="behavioral_health", privacy_law="HIPAA",           api_availability="partner_only", description="CMHC encounter and treatment data"),
        GovernmentSystem(system_id="sys-sud",          name="SUD Treatment Programs",            domain="behavioral_health", privacy_law="42_CFR_Part_2",   api_availability="partner_only", description="Substance use disorder treatment — strictest privacy"),
        GovernmentSystem(system_id="sys-hmis",         name="HMIS (HUD)",                        domain="housing",           privacy_law="HMIS_Privacy",    api_availability="partner_only", description="Homeless Management Information System — shelter and service records"),
        GovernmentSystem(system_id="sys-hcv",          name="HCV / Section 8 (HUD)",             domain="housing",           privacy_law="Privacy_Act",     api_availability="none",         description="Housing Choice Voucher program — rental assistance"),
        GovernmentSystem(system_id="sys-psh",          name="Permanent Supportive Housing",      domain="housing",           privacy_law="HMIS_Privacy",    api_availability="partner_only", description="PSH waitlist and placement tracking"),
        GovernmentSystem(system_id="sys-snap",         name="SNAP / EBT",                        domain="income",            privacy_law="Privacy_Act",     api_availability="none",         description="Supplemental Nutrition Assistance Program"),
        GovernmentSystem(system_id="sys-ssi",          name="SSI (Social Security)",             domain="income",            privacy_law="Privacy_Act",     api_availability="partner_only", description="Supplemental Security Income for disabled individuals"),
        GovernmentSystem(system_id="sys-ssdi",         name="SSDI (Social Security)",            domain="income",            privacy_law="Privacy_Act",     api_availability="partner_only", description="Social Security Disability Insurance"),
        GovernmentSystem(system_id="sys-tanf",         name="TANF",                              domain="income",            privacy_law="Privacy_Act",     api_availability="none",         description="Temporary Assistance for Needy Families"),
        GovernmentSystem(system_id="sys-wic",          name="WIC (USDA)",                        domain="income",            privacy_law="Privacy_Act",     api_availability="none",         description="Women, Infants, and Children nutrition program"),
        GovernmentSystem(system_id="sys-liheap",       name="LIHEAP",                            domain="income",            privacy_law="Privacy_Act",     api_availability="none",         description="Low Income Home Energy Assistance Program"),
        GovernmentSystem(system_id="sys-ui",           name="Unemployment Insurance",            domain="income",            privacy_law="State_Law",       api_availability="none",         description="State unemployment insurance claims and payments"),
        GovernmentSystem(system_id="sys-eitc",         name="EITC (IRS)",                        domain="income",            privacy_law="Privacy_Act",     api_availability="none",         description="Earned Income Tax Credit — filed through IRS"),
        GovernmentSystem(system_id="sys-probation",    name="Probation / Parole",                domain="justice",           privacy_law="CJIS",            api_availability="partner_only", description="Adult probation and parole supervision records"),
        GovernmentSystem(system_id="sys-doc",          name="Department of Corrections",         domain="justice",           privacy_law="CJIS",            api_availability="partner_only", description="Incarceration, booking, and release records"),
        GovernmentSystem(system_id="sys-drug-court",   name="Drug Court",                        domain="justice",           privacy_law="42_CFR_Part_2",   api_availability="partner_only", description="Drug court enrollment and compliance tracking"),
        GovernmentSystem(system_id="sys-foster-care",  name="Foster Care (Title IV-E)",          domain="child_welfare",     privacy_law="CAPTA",           api_availability="partner_only", description="Child welfare foster care records"),
        GovernmentSystem(system_id="sys-head-start",   name="Head Start (HHS)",                  domain="education",         privacy_law="FERPA",           api_availability="none",         description="Early childhood education and family services"),
        GovernmentSystem(system_id="sys-iep",          name="Special Education / IEP",           domain="education",         privacy_law="FERPA",           api_availability="none",         description="Individualized Education Programs for children with disabilities"),
        GovernmentSystem(system_id="sys-va-disability", name="VA Disability Compensation",       domain="veterans",          privacy_law="38_USC_5705",     api_availability="partner_only", description="Veteran disability ratings and compensation"),
        GovernmentSystem(system_id="sys-hudvash",      name="HUD-VASH",                          domain="veterans",          privacy_law="38_USC_5705",     api_availability="partner_only", description="HUD-VA Supportive Housing for homeless veterans"),
        GovernmentSystem(system_id="sys-ssvf",         name="SSVF (VA)",                         domain="veterans",          privacy_law="38_USC_5705",     api_availability="partner_only", description="Supportive Services for Veteran Families"),
        GovernmentSystem(system_id="sys-act-team",     name="Assertive Community Treatment",     domain="behavioral_health", privacy_law="HIPAA",           api_availability="partner_only", description="ACT team encounters, medication, and case management"),
        GovernmentSystem(system_id="sys-pace",         name="PACE (CMS)",                        domain="health",            privacy_law="HIPAA",           api_availability="partner_only", description="Program of All-inclusive Care for the Elderly"),
        GovernmentSystem(system_id="sys-ltss",         name="LTSS (Medicaid)",                   domain="health",            privacy_law="HIPAA",           api_availability="partner_only", description="Long-Term Services and Supports via Medicaid waiver"),
        GovernmentSystem(system_id="sys-wearable",     name="Wearable / CGM Data",               domain="health",            privacy_law="HIPAA",           api_availability="public",       description="Apple Watch, Oura, CGM, and other wearable biometric streams"),
    ]

    return GovernmentSystemsResponse(
        total_systems=len(systems),
        systems=systems,
    )


@app.get(
    "/api/v2/gaps",
    response_model=DataGapsResponse,
    tags=["System-Wide"],
    summary="Data gaps between systems",
    description=(
        "Returns all identified data gaps — structural barriers preventing "
        "data from flowing between government systems.\n\n"
        "Gap types:\n"
        "- **Legal**: Statutory prohibition (42 CFR Part 2, CJIS, FERPA)\n"
        "- **Technical**: No API, incompatible formats\n"
        "- **Political**: Jurisdictional resistance\n"
        "- **Structural**: Policy design (e.g., Medicaid inmate exclusion)\n"
        "- **Resource**: Budget/staffing constraints\n\n"
        "Critical gaps have patient safety implications and are the highest "
        "priority for bridge development."
    ),
)
async def get_data_gaps() -> DataGapsResponse:
    """Return all data gaps between integrated government systems."""
    gaps = [
        DataGap(gap_id="gap-001", system_a="SUD Treatment (42 CFR Part 2)",  system_b="Medicaid EHR", gap_type="legal",     severity="critical", description="42 CFR Part 2 prohibits SUD treatment data from flowing to Medicaid without patient consent for each disclosure. ER physicians treating overdose patients cannot see SUD history.", blocking_statute="42 CFR Part 2", workaround="Patient-directed consent via SMART on FHIR; Part 2 Final Rule (2024) expanded QSO definitions"),
        DataGap(gap_id="gap-002", system_a="Department of Corrections",      system_b="Medicaid",     gap_type="structural", severity="critical", description="Medicaid Inmate Exclusion Policy (42 USC 1396d(a)(29)(A)): Medicaid is suspended upon incarceration. Coverage gap causes medication lapse and treatment interruption at release.", blocking_statute="42 USC 1396d(a)(29)(A)", workaround="Pre-release Medicaid reinstatement (pilot in 5 states); 21st Century Cures Act Section 5032"),
        DataGap(gap_id="gap-003", system_a="SNAP",                           system_b="HMIS",         gap_type="technical",  severity="high",     description="SNAP case management runs on legacy COBOL mainframes with no API. HMIS cannot confirm SNAP benefit status, preventing coordinated economic support planning.", blocking_statute=None, workaround="Manual data sharing agreement; state-level data warehouse intermediary"),
        DataGap(gap_id="gap-004", system_a="IEP / Special Education",        system_b="CMHC",         gap_type="legal",      severity="high",     description="FERPA prohibits disclosure of education records to CMHC without consent or judicial order. Children with IEPs have behavioral health needs invisible to mental health system.", blocking_statute="FERPA (20 USC 1232g)", workaround="Parent/guardian consent; state education-health data sharing legislation"),
        DataGap(gap_id="gap-005", system_a="Child Welfare / Foster Care",    system_b="HMIS",         gap_type="political",  severity="moderate", description="Child welfare agencies rarely share data with HMIS due to jurisdictional concerns. Former foster youth aging out lack housing history visible to CoC.", blocking_statute=None, workaround="Memoranda of Understanding between child welfare and CoC"),
        DataGap(gap_id="gap-006", system_a="VA Health (38 USC 5705)",        system_b="Community EHR", gap_type="legal",     severity="high",     description="VA mental health records have highest federal confidentiality protection. VA-to-community care transitions lose behavioral health context.", blocking_statute="38 USC 5705", workaround="VA MISSION Act community care integration; patient authorization via Blue Button"),
    ]

    return DataGapsResponse(
        total_gaps=len(gaps),
        critical_gaps=sum(1 for g in gaps if g.severity == "critical"),
        gaps=gaps,
    )


@app.get(
    "/api/v2/provisions",
    response_model=ProvisionsResponse,
    tags=["System-Wide"],
    summary="Legal provisions enabling/blocking data sharing",
    description=(
        "Returns the legal provisions that govern data sharing between "
        "DOMES-integrated systems — both enabling provisions (that allow "
        "data flow with consent or under specific conditions) and blocking "
        "provisions (that prohibit data flow).\n\n"
        "The DOMES legal matching engine maps each data fragment to applicable "
        "provisions to ensure all data use is legally authorized."
    ),
)
async def get_provisions() -> ProvisionsResponse:
    """Return legal provisions governing data sharing in DOMES."""
    provisions = [
        LegalProvision(provision_id="prov-001", name="HIPAA TPO Exception",             provision_type="right",      domain="health",         description="HIPAA permits disclosure for Treatment, Payment, and Healthcare Operations without individual authorization.", enables=["medicaid_to_ehr", "ehr_to_cmhc", "claims_to_dome"], blocks=[], citation="45 CFR 164.502(a)(1)"),
        LegalProvision(provision_id="prov-002", name="42 CFR Part 2 (SUD Prohibition)", provision_type="protection", domain="substance_use",  description="Prohibits disclosure of patient-identifying SUD treatment information without specific written consent.", enables=[], blocks=["sud_to_medicaid", "sud_to_ehr", "sud_to_court"], citation="42 CFR Part 2; updated 2024 Final Rule"),
        LegalProvision(provision_id="prov-003", name="FERPA (Education Records)",       provision_type="protection", domain="education",      description="Prohibits disclosure of student education records without consent. Applies to IEP records.", enables=[], blocks=["iep_to_cmhc", "school_to_hmis"], citation="20 USC 1232g; 34 CFR Part 99"),
        LegalProvision(provision_id="prov-004", name="CJIS Policy (Criminal Justice)",  provision_type="protection", domain="justice",        description="FBI CJIS Security Policy restricts access to criminal justice information to authorized law enforcement.", enables=[], blocks=["doc_to_medicaid", "doc_to_hmis"], citation="FBI CJIS Security Policy v5.9.2"),
        LegalProvision(provision_id="prov-005", name="HITECH Breach Notification",      provision_type="obligation", domain="health",         description="Covered entities must notify individuals and HHS of unsecured PHI breaches.", enables=[], blocks=[], citation="HITECH Act Section 13402; 45 CFR 164.400-414"),
        LegalProvision(provision_id="prov-006", name="ADA Title II (Equal Access)",     provision_type="right",      domain="civil_rights",   description="People with disabilities have the right to reasonable accommodation in all government programs and services.", enables=["accommodation_request", "service_coordination"], blocks=[], citation="ADA Title II; 28 CFR Part 35"),
        LegalProvision(provision_id="prov-007", name="21st Century Cures Act (TEFCA)",  provision_type="right",      domain="health",         description="Establishes the Trusted Exchange Framework enabling secure interoperable health data exchange.", enables=["fhir_network_exchange", "patient_access_api"], blocks=[], citation="21st Century Cures Act, Pub. L. 114-255, Sec. 4003"),
        LegalProvision(provision_id="prov-008", name="Medicaid Inmate Exclusion",       provision_type="protection", domain="health",         description="Federal law prohibits Medicaid payment for services provided to incarcerated individuals.", enables=[], blocks=["medicaid_during_incarceration"], citation="42 USC 1396d(a)(29)(A); SSA Section 1905(a)(29)(A)"),
        LegalProvision(provision_id="prov-009", name="CAPTA (Child Abuse Records)",     provision_type="protection", domain="child_welfare",  description="Child abuse and neglect records are strictly confidential; disclosure limited to specific purposes.", enables=[], blocks=["child_welfare_to_hmis", "child_welfare_to_courts_broad"], citation="CAPTA, 42 USC 5106a(b)(2)(B)(viii)"),
        LegalProvision(provision_id="prov-010", name="Privacy Act of 1974",             provision_type="protection", domain="income",         description="Federal records about individuals (SSA, SNAP, IRS) may not be disclosed without consent or court order.", enables=[], blocks=["ssa_to_third_party", "snap_to_hmis_direct"], citation="Privacy Act of 1974, 5 USC 552a"),
    ]

    return ProvisionsResponse(
        total_provisions=len(provisions),
        provisions=provisions,
    )


# ---------------------------------------------------------------------------
# Module-level import guard
# ---------------------------------------------------------------------------

import math  # noqa: E402 — imported at module bottom to avoid circular; used in forecast
