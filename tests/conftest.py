"""Shared pytest fixtures for THE DOME test suite."""

from __future__ import annotations

import json
import os
from datetime import date, datetime
from pathlib import Path
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

FIXTURES_DIR = Path(__file__).parent / "fixtures"

# ---------------------------------------------------------------------------
# Database fixtures (in-memory SQLite for speed)
# ---------------------------------------------------------------------------

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_engine():
    """Create a fresh in-memory SQLite engine per test."""
    engine = create_async_engine(TEST_DB_URL, echo=False)
    from dome.db.tables import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(async_engine) -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional DB session that rolls back after each test."""
    session_factory = async_sessionmaker(async_engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def app_client(async_engine) -> AsyncGenerator[AsyncClient, None]:
    """Provide an httpx AsyncClient wired to the FastAPI app with test DB."""
    from dome.main import app
    from dome.db.database import get_session

    session_factory = async_sessionmaker(async_engine, expire_on_commit=False)

    async def _override_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_session] = _override_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Fixture data loaders
# ---------------------------------------------------------------------------


@pytest.fixture
def trajectory_3_data() -> dict:
    """Maria — moderate net cost (trajectory 3)."""
    return json.loads((FIXTURES_DIR / "trajectory_3_person.json").read_text())


@pytest.fixture
def trajectory_4_data() -> dict:
    """James — high net cost (trajectory 4)."""
    return json.loads((FIXTURES_DIR / "trajectory_4_person.json").read_text())


@pytest.fixture
def trajectory_1_data() -> dict:
    """Sarah — net contributor (trajectory 1)."""
    return json.loads((FIXTURES_DIR / "trajectory_1_person.json").read_text())


# ---------------------------------------------------------------------------
# Model instance fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_eligibility_snapshot() -> dict:
    return {
        "medicaid": True, "medicare": False, "marketplace_subsidy": True,
        "snap": True, "tanf": False, "housing_assistance": True,
        "ssi": False, "ssdi": False, "unemployment_insurance": True,
        "wioa": True, "va_benefits": False,
    }


@pytest.fixture
def sample_enrollment_snapshot() -> dict:
    return {
        "medicaid": True, "medicare": False, "marketplace_subsidy": False,
        "snap": True, "tanf": False, "housing_assistance": False,
        "ssi": False, "ssdi": False, "unemployment_insurance": False,
        "wioa": False, "va_benefits": False,
    }


@pytest.fixture
def sample_budget_key(sample_eligibility_snapshot, sample_enrollment_snapshot) -> dict:
    """A PersonBudgetKey dict for Maria (trajectory 3)."""
    return {
        "person_uid": "dome-maria-034",
        "age": 34,
        "sex_at_birth": "female",
        "current_tract_fips": "42101002500",
        "household_size": 3,
        "dependents_ages": [6, 4],
        "current_annual_income": 24000.0,
        "income_volatility_score": 0.65,
        "employment_status": "gig",
        "occupation_code": "45-2011",
        "educational_attainment": "some_college",
        "disability_flag": False,
        "chronic_condition_flags": ["pre_diabetes", "hypertension_stage1"],
        "high_need_flag": False,
        "housing_status": "cost_burdened",
        "homelessness_history_flag": False,
        "area_deprivation_index": 72.0,
        "justice_involvement_flag": False,
        "past_12m_jail_days": 0,
        "past_12m_prison_days": 0,
        "past_12m_police_contacts": 0,
        "eligibility_snapshot": sample_eligibility_snapshot,
        "enrollment_snapshot": sample_enrollment_snapshot,
        "budget_horizons": [
            {"label": "1y", "start_date": "2026-01-01", "end_date": "2027-01-01", "time_step": "year"},
            {"label": "lifetime", "start_date": "2026-01-01", "end_date": "2072-01-01", "time_step": "year"},
        ],
    }


@pytest.fixture
def sample_fiscal_events() -> list[dict]:
    """A few fiscal events for Maria."""
    return [
        {
            "event_id": "evt-test-001",
            "person_uid": "dome-maria-034",
            "event_date": "2025-03-10",
            "payer_level": "federal",
            "payer_entity": "CMS-Medicaid",
            "program_or_fund": "Medicaid",
            "domain": "healthcare",
            "mechanism": "service_utilization",
            "service_category": "outpatient_visit",
            "utilization_unit": "visit",
            "quantity": 4.0,
            "amount_paid": 1400.0,
            "amount_type": "actual_claim",
            "confidence": 0.95,
            "data_source_system": "state_medicaid",
            "attribution_tags": ["primary_care"],
        },
        {
            "event_id": "evt-test-002",
            "person_uid": "dome-maria-034",
            "event_date": "2025-06-22",
            "payer_level": "federal",
            "payer_entity": "CMS-Medicaid",
            "program_or_fund": "Medicaid",
            "domain": "healthcare",
            "mechanism": "service_utilization",
            "service_category": "er_visit",
            "utilization_unit": "visit",
            "quantity": 1.0,
            "amount_paid": 2200.0,
            "amount_type": "actual_claim",
            "confidence": 0.95,
            "data_source_system": "state_medicaid",
            "attribution_tags": ["anxiety_episode"],
        },
    ]
