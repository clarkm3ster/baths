"""Tests for the persons API endpoints."""

import pytest
import pytest_asyncio
from httpx import AsyncClient


class TestPersonsAPI:
    @pytest.mark.asyncio
    async def test_create_person(self, app_client: AsyncClient):
        response = await app_client.post(
            "/api/v1/persons/",
            json={
                "person_uid": "test-api-001",
                "name_hash": "testhash123",
                "dob": "1990-05-15",
                "sex_at_birth": "female",
                "employment_status": "FT",
                "current_annual_income": 50000,
                "housing_status": "stable",
                "household_size": 1,
                "highest_credential": "BA",
            },
        )
        assert response.status_code in (200, 201)
        data = response.json()
        assert data["person_uid"] == "test-api-001"

    @pytest.mark.asyncio
    async def test_get_person(self, app_client: AsyncClient):
        # Create first
        await app_client.post(
            "/api/v1/persons/",
            json={
                "person_uid": "test-api-002",
                "name_hash": "testhash456",
                "dob": "1985-12-01",
                "sex_at_birth": "male",
                "employment_status": "FT",
                "housing_status": "stable",
                "household_size": 1,
                "highest_credential": "HS",
            },
        )
        response = await app_client.get("/api/v1/persons/test-api-002")
        assert response.status_code == 200
        data = response.json()
        assert data["person_uid"] == "test-api-002"

    @pytest.mark.asyncio
    async def test_get_nonexistent_person(self, app_client: AsyncClient):
        response = await app_client.get("/api/v1/persons/nonexistent-999")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_add_fiscal_events(self, app_client: AsyncClient):
        # Create person first
        await app_client.post(
            "/api/v1/persons/",
            json={
                "person_uid": "test-api-003",
                "name_hash": "testhash789",
                "dob": "1992-03-15",
                "sex_at_birth": "female",
                "employment_status": "gig",
                "housing_status": "cost_burdened",
                "household_size": 3,
                "dependents_ages": [6, 4],
                "highest_credential": "some_college",
            },
        )
        response = await app_client.post(
            "/api/v1/persons/test-api-003/fiscal-events",
            json=[
                {
                    "event_date": "2025-03-10",
                    "payer_level": "federal",
                    "payer_entity": "CMS-Medicaid",
                    "program_or_fund": "Medicaid",
                    "domain": "healthcare",
                    "mechanism": "service_utilization",
                    "service_category": "er_visit",
                    "utilization_unit": "visit",
                    "quantity": 1.0,
                    "amount_paid": 2200.0,
                },
            ],
        )
        assert response.status_code in (200, 201)

    @pytest.mark.asyncio
    async def test_health_endpoint(self, app_client: AsyncClient):
        response = await app_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
