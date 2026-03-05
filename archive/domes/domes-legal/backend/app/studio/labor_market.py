"""Labor Market -- employment as intervention surface.

Provides:
- Job opening registry with wage, credential, and commute data
- Credential pathway modeling (current -> target with steps, cost, funding)
- Labor market analysis matching a person to viable job opportunities
- Job fit scoring (credential match, wage improvement, commute feasibility)
- ROI estimation for credential investments

All functions are stdlib-only and operate on Pydantic models.
"""
from __future__ import annotations

import math
import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class JobOpening(BaseModel):
    """A job opening in the labor market."""
    job_id: str = Field(default_factory=lambda: f"job-{uuid.uuid4().hex[:12]}")
    title: str
    employer: str
    wage_hourly: float = Field(ge=0.0)
    wage_annual: float = Field(ge=0.0)
    credentials_required: list[str] = Field(
        default_factory=list,
        description="Credentials or certifications required, e.g. 'CDL-A', 'CNA', 'ServSafe'",
    )
    location: dict[str, Any] = Field(
        default_factory=dict,
        description="Location dict with lat, lng, and address fields",
    )
    commute_minutes: int = Field(default=30, ge=0)
    benefits: dict[str, Any] = Field(
        default_factory=dict,
        description="Benefits dict, e.g. {'health_insurance': True, 'pto_days': 10, '401k_match': 0.03}",
    )
    industry: str = ""
    posted_at: datetime = Field(default_factory=datetime.utcnow)


class CredentialPathway(BaseModel):
    """A pathway from current credentials to a target credential."""
    pathway_id: str = Field(default_factory=lambda: f"path-{uuid.uuid4().hex[:12]}")
    current_credentials: list[str] = Field(default_factory=list)
    target_credential: str
    steps: list[str] = Field(
        default_factory=list,
        description="Ordered list of steps to obtain the target credential",
    )
    estimated_weeks: int = Field(default=0, ge=0)
    estimated_cost: float = Field(default=0.0, ge=0.0)
    funding_sources: list[str] = Field(
        default_factory=list,
        description="Available funding: 'pell_grant', 'wioa', 'employer_tuition', 'state_grant', etc.",
    )


class LaborMarketAnalysis(BaseModel):
    """Comprehensive labor market analysis for a person."""
    person_id: str
    current_wage: float = 0.0
    target_wage: float = 0.0
    matched_jobs: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Scored job matches, each with job data and fit_score",
    )
    credential_gaps: list[str] = Field(
        default_factory=list,
        description="Credentials the person lacks for matched jobs",
    )
    pathways: list[CredentialPathway] = Field(
        default_factory=list,
        description="Recommended credential pathways to close gaps",
    )
    commute_feasibility: dict[str, Any] = Field(
        default_factory=dict,
        description="Commute analysis: avg commute, jobs within range, transit options",
    )


# ---------------------------------------------------------------------------
# Distance / commute estimation
# ---------------------------------------------------------------------------

_EARTH_RADIUS_MILES = 3_958.8
_AVG_DRIVING_MPH = 25.0  # urban average including stops


def _haversine_miles(
    lat1: float, lng1: float,
    lat2: float, lng2: float,
) -> float:
    """Great-circle distance between two lat/lng points in miles."""
    lat1_r, lat2_r = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return _EARTH_RADIUS_MILES * c


def _estimate_commute_minutes(
    person_location: dict[str, Any],
    job_location: dict[str, Any],
) -> int:
    """Estimate one-way commute time in minutes based on straight-line distance.

    Uses a simple distance / average speed model. Real implementations
    would call a routing API.
    """
    p_lat = person_location.get("lat")
    p_lng = person_location.get("lng")
    j_lat = job_location.get("lat")
    j_lng = job_location.get("lng")

    if any(v is None for v in (p_lat, p_lng, j_lat, j_lng)):
        return 30  # default when location data is missing

    dist = _haversine_miles(p_lat, p_lng, j_lat, j_lng)
    # Add 20% for road indirectness
    road_dist = dist * 1.2
    minutes = (road_dist / _AVG_DRIVING_MPH) * 60
    return max(int(round(minutes)), 1)


# ---------------------------------------------------------------------------
# Job fit scoring
# ---------------------------------------------------------------------------

