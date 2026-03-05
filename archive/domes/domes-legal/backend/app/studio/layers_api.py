"""Layers API — REST endpoints for all 10 Dome OS layers.

Exposes lightweight endpoints that exercise each layer's core functions
without requiring database persistence (layers operate on Pydantic models
in-memory; persistence is handled by the Studio ORM layer above).
"""
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any

# Layer imports
from app.studio.governance import (
    file_appeal, review_appeal, get_appeal_stats,
    request_data_right, fulfill_data_right, calculate_benefit_share,
    AppealRequest, DataRights,
)
from app.studio.bio_experiment import (
    design_trial, record_measurement, analyze_trial, should_stop_early,
    PersonalTrial,
)
from app.studio.evidence_registry import (
    score_external_validity, translate_clinical_to_fiscal,
)
from app.studio.treasury import (
    create_account, disburse, calculate_cliff_guard, suggest_income_bridge,
)
from app.studio.provider_marketplace import (
    match_providers, create_referral, track_outcome,
    Provider, Referral,
)
from app.studio.labor_market import (
    analyze_labor_market, score_job_fit, estimate_roi_of_credential,
    JobOpening,
)
from app.studio.capital_markets import (
    pool_contracts, price_bond, stress_test, calculate_coupon,
    SettlementContract,
)
from app.studio.spatial_mobility import (
    calculate_access_score, analyze_spatial_access, estimate_mobility_cost,
    MobilityProfile,
)
from app.studio.info_security import (
    log_exposure, calculate_cognitive_health, generate_environment_report,
    detect_cascade_risk,
)
from app.studio.narrative_synthesis import (
    extract_threads, assemble_package, score_production_potential,
)

router = APIRouter(tags=["layers"])


# ── Governance ────────────────────────────────────────────────────

class AppealBody(BaseModel):
    person_id: str
    prediction_type: str
    prediction_id: str
    grounds: str
    evidence: list[str] = Field(default_factory=list)

@router.post("/governance/appeals")
def api_file_appeal(body: AppealBody):
    return file_appeal(
        person_id=body.person_id,
        prediction_type=body.prediction_type,
        prediction_id=body.prediction_id,
        grounds=body.grounds,
        evidence=body.evidence,
    ).model_dump()


class DataRightBody(BaseModel):
    person_id: str
    right_type: str
    details: str = ""

@router.post("/governance/data-rights")
def api_request_data_right(body: DataRightBody):
    return request_data_right(
        person_id=body.person_id,
        right_type=body.right_type,
        details=body.details,
    ).model_dump()


class BenefitShareBody(BaseModel):
    person_id: str
    production_revenue: float

@router.post("/governance/benefit-share")
def api_benefit_share(body: BenefitShareBody):
    return calculate_benefit_share(body.person_id, body.production_revenue)


# ── Bio Experiment ────────────────────────────────────────────────

class TrialDesignBody(BaseModel):
    person_id: str
    hypothesis: str
    intervention: str
    control: str
    metric_name: str
    n_cycles: int = 3
    phase_days: int = 14

@router.post("/bio/trials")
def api_design_trial(body: TrialDesignBody):
    trial = design_trial(
        person_id=body.person_id,
        hypothesis=body.hypothesis,
        intervention=body.intervention,
        control=body.control,
        metric_name=body.metric_name,
        n_cycles=body.n_cycles,
        phase_days=body.phase_days,
    )
    return trial.model_dump()


# ── Evidence Registry ─────────────────────────────────────────────

class ExternalValidityBody(BaseModel):
    study_population: dict[str, Any]
    person_context: dict[str, Any]

@router.post("/evidence/external-validity")
def api_external_validity(body: ExternalValidityBody):
    score = score_external_validity(body.study_population, body.person_context)
    return {"external_validity_score": score}


class ClinicalToFiscalBody(BaseModel):
    clinical_endpoint: str
    effect_size: float
    person_context: dict[str, Any]
    baseline_annual_cost: float | None = None

@router.post("/evidence/clinical-to-fiscal")
def api_clinical_to_fiscal(body: ClinicalToFiscalBody):
    return translate_clinical_to_fiscal(
        clinical_endpoint=body.clinical_endpoint,
        effect_size=body.effect_size,
        person_context=body.person_context,
        baseline_annual_cost=body.baseline_annual_cost,
    )


# ── Treasury ──────────────────────────────────────────────────────

class CliffGuardBody(BaseModel):
    benefits: dict[str, float]
    earned_income: float
    person_id: str = ""

@router.post("/treasury/cliff-guard")
def api_cliff_guard(body: CliffGuardBody):
    result = calculate_cliff_guard(
        benefits=body.benefits,
        earned_income=body.earned_income,
        person_id=body.person_id,
    )
    return result.model_dump()


class IncomeBridgeBody(BaseModel):
    benefits: dict[str, float]
    earned_income: float
    target_income: float
    person_id: str = ""

@router.post("/treasury/income-bridge")
def api_income_bridge(body: IncomeBridgeBody):
    guard = calculate_cliff_guard(
        benefits=body.benefits,
        earned_income=body.earned_income,
        person_id=body.person_id,
    )
    return suggest_income_bridge(guard, body.target_income)


# ── Provider Marketplace ──────────────────────────────────────────

class ProviderMatchBody(BaseModel):
    person_needs: dict[str, Any]
    providers: list[dict[str, Any]]
    max_results: int = 5

