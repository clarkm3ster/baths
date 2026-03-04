"""
Dome Studio -- Stage Gate Pipeline

Implements stage-gate checks for Dome productions. A production must pass
gate checks to advance between stages:

  development -> pre_production -> production -> post -> distribution

Each gate has a set of requirements. All must be met to pass.
Uses plain dicts / TypedDicts for input types to stay self-contained.
"""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Stage ordering
# ---------------------------------------------------------------------------

STAGES = [
    "development",
    "pre_production",
    "production",
    "post",
    "distribution",
]

# Map: to advance *into* a stage, you must pass this gate.
GATE_FOR_STAGE: dict[str, str] = {
    "development":    "greenlight",
    "pre_production": "pre_production",
    "production":     "production",
    "post":           "picture_lock",
    "distribution":   "ship",
}


# ---------------------------------------------------------------------------
# Result models
# ---------------------------------------------------------------------------

class RequirementResult(BaseModel):
    """Single requirement check inside a gate."""
    name: str
    met: bool
    detail: str = ""


class GateCheck(BaseModel):
    """Outcome of running a full gate check."""
    gate_name: str
    passed: bool
    requirements: list[RequirementResult] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_REAL_CHARACTER_TYPES = {"real", "historical", "living", "real_person"}
_TIER2_PLUS = {"tier2", "tier3", "tier4", "full", "broad", "tier2+"}