def score_job_fit(
    person: dict[str, Any],
    job: JobOpening,
) -> float:
    """Score how well a job fits a person (0.0 - 1.0).

    Factors:
    - Credential match (0.35): Does the person have the required credentials?
    - Wage improvement (0.30): How much better is this job's wage?
    - Commute feasibility (0.20): Is the commute within acceptable range?
    - Benefits value (0.15): Does the job offer health insurance, PTO, etc.?

    Args:
        person: Dict with keys:
            - credentials (list[str]): Person's current credentials
            - current_wage (float): Current hourly or annual wage
            - location (dict): Person's location with lat/lng
            - max_commute_minutes (int): Maximum tolerable commute
        job: The JobOpening to score against.

    Returns:
        Float score from 0.0 to 1.0.
    """
    person_creds = {c.lower() for c in person.get("credentials", [])}
    current_wage = float(person.get("current_wage", 0))
    person_loc = person.get("location", {})
    max_commute = int(person.get("max_commute_minutes", 60))

    scores: dict[str, float] = {}

    # 1. Credential match (0.35)
    required = [c.lower() for c in job.credentials_required]
    if not required:
        scores["credential_match"] = 1.0  # no credentials needed
    else:
        matched = sum(1 for c in required if c in person_creds)
        scores["credential_match"] = matched / len(required)

    # 2. Wage improvement (0.30)
    job_wage = job.wage_annual if job.wage_annual > 0 else job.wage_hourly * 2_080
    if current_wage <= 0:
        scores["wage_improvement"] = 1.0 if job_wage > 0 else 0.5
    else:
        # Normalize current_wage to annual if it looks hourly (< 200)
        if current_wage < 200:
            current_annual = current_wage * 2_080
        else:
            current_annual = current_wage

        if job_wage <= 0:
            scores["wage_improvement"] = 0.0
        else:
            improvement_ratio = job_wage / current_annual
            # Score: 1.0 ratio = 0.3 (lateral), 1.5 ratio = 1.0, <1.0 = worse
            if improvement_ratio < 1.0:
                scores["wage_improvement"] = max(improvement_ratio * 0.3, 0.0)
            else:
                scores["wage_improvement"] = min(
                    0.3 + (improvement_ratio - 1.0) * 1.4, 1.0
                )

    # 3. Commute feasibility (0.20)
    commute_mins = _estimate_commute_minutes(person_loc, job.location)
    if commute_mins <= max_commute:
        # Linear: 0 min = 1.0, max_commute = 0.3
        scores["commute_feasibility"] = max(
            1.0 - (commute_mins / max_commute) * 0.7, 0.3
        )
    else:
        # Beyond max: rapid decay
        overage_ratio = commute_mins / max_commute
        scores["commute_feasibility"] = max(0.3 / overage_ratio, 0.0)

    # 4. Benefits value (0.15)
    benefits = job.benefits
    benefit_score = 0.0
    if benefits.get("health_insurance"):
        benefit_score += 0.4
    if benefits.get("pto_days", 0) >= 10:
        benefit_score += 0.2
    elif benefits.get("pto_days", 0) > 0:
        benefit_score += 0.1
    if benefits.get("401k_match", 0) > 0:
        benefit_score += 0.2
    if benefits.get("dental") or benefits.get("vision"):
        benefit_score += 0.1
    if benefits.get("childcare") or benefits.get("childcare_stipend"):
        benefit_score += 0.1
    scores["benefits_value"] = min(benefit_score, 1.0)

    # Weighted total
    weights = {
        "credential_match": 0.35,
        "wage_improvement": 0.30,
        "commute_feasibility": 0.20,
        "benefits_value": 0.15,
    }

    total = sum(scores.get(f, 0) * w for f, w in weights.items())
    return round(min(max(total, 0.0), 1.0), 4)


# ---------------------------------------------------------------------------
# Credential gap analysis
# ---------------------------------------------------------------------------

def _find_credential_gaps(
    person_credentials: list[str],
    jobs: list[JobOpening],
) -> list[str]:
    """Identify credentials required by matched jobs that the person lacks."""
    person_creds = {c.lower() for c in person_credentials}
    gaps: set[str] = set()

    for job in jobs:
        for cred in job.credentials_required:
            if cred.lower() not in person_creds:
                gaps.add(cred)

    return sorted(gaps)


