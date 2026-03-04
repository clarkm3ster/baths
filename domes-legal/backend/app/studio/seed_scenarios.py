"""Seed Scenarios — End-to-end person lifecycles through all 10 Dome OS layers.

Takes the 5 canonical BATHS profiles (Marcus Thompson, Sarah Chen, James
Williams, Maria Rodriguez, Robert Jackson) and generates complete,
realistic scenarios that exercise every Dome OS layer.

Each scenario returns a dict keyed by layer name, containing the output
of that layer's core functions for the given person.  A single call to
`build_scenario("marcus")` produces CliffGuard analysis, N-of-1 trial
design, provider matches, labor market analysis, spatial access scores,
governance events, evidence translations, digital exposure reports,
settlement contracts, and narrative packages — all coherent and
cross-referenced.

Usage:
    from app.studio.seed_scenarios import build_scenario, build_all_scenarios

    marcus = build_scenario("marcus")
    all_five = build_all_scenarios()
"""
from __future__ import annotations

from datetime import datetime, timedelta

# Layer imports
from app.studio.treasury import (
    create_account, disburse, calculate_cliff_guard, suggest_income_bridge,
)
from app.studio.bio_experiment import (
    design_trial, record_measurement, analyze_trial, should_stop_early,
)
from app.studio.provider_marketplace import (
    Provider, match_providers, create_referral, track_outcome,
)
from app.studio.labor_market import (
    JobOpening, analyze_labor_market, estimate_roi_of_credential,
)
from app.studio.spatial_mobility import (
    MobilityProfile, analyze_spatial_access, estimate_mobility_cost,
)
from app.studio.governance import (
    file_appeal, review_appeal, get_appeal_stats,
    request_data_right, calculate_benefit_share,
)
from app.studio.evidence_registry import (
    score_external_validity, translate_clinical_to_fiscal, EvidenceEntry,
)
from app.studio.info_security import (
    ExposureEvent, log_exposure, calculate_cognitive_health,
    generate_environment_report, detect_cascade_risk,
)
from app.studio.capital_markets import (
    SettlementContract, pool_contracts, price_bond, stress_test,
)
from app.studio.narrative_synthesis import (
    assemble_package, score_production_potential,
)


# ═══════════════════════════════════════════════════════════════════
# Person profiles — demographics + circumstances
# ═══════════════════════════════════════════════════════════════════

PROFILES = {
    "marcus": {
        "person_id": "marcus-thompson",
        "name": "Marcus Thompson",
        "age": 34,
        "sex": "male",
        "race_ethnicity": "black",
        "conditions": ["substance_use_disorder", "depression"],
        "setting": "outpatient",
        "severity": "moderate",
        "earned_income": 22880.0,  # $11/hr * 2080
        "benefits": {"snap": 2400, "medicaid": 8000},
        "credentials": [],
        "location": {"lat": 39.9918, "lng": -75.1286},  # Kensington, Philadelphia
        "has_vehicle": False,
        "transit_pass": True,
        "mobility_constraints": [],
        "travel_budget": 80.0,
        "insurance": "medicaid",
        "language": "en",
        "systems_involved": ["doc", "medicaid", "bha", "hmis", "probation",
                             "snap", "unemployment", "mco", "pdmp", "shelter"],
        "annual_cost_fragmented": 87400.0,
        "annual_cost_coordinated": 34200.0,
    },
    "sarah": {
        "person_id": "sarah-chen",
        "name": "Sarah Chen",
        "age": 28,
        "sex": "female",
        "race_ethnicity": "asian",
        "conditions": ["ptsd", "anxiety"],
        "setting": "outpatient",
        "severity": "moderate",
        "earned_income": 0.0,  # unemployed, on TANF
        "benefits": {"tanf": 4800, "snap": 3600, "medicaid": 8000, "ccdf": 6000},
        "credentials": [],
        "location": {"lat": 39.9526, "lng": -75.1652},  # Center City, Philadelphia
        "has_vehicle": False,
        "transit_pass": False,
        "mobility_constraints": ["child_care_hours"],
        "travel_budget": 40.0,
        "insurance": "medicaid",
        "language": "zh",  # Mandarin-speaking
        "systems_involved": ["sacwis", "tanf", "pha", "medicaid",
                             "court_cms", "snap", "mco"],
        "annual_cost_fragmented": 72200.0,
        "annual_cost_coordinated": 29100.0,
    },
    "james": {
        "person_id": "james-williams",
        "name": "James Williams",
        "age": 52,
        "sex": "male",
        "race_ethnicity": "black",
        "conditions": ["ptsd", "chronic_pain", "diabetes"],
        "setting": "outpatient",
        "severity": "moderate",
        "earned_income": 0.0,  # SSI + VA disability
        "benefits": {"ssi": 10800, "medicaid": 8000},
        "credentials": [],
        "location": {"lat": 39.9637, "lng": -75.2406},  # West Philadelphia
        "has_vehicle": True,
        "transit_pass": False,
        "mobility_constraints": ["wheelchair"],
        "travel_budget": 150.0,
        "insurance": "medicaid",
        "language": "en",
        "systems_involved": ["va", "medicaid", "ssa", "pdmp", "hie", "mco", "ssi"],
        "annual_cost_fragmented": 94100.0,
        "annual_cost_coordinated": 52300.0,
    },
    "maria": {
        "person_id": "maria-rodriguez",
        "name": "Maria Rodriguez",
        "age": 16,
        "sex": "female",
        "race_ethnicity": "hispanic",
        "conditions": ["trauma", "adhd"],
        "setting": "outpatient",
        "severity": "moderate",
        "earned_income": 0.0,
        "benefits": {"medicaid": 8000},
        "credentials": [],
        "location": {"lat": 40.0379, "lng": -75.1396},  # North Philadelphia
        "has_vehicle": False,
        "transit_pass": False,
        "mobility_constraints": [],
        "travel_budget": 20.0,
        "insurance": "medicaid",
        "language": "es",
        "systems_involved": ["sacwis", "education", "juvenile_justice",
                             "medicaid", "mco"],
        "annual_cost_fragmented": 68500.0,
        "annual_cost_coordinated": 31200.0,
    },
    "robert": {
        "person_id": "robert-jackson",
        "name": "Robert Jackson",
        "age": 45,
        "sex": "male",
        "race_ethnicity": "black",
        "conditions": ["schizophrenia", "diabetes", "hypertension"],
        "setting": "emergency",
        "severity": "severe",
        "earned_income": 0.0,
        "benefits": {"ssi": 10800, "medicaid": 8000, "snap": 2400},
        "credentials": [],
        "location": {"lat": 39.9550, "lng": -75.1550},  # Downtown Philadelphia (no fixed address)
        "has_vehicle": False,
        "transit_pass": False,
        "mobility_constraints": ["limited_walking"],
        "travel_budget": 0.0,
        "insurance": "medicaid",
        "language": "en",
        "systems_involved": ["medicaid", "bha", "hmis", "shelter",
                             "snap", "ssi", "mco", "er"],
        "annual_cost_fragmented": 94800.0,
        "annual_cost_coordinated": 38200.0,
    },
}