def _find_primary_character(
    production: dict[str, Any],
    characters: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """Locate the character record matching the production's character_id."""
    char_id = production.get("character_id")
    for c in characters:
        if str(c.get("id", "")) == str(char_id) or c.get("character_id") == char_id:
            return c
    return characters[0] if characters else None


def _is_real_character(char: dict[str, Any] | None) -> bool:
    if char is None:
        return False
    return (char.get("character_type", "fictional") or "fictional").lower() in _REAL_CHARACTER_TYPES


# ---------------------------------------------------------------------------
# Individual gate implementations
# ---------------------------------------------------------------------------

def _check_greenlight(
    production: dict[str, Any],
    characters: list[dict[str, Any]],
    **_kw: Any,
) -> GateCheck:
    """Gate before entering *development*.

    Requirements:
      - character_id present
      - consent tier appropriate for character type (real needs tier2+)
      - at least 1 team member with role Showrunner
      - budget_total > 0
    """
    reqs: list[RequirementResult] = []

    # 1. character_id
    char_id = production.get("character_id")
    reqs.append(RequirementResult(
        name="character_id_present",
        met=char_id is not None and char_id != "",
        detail=f"character_id={'present' if char_id else 'missing'}",
    ))

    # 2. consent tier vs character type
    primary = _find_primary_character(production, characters)
    consent_tier = (production.get("consent_tier") or "").lower().strip()
    is_real = _is_real_character(primary)
    char_type_label = (primary.get("character_type", "fictional") if primary else "fictional")

    if is_real:
        tier_ok = consent_tier in _TIER2_PLUS
        tier_detail = f"real character ({char_type_label}) requires tier2+; got '{consent_tier}'"
    else:
        tier_ok = consent_tier != ""
        tier_detail = f"fictional character; consent_tier='{consent_tier}'"

    reqs.append(RequirementResult(
        name="consent_tier_appropriate",
        met=tier_ok,
        detail=tier_detail,
    ))

    # 3. at least 1 Showrunner
    team: list[dict[str, Any]] = production.get("team", [])
    showrunners = [
        m for m in team
        if (m.get("role", "") or "").lower() == "showrunner"
    ]
    reqs.append(RequirementResult(
        name="showrunner_assigned",
        met=len(showrunners) >= 1,
        detail=f"{len(showrunners)} showrunner(s) on team",
    ))

    # 4. budget > 0
    budget = production.get("budget_total", 0) or 0
    reqs.append(RequirementResult(
        name="budget_positive",
        met=float(budget) > 0,
        detail=f"budget_total={budget}",
    ))

    return GateCheck(
        gate_name="greenlight",
        passed=all(r.met for r in reqs),
        requirements=reqs,
    )


def _check_pre_production(
    production: dict[str, Any],
    characters: list[dict[str, Any]],
    **_kw: Any,
) -> GateCheck:
    """Gate: development -> pre_production.

    Requirements:
      - Dome Build Sheet complete (character has initial_conditions)
      - at least 2 team members
      - all development deliverables marked complete
    """
    reqs: list[RequirementResult] = []

    # 1. Dome Build Sheet
    primary = _find_primary_character(production, characters)
    has_initial = False
    if primary:
        ic = primary.get("initial_conditions")
        has_initial = ic is not None and ic != "" and ic != {} and ic != []
    reqs.append(RequirementResult(
        name="dome_build_sheet_complete",
        met=has_initial,
        detail="initial_conditions " + ("present" if has_initial else "missing"),
    ))

    # 2. team >= 2
    team = production.get("team", [])
    reqs.append(RequirementResult(
        name="team_minimum",
        met=len(team) >= 2,
        detail=f"{len(team)} team member(s)",
    ))

    # 3. development deliverables done
    deliverables: list[dict[str, Any]] = production.get("deliverables", [])
    dev_dels = [
        d for d in deliverables
        if (d.get("stage", "") or "").lower() in ("development", "dev")
    ]
    done_count = sum(
        1 for d in dev_dels
        if d.get("completed", False) or d.get("status") == "done"
    )
    all_done = len(dev_dels) > 0 and done_count == len(dev_dels)
    reqs.append(RequirementResult(
        name="development_deliverables_complete",
        met=all_done,
        detail=f"{done_count}/{len(dev_dels)} development deliverables done",
    ))

    return GateCheck(
        gate_name="pre_production",
        passed=all(r.met for r in reqs),
        requirements=reqs,
    )


def _check_production(
    production: dict[str, Any],
    characters: list[dict[str, Any]],
    gaps: list[dict[str, Any]] | None = None,
    **_kw: Any,
) -> GateCheck:
    """Gate: pre_production -> production.

    Requirements:
      - Skeleton Key Pack started (gap log initiated)
      - ethics review if real character
      - production budget allocated across remaining stages
    """
    gaps = gaps or []
    reqs: list[RequirementResult] = []

    # 1. Skeleton Key Pack / gap log
    gap_log_started = len(gaps) > 0 or production.get("gap_log_initiated", False)
    reqs.append(RequirementResult(
        name="skeleton_key_pack_started",
        met=gap_log_started,
        detail=f"{len(gaps)} gap(s) logged" if gaps else "gap_log_initiated flag checked",
    ))

    # 2. ethics review for real characters
    primary = _find_primary_character(production, characters)
    is_real = _is_real_character(primary)
    char_type_label = (primary.get("character_type", "fictional") if primary else "fictional")

    if is_real:
        ethics_done = production.get("ethics_review_complete", False)
        reqs.append(RequirementResult(
            name="ethics_review",
            met=ethics_done,
            detail=f"real character ({char_type_label}); ethics_review_complete={ethics_done}",
        ))
    else:
        reqs.append(RequirementResult(
            name="ethics_review",
            met=True,
            detail="fictional character; ethics review not required",
        ))

    # 3. budget allocated across remaining stages
    budget_alloc: dict[str, Any] = production.get("budget_allocation", {}) or {}
    remaining = {"production", "post", "distribution"}
    has_keys = remaining.issubset(set(budget_alloc.keys()))
    all_positive = all(
        float(budget_alloc.get(s, 0) or 0) > 0 for s in remaining
    ) if has_keys else False
    reqs.append(RequirementResult(
        name="budget_allocated_remaining_stages",
        met=has_keys and all_positive,
        detail=f"stages with budget: {sorted(budget_alloc.keys())}; need {sorted(remaining)}",
    ))

    return GateCheck(
        gate_name="production",
        passed=all(r.met for r in reqs),
        requirements=reqs,
    )


def _check_picture_lock(
    production: dict[str, Any],
    gaps: list[dict[str, Any]] | None = None,
    assets: list[dict[str, Any]] | None = None,
    **_kw: Any,
) -> GateCheck:
    """Gate: production -> post (Picture Lock).

    Requirements:
      - at least 1 IP asset created
      - gap log has entries
      - all production deliverables marked
    """
    gaps = gaps or []
    assets = assets or []
    reqs: list[RequirementResult] = []

    # 1. IP asset
    reqs.append(RequirementResult(
        name="ip_asset_exists",
        met=len(assets) >= 1,
        detail=f"{len(assets)} IP asset(s)",
    ))

    # 2. gap log has entries
    reqs.append(RequirementResult(
        name="gap_log_has_entries",
        met=len(gaps) > 0,
        detail=f"{len(gaps)} gap(s) in log",
    ))

    # 3. production deliverables done
    deliverables: list[dict[str, Any]] = production.get("deliverables", [])
    prod_dels = [
        d for d in deliverables
        if (d.get("stage", "") or "").lower() == "production"
    ]
    done_count = sum(
        1 for d in prod_dels
        if d.get("completed", False) or d.get("status") == "done"
    )
    all_done = len(prod_dels) > 0 and done_count == len(prod_dels)
    reqs.append(RequirementResult(
        name="production_deliverables_complete",
        met=all_done,
        detail=f"{done_count}/{len(prod_dels)} production deliverables done",
    ))

    return GateCheck(
        gate_name="picture_lock",
        passed=all(r.met for r in reqs),
        requirements=reqs,
    )


def _check_ship(
    production: dict[str, Any],
    gaps: list[dict[str, Any]] | None = None,
    assets: list[dict[str, Any]] | None = None,
    learnings: list[dict[str, Any]] | None = None,
    **_kw: Any,
) -> GateCheck:
    """Gate: post -> distribution (Ship).

    Requirements:
      - learning package generated
      - postmortem complete (all gaps triaged)
      - IP rights registered for all assets
    """
    gaps = gaps or []
    assets = assets or []
    learnings = learnings or []
    reqs: list[RequirementResult] = []

    # 1. learning package
    has_learning = (
        len(learnings) > 0
        or production.get("learning_package_generated", False)
    )
    reqs.append(RequirementResult(
        name="learning_package_generated",
        met=has_learning,
        detail=f"{len(learnings)} learning(s) recorded" if learnings else "no learnings yet",
    ))

    # 2. postmortem -- all gaps triaged
    _UNTRIAGED = {"new", "untriaged", "open", ""}
    untriaged = [
        g for g in gaps
        if (g.get("status", "new") or "new").lower() in _UNTRIAGED
    ]
    all_triaged = len(gaps) > 0 and len(untriaged) == 0
    reqs.append(RequirementResult(
        name="postmortem_complete",
        met=all_triaged,
        detail=f"{len(untriaged)} untriaged gap(s) of {len(gaps)} total",
    ))

    # 3. IP rights registered for every asset
    registered_count = sum(
        1 for a in assets
        if a.get("ip_rights_registered", False) or a.get("rights_registered", False)
    )
    all_registered = len(assets) > 0 and registered_count == len(assets)
    reqs.append(RequirementResult(
        name="ip_rights_registered",
        met=all_registered,
        detail=f"{registered_count}/{len(assets)} asset(s) with IP rights registered",
    ))

    return GateCheck(
        gate_name="ship",
        passed=all(r.met for r in reqs),
        requirements=reqs,
    )


# ---------------------------------------------------------------------------
# Gate dispatcher
# ---------------------------------------------------------------------------

_GATE_HANDLERS: dict[str, Any] = {
    "greenlight":     _check_greenlight,
    "pre_production": _check_pre_production,
    "production":     _check_production,
    "picture_lock":   _check_picture_lock,
    "ship":           _check_ship,
}


def check_gate(
    production_data: dict[str, Any],
    gate_name: str,
    characters: list[dict[str, Any]] | None = None,
    gaps: list[dict[str, Any]] | None = None,
    assets: list[dict[str, Any]] | None = None,
    learnings: list[dict[str, Any]] | None = None,
) -> GateCheck:
    """Run all requirement checks for a named gate."""
    handler = _GATE_HANDLERS.get(gate_name)
    if handler is None:
        return GateCheck(
            gate_name=gate_name,
            passed=False,
            requirements=[RequirementResult(
                name="unknown_gate",
                met=False,
                detail=f"No gate handler for '{gate_name}'. Valid gates: {sorted(_GATE_HANDLERS.keys())}",
            )],
        )

    return handler(
        production=production_data,
        characters=characters or [],
        gaps=gaps,
        assets=assets,
        learnings=learnings,
    )


# ---------------------------------------------------------------------------
# Advance helper
# ---------------------------------------------------------------------------

def advance_production(
    production_data: dict[str, Any],
    characters: list[dict[str, Any]] | None = None,
    gaps: list[dict[str, Any]] | None = None,
    assets: list[dict[str, Any]] | None = None,
    learnings: list[dict[str, Any]] | None = None,
) -> tuple[bool, GateCheck]:
    """Check the next gate for a production and report whether it can advance.

    Reads production_data["current_stage"] to determine which gate to
    check. If the production is already at the final stage (distribution),
    advancement is denied with an informational gate check.

    Returns:
        (can_advance, gate_check) -- boolean plus the full GateCheck result.
    """
    current = (production_data.get("current_stage") or "").lower().strip()

    # No stage yet -- needs greenlight
    if current == "" or current not in STAGES:
        gate_name = "greenlight"
    else:
        idx = STAGES.index(current)
        if idx >= len(STAGES) - 1:
            return (
                False,
                GateCheck(
                    gate_name="beyond_final_stage",
                    passed=False,
                    requirements=[RequirementResult(
                        name="already_at_final_stage",
                        met=False,
                        detail=f"Production is already at '{current}', the final stage.",
                    )],
                ),
            )
        next_stage = STAGES[idx + 1]
        gate_name = GATE_FOR_STAGE[next_stage]

    result = check_gate(
        production_data=production_data,
        gate_name=gate_name,
        characters=characters,
        gaps=gaps,
        assets=assets,
        learnings=learnings,
    )

    return (result.passed, result)