@router.post("/providers/match")
def api_match_providers(body: ProviderMatchBody):
    provider_objs = [Provider(**p) for p in body.providers]
    results = match_providers(body.person_needs, provider_objs, body.max_results)
    return [
        {
            "provider": r["provider"].model_dump(),
            "total_score": r["total_score"],
            "score_breakdown": r["score_breakdown"],
        }
        for r in results
    ]


# ── Labor Market ──────────────────────────────────────────────────

class LaborAnalysisBody(BaseModel):
    person_id: str
    current_credentials: list[str] = Field(default_factory=list)
    current_wage: float = 0.0
    location: dict[str, Any] = Field(default_factory=dict)
    max_commute_minutes: int = 60
    jobs: list[dict[str, Any]] = Field(default_factory=list)
    target_wage: float | None = None

@router.post("/labor/analyze")
def api_labor_analysis(body: LaborAnalysisBody):
    job_objs = [JobOpening(**j) for j in body.jobs]
    result = analyze_labor_market(
        person_id=body.person_id,
        current_credentials=body.current_credentials,
        current_wage=body.current_wage,
        location=body.location,
        max_commute_minutes=body.max_commute_minutes,
        jobs=job_objs,
        target_wage=body.target_wage,
    )
    return result.model_dump()


# ── Capital Markets ───────────────────────────────────────────────

class BondPoolBody(BaseModel):
    contracts: list[dict[str, Any]]
    bond_name: str
    tranche: str = "mezzanine"

@router.post("/capital/pool")
def api_pool_contracts(body: BondPoolBody):
    contract_objs = [SettlementContract(**c) for c in body.contracts]
    bond = pool_contracts(contract_objs, body.bond_name, body.tranche)
    pricing = price_bond(bond, contract_objs)
    stress = stress_test(bond, contract_objs)
    return {
        "bond": bond.model_dump(),
        "pricing": pricing.model_dump(),
        "stress_test": stress,
    }


# ── Spatial / Mobility ────────────────────────────────────────────

class SpatialAnalysisBody(BaseModel):
    profile: dict[str, Any]
    destinations: list[dict[str, Any]]

@router.post("/spatial/analyze")
def api_spatial_analysis(body: SpatialAnalysisBody):
    profile = MobilityProfile(**body.profile)
    result = analyze_spatial_access(profile, body.destinations)
    return result.model_dump()


# ── Info Security ─────────────────────────────────────────────────

class CognitiveHealthBody(BaseModel):
    person_id: str
    events: list[dict[str, Any]]
    financial_stress_score: float = 0.0

@router.post("/infosec/cognitive-health")
def api_cognitive_health(body: CognitiveHealthBody):
    from app.studio.info_security import ExposureEvent
    event_objs = [ExposureEvent(**e) for e in body.events]
    report = generate_environment_report(body.person_id, event_objs)
    cascade = detect_cascade_risk(body.person_id, event_objs, body.financial_stress_score)
    return {
        "report": report.model_dump(),
        "cascade_risk": cascade,
    }


# ── Narrative Synthesis ───────────────────────────────────────────

class NarrativeBody(BaseModel):
    person_id: str
    events: list[dict[str, Any]]
    consent_tier: str = "tier1_public"

@router.post("/narrative/synthesize")
def api_narrative_synthesis(body: NarrativeBody):
    package = assemble_package(body.person_id, body.events)
    score = score_production_potential(package, body.consent_tier)
    return {
        "package": package.model_dump(),
        "production_score": score,
    }


# ── Full Packet (aggregated endpoint for frontend) ───────────────

_PERSON_ID_TO_NAME = {
    "marcus-thompson": "marcus",
    "sarah-chen": "sarah",
    "james-williams": "james",
    "maria-rodriguez": "maria",
    "robert-jackson": "robert",
    "1": "marcus", "2": "sarah", "3": "james", "4": "maria", "5": "robert",
}


@router.get("/full_packet/{person_id}")
def api_full_packet(person_id: str):
    """Aggregated full packet: all 10 layers for one person in a single response.

    Accepts person_id (e.g. 'marcus-thompson'), short name ('marcus'), or
    numeric ID ('1'-'5').  Powers the entire person detail page with one fetch.
    """
    from app.studio.seed_scenarios import build_scenario, PROFILES

    name = _PERSON_ID_TO_NAME.get(person_id, person_id)
    if name not in PROFILES:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown person '{person_id}'. Available: {list(PROFILES.keys())}",
        )
    return build_scenario(name)


@router.get("/full_packet")
def api_full_packet_list():
    """List all available persons for full_packet queries."""
    from app.studio.seed_scenarios import PROFILES
    return {
        "persons": [
            {"id": p["person_id"], "name": p["name"], "key": key}
            for key, p in PROFILES.items()
        ]
    }


# ── Demo / Scenarios ──────────────────────────────────────────────

@router.get("/demo/{person_name}")
def api_demo_scenario(person_name: str):
    """Full 10-layer scenario for a canonical person.

    Available: marcus, sarah, james, maria, robert
    """
    from app.studio.seed_scenarios import build_scenario
    try:
        return build_scenario(person_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/demo")
def api_demo_all():
    """All 5 canonical scenarios + the Prevention-Backed Security bond."""
    from app.studio.seed_scenarios import build_all_scenarios, build_bond_pool
    return {
        "scenarios": build_all_scenarios(),
        "bond_pool": build_bond_pool(),
    }
