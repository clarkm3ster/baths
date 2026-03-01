"""Tests for identity models."""

from datetime import date

import pytest

from dome.models.identity import AddressEntry, CrossSystemIds, IdentitySpine


class TestAddressEntry:
    def test_valid_address(self):
        addr = AddressEntry(
            street_hash="abc123",
            city="Philadelphia",
            state="PA",
            zip5="19134",
            tract_fips="42101002500",
            start_date=date(2020, 1, 1),
        )
        assert addr.city == "Philadelphia"
        assert addr.end_date is None

    def test_address_with_end_date(self):
        addr = AddressEntry(
            street_hash="abc123",
            city="Chicago",
            state="IL",
            zip5="60612",
            tract_fips="17031839100",
            start_date=date(2020, 1, 1),
            end_date=date(2022, 6, 30),
        )
        assert addr.end_date == date(2022, 6, 30)


class TestCrossSystemIds:
    def test_defaults_to_none(self):
        ids = CrossSystemIds()
        assert ids.medicaid_id is None
        assert ids.va_id is None
        assert ids.court_case_ids == []

    def test_partial_ids(self):
        ids = CrossSystemIds(medicaid_id="MC-123", snap_case_id="SNAP-456")
        assert ids.medicaid_id == "MC-123"
        assert ids.snap_case_id == "SNAP-456"
        assert ids.medicare_id is None


class TestIdentitySpine:
    def test_minimal_spine(self):
        spine = IdentitySpine(
            name_hash="hash123",
            dob=date(1990, 5, 15),
            sex_at_birth="female",
            address_history=[],
            cross_system_ids=CrossSystemIds(),
            linkage_confidence_by_system={},
        )
        assert spine.ssn_hash is None
        assert spine.sex_at_birth == "female"

    def test_full_spine(self):
        spine = IdentitySpine(
            ssn_hash="sha256_ssn",
            name_hash="hash456",
            dob=date(1985, 12, 1),
            sex_at_birth="male",
            address_history=[
                AddressEntry(
                    street_hash="st_hash",
                    city="Austin",
                    state="TX",
                    zip5="78704",
                    tract_fips="48453001702",
                    start_date=date(2022, 1, 1),
                ),
            ],
            cross_system_ids=CrossSystemIds(
                medicare_id="MCR-789",
                medicaid_id="MCD-012",
            ),
            linkage_confidence_by_system={"medicare": 0.95, "medicaid": 0.92},
        )
        assert len(spine.address_history) == 1
        assert spine.linkage_confidence_by_system["medicare"] == 0.95
