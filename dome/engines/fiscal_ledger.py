"""Fiscal ledger engine for THE DOME (Step 2).

Transforms raw claim and benefit data from disparate source systems into
standardised ``FiscalEvent`` records, deduplicates them, and provides
aggregation primitives for the Whole-Person Budget engine.

The ledger applies program-level metadata (payer level, domain, mechanism)
using a program lookup table and fills in missing dollar amounts via
published unit costs from ``dome.data.unit_costs``.

Usage::

    ledger = FiscalLedger()
    events = ledger.populate_from_claims("person-123", raw_claims)
    summary = ledger.summarize(events, group_by=["domain", "payer_level"])
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from datetime import date
from typing import Any, Sequence
from uuid import uuid4


# ---------------------------------------------------------------------------
# Program metadata lookup
# ---------------------------------------------------------------------------

# Maps program_or_fund key -> (payer_level, domain, mechanism, default_service_category, utilization_unit)
# This provides fallback classification when the raw claim does not specify them.
_PROGRAM_LOOKUP: dict[str, tuple[str, str, str, str, str]] = {
    # Healthcare
    "medicaid": ("state", "healthcare", "service_utilization", "general_medical", "claim"),
    "medicare": ("federal", "healthcare", "service_utilization", "general_medical", "claim"),
    "chip": ("state", "healthcare", "service_utilization", "pediatric", "claim"),
    "va_health": ("federal", "healthcare", "service_utilization", "veteran_care", "visit"),
    "marketplace_aca": ("federal", "healthcare", "service_utilization", "general_medical", "claim"),
    "ryan_white": ("federal", "healthcare", "service_utilization", "hiv_aids", "visit"),
    "samhsa_grant": ("federal", "healthcare", "service_utilization", "behavioral_health", "session"),
    "community_health_center": ("federal", "healthcare", "service_utilization", "primary_care", "visit"),
    # Income support
    "snap": ("federal", "food", "in_kind_benefit", "food_assistance", "month"),
    "wic": ("federal", "food", "in_kind_benefit", "nutrition_supplement", "month"),
    "tanf": ("federal", "income_support", "cash_transfer", "cash_assistance", "month"),
    "ssi": ("federal", "income_support", "cash_transfer", "disability_income", "month"),
    "ssdi": ("federal", "income_support", "cash_transfer", "disability_income", "month"),
    "eitc": ("federal", "income_support", "tax_expenditure", "tax_credit", "year"),
    "ctc": ("federal", "income_support", "tax_expenditure", "tax_credit", "year"),
    "unemployment_insurance": ("state", "income_support", "cash_transfer", "unemployment_benefit", "week"),
    "general_assistance": ("local", "income_support", "cash_transfer", "general_relief", "month"),
    # Housing
    "section_8_hcv": ("federal", "housing", "in_kind_benefit", "rental_assistance", "month"),
    "public_housing": ("federal", "housing", "in_kind_benefit", "public_housing_unit", "month"),
    "permanent_supportive_housing": ("local", "housing", "in_kind_benefit", "psh", "month"),
    "rapid_rehousing": ("local", "housing", "in_kind_benefit", "rapid_rehousing", "episode"),
    "emergency_shelter": ("local", "housing", "in_kind_benefit", "shelter", "night"),
    "liheap": ("federal", "housing", "in_kind_benefit", "energy_assistance", "year"),
    # Justice
    "county_jail": ("local", "justice", "service_utilization", "incarceration", "bed_day"),
    "state_prison": ("state", "justice", "service_utilization", "incarceration", "bed_day"),
    "federal_prison": ("federal", "justice", "service_utilization", "incarceration", "bed_day"),
    "probation": ("local", "justice", "service_utilization", "community_supervision", "month"),
    "parole": ("state", "justice", "service_utilization", "community_supervision", "month"),
    "drug_court": ("local", "justice", "service_utilization", "specialty_court", "episode"),
    "juvenile_detention": ("local", "justice", "service_utilization", "juvenile_incarceration", "bed_day"),
    # Education
    "k12_public": ("local", "education", "service_utilization", "k12_enrollment", "year"),
    "special_education": ("local", "education", "service_utilization", "special_ed", "year"),
    "head_start": ("federal", "education", "service_utilization", "early_childhood", "year"),
    "pell_grant": ("federal", "education", "cash_transfer", "higher_ed_aid", "year"),
    "job_corps": ("federal", "education", "service_utilization", "workforce_training", "year"),
    "vocational_rehab": ("state", "education", "service_utilization", "voc_rehab", "case"),
    # Child welfare
    "foster_care": ("state", "child_family", "service_utilization", "foster_placement", "month"),
    "adoption_assistance": ("state", "child_family", "cash_transfer", "adoption_subsidy", "year"),
    "child_care_subsidy": ("federal", "child_family", "in_kind_benefit", "child_care", "year"),
}

# Maps service_category to unit_cost key for fallback cost estimation
_SERVICE_TO_COST_KEY: dict[str, str] = {
    # Healthcare
    "er_visit": "er_visit",
    "emergency_room": "er_visit",
    "inpatient": "inpatient_day",
    "inpatient_day": "inpatient_day",
    "icu": "icu_day",
    "icu_day": "icu_day",
    "nursing_home": "nursing_home_day",
    "home_health": "home_health_visit",
    "outpatient": "outpatient_visit",
    "outpatient_visit": "outpatient_visit",
    "mental_health": "mental_health_session",
    "mental_health_session": "mental_health_session",
    "substance_abuse": "substance_abuse_treatment_day",
    "substance_abuse_treatment": "substance_abuse_treatment_day",
    "pharmacy": "prescription_monthly",
    "prescription": "prescription_monthly",
    "dental": "dental_visit",
    "vision": "vision_exam",
    "dme": "dme_monthly",
    "ambulance": "ambulance_transport",
    # Justice
    "incarceration": "jail_day",
    "jail": "jail_day",
    "prison": "prison_day",
    "community_supervision": "probation_annual",
    "specialty_court": "drug_court_episode",
    "juvenile_incarceration": "juvenile_detention_day",
    # Housing
    "shelter": "shelter_night",
    "rental_assistance": "section_8_voucher_annual",
    "public_housing_unit": "public_housing_unit_annual",
    "psh": "permanent_supportive_housing_annual",
    "rapid_rehousing": "rapid_rehousing_episode",
    "energy_assistance": "liheap_average_benefit",
    # Income support
    "food_assistance": "snap_per_person_monthly",
    "nutrition_supplement": "wic_per_person_annual",
    "cash_assistance": "tanf_annual",
    "disability_income": "ssdi_annual",
    "unemployment_benefit": "unemployment_insurance_weekly",
    # Education
    "k12_enrollment": "k12_per_pupil_annual",
    "special_ed": "special_ed_additional_annual",
    "early_childhood": "head_start_per_child_annual",
    "higher_ed_aid": "pell_grant_average",
    "workforce_training": "job_corps_per_participant_annual",
    "voc_rehab": "vocational_rehab_per_case",
    # Child welfare
    "foster_placement": "foster_care_monthly",
    "adoption_subsidy": "adoption_assistance_annual",
    "child_care": "child_care_subsidy_annual",
}


def _load_unit_costs() -> dict[str, float]:
    """Load unit costs from dome.data, falling back to an empty dict."""
    try:
        from dome.data.unit_costs import UNIT_COSTS
        return dict(UNIT_COSTS)
    except ImportError:
        return {}


class FiscalLedger:
    """Fiscal ledger engine that standardises raw claims into FiscalEvents.

    The ledger performs three key functions:

    1. **Mapping**: Translates raw claim fields into the FiscalEvent schema,
       applying program-level metadata defaults for payer_level, domain,
       mechanism, and service_category.

    2. **Cost estimation**: When a raw claim lacks an ``amount`` field, the
       ledger estimates cost by multiplying ``quantity`` by the relevant
       unit cost from ``dome.data.unit_costs``.

    3. **Deduplication**: Events are deduplicated by ``event_id`` so that
       the same claim ingested from multiple systems is counted only once.
    """

    def __init__(self) -> None:
        self._unit_costs = _load_unit_costs()

    # ------------------------------------------------------------------ #
    #  Core: populate_from_claims
    # ------------------------------------------------------------------ #

    def populate_from_claims(
        self,
        person_uid: str,
        raw_claims: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Convert raw claim dicts into standardised FiscalEvent dicts.

        Parameters
        ----------
        person_uid:
            Unique person identifier to stamp on every event.
        raw_claims:
            List of dicts with at least ``event_date`` and
            ``program_or_fund`` (or ``program``).  Additional optional
            fields: ``amount``, ``quantity``, ``service_category``,
            ``payer_level``, ``domain``, ``mechanism``,
            ``utilization_unit``, ``payer_entity``, ``data_source_system``,
            ``confidence``, ``attribution_tags``, ``event_id``.

        Returns
        -------
        list[dict]:
            Deduplicated FiscalEvent-compatible dicts, sorted by
            event_date ascending.
        """
        events: list[dict[str, Any]] = []

        for claim in raw_claims:
            event = self._map_single_claim(person_uid, claim)
            if event is not None:
                events.append(event)

        # Deduplicate by event_id (keep first occurrence)
        events = self._deduplicate(events)

        # Sort chronologically
        events.sort(key=lambda e: e["event_date"])

        return events

    def _map_single_claim(
        self,
        person_uid: str,
        claim: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Map a single raw claim dict to a FiscalEvent-compatible dict.

        Returns None if the claim is unparseable (missing date).
        """
        # Parse event date
        raw_date = claim.get("event_date") or claim.get("date") or claim.get("service_date")
        if raw_date is None:
            return None

        if isinstance(raw_date, str):
            try:
                event_date = date.fromisoformat(raw_date)
            except ValueError:
                return None
        elif isinstance(raw_date, date):
            event_date = raw_date
        else:
            return None

        # Resolve program key
        program = (
            claim.get("program_or_fund")
            or claim.get("program")
            or claim.get("fund")
            or "unknown"
        )
        program_key = program.lower().replace(" ", "_").replace("-", "_")

        # Lookup program metadata with fallbacks
        lookup = _PROGRAM_LOOKUP.get(program_key)
        if lookup:
            default_payer, default_domain, default_mechanism, default_svc_cat, default_unit = lookup
        else:
            default_payer = "federal"
            default_domain = "other"
            default_mechanism = "service_utilization"
            default_svc_cat = "unclassified"
            default_unit = "claim"

        payer_level = claim.get("payer_level", default_payer)
        domain = claim.get("domain", default_domain)
        mechanism = claim.get("mechanism", default_mechanism)
        service_category = claim.get("service_category", default_svc_cat)
        utilization_unit = claim.get("utilization_unit", default_unit)
        payer_entity = claim.get("payer_entity", program)

        # Quantity
        quantity = claim.get("quantity")
        if quantity is not None:
            try:
                quantity = float(quantity)
            except (ValueError, TypeError):
                quantity = None

        # Amount: use provided amount, or estimate from unit costs
        raw_amount = claim.get("amount") or claim.get("amount_paid")
        amount_type: str

        if raw_amount is not None:
            try:
                amount_paid = float(raw_amount)
                amount_type = "actual_claim"
            except (ValueError, TypeError):
                amount_paid = 0.0
                amount_type = "estimated_unit_cost"
        else:
            # Estimate from unit costs
            amount_paid = self._estimate_cost(service_category, utilization_unit, quantity)
            amount_type = "estimated_unit_cost"

        # Confidence
        confidence = claim.get("confidence")
        if confidence is not None:
            try:
                confidence = min(max(float(confidence), 0.0), 1.0)
            except (ValueError, TypeError):
                confidence = 0.5
        else:
            confidence = 1.0 if amount_type == "actual_claim" else 0.7

        # Event ID: use provided or generate deterministic hash
        event_id = claim.get("event_id")
        if not event_id:
            event_id = self._generate_event_id(
                person_uid, event_date, program, service_category, amount_paid, claim,
            )

        data_source = (
            claim.get("data_source_system")
            or claim.get("data_source")
            or claim.get("source_system")
            or "unknown"
        )

        attribution_tags = claim.get("attribution_tags", [])
        if isinstance(attribution_tags, str):
            attribution_tags = [attribution_tags]

        return {
            "event_id": event_id,
            "person_uid": person_uid,
            "event_date": event_date.isoformat() if isinstance(event_date, date) else str(event_date),
            "payer_level": payer_level,
            "payer_entity": payer_entity,
            "program_or_fund": program,
            "domain": domain,
            "mechanism": mechanism,
            "service_category": service_category,
            "utilization_unit": utilization_unit,
            "quantity": quantity,
            "amount_paid": round(amount_paid, 2),
            "amount_type": amount_type,
            "confidence": round(confidence, 4),
            "data_source_system": data_source,
            "attribution_tags": attribution_tags,
        }

    # ------------------------------------------------------------------ #
    #  Cost estimation
    # ------------------------------------------------------------------ #

    def _estimate_cost(
        self,
        service_category: str,
        utilization_unit: str,
        quantity: float | None,
    ) -> float:
        """Estimate dollar cost from unit costs when no amount is provided.

        Strategy:
        1. Look up service_category in the service-to-cost-key mapping.
        2. Find the matching unit cost from the loaded UNIT_COSTS table.
        3. Multiply by quantity (default 1 if quantity is missing).
        """
        cost_key = _SERVICE_TO_COST_KEY.get(service_category)
        if cost_key is None:
            # Try service_category directly as a unit cost key
            cost_key = service_category

        unit_cost = self._unit_costs.get(cost_key, 0.0)

        if unit_cost == 0.0:
            # Try the utilization_unit as a fallback key
            unit_cost = self._unit_costs.get(utilization_unit, 0.0)

        effective_qty = quantity if quantity is not None and quantity > 0 else 1.0

        return unit_cost * effective_qty

    # ------------------------------------------------------------------ #
    #  Deduplication
    # ------------------------------------------------------------------ #

    @staticmethod
    def _deduplicate(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Deduplicate events by event_id, keeping the first occurrence."""
        seen: set[str] = set()
        unique: list[dict[str, Any]] = []
        for event in events:
            eid = event.get("event_id", "")
            if eid not in seen:
                seen.add(eid)
                unique.append(event)
        return unique

    # ------------------------------------------------------------------ #
    #  Deterministic event ID generation
    # ------------------------------------------------------------------ #

    @staticmethod
    def _generate_event_id(
        person_uid: str,
        event_date: date,
        program: str,
        service_category: str,
        amount: float,
        claim: dict[str, Any],
    ) -> str:
        """Generate a deterministic event ID from claim attributes.

        Uses SHA-256 of the claim's distinguishing fields so that the
        same logical event ingested from two systems yields the same
        event_id and is properly deduplicated.
        """
        # Include a claim-specific discriminator if available
        discriminator = claim.get("claim_id") or claim.get("record_id") or ""
        payload = (
            f"{person_uid}|{event_date.isoformat()}|{program}|"
            f"{service_category}|{amount:.2f}|{discriminator}"
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]

    # ------------------------------------------------------------------ #
    #  Aggregation / summarization
    # ------------------------------------------------------------------ #

    def summarize(
        self,
        events: list[dict[str, Any]],
        group_by: str | Sequence[str] = "domain",
    ) -> dict[str, Any]:
        """Aggregate fiscal events into spending summaries.

        Parameters
        ----------
        events:
            List of FiscalEvent-compatible dicts (as returned by
            ``populate_from_claims``).
        group_by:
            Field name(s) to group by.  Can be a single string or a
            sequence of strings for multi-level grouping.  Valid fields
            include ``domain``, ``payer_level``, ``mechanism``,
            ``program_or_fund``, ``service_category``, ``amount_type``.

        Returns
        -------
        dict with structure::

            {
                "total_spend": float,
                "event_count": int,
                "by_group": {
                    "<group_key>": {
                        "total_spend": float,
                        "event_count": int,
                        "avg_per_event": float,
                        "pct_of_total": float,
                    },
                    ...
                },
                "date_range": {"min": str, "max": str},
                "confidence_weighted_spend": float,
            }
        """
        if isinstance(group_by, str):
            group_keys = [group_by]
        else:
            group_keys = list(group_by)

        # Overall totals
        total_spend = 0.0
        confidence_weighted = 0.0
        event_count = len(events)
        dates: list[str] = []

        # Per-group accumulators
        group_spend: dict[str, float] = defaultdict(float)
        group_count: dict[str, int] = defaultdict(int)

        for event in events:
            amount = float(event.get("amount_paid", 0.0))
            conf = float(event.get("confidence", 1.0))
            total_spend += amount
            confidence_weighted += amount * conf

            d = event.get("event_date")
            if d:
                dates.append(str(d))

            # Build composite group key
            key_parts = []
            for gk in group_keys:
                key_parts.append(str(event.get(gk, "unknown")))
            composite_key = " | ".join(key_parts)

            group_spend[composite_key] += amount
            group_count[composite_key] += 1

        # Build group summaries
        by_group: dict[str, dict[str, Any]] = {}
        for key in sorted(group_spend.keys()):
            spend = group_spend[key]
            count = group_count[key]
            by_group[key] = {
                "total_spend": round(spend, 2),
                "event_count": count,
                "avg_per_event": round(spend / count, 2) if count > 0 else 0.0,
                "pct_of_total": round(spend / total_spend * 100, 2) if total_spend > 0 else 0.0,
            }

        # Date range
        sorted_dates = sorted(dates) if dates else []
        date_range = {
            "min": sorted_dates[0] if sorted_dates else None,
            "max": sorted_dates[-1] if sorted_dates else None,
        }

        return {
            "total_spend": round(total_spend, 2),
            "event_count": event_count,
            "by_group": by_group,
            "date_range": date_range,
            "confidence_weighted_spend": round(confidence_weighted, 2),
        }
