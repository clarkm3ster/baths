"""Core matching engine for DOMES.

Given a PersonProfile and a list of provision dicts (rows from the DB), this
module scores every provision for relevance, explains *why* it matched, and
returns a sorted list of MatchResult objects.
"""

from __future__ import annotations

import json
from typing import Any

from app.circumstances import AGE_EXPANSIONS, MatchResult, PersonProfile

# Provision-type weights: direct rights matter most.
_TYPE_WEIGHT: dict[str, float] = {
    "right": 1.0,
    "protection": 0.95,
    "obligation": 0.90,
    "enforcement": 0.85,
}

# Domain display order (stable secondary sort).
_DOMAIN_ORDER: dict[str, int] = {
    "health": 0,
    "civil_rights": 1,
    "housing": 2,
    "income": 3,
    "education": 4,
    "justice": 5,
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_applies_when(raw: str | dict) -> dict[str, list[str]]:
    """Safely parse the applies_when column (stored as JSON text)."""
    if isinstance(raw, dict):
        return raw
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return parsed
    except (json.JSONDecodeError, TypeError):
        pass
    return {}


def _parse_json_list(raw: str | list) -> list[str]:
    if isinstance(raw, list):
        return raw
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return [str(x) for x in parsed]
    except (json.JSONDecodeError, TypeError):
        pass
    return []


def _profile_field(profile: PersonProfile, key: str) -> list[str]:
    """Return the profile values relevant to a given applies_when key.

    This function bridges the gap between the profile model's field names and
    the diverse condition keys used in the seed data's ``applies_when`` JSON.
    """
    if key == "insurance":
        vals = list(profile.insurance)
        # Map "uninsured" to "none" which seed data uses
        if "uninsured" in vals:
            vals.append("none")
        # "medicaid" also implies "medicaid_managed_care" for broader matching
        if "medicaid" in vals:
            vals.append("medicaid_managed_care")
        return vals

    if key in ("disability", "disabilities"):
        vals = list(profile.disabilities)
        # Map profile values to seed data vocabulary
        expansions: dict[str, list[str]] = {
            "mental_health": ["mental_health", "mental"],
            "idd": ["idd", "intellectual", "developmental", "developmental_delay"],
            "physical": ["physical"],
            "sud": ["sud", "substance_use"],
            "chronic_illness": ["chronic_illness"],
        }
        expanded: list[str] = []
        for d in vals:
            expanded.extend(expansions.get(d, [d]))
        return expanded

    if key in ("age", "age_group"):
        if not profile.age_group:
            vals = []
        else:
            vals = list(AGE_EXPANSIONS.get(profile.age_group, [profile.age_group]))
        # Add additional age aliases used by seed data
        age_aliases: dict[str, list[str]] = {
            "under_18": ["under_19", "under_21", "under_26", "under_65",
                         "school_age", "3_to_21", "birth_to_21"],
            "18_to_21": ["under_21", "under_26", "under_65", "school_age",
                         "3_to_21", "birth_to_21"],
            "22_to_64": ["adult", "under_65", "19_to_64"],
            "65_plus": ["adult", "elderly", "65_or_older"],
        }
        if profile.age_group:
            vals.extend(age_aliases.get(profile.age_group, []))
        if profile.pregnant:
            vals.extend(["pregnant", "childbearing"])
        return list(dict.fromkeys(vals))  # deduplicate preserving order

    if key == "housing":
        return profile.housing

    if key in ("income", "income_level"):
        vals = list(profile.income)
        # Map profile income values to seed data income_level vocabulary
        if "below_poverty" in vals:
            vals.extend([
                "below_130_fpl", "below_133_fpl", "below_138_fpl",
                "below_150_fpl", "low_income", "below_ssi_limit",
                "below_50_ami", "below_30_ami", "cannot_afford_attorney",
            ])
        if "unemployed" in vals:
            vals.extend(["low_income", "cannot_afford_attorney"])
        if "ssi" in vals or "ssdi" in vals or "tanf" in vals:
            vals.append("low_income")
        return list(dict.fromkeys(vals))

    if key == "benefits":
        # Map income list items that are benefits
        return [v for v in profile.income if v in ("ssi", "ssdi", "snap", "tanf")]

    if key == "system_involvement":
        return profile.system_involvement

    if key == "background":
        # Map profile fields to seed data "background" values
        vals: list[str] = []
        if profile.dv_survivor:
            vals.extend(["domestic_violence_survivor", "sexual_assault_survivor"])
        if "incarcerated" in profile.system_involvement:
            vals.append("incarcerated")
        if "recently_released" in profile.system_involvement:
            vals.extend(["formerly_incarcerated", "criminal_record"])
        if "probation" in profile.system_involvement:
            vals.append("criminal_record")
        if "foster_care" in profile.system_involvement:
            vals.append("former_foster_care")
        return vals

    if key == "condition":
        # Map disabilities to "condition" vocabulary used in seed data
        vals: list[str] = []
        if "mental_health" in profile.disabilities:
            vals.extend(["mental_health", "suicide_risk"])
        if "sud" in profile.disabilities:
            vals.append("substance_use")
        if "chronic_illness" in profile.disabilities:
            vals.extend(["any_preexisting", "serious_medical_condition"])
        if profile.disabilities:
            vals.append("any_preexisting")
        return vals

    if key == "setting":
        # Infer settings from the person's circumstances
        vals: list[str] = []
        if profile.housing:
            vals.extend(["housing", "rental"])
        if "public_housing" in profile.housing or "section_8" in profile.housing:
            vals.append("federally_funded")
        if "incarcerated" in profile.system_involvement:
            vals.extend(["prison", "jail", "correctional_facility"])
        if "juvenile_justice" in profile.system_involvement:
            vals.append("juvenile_facility")
        if profile.age_group in ("under_18", "18_to_21"):
            vals.append("school")
        if profile.insurance:
            vals.extend(["healthcare_facility", "insurance", "health_plan"])
        if "medicaid" in profile.insurance or "medicare" in profile.insurance:
            vals.extend(["federally_funded", "government", "public_program"])
        if profile.disabilities:
            vals.extend(["government", "public_program", "public_accommodation"])
        return list(dict.fromkeys(vals))

    if key == "situation":
        vals: list[str] = []
        if "incarcerated" in profile.system_involvement:
            vals.extend(["criminal_charges", "pretrial"])
        if "recently_released" in profile.system_involvement:
            vals.extend(["reentry", "approaching_release"])
        return vals

    if key == "employment":
        # Not directly modeled, but can infer from income
        vals: list[str] = []
        if "below_poverty" in profile.income and "unemployed" not in profile.income:
            vals.append("employed")
        if "unemployed" in profile.income:
            vals.append("seeking_employment")
        return vals

    if key == "household":
        # Limited inference
        vals: list[str] = []
        if profile.pregnant:
            vals.append("pregnant")
        return vals

    if key == "pregnant":
        return ["pregnant"] if profile.pregnant else []
    if key == "veteran":
        return ["veteran"] if profile.veteran else []
    if key == "dv_survivor":
        return ["dv_survivor"] if profile.dv_survivor else []
    if key == "immigrant":
        return ["immigrant"] if profile.immigrant else []
    if key == "lgbtq":
        return ["lgbtq"] if profile.lgbtq else []
    if key == "rural":
        return ["rural"] if profile.rural else []
    if key == "state":
        return [profile.state] if profile.state else []
    return []


def _condition_matches(
    profile: PersonProfile,
    key: str,
    required_values: list[str],
) -> tuple[bool, str]:
    """Check whether the profile satisfies a single applies_when condition.

    Returns ``(matched: bool, reason: str)``.
    """
    profile_values = _profile_field(profile, key)

    # "any" means the person just needs *something* in this field
    if "any" in required_values:
        if profile_values:
            return True, f"Has {key}: {', '.join(profile_values)}"
        return False, ""

    overlap = set(profile_values) & set(required_values)
    if overlap:
        return True, f"Matches {key}: {', '.join(sorted(overlap))}"
    return False, ""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def match_provisions(
    profile: PersonProfile,
    provisions: list[dict[str, Any]],
) -> list[MatchResult]:
    """Score and rank every provision against the person's profile.

    Scoring rules
    -------------
    * If ``applies_when`` is empty the provision is universal (score 0.4).
    * Otherwise we count how many condition keys match vs total keys.
      - All match  -> base 1.0
      - Most match -> base 0.8
      - Some match -> base 0.6
      - One match  -> base 0.5
    * The base is then scaled slightly by provision_type weight.
    """
    results: list[MatchResult] = []

    for prov in provisions:
        conditions = _parse_applies_when(prov.get("applies_when", "{}"))
        enforcement = _parse_json_list(prov.get("enforcement_mechanisms", "[]"))
        prov_type: str = prov.get("provision_type", "right")
        domain: str = prov.get("domain", "")

        reasons: list[str] = []

        # --- Universal provision (empty conditions) ---
        if not conditions:
            reasons.append("Universal provision that applies to everyone")
            base_score = 0.4
        else:
            total_keys = len(conditions)
            matched_keys = 0

            for key, required_values in conditions.items():
                if not isinstance(required_values, list):
                    required_values = [str(required_values)]
                hit, reason = _condition_matches(profile, key, required_values)
                if hit:
                    matched_keys += 1
                    reasons.append(reason)

            if matched_keys == 0:
                continue  # provision does not apply at all

            ratio = matched_keys / total_keys
            if ratio >= 1.0:
                base_score = 1.0
            elif ratio >= 0.75:
                base_score = 0.8
            elif ratio >= 0.5:
                base_score = 0.6
            else:
                base_score = 0.5

        # Slight adjustment by provision type
        type_weight = _TYPE_WEIGHT.get(prov_type, 0.9)
        relevance = round(min(base_score * type_weight, 1.0), 2)

        results.append(
            MatchResult(
                provision_id=prov.get("id", 0),
                citation=prov.get("citation", ""),
                title=prov.get("title", ""),
                domain=domain,
                provision_type=prov_type,
                relevance_score=relevance,
                match_reasons=reasons,
                enforcement_steps=enforcement,
                full_text=prov.get("full_text", ""),
                source_url=prov.get("source_url", ""),
                cross_references=_parse_json_list(prov.get("cross_references", "[]")),
            )
        )

    # Sort: highest relevance first, then by domain order
    results.sort(
        key=lambda r: (
            -r.relevance_score,
            _DOMAIN_ORDER.get(r.domain, 99),
        )
    )
    return results