# ═══════════════════════════════════════════════════════════════════
# Provider registry (shared across all scenarios)
# ═══════════════════════════════════════════════════════════════════

PROVIDERS = [
    Provider(
        provider_id="prov-kens-bh",
        name="Kensington Behavioral Health Center",
        service_types=["mental_health", "substance_use", "crisis"],
        accepts_medicaid=True, accepts_medicare=False, sliding_scale=True,
        languages=["en", "es"],
        location={"lat": 39.9920, "lng": -75.1300, "address": "3100 Kensington Ave"},
        availability_score=0.6, quality_score=0.82, wait_days=7,
    ),
    Provider(
        provider_id="prov-temple-pc",
        name="Temple University Primary Care",
        service_types=["primary_care", "diabetes_management", "chronic_pain"],
        accepts_medicaid=True, accepts_medicare=True, sliding_scale=False,
        languages=["en", "es", "zh"],
        location={"lat": 40.0034, "lng": -75.1496, "address": "3401 N Broad St"},
        availability_score=0.4, quality_score=0.90, wait_days=21,
    ),
    Provider(
        provider_id="prov-phr-housing",
        name="Project HOME Reentry Housing",
        service_types=["housing_assistance", "reentry_services"],
        accepts_medicaid=False, accepts_medicare=False, sliding_scale=True,
        languages=["en", "es"],
        location={"lat": 39.9650, "lng": -75.1570, "address": "1515 Fairmount Ave"},
        availability_score=0.3, quality_score=0.88, wait_days=30,
    ),
    Provider(
        provider_id="prov-wf-dev",
        name="Philadelphia Works Workforce Development",
        service_types=["workforce_development", "job_training", "credential_programs"],
        accepts_medicaid=False, accepts_medicare=False, sliding_scale=True,
        languages=["en", "es", "zh"],
        location={"lat": 39.9550, "lng": -75.1630, "address": "1617 JFK Blvd"},
        availability_score=0.7, quality_score=0.75, wait_days=14,
    ),
    Provider(
        provider_id="prov-wc-dv",
        name="Women's Center of Montgomery County",
        service_types=["domestic_violence", "mental_health", "legal_aid"],
        accepts_medicaid=True, accepts_medicare=False, sliding_scale=True,
        languages=["en", "zh", "ko"],
        location={"lat": 39.9530, "lng": -75.1680, "address": "100 S Broad St"},
        availability_score=0.5, quality_score=0.91, wait_days=3,
    ),
    Provider(
        provider_id="prov-va-med",
        name="Philadelphia VA Medical Center",
        service_types=["primary_care", "mental_health", "chronic_pain", "ptsd"],
        accepts_medicaid=True, accepts_medicare=True, sliding_scale=False,
        languages=["en"],
        location={"lat": 39.9560, "lng": -75.2340, "address": "3900 Woodland Ave"},
        availability_score=0.5, quality_score=0.85, wait_days=28,
    ),
    Provider(
        provider_id="prov-act-team",
        name="Community ACT Team - PATH Program",
        service_types=["mental_health", "housing_assistance", "case_management"],
        accepts_medicaid=True, accepts_medicare=False, sliding_scale=True,
        languages=["en", "es"],
        location={"lat": 39.9540, "lng": -75.1560, "address": "810 Arch St"},
        availability_score=0.4, quality_score=0.87, wait_days=14,
    ),
    Provider(
        provider_id="prov-juv-mentor",
        name="Big Brothers Big Sisters - Philadelphia",
        service_types=["mentorship", "youth_development", "education_support"],
        accepts_medicaid=False, accepts_medicare=False, sliding_scale=True,
        languages=["en", "es"],
        location={"lat": 39.9575, "lng": -75.1690, "address": "230 S Broad St"},
        availability_score=0.6, quality_score=0.83, wait_days=21,
    ),
]