def _build_pathways(
    current_credentials: list[str],
    credential_gaps: list[str],
) -> list[CredentialPathway]:
    """Build credential pathways for each gap.

    Uses heuristic estimates for duration, cost, and funding based on
    credential type. Real implementations would query a training provider
    database.
    """
    # Heuristic credential metadata: (weeks, cost, steps_template, funding)
    _CREDENTIAL_DB: dict[str, tuple[int, float, list[str], list[str]]] = {
        "cdl-a": (
            8, 5_000,
            ["Complete DOT physical", "Enroll in CDL training program", "Pass written CDL exam", "Complete driving hours", "Pass skills test"],
            ["wioa", "pell_grant", "state_grant"],
        ),
        "cdl-b": (
            4, 3_000,
            ["Complete DOT physical", "Enroll in CDL-B program", "Pass written exam", "Pass skills test"],
            ["wioa", "pell_grant"],
        ),
        "cna": (
            6, 1_500,
            ["Enroll in state-approved CNA program", "Complete classroom hours", "Complete clinical hours", "Pass state competency exam"],
            ["wioa", "pell_grant", "employer_tuition"],
        ),
        "servsafe": (
            1, 200,
            ["Study ServSafe coursebook", "Take ServSafe certification exam"],
            ["employer_tuition"],
        ),
        "osha-10": (
            1, 150,
            ["Complete OSHA 10-hour training course", "Pass assessment"],
            ["employer_tuition", "wioa"],
        ),
        "osha-30": (
            1, 300,
            ["Complete OSHA 30-hour training course", "Pass assessment"],
            ["employer_tuition", "wioa"],
        ),
        "comptia-a+": (
            12, 2_500,
            ["Study Core 1 (220-1101)", "Pass Core 1 exam", "Study Core 2 (220-1102)", "Pass Core 2 exam"],
            ["wioa", "pell_grant", "employer_tuition"],
        ),
        "phlebotomy": (
            8, 2_000,
            ["Enroll in phlebotomy program", "Complete classroom instruction", "Complete clinical practicum", "Pass national certification exam"],
            ["wioa", "pell_grant"],
        ),
        "forklift": (
            1, 200,
            ["Complete OSHA-compliant forklift training", "Pass written evaluation", "Pass practical driving evaluation"],
            ["employer_tuition"],
        ),
        "emt-basic": (
            16, 3_500,
            ["Complete EMT-B coursework", "Complete clinical rotations", "Pass NREMT cognitive exam", "Pass NREMT psychomotor exam"],
            ["wioa", "pell_grant", "state_grant"],
        ),
        "hvac-epa-608": (
            2, 400,
            ["Study EPA Section 608 material", "Pass EPA 608 certification exam"],
            ["wioa", "employer_tuition"],
        ),
    }

    # Default for unknown credentials
    _DEFAULT = (
        12, 3_000,
        ["Research program requirements", "Enroll in training program", "Complete coursework", "Pass certification exam"],
        ["wioa", "pell_grant"],
    )

    pathways: list[CredentialPathway] = []

    for gap in credential_gaps:
        weeks, cost, steps, funding = _CREDENTIAL_DB.get(
            gap.lower(), _DEFAULT
        )

        pathways.append(CredentialPathway(
            current_credentials=list(current_credentials),
            target_credential=gap,
            steps=steps,
            estimated_weeks=weeks,
            estimated_cost=cost,
            funding_sources=funding,
        ))

    return pathways


# ---------------------------------------------------------------------------
# Labor market analysis
# ---------------------------------------------------------------------------

def analyze_labor_market(
    person_id: str,
    current_credentials: list[str],
    current_wage: float,
    location: dict[str, Any],
    max_commute_minutes: int = 60,
    jobs: list[JobOpening] | None = None,
    target_wage: float | None = None,
) -> LaborMarketAnalysis:
    """Run a comprehensive labor market analysis for a person.

    Scores all provided jobs against the person's profile, identifies
    credential gaps, builds pathways to close those gaps, and analyzes
    commute feasibility.

    Args:
        person_id: Unique identifier for the person.
        current_credentials: Person's existing credentials/certifications.
        current_wage: Current hourly wage (or annual if > 200).
        location: Person's location dict with lat/lng.
        max_commute_minutes: Maximum tolerable one-way commute.
        jobs: List of JobOpening instances to analyze against. If None,
            returns an empty analysis.
        target_wage: Desired wage. If not set, defaults to 1.5x current.

    Returns:
        LaborMarketAnalysis with matched jobs, gaps, pathways, and commute data.
    """
    jobs = jobs or []

    # Normalize wage to annual
    if current_wage < 200:
        current_annual = current_wage * 2_080
    else:
        current_annual = current_wage

    if target_wage is None:
        target_annual = current_annual * 1.5
    elif target_wage < 200:
        target_annual = target_wage * 2_080
    else:
        target_annual = target_wage

    person = {
        "credentials": current_credentials,
        "current_wage": current_annual,
        "location": location,
        "max_commute_minutes": max_commute_minutes,
    }

    # Score and rank all jobs
    matched_jobs: list[dict[str, Any]] = []
    commute_times: list[int] = []

    for job in jobs:
        fit = score_job_fit(person, job)
        commute = _estimate_commute_minutes(location, job.location)
        commute_times.append(commute)

        matched_jobs.append({
            "job": job.model_dump(),
            "fit_score": fit,
            "estimated_commute_minutes": commute,
            "within_commute_range": commute <= max_commute_minutes,
        })

    # Sort by fit score descending
    matched_jobs.sort(key=lambda x: -x["fit_score"])

    # Credential gaps across all matched jobs
    credential_gaps = _find_credential_gaps(current_credentials, jobs)

    # Build pathways for each gap
    pathways = _build_pathways(current_credentials, credential_gaps)

    # Commute feasibility summary
    jobs_in_range = sum(1 for c in commute_times if c <= max_commute_minutes)
    avg_commute = (
        sum(commute_times) / len(commute_times) if commute_times else 0
    )

    commute_feasibility = {
        "total_jobs": len(jobs),
        "jobs_within_range": jobs_in_range,
        "jobs_outside_range": len(jobs) - jobs_in_range,
        "max_commute_minutes": max_commute_minutes,
        "average_commute_minutes": round(avg_commute, 1),
        "shortest_commute_minutes": min(commute_times) if commute_times else 0,
        "longest_commute_minutes": max(commute_times) if commute_times else 0,
    }

    return LaborMarketAnalysis(
        person_id=person_id,
        current_wage=current_annual,
        target_wage=target_annual,
        matched_jobs=matched_jobs,
        credential_gaps=credential_gaps,
        pathways=pathways,
        commute_feasibility=commute_feasibility,
    )


