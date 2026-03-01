"""Person CRUD router for THE DOME API.

Provides endpoints to create and retrieve persons, and to ingest and
query their fiscal event history.  All person data is persisted in
``PersonTable`` as JSON blobs; fiscal events are stored in
``FiscalEventTable`` with relational foreign keys.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dome.db.database import get_session
from dome.db.tables import FiscalEventTable, PersonTable
from dome.models.budget_key import PersonBudgetKey
from dome.models.dome_metrics import DomeMetrics
from dome.models.dynamic_state import (
    DynamicState,
    EconState,
    EducationState,
    FamilyState,
    HousingState,
)
from dome.models.fiscal_event import FiscalEvent
from dome.models.identity import CrossSystemIds, IdentitySpine
from dome.models.person import Person
from dome.models.static_profile import StaticProfile
from dome.schemas.person_schemas import (
    FiscalEventCreateRequest,
    PersonCreateRequest,
)

logger = logging.getLogger("dome.api.persons")

router = APIRouter(prefix="/persons", tags=["persons"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_person_from_request(req: PersonCreateRequest) -> Person:
    """Construct a full ``Person`` domain model from the create request.

    Fills in default sub-models for fields that the caller did not provide
    (e.g. empty ``DomeMetrics``, default ``DynamicState`` sub-states).
    """
    now = datetime.now(tz=timezone.utc)

    # --- Identity spine ---
    identity_spine = IdentitySpine(
        ssn_hash=req.ssn_hash,
        name_hash=req.name_hash,
        dob=req.dob,
        sex_at_birth=req.sex_at_birth,
        address_history=[addr.model_dump() for addr in req.address_history]
        if req.address_history
        else [],
        cross_system_ids=CrossSystemIds(**req.cross_system_ids.model_dump()),
    )

    # --- Static profile ---
    # Derive tract FIPS from address history when not explicitly provided.
    birth_fips = req.birth_tract_fips or (
        req.address_history[0].tract_fips if req.address_history else "00000000000"
    )
    current_fips = req.current_tract_fips or (
        req.address_history[-1].tract_fips if req.address_history else "00000000000"
    )

    static_profile = StaticProfile(
        birth_tract_fips=birth_fips,
        current_tract_fips=current_fips,
        parental_income_quintile=req.parental_income_quintile,
        parental_education_level=req.parental_education_level,
        ace_score_estimate=req.ace_score_estimate,
        birth_weight_grams=req.birth_weight_grams,
        genetics_risk_flags=req.genetics_risk_flags,
    )

    # --- Dynamic state (with minimal defaults) ---
    age_years = (now.date() - req.dob).days / 365.25

    dynamic_state = DynamicState(
        timestamp=now,
        age_years=round(age_years, 2),
        econ_state=EconState(
            current_annual_income=req.current_annual_income,
            employment_status=req.employment_status,
        ),
        housing_state=HousingState(
            housing_status=req.housing_status,
        ),
        family_state=FamilyState(
            household_size=req.household_size,
            dependents_ages=req.dependents_ages,
        ),
        education_state=EducationState(
            highest_credential=req.highest_credential,
        ),
    )
    # Inject chronic conditions into bio_state
    dynamic_state.bio_state.chronic_conditions = req.chronic_conditions

    # --- DOME metrics (empty) ---
    dome_metrics = DomeMetrics()

    # --- Budget key ---
    budget_key = PersonBudgetKey(
        person_uid=req.person_uid,
        age=int(age_years),
        sex_at_birth=req.sex_at_birth,
        current_tract_fips=current_fips,
        household_size=req.household_size,
        dependents_ages=req.dependents_ages,
        current_annual_income=req.current_annual_income,
        employment_status=req.employment_status,
        educational_attainment=req.highest_credential,
        disability_flag=req.disability_flag,
        chronic_condition_flags=req.chronic_conditions,
        housing_status=req.housing_status,
    )

    return Person(
        person_uid=req.person_uid,
        identity_spine=identity_spine,
        static_profile=static_profile,
        dynamic_state=dynamic_state,
        dome_metrics=dome_metrics,
        fiscal_history=[],
        whole_person_budget_key=budget_key,
    )


async def _load_person_row(
    uid: str, session: AsyncSession
) -> PersonTable:
    """Load a ``PersonTable`` row by *person_uid*, raising 404 if absent."""
    stmt = select(PersonTable).where(PersonTable.person_uid == uid)
    result = await session.execute(stmt)
    row = result.scalar_one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Person {uid!r} not found")
    return row


def _deserialize_person(row: PersonTable) -> Person:
    """Reconstruct a ``Person`` domain model from a ``PersonTable`` row."""
    return Person(
        person_uid=row.person_uid,
        identity_spine=IdentitySpine(**(row.identity_spine_json or {})),
        static_profile=StaticProfile(**(row.static_profile_json or {})),
        dynamic_state=DynamicState(**(row.dynamic_state_json or {})),
        dome_metrics=DomeMetrics(**(row.dome_metrics_json or {})),
        fiscal_history=[],
        whole_person_budget_key=PersonBudgetKey(**(row.budget_key_json or {})),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post("/", status_code=201, summary="Create a new person")
async def create_person(
    req: PersonCreateRequest,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Create a new person record in THE DOME.

    Accepts a ``PersonCreateRequest`` payload, constructs the full domain
    model with sensible defaults for unspecified fields, and persists the
    person to the ``persons`` table as JSON blobs.

    Returns the ``person_uid`` of the newly created record.
    """
    # Check for duplicate
    existing = await session.execute(
        select(PersonTable).where(PersonTable.person_uid == req.person_uid)
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=400,
            detail=f"Person with uid {req.person_uid!r} already exists",
        )

    try:
        person = _build_person_from_request(req)
    except Exception as exc:
        logger.exception("Failed to build Person model from request")
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    row = PersonTable(
        person_uid=person.person_uid,
        identity_spine_json=person.identity_spine.model_dump(mode="json"),
        static_profile_json=person.static_profile.model_dump(mode="json"),
        dynamic_state_json=person.dynamic_state.model_dump(mode="json"),
        dome_metrics_json=person.dome_metrics.model_dump(mode="json"),
        budget_key_json=person.whole_person_budget_key.model_dump(mode="json"),
    )
    session.add(row)
    await session.flush()

    logger.info("Created person %s", person.person_uid)
    return {"person_uid": person.person_uid}