# ═══════════════════════════════════════════════════════════════════
# Job openings registry (shared)
# ═══════════════════════════════════════════════════════════════════

JOBS = [
    JobOpening(
        job_id="job-cdl-b", title="Delivery Driver",
        employer="UPS Supply Chain", wage_hourly=26.0, wage_annual=54080.0,
        credentials_required=["CDL-B"],
        location={"lat": 39.9380, "lng": -75.1280}, commute_minutes=30,
        benefits={"health_insurance": True, "pto_days": 15, "401k_match": 0.04},
        industry="logistics",
    ),
    JobOpening(
        job_id="job-warehouse", title="Warehouse Associate",
        employer="Amazon PHL1", wage_hourly=18.0, wage_annual=37440.0,
        credentials_required=["forklift"],
        location={"lat": 39.8700, "lng": -75.2400}, commute_minutes=45,
        benefits={"health_insurance": True, "pto_days": 10},
        industry="warehousing",
    ),
    JobOpening(
        job_id="job-med-coder", title="Medical Coding Specialist",
        employer="Jefferson Health", wage_hourly=22.0, wage_annual=45760.0,
        credentials_required=["comptia-a+"],
        location={"lat": 39.9490, "lng": -75.1580}, commute_minutes=20,
        benefits={"health_insurance": True, "pto_days": 20, "401k_match": 0.03, "dental": True},
        industry="healthcare",
    ),
    JobOpening(
        job_id="job-peer-recovery", title="Peer Recovery Specialist",
        employer="DBHIDS Philadelphia", wage_hourly=18.0, wage_annual=37440.0,
        credentials_required=["cna"],
        location={"lat": 39.9520, "lng": -75.1635}, commute_minutes=25,
        benefits={"health_insurance": True, "pto_days": 12},
        industry="social_services",
    ),
    JobOpening(
        job_id="job-food-service", title="Food Service Worker",
        employer="Aramark - School District", wage_hourly=15.0, wage_annual=31200.0,
        credentials_required=["servsafe"],
        location={"lat": 40.0350, "lng": -75.1400}, commute_minutes=15,
        benefits={"health_insurance": True, "pto_days": 10, "childcare_stipend": True},
        industry="food_service",
    ),
    JobOpening(
        job_id="job-phlebotomist", title="Phlebotomist",
        employer="LabCorp Philadelphia", wage_hourly=19.0, wage_annual=39520.0,
        credentials_required=["phlebotomy"],
        location={"lat": 39.9530, "lng": -75.1660}, commute_minutes=20,
        benefits={"health_insurance": True, "pto_days": 15, "dental": True, "vision": True},
        industry="healthcare",
    ),
]


# ═══════════════════════════════════════════════════════════════════
# Destinations registry (Philadelphia-specific, shared)
# ═══════════════════════════════════════════════════════════════════

DESTINATIONS = [
    {"type": "hospital", "name": "Temple University Hospital",
     "lat": 40.0034, "lng": -75.1496, "wheelchair_accessible": True},
    {"type": "pharmacy", "name": "CVS Pharmacy - Kensington",
     "lat": 39.9900, "lng": -75.1310, "wheelchair_accessible": True},
    {"type": "grocery", "name": "Cousin's Supermarket",
     "lat": 39.9850, "lng": -75.1340, "wheelchair_accessible": True},
    {"type": "primary_care", "name": "Health Center #4",
     "lat": 39.9750, "lng": -75.1450, "wheelchair_accessible": True},
    {"type": "mental_health", "name": "Kensington BH Center",
     "lat": 39.9920, "lng": -75.1300, "wheelchair_accessible": True},
    {"type": "wic_office", "name": "WIC Office - North Philly",
     "lat": 40.0100, "lng": -75.1500, "wheelchair_accessible": True},
    {"type": "dialysis", "name": "DaVita Kidney Care",
     "lat": 39.9680, "lng": -75.2200, "wheelchair_accessible": True},
    {"type": "grocery", "name": "ShopRite - Fox Street",
     "lat": 40.0000, "lng": -75.1260, "wheelchair_accessible": True},
]