# ---------------------------------------------------------------------------
# Credential ROI estimation
# ---------------------------------------------------------------------------

def estimate_roi_of_credential(
    pathway: CredentialPathway,
    current_wage: float,
    target_wage: float,
    working_years_remaining: int = 25,
) -> dict[str, Any]:
    """Estimate the return on investment of pursuing a credential.

    Calculates the financial case for obtaining a credential by comparing
    the upfront investment (cost + lost wages during training) against
    the annual wage increase over a working career.

    Args:
        pathway: The CredentialPathway to evaluate.
        current_wage: Current annual wage (or hourly if < 200).
        target_wage: Expected annual wage after credential (or hourly if < 200).
        working_years_remaining: Years of employment remaining (default 25).

    Returns:
        Dict with:
        - investment: total cost (tuition + opportunity cost)
        - annual_return: additional annual earnings
        - payback_months: months to recoup investment
        - lifetime_roi: total additional earnings over career minus investment
        - roi_percentage: lifetime ROI as percentage of investment
        - funded_cost: portion of tuition covered by funding sources
        - out_of_pocket: net tuition after funding
    """
    # Normalize wages to annual
    if current_wage < 200:
        current_annual = current_wage * 2_080
    else:
        current_annual = current_wage

    if target_wage < 200:
        target_annual = target_wage * 2_080
    else:
        target_annual = target_wage

    # Training duration in years
    training_years = pathway.estimated_weeks / 52.0

    # Opportunity cost: wages foregone during training (assume 50% capacity
    # reduction -- many programs allow part-time work)
    opportunity_cost = current_annual * training_years * 0.5

    # Funding estimate: assume each funding source covers ~30% of tuition
    # (conservative; real calculation depends on eligibility)
    num_funding = len(pathway.funding_sources)
    funding_coverage = min(num_funding * 0.30, 0.90)  # cap at 90%
    funded_amount = pathway.estimated_cost * funding_coverage
    out_of_pocket = pathway.estimated_cost - funded_amount

    # Total investment
    total_investment = out_of_pocket + opportunity_cost

    # Annual return
    annual_return = max(target_annual - current_annual, 0.0)

    # Payback period
    if annual_return > 0:
        payback_years = total_investment / annual_return
        payback_months = int(round(payback_years * 12))
    else:
        payback_months = 0

    # Lifetime ROI
    effective_earning_years = max(working_years_remaining - training_years, 0)
    lifetime_earnings_gain = annual_return * effective_earning_years
    lifetime_roi = lifetime_earnings_gain - total_investment

    roi_percentage = (
        (lifetime_roi / total_investment * 100) if total_investment > 0 else 0.0
    )

    return {
        "credential": pathway.target_credential,
        "investment": round(total_investment, 2),
        "tuition_cost": round(pathway.estimated_cost, 2),
        "opportunity_cost": round(opportunity_cost, 2),
        "funded_cost": round(funded_amount, 2),
        "out_of_pocket": round(out_of_pocket, 2),
        "funding_sources": pathway.funding_sources,
        "annual_return": round(annual_return, 2),
        "payback_months": payback_months,
        "lifetime_roi": round(lifetime_roi, 2),
        "roi_percentage": round(roi_percentage, 1),
        "training_weeks": pathway.estimated_weeks,
        "working_years_remaining": working_years_remaining,
    }
