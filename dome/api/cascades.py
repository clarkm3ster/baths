"""Cascade detection router for THE DOME API.

Provides endpoints to run cascade detection on a person's current state
and to retrieve stored cascade alerts.  Detection delegates to
``CascadeDetector`` which matches person-state transitions against known
cascade definitions and projects cost divergence between intervention
and non-intervention paths.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dome.db.database import get_session
from dome.db.tables import CascadeAlertTable, FiscalEventTable, PersonTable
from dome.models.dome_metrics import DomeMetrics
from dome.models.dynamic_state import DynamicState
from dome.schemas.cascade_schemas import CascadeAlertSummary, CascadeDetectRequest

logger = logging.getLogger("dome.api.cascades")

router = APIRouter(prefix="/persons", tags=["cascades"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _load_person_row(uid: str, session: AsyncSession) -> PersonTable:
    """Load a ``PersonTable`` row by *person_uid*, raising 404 if absent."""
    stmt = select(PersonTable).where(PersonTable.person_uid == uid)
    result = await session.execute(stmt)
    row = result.scalar_one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Person {uid!r} not found")
    return row


async def _load_fiscal_events(uid: str, session: AsyncSession) -> list[dict]:
    """Load all fiscal event rows for a person as dicts."""
    stmt = (
        select(FiscalEventTable)
        .where(FiscalEventTable.person_uid == uid)
        .order_by(FiscalEventTable.event_date.asc())
    )
    result = await session.execute(stmt)
    rows = result.scalars().all()
    return [
        {
            "event_id": r.event_id,
            "person_uid": r.person_uid,
            "event_date": str(r.event_date.date()) if r.event_date else None,
            "payer_level": r.payer_level,
            "payer_entity": r.payer_entity,
            "program_or_fund": r.program_or_fund,
            "domain": r.domain,
            "mechanism": r.mechanism,
            "service_category": r.service_category,
            "amount_paid": r.amount_paid,
            "confidence": r.confidence,
        }
        for r in rows
    ]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post(
    "/{uid}/detect-cascades",
    summary="Detect cascade failures",
    response_model=list[CascadeAlertSummary],
)
async def detect_cascades(
    uid: str,
    req: CascadeDetectRequest,
    session: AsyncSession = Depends(get_session),
) -> list[CascadeAlertSummary]:
    """Run cascade detection for person *uid*.

    Loads the person's dynamic state, DOME metrics, and fiscal history,
    then invokes ``CascadeDetector.detect()`` to identify any cascade
    failure patterns the person has entered.  Detected alerts are
    persisted to the ``cascade_alerts`` table and returned as a list of
    ``CascadeAlertSummary`` objects.

    If the CascadeDetector engine is not available, a fallback detection
    heuristic is applied based on fiscal event patterns.
    """
    row = await _load_person_row(uid, session)
    fiscal_events = await _load_fiscal_events(uid, session)

    # Reconstruct state objects for the engine
    dynamic_state = DynamicState(**(row.dynamic_state_json or {}))
    dome_metrics = DomeMetrics(**(row.dome_metrics_json or {}))

    try:
        from dome.engines.cascade_detector import CascadeDetector

        detector = CascadeDetector()
        alerts = detector.detect(
            person_uid=uid,
            dynamic_state=dynamic_state,
            dome_metrics=dome_metrics,
            fiscal_history=fiscal_events,
            lookback_months=req.lookback_months,
            min_confidence=req.min_confidence,
            cascade_ids=req.cascade_ids,
        )
    except (ImportError, AttributeError) as exc:
        logger.warning(
            "CascadeDetector unavailable (%s), generating fallback alerts", exc
        )
        alerts = _fallback_detect(uid, dynamic_state, fiscal_events, req)
    except Exception as exc:
        logger.exception("CascadeDetector.detect() failed")
        raise HTTPException(
            status_code=500, detail=f"Cascade detection failed: {exc}"
        ) from exc

    # Persist alerts to DB
    summaries: list[CascadeAlertSummary] = []
    for alert in alerts:
        # Normalize: accept both Pydantic models and dicts
        if hasattr(alert, "model_dump"):
            a = alert.model_dump(mode="json")
        elif isinstance(alert, dict):
            a = alert
        else:
            a = dict(alert)

        alert_id = a.get("alert_id", str(uuid4()))
        cascade_id = a.get("cascade_id", "unknown")
        current_link_index = a.get("current_link_index", 0)
        confidence = a.get("confidence", 0.0)
        path_a = a.get("path_a_projected_cost", 0.0)
        path_b = a.get("path_b_projected_cost", 0.0)
        recommended = a.get("recommended_interventions", [])

        alert_row = CascadeAlertTable(
            alert_id=alert_id,
            person_uid=uid,
            cascade_id=cascade_id,
            current_link_index=current_link_index,
            confidence=confidence,
            detected_at=datetime.now(tz=timezone.utc),
            path_a_projected_cost=path_a,
            path_b_projected_cost=path_b,
            recommended_interventions_json=recommended,
        )
        session.add(alert_row)

        summaries.append(
            CascadeAlertSummary(
                alert_id=alert_id,
                cascade_id=cascade_id,
                cascade_name=a.get("cascade_name", cascade_id),
                current_link_index=current_link_index,
                confidence=confidence,
                path_a_projected_cost=path_a,
                path_b_projected_cost=path_b,
                potential_savings=path_a - path_b,
                recommended_interventions=recommended,
            )
        )

    await session.flush()
    logger.info(
        "Detected %d cascade alerts for person %s", len(summaries), uid
    )
    return summaries


@router.get("/{uid}/cascade-alerts", summary="Get cascade alerts")
async def get_cascade_alerts(
    uid: str,
    session: AsyncSession = Depends(get_session),
) -> list[dict]:
    """Retrieve all stored cascade alerts for person *uid*.

    Returns every ``CascadeAlertTable`` row associated with the person
    as a list of dictionaries, ordered by detection time (most recent
    first).
    """
    # Validate person exists
    await _load_person_row(uid, session)

    stmt = (
        select(CascadeAlertTable)
        .where(CascadeAlertTable.person_uid == uid)
        .order_by(CascadeAlertTable.created_at.desc())
    )
    result = await session.execute(stmt)
    rows = result.scalars().all()

    alerts = []
    for row in rows:
        alerts.append(
            {
                "alert_id": row.alert_id,
                "person_uid": row.person_uid,
                "cascade_id": row.cascade_id,
                "current_link_index": row.current_link_index,
                "confidence": row.confidence,
                "detected_at": row.detected_at.isoformat() if row.detected_at else None,
                "path_a_projected_cost": row.path_a_projected_cost,
                "path_b_projected_cost": row.path_b_projected_cost,
                "potential_savings": (
                    (row.path_a_projected_cost or 0) - (row.path_b_projected_cost or 0)
                ),
                "recommended_interventions": row.recommended_interventions_json or [],
            }
        )

    return alerts


# ---------------------------------------------------------------------------
# Fallback detection — used when CascadeDetector is unavailable
# ---------------------------------------------------------------------------


def _fallback_detect(
    uid: str,
    dynamic_state: DynamicState,
    fiscal_events: list[dict],
    req: CascadeDetectRequest,
) -> list[dict]:
    """Heuristic cascade detection based on observable state signals.

    Checks for common cascade-entry indicators:
    1. Housing instability + rising healthcare costs
    2. Justice involvement + employment loss
    3. High ED utilization pattern

    Returns a list of alert dicts that can be persisted.
    """
    alerts: list[dict] = []
    now = datetime.now(tz=timezone.utc)

    # Heuristic 1: Housing instability cascade
    housing_unstable = dynamic_state.housing_state.housing_status in (
        "shelter",
        "street",
        "doubled_up",
    )
    healthcare_events = [
        e for e in fiscal_events if e.get("domain") == "healthcare"
    ]
    high_healthcare = sum(e.get("amount_paid", 0) for e in healthcare_events) > 10_000

    if housing_unstable and high_healthcare:
        alert = {
            "alert_id": str(uuid4()),
            "person_uid": uid,
            "cascade_id": "housing_health_spiral",
            "cascade_name": "Housing-Health Spiral",
            "current_link_index": 1,
            "confidence": 0.65,
            "detected_at": now.isoformat(),
            "path_a_projected_cost": 250_000.0,
            "path_b_projected_cost": 85_000.0,
            "recommended_interventions": [
                "rapid_rehousing",
                "care_coordination",
                "behavioral_health_referral",
            ],
        }
        if alert["confidence"] >= req.min_confidence:
            alerts.append(alert)

    # Heuristic 2: Justice-employment cascade
    justice_involved = dynamic_state.justice_state.justice_involvement_flag
    unemployed = dynamic_state.econ_state.employment_status in (
        "unemployed",
        "NILF",
    )

    if justice_involved and unemployed:
        alert = {
            "alert_id": str(uuid4()),
            "person_uid": uid,
            "cascade_id": "justice_employment_cascade",
            "cascade_name": "Justice-Employment Cascade",
            "current_link_index": 0,
            "confidence": 0.55,
            "detected_at": now.isoformat(),
            "path_a_projected_cost": 180_000.0,
            "path_b_projected_cost": 60_000.0,
            "recommended_interventions": [
                "workforce_development",
                "transitional_employment",
                "legal_aid",
            ],
        }
        if alert["confidence"] >= req.min_confidence:
            alerts.append(alert)

    # Heuristic 3: High-cost chronic disease escalation
    chronic_count = len(dynamic_state.bio_state.chronic_conditions)
    if chronic_count >= 3 and high_healthcare:
        alert = {
            "alert_id": str(uuid4()),
            "person_uid": uid,
            "cascade_id": "chronic_disease_escalation",
            "cascade_name": "Chronic Disease Escalation",
            "current_link_index": 2,
            "confidence": 0.70,
            "detected_at": now.isoformat(),
            "path_a_projected_cost": 500_000.0,
            "path_b_projected_cost": 200_000.0,
            "recommended_interventions": [
                "chronic_care_management",
                "medication_therapy_management",
                "community_health_worker",
            ],
        }
        if alert["confidence"] >= req.min_confidence:
            alerts.append(alert)

    # Filter by cascade_ids if provided
    if req.cascade_ids:
        alerts = [a for a in alerts if a["cascade_id"] in req.cascade_ids]

    return alerts