# ═══════════════════════════════════════════════════════════════════
# Per-person scenario builders
# ═══════════════════════════════════════════════════════════════════

def _build_treasury(p: dict) -> dict:
    """CliffGuard + income bridge analysis."""
    account = create_account(
        person_id=p["person_id"],
        initial_balance=500.0,
        restricted_uses=["housing", "food", "medical", "transit"],
    )
    cliff = calculate_cliff_guard(
        benefits=p["benefits"],
        earned_income=p["earned_income"],
        person_id=p["person_id"],
    )
    # Target income: enough to clear the cliffs
    target = max(p["earned_income"] * 1.5, 35000.0) if p["earned_income"] > 0 else 30000.0
    bridge = suggest_income_bridge(cliff, target)
    return {
        "account": account.model_dump(),
        "cliff_guard": cliff.model_dump(),
        "income_bridge": bridge,
        "target_income": target,
    }


def _build_bio_experiment(p: dict) -> dict:
    """N-of-1 trial design + simulated measurements."""
    # Trial design varies by person
    trials_config = {
        "marcus-thompson": {
            "hypothesis": "Buprenorphine + counseling reduces cravings more than counseling alone",
            "intervention": "Buprenorphine 8mg sublingual + weekly counseling",
            "control": "Weekly counseling only",
            "metric_name": "daily_craving_score",
            "control_data": [6.2, 5.8, 6.5, 7.0, 6.1, 5.9, 6.3, 6.8],
            "intervention_data": [4.1, 3.5, 3.8, 3.2, 4.0, 3.6, 3.3, 2.9],
        },
        "sarah-chen": {
            "hypothesis": "Trauma-focused CBT reduces PTSD symptoms more than standard therapy",
            "intervention": "Trauma-focused CBT (12-session protocol)",
            "control": "Standard supportive therapy",
            "metric_name": "PCL5_score",
            "control_data": [52, 50, 53, 48, 51, 49, 50, 47],
            "intervention_data": [45, 38, 35, 32, 30, 28, 27, 25],
        },
        "james-williams": {
            "hypothesis": "Yoga + PT reduces chronic pain more than standard care",
            "intervention": "Yoga (3x/week) + physical therapy (2x/week)",
            "control": "Standard pain management (medication only)",
            "metric_name": "pain_VAS_0_10",
            "control_data": [7.5, 7.2, 7.8, 7.0, 7.3, 7.6, 7.1, 7.4],
            "intervention_data": [6.0, 5.2, 4.8, 4.5, 4.2, 4.0, 3.8, 4.1],
        },
        "maria-rodriguez": {
            "hypothesis": "Structured mentorship improves academic engagement more than standard services",
            "intervention": "Weekly mentor meetings + academic tutoring",
            "control": "Standard foster care services",
            "metric_name": "weekly_attendance_pct",
            "control_data": [60, 55, 65, 50, 58, 62, 55, 60],
            "intervention_data": [72, 78, 80, 85, 82, 88, 90, 87],
        },
        "robert-jackson": {
            "hypothesis": "Housing First + ACT reduces ER visits compared to shelter + standard care",
            "intervention": "Permanent supportive housing + ACT team",
            "control": "Emergency shelter + drop-in services",
            "metric_name": "monthly_ER_visits",
            "control_data": [3, 2, 4, 3, 5, 2, 3, 4],
            "intervention_data": [1, 1, 0, 1, 0, 0, 1, 0],
        },
    }

    cfg = trials_config[p["person_id"]]
    trial = design_trial(
        person_id=p["person_id"],
        hypothesis=cfg["hypothesis"],
        intervention=cfg["intervention"],
        control=cfg["control"],
        metric_name=cfg["metric_name"],
        n_cycles=2,
        phase_days=14,
    )

    # Record measurements into control and intervention phases
    for i, phase in enumerate(trial.phases):
        data = []
        if phase.phase_type == "control":
            data = cfg["control_data"]
        elif phase.phase_type == "intervention":
            data = cfg["intervention_data"]
        for val in data:
            trial = record_measurement(trial, i, float(val))

    # Analyze
    result = analyze_trial(trial)
    stop_decision, stop_reason = should_stop_early(trial)

    return {
        "trial": trial.model_dump(),
        "result": result.model_dump(),
        "should_stop": stop_decision,
        "stop_reason": stop_reason,
    }