@router.get("/{uid}", summary="Get a person by UID")
async def get_person(
    uid: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Retrieve the full person record for *uid*.

    Loads the ``PersonTable`` row from the database, deserializes all JSON
    blobs back into their Pydantic domain models, and returns the complete
    ``Person`` object.
    """
    row = await _load_person_row(uid, session)
    person = _deserialize_person(row)

    # Attach stored budget / trajectory if available
    response = person.model_dump(mode="json")
    if row.budget_json:
        response["whole_person_budget"] = row.budget_json
    if row.trajectory_json:
        response["fiscal_trajectory_tag"] = row.trajectory_json

    return response


@router.post("/{uid}/fiscal-events", status_code=201, summary="Add fiscal events")
async def add_fiscal_events(
    uid: str,
    events: list[FiscalEventCreateRequest],
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Ingest a batch of fiscal events for person *uid*.

    Each ``FiscalEventCreateRequest`` is converted to a ``FiscalEvent``
    domain model (with a generated UUID), then persisted to the
    ``fiscal_events`` table.

    Returns the number of events successfully saved.
    """
    # Validate person exists
    await _load_person_row(uid, session)

    if not events:
        raise HTTPException(status_code=400, detail="No fiscal events provided")

    saved = 0
    for ev_req in events:
        event_id = str(uuid4())
        fe_row = FiscalEventTable(
            event_id=event_id,
            person_uid=uid,
            event_date=datetime.combine(ev_req.event_date, datetime.min.time()),
            payer_level=ev_req.payer_level,
            payer_entity=ev_req.payer_entity,
            program_or_fund=ev_req.program_or_fund,
            domain=ev_req.domain,
            mechanism=ev_req.mechanism,
            service_category=ev_req.service_category,
            utilization_unit=ev_req.utilization_unit,
            quantity=ev_req.quantity,
            amount_paid=ev_req.amount_paid,
            amount_type=ev_req.amount_type,
            confidence=ev_req.confidence,
            data_source_system=ev_req.data_source_system,
            attribution_tags_json=ev_req.attribution_tags,
        )
        session.add(fe_row)
        saved += 1

    await session.flush()
    logger.info("Saved %d fiscal events for person %s", saved, uid)
    return {"person_uid": uid, "events_saved": saved}


@router.get("/{uid}/fiscal-history", summary="Get fiscal history")
async def get_fiscal_history(
    uid: str,
    session: AsyncSession = Depends(get_session),
) -> list[dict]:
    """Retrieve all fiscal events for person *uid*.

    Loads every ``FiscalEventTable`` row linked to the person and returns
    them as a list of dictionaries ordered by event date.
    """
    # Validate person exists
    await _load_person_row(uid, session)

    stmt = (
        select(FiscalEventTable)
        .where(FiscalEventTable.person_uid == uid)
        .order_by(FiscalEventTable.event_date.asc())
    )
    result = await session.execute(stmt)
    rows = result.scalars().all()

    events = []
    for row in rows:
        events.append(
            {
                "event_id": row.event_id,
                "person_uid": row.person_uid,
                "event_date": row.event_date.isoformat() if row.event_date else None,
                "payer_level": row.payer_level,
                "payer_entity": row.payer_entity,
                "program_or_fund": row.program_or_fund,
                "domain": row.domain,
                "mechanism": row.mechanism,
                "service_category": row.service_category,
                "utilization_unit": row.utilization_unit,
                "quantity": row.quantity,
                "amount_paid": row.amount_paid,
                "amount_type": row.amount_type,
                "confidence": row.confidence,
                "data_source_system": row.data_source_system,
                "attribution_tags": row.attribution_tags_json or [],
            }
        )

    return events