def _build_providers(p: dict) -> dict:
    """Provider matching + referral creation."""
    needs = {
        "service_type": {
            "marcus-thompson": "substance_use",
            "sarah-chen": "domestic_violence",
            "james-williams": "chronic_pain",
            "maria-rodriguez": "mentorship",
            "robert-jackson": "case_management",
        }[p["person_id"]],
        "insurance": p["insurance"],
        "language": p["language"],
        "location": p["location"],
        "max_distance_miles": 15.0,
    }

    matches = match_providers(needs, PROVIDERS, max_results=3)

    # Create referral to top match
    referrals = []
    if matches:
        top = matches[0]["provider"]
        ref = create_referral(p["person_id"], top.provider_id, needs["service_type"])
        ref = track_outcome(ref, 0.85, "Successful initial engagement")
        referrals.append(ref.model_dump())

    return {
        "matches": [
            {
                "provider_name": m["provider"].name,
                "provider_id": m["provider"].provider_id,
                "total_score": m["total_score"],
                "score_breakdown": m["score_breakdown"],
            }
            for m in matches
        ],
        "referrals": referrals,
    }


def _build_labor_market(p: dict) -> dict:
    """Labor market analysis + credential ROI."""
    analysis = analyze_labor_market(
        person_id=p["person_id"],
        current_credentials=p["credentials"],
        current_wage=p["earned_income"],
        location=p["location"],
        max_commute_minutes=60,
        jobs=JOBS,
    )

    # Estimate ROI for top credential pathway
    roi_results = []
    for pathway in analysis.pathways[:2]:
        # Find a matching job's wage as target
        target_wage = 37440.0  # default $18/hr
        for job_match in analysis.matched_jobs:
            job_data = job_match.get("job", {})
            job_creds = [c.lower() for c in job_data.get("credentials_required", [])]
            if pathway.target_credential.lower() in job_creds:
                target_wage = job_data.get("wage_annual", 37440.0)
                break

        working_years = max(65 - p["age"], 10)
        roi = estimate_roi_of_credential(
            pathway, p["earned_income"], target_wage, working_years,
        )
        roi_results.append(roi)

    return {
        "analysis": analysis.model_dump(),
        "credential_roi": roi_results,
    }


def _build_spatial(p: dict) -> dict:
    """Spatial access + mobility cost."""
    profile = MobilityProfile(
        person_id=p["person_id"],
        home_location=p["location"],
        has_vehicle=p["has_vehicle"],
        transit_pass=p["transit_pass"],
        mobility_constraints=p["mobility_constraints"],
        typical_travel_budget_monthly=p["travel_budget"],
    )

    analysis = analyze_spatial_access(profile, DESTINATIONS)

    cost = estimate_mobility_cost(profile, {
        "primary_care": 2,
        "pharmacy": 4,
        "grocery": 8,
        "mental_health": 4,
    })

    return {
        "spatial_analysis": analysis.model_dump(),
        "monthly_cost": cost,
    }


def _build_governance(p: dict) -> dict:
    """Appeals + data rights requests."""
    appeals_config = {
        "marcus-thompson": {
            "prediction_type": "classification",
            "prediction_id": "risk-recidivism-2026-001",
            "grounds": "Risk score based on prior conviction history does not account for 6 months of successful SUD treatment and stable program engagement",
            "decision": "overturned",
        },
        "sarah-chen": {
            "prediction_type": "alert",
            "prediction_id": "cps-risk-2026-042",
            "grounds": "Risk alert triggered by address change was due to fleeing DV situation, not instability — reunification timeline is on track",
            "decision": "overturned",
        },
        "james-williams": {
            "prediction_type": "classification",
            "prediction_id": "va-disability-reduction-2026-008",
            "grounds": "Disability rating reduction based on single assessment does not reflect ongoing PTSD symptoms and chronic pain limitations",
            "decision": "upheld",  # still under review
        },
        "maria-rodriguez": {
            "prediction_type": "classification",
            "prediction_id": "juv-risk-2026-015",
            "grounds": "Juvenile risk classification does not account for trauma history or current engagement with mentorship program",
            "decision": "overturned",
        },
        "robert-jackson": {
            "prediction_type": "alert",
            "prediction_id": "shelter-ban-2026-003",
            "grounds": "Shelter ban classification triggered by behavioral incident during psychiatric crisis — not volitional",
            "decision": "overturned",
        },
    }

    cfg = appeals_config[p["person_id"]]
    appeal = file_appeal(
        person_id=p["person_id"],
        prediction_type=cfg["prediction_type"],
        prediction_id=cfg["prediction_id"],
        grounds=cfg["grounds"],
        evidence=["treatment_records", "case_manager_statement"],
    )
    if cfg["decision"] != "upheld":
        appeal = review_appeal(appeal, cfg["decision"], f"Appeal {cfg['decision']} after review of submitted evidence")

    # Data rights request
    rights_config = {
        "marcus-thompson": ("export", "Export all SUD treatment records for coordinated care planning"),
        "sarah-chen": ("export", "Export all child welfare records for family court reunification hearing"),
        "james-williams": ("correction", "Correct VA disability rating assessment — missing chronic pain documentation"),
        "maria-rodriguez": ("correction", "Correct juvenile record — incident reclassified from delinquent to status offense"),
        "robert-jackson": ("access_log", "Review all agencies that accessed shelter and behavioral health records in past 12 months"),
    }
    rt, details = rights_config[p["person_id"]]
    right = request_data_right(p["person_id"], rt, details)

    # Benefit share
    benefit = calculate_benefit_share(p["person_id"], p["annual_cost_fragmented"] * 0.1)

    return {
        "appeal": appeal.model_dump(),
        "data_right": right.model_dump(),
        "benefit_share": benefit,
        "appeal_stats": get_appeal_stats([appeal]),
    }


def _build_evidence(p: dict) -> dict:
    """Evidence registry — external validity + clinical-to-fiscal translation."""
    # Map each person to their primary clinical endpoint
    endpoint_config = {
        "marcus-thompson": ("PHQ9", 4.0),    # PHQ9 drop of 4 points
        "sarah-chen": ("GAD7", 6.0),         # GAD7 drop of 6 points
        "james-williams": ("pain_VAS", 3.0), # pain VAS drop of 3 cm
        "maria-rodriguez": ("PROMIS_physical", 5.0),  # 5 T-score improvement
        "robert-jackson": ("readmission_30d", 0.15),  # 15% absolute reduction
    }

    endpoint, effect = endpoint_config[p["person_id"]]

    study_pop = {
        "mean_age": p["age"] + 5,
        "age_range": [p["age"] - 10, p["age"] + 20],
        "pct_female": 0.52 if p["sex"] == "female" else 0.48,
        "race_ethnicity": [p["race_ethnicity"], "white", "hispanic"],
        "conditions": p["conditions"],
        "setting": p["setting"],
        "severity": p["severity"],
    }

    person_ctx = {
        "age": p["age"],
        "sex": p["sex"],
        "race_ethnicity": p["race_ethnicity"],
        "conditions": p["conditions"],
        "setting": p["setting"],
        "severity": p["severity"],
    }

    validity = score_external_validity(study_pop, person_ctx)
    fiscal = translate_clinical_to_fiscal(endpoint, effect, person_ctx)

    return {
        "clinical_endpoint": endpoint,
        "effect_size": effect,
        "external_validity_score": validity,
        "fiscal_translation": fiscal,
    }


def _build_infosec(p: dict) -> dict:
    """Digital exposure events + cognitive health + cascade risk."""
    now = datetime.utcnow()

    exposure_configs = {
        "marcus-thompson": [
            ("predatory_ad", "facebook", 0.7, {"ad_category": "payday_loan", "amount_targeted": 500}),
            ("predatory_ad", "facebook", 0.6, {"ad_category": "subprime_credit_card"}),
            ("predatory_ad", "instagram", 0.8, {"ad_category": "cash_advance_app"}),
            ("scam_contact", "phone", 0.9, {"type": "fake_debt_collector"}),
            ("predatory_ad", "facebook", 0.5, {"ad_category": "rent_to_own_electronics"}),
            ("phishing", "email", 0.7, {"type": "fake_unemployment_office"}),
            ("doomscrolling", "tiktok", 0.3, {"hours": 3.5}),
            ("predatory_ad", "google", 0.6, {"ad_category": "bail_bond_services"}),
        ],
        "sarah-chen": [
            ("misinformation", "wechat", 0.6, {"topic": "custody_law_myths"}),
            ("misinformation", "facebook", 0.5, {"topic": "immigration_enforcement_rumors"}),
            ("doomscrolling", "tiktok", 0.3, {"hours": 2.0}),
            ("misinformation", "wechat", 0.7, {"topic": "false_cps_procedures"}),
        ],
        "james-williams": [
            ("scam_contact", "phone", 0.9, {"type": "va_impersonation"}),
            ("scam_contact", "email", 0.8, {"type": "va_benefits_phishing"}),
            ("phishing", "email", 0.7, {"type": "fake_va_login"}),
            ("scam_contact", "phone", 0.8, {"type": "fake_disability_review"}),
            ("predatory_ad", "facebook", 0.5, {"ad_category": "miracle_pain_cure"}),
            ("scam_contact", "sms", 0.7, {"type": "va_prescription_scam"}),
        ],
        "maria-rodriguez": [
            ("doomscrolling", "tiktok", 0.4, {"hours": 4.5}),
            ("doomscrolling", "instagram", 0.3, {"hours": 3.0}),
            ("doomscrolling", "tiktok", 0.5, {"hours": 5.0}),
            ("algorithmic_radicalization", "youtube", 0.7, {"content": "anti_school_rhetoric"}),
            ("doomscrolling", "tiktok", 0.4, {"hours": 4.0}),
            ("doomscrolling", "instagram", 0.3, {"hours": 2.5}),
            ("algorithmic_radicalization", "youtube", 0.6, {"content": "conspiracy_content"}),
            ("doomscrolling", "tiktok", 0.5, {"hours": 6.0}),
            ("doomscrolling", "tiktok", 0.4, {"hours": 3.5}),
            ("doomscrolling", "instagram", 0.3, {"hours": 2.0}),
            ("algorithmic_radicalization", "tiktok", 0.8, {"content": "self_harm_adjacent"}),
            ("doomscrolling", "tiktok", 0.5, {"hours": 5.5}),
        ],
        "robert-jackson": [
            ("scam_contact", "phone", 0.9, {"type": "fake_ssi_office"}),
            ("predatory_ad", "public_wifi", 0.7, {"ad_category": "predatory_shelter_services"}),
            ("scam_contact", "in_person", 0.8, {"type": "identity_theft_attempt"}),
            ("predatory_ad", "public_wifi", 0.6, {"ad_category": "fake_housing_program"}),
            ("predatory_ad", "public_wifi", 0.8, {"ad_category": "cash_for_benefits_card"}),
            ("phishing", "public_wifi", 0.7, {"type": "fake_government_portal"}),
            ("scam_contact", "phone", 0.9, {"type": "fake_disability_lawyer"}),
            ("predatory_ad", "public_wifi", 0.7, {"ad_category": "payday_loan"}),
        ],
    }

    events = []
    for i, (etype, platform, severity, ctx) in enumerate(exposure_configs[p["person_id"]]):
        evt = log_exposure(
            person_id=p["person_id"],
            exposure_type=etype,
            source_platform=platform,
            severity=severity,
            context=ctx,
        )
        # Backdate events across the 30-day window
        days_ago = 30 - (i * 30 // max(len(exposure_configs[p["person_id"]]), 1))
        evt = evt.model_copy(update={
            "detected_at": now - timedelta(days=max(days_ago, 0))
        })
        events.append(evt)

    report = generate_environment_report(p["person_id"], events)

    # Financial stress score based on benefits cliff proximity
    financial_stress = min(
        (p["annual_cost_fragmented"] - p["annual_cost_coordinated"]) / p["annual_cost_fragmented"],
        1.0,
    )
    cascade = detect_cascade_risk(p["person_id"], events, financial_stress)

    return {
        "exposure_count": len(events),
        "report": report.model_dump(),
        "cascade_risk": cascade,
    }


def _build_capital_markets(p: dict) -> SettlementContract:
    """Create a settlement contract for this person's intervention."""
    savings_split = {
        "marcus-thompson": {"medicaid": 22150, "corrections": 10500, "shelter": 12600, "snap": 2000},
        "sarah-chen": {"medicaid": 8000, "tanf": 4800, "foster_care": 18000, "court": 5000},
        "james-williams": {"medicaid": 15000, "va": 18000, "ssi": 5000, "pharmacy": 3800},
        "maria-rodriguez": {"medicaid": 8000, "foster_care": 15000, "education": 8000, "juvenile_justice": 6300},
        "robert-jackson": {"medicaid": 30000, "shelter": 12000, "er": 8400, "ssi": 2000, "bha": 4200},
    }

    success_probs = {
        "marcus-thompson": 0.65,
        "sarah-chen": 0.72,
        "james-williams": 0.58,
        "maria-rodriguez": 0.70,
        "robert-jackson": 0.55,
    }

    interventions = {
        "marcus-thompson": "Coordinated reentry: SUD treatment + housing + workforce development",
        "sarah-chen": "DV survivor support: trauma therapy + housing + legal aid + job training",
        "james-williams": "Dual-eligible care coordination: VA-Medicaid integration + pain management",
        "maria-rodriguez": "Youth wraparound: mentorship + trauma therapy + education advocacy",
        "robert-jackson": "Housing First + ACT: permanent supportive housing + intensive case management",
    }

    return SettlementContract(
        person_id=p["person_id"],
        intervention_type=interventions[p["person_id"]],
        expected_savings=savings_split[p["person_id"]],
        probability_of_success=success_probs[p["person_id"]],
        verification_method="claims_analysis_12mo",
        term_years=3,
        status="active",
    )


def _build_narrative(p: dict, layer_results: dict) -> dict:
    """Narrative synthesis from all layer data."""
    # Convert layer results into narrative events
    events = []

    # Financial events from treasury
    cliff = layer_results.get("treasury", {}).get("cliff_guard", {})
    if cliff.get("cliff_zones"):
        events.append({
            "type": "cliff_zone_entered",
            "domain": "financial",
            "timestamp": "2026-01-15T00:00:00",
            "details": {
                "amount": cliff.get("max_safe_income", 0),
                "cliff_zones": len(cliff.get("cliff_zones", [])),
            },
        })

    # Health events from bio experiment
    trial_result = layer_results.get("bio_experiment", {}).get("result", {})
    if trial_result.get("p_value", 1.0) < 0.05:
        events.append({
            "type": "trial_decisive_benefit",
            "domain": "health",
            "timestamp": "2026-02-01T00:00:00",
            "details": {
                "metric": trial_result.get("trial_id", ""),
                "effect_size": trial_result.get("effect_size", 0),
            },
        })

    # Governance events
    appeal = layer_results.get("governance", {}).get("appeal", {})
    if appeal.get("status") == "overturned":
        events.append({
            "type": "appeal_overturned",
            "domain": "legal",
            "timestamp": "2026-02-15T00:00:00",
            "details": {"prediction_id": appeal.get("prediction_id", "")},
        })

    # Infosec cascade events
    cascade = layer_results.get("info_security", {}).get("cascade_risk", {})
    if cascade.get("risk_level") in ("critical", "high"):
        events.append({
            "type": "cascade_risk_critical" if cascade["risk_level"] == "critical" else "exposure_critical",
            "domain": "digital",
            "timestamp": "2026-02-20T00:00:00",
            "details": {"risk_score": cascade.get("risk_score", 0)},
        })

    # Spatial access gaps
    spatial = layer_results.get("spatial", {}).get("spatial_analysis", {})
    if spatial.get("critical_gaps"):
        events.append({
            "type": "benefit_cutoff",
            "domain": "housing",
            "timestamp": "2026-01-20T00:00:00",
            "details": {"gaps": len(spatial["critical_gaps"])},
        })

    # Labor market credential gap
    labor = layer_results.get("labor_market", {}).get("analysis", {})
    if labor.get("credential_gaps"):
        events.append({
            "type": "credential_gap_identified",
            "domain": "employment",
            "timestamp": "2026-01-25T00:00:00",
            "details": {"gaps": labor["credential_gaps"]},
        })

    package = assemble_package(p["person_id"], events)
    score = score_production_potential(package, "tier2_standard")

    return {
        "events_fed": len(events),
        "package": package.model_dump(),
        "production_score": score,
    }


# ═══════════════════════════════════════════════════════════════════
# Public API
# ═══════════════════════════════════════════════════════════════════

def build_scenario(name: str) -> dict:
    """Build a complete scenario for one person across all 10 layers.

    Args:
        name: One of "marcus", "sarah", "james", "maria", "robert".

    Returns:
        Dict keyed by layer name, each containing that layer's output.
    """
    name = name.lower().strip()
    if name not in PROFILES:
        available = ", ".join(sorted(PROFILES.keys()))
        raise ValueError(f"Unknown profile '{name}'. Available: {available}")

    p = PROFILES[name]
    result = {"person": {"id": p["person_id"], "name": p["name"]}}

    # Build each layer
    result["treasury"] = _build_treasury(p)
    result["bio_experiment"] = _build_bio_experiment(p)
    result["providers"] = _build_providers(p)
    result["labor_market"] = _build_labor_market(p)
    result["spatial"] = _build_spatial(p)
    result["governance"] = _build_governance(p)
    result["evidence"] = _build_evidence(p)
    result["info_security"] = _build_infosec(p)

    # Capital markets — contract for this person
    contract = _build_capital_markets(p)
    result["capital_markets"] = {"contract": contract.model_dump()}

    # Narrative synthesis — feeds from all other layer results
    result["narrative"] = _build_narrative(p, result)

    return result


def build_all_scenarios() -> dict:
    """Build scenarios for all 5 people.

    Returns:
        Dict mapping person name to their full scenario.
    """
    return {name: build_scenario(name) for name in PROFILES}


def build_bond_pool() -> dict:
    """Build the Prevention-Backed Security bond from all 5 contracts.

    Returns:
        Dict with bond details, pricing, and stress test results.
    """
    contracts = [_build_capital_markets(PROFILES[name]) for name in PROFILES]
    bond = pool_contracts(contracts, "Philadelphia Prevention Bond 2026-A", "mezzanine")
    pricing = price_bond(bond, contracts)
    stress = stress_test(bond, contracts)

    return {
        "bond": bond.model_dump(),
        "pricing": pricing.model_dump(),
        "stress_test": stress,
        "contracts": [c.model_dump() for c in contracts],
        "total_expected_savings": sum(sum(c.expected_savings.values()) for c in contracts),
        "total_notional": bond.total_notional,
    }
