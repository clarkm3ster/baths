"""
Coordination Engine: Given constraints (population, budget, politics, domains),
recommends optimal coordination model(s) and generates architecture blueprints.
"""
import json
from sqlalchemy.orm import Session
from app.models import CoordinationModel, Architecture


DOMAIN_WEIGHTS = {
    "health": 1.0,
    "behavioral_health": 0.9,
    "housing": 0.8,
    "income": 0.7,
    "education": 0.7,
    "child_welfare": 0.8,
    "justice": 0.7,
    "social_support": 0.6,
    "immigration": 0.5,
}

POLITICAL_SCORES = {"high": 1.0, "moderate": 0.7, "low": 0.4, "contentious": 0.2}
CONTEXT_ALIGNMENT = {
    "supportive": {"high": 1.0, "moderate": 0.9, "low": 0.7, "contentious": 0.5},
    "neutral": {"high": 0.9, "moderate": 0.8, "low": 0.5, "contentious": 0.3},
    "resistant": {"high": 0.7, "moderate": 0.5, "low": 0.3, "contentious": 0.1},
    "hostile": {"high": 0.5, "moderate": 0.3, "low": 0.1, "contentious": 0.0},
}


def score_model(model: CoordinationModel, constraints: dict) -> dict:
    """Score a coordination model against given constraints. Returns dict of dimension scores."""

    domains_needed = set(constraints.get("domains", []))
    domains_covered = set(json.loads(model.domains_covered or "[]"))
    budget_range = json.loads(model.typical_budget_range or "{}")
    annual_budget = constraints.get("annual_budget", 0)
    political_context = constraints.get("political_context", "neutral")
    population = constraints.get("population_size", 0)

    # Coverage score: how many needed domains does this model cover?
    if domains_needed:
        covered = domains_needed & domains_covered
        coverage = len(covered) / len(domains_needed)
        # Weight by domain importance
        if covered:
            weighted = sum(DOMAIN_WEIGHTS.get(d, 0.5) for d in covered)
            max_weighted = sum(DOMAIN_WEIGHTS.get(d, 0.5) for d in domains_needed)
            coverage = weighted / max_weighted if max_weighted else 0
    else:
        coverage = len(domains_covered) / 6.0  # general coverage

    # Budget feasibility: is the budget sufficient?
    budget_min = budget_range.get("min", 0)
    budget_max = budget_range.get("max", float("inf"))
    if annual_budget <= 0:
        budget_score = 0.5  # unknown budget
    elif annual_budget >= budget_min and annual_budget <= budget_max:
        budget_score = 1.0
    elif annual_budget < budget_min:
        budget_score = max(0.1, annual_budget / budget_min)
    else:
        budget_score = 0.9  # over budget is fine

    # Political feasibility
    model_political = model.political_feasibility or "moderate"
    political_score = CONTEXT_ALIGNMENT.get(political_context, {}).get(model_political, 0.5)

    # Speed score (inverse of timeline)
    timeline = model.timeline_to_launch or "12-18 months"
    months = _parse_timeline_months(timeline)
    time_horizon = constraints.get("time_horizon", "3yr")
    horizon_months = {"1yr": 12, "3yr": 36, "5yr": 60}.get(time_horizon, 36)
    if months <= horizon_months * 0.3:
        speed = 1.0
    elif months <= horizon_months * 0.6:
        speed = 0.8
    elif months <= horizon_months:
        speed = 0.5
    else:
        speed = 0.2

    # Evidence strength
    evidence_scores = {"strong": 1.0, "moderate": 0.7, "emerging": 0.4, "limited": 0.2}
    sustainability = evidence_scores.get(model.evidence_rating, 0.5)

    # Population fit
    pop_score = 0.7  # default
    if population > 0:
        if model.category == "specialized" and population > 5000:
            pop_score = 0.4  # PACE etc not great for huge pops
        elif model.category == "managed_care" and population < 500:
            pop_score = 0.4  # MCOs need scale
        elif model.category == "community_based":
            pop_score = 0.9 if population < 10000 else 0.6

    # Cost efficiency (budget per person if applicable)
    if population > 0 and annual_budget > 0:
        per_person = annual_budget / population
        if per_person > 50000:
            cost_efficiency = 0.4  # very expensive
        elif per_person > 20000:
            cost_efficiency = 0.6
        elif per_person > 5000:
            cost_efficiency = 0.9
        else:
            cost_efficiency = 0.7  # maybe too cheap
    else:
        cost_efficiency = 0.5

    composite = (
        coverage * 0.25
        + budget_score * 0.15
        + political_score * 0.20
        + speed * 0.10
        + sustainability * 0.10
        + pop_score * 0.10
        + cost_efficiency * 0.10
    )

    return {
        "model_id": model.id,
        "model_name": model.name,
        "composite": round(composite, 3),
        "coverage": round(coverage, 3),
        "budget_feasibility": round(budget_score, 3),
        "political_feasibility": round(political_score, 3),
        "speed": round(speed, 3),
        "sustainability": round(sustainability, 3),
        "population_fit": round(pop_score, 3),
        "cost_efficiency": round(cost_efficiency, 3),
    }


def recommend_models(db: Session, constraints: dict) -> list[dict]:
    """Score all models and return ranked recommendations."""
    models = db.query(CoordinationModel).all()
    scored = [score_model(m, constraints) for m in models]
    scored.sort(key=lambda s: s["composite"], reverse=True)
    return scored


def generate_architecture(db: Session, constraints: dict) -> dict:
    """Generate a complete architecture blueprint from constraints."""
    recommendations = recommend_models(db, constraints)
    if not recommendations:
        return {"error": "No models available"}

    top = recommendations[0]
    primary_model = db.query(CoordinationModel).get(top["model_id"])

    # Check if hybrid is needed (top model doesn't cover all domains)
    domains_needed = set(constraints.get("domains", []))
    primary_domains = set(json.loads(primary_model.domains_covered or "[]"))
    uncovered = domains_needed - primary_domains
    hybrid_ids = []
    hybrid_rationale = []

    if uncovered and len(recommendations) > 1:
        # Find complementary models
        for rec in recommendations[1:]:
            comp_model = db.query(CoordinationModel).get(rec["model_id"])
            comp_domains = set(json.loads(comp_model.domains_covered or "[]"))
            overlap = uncovered & comp_domains
            if overlap:
                hybrid_ids.append(rec["model_id"])
                hybrid_rationale.append(
                    f"{comp_model.name} adds coverage for: {', '.join(overlap)}"
                )
                uncovered -= overlap
            if not uncovered:
                break

    # Build implementation phases
    phases = _generate_phases(primary_model, constraints, hybrid_ids)

    # Build stakeholder map
    stakeholders = _generate_stakeholders(primary_model, constraints)

    # Build budget breakdown
    budget = _generate_budget(primary_model, constraints)

    # Build risk register
    risks = _generate_risks(primary_model, constraints)

    # Build workforce plan
    workforce = _generate_workforce(primary_model, constraints)

    # Build authority map
    authority = _generate_authority_map(primary_model, constraints)

    rationale = f"Recommended {primary_model.name} as primary model (composite score: {top['composite']})."
    if hybrid_ids:
        rationale += f" Hybrid additions: {'; '.join(hybrid_rationale)}."
    if uncovered:
        rationale += f" Note: domains still uncovered: {', '.join(uncovered)}."

    arch = Architecture(
        name=f"{constraints.get('geography', 'Architecture')} {primary_model.abbreviation} Blueprint",
        description=rationale,
        status="draft",
        population_size=constraints.get("population_size"),
        population_description=constraints.get("population_description", ""),
        annual_budget=constraints.get("annual_budget"),
        geography=constraints.get("geography", ""),
        political_context=constraints.get("political_context", "neutral"),
        time_horizon=constraints.get("time_horizon", "3yr"),
        primary_model_id=primary_model.id,
        hybrid_model_ids=json.dumps(hybrid_ids),
        model_rationale=rationale,
        domains_targeted=json.dumps(list(constraints.get("domains", []))),
        constraints=json.dumps(constraints.get("constraints", {})),
        scores=json.dumps(top),
        implementation_phases=json.dumps(phases),
        stakeholders=json.dumps(stakeholders),
        budget_breakdown=json.dumps(budget),
        risks=json.dumps(risks),
        workforce_plan=json.dumps(workforce),
        authority_map=json.dumps(authority),
    )
    db.add(arch)
    db.commit()
    db.refresh(arch)

    return arch._dict()


def _parse_timeline_months(timeline: str) -> int:
    """Parse '12-18 months' -> 15 (midpoint)."""
    import re
    nums = re.findall(r"\d+", timeline)
    if len(nums) >= 2:
        return (int(nums[0]) + int(nums[1])) // 2
    elif nums:
        return int(nums[0])
    return 12


def _generate_phases(model: CoordinationModel, constraints: dict, hybrid_ids: list) -> list:
    """Generate implementation phases based on model and time horizon."""
    horizon = constraints.get("time_horizon", "3yr")
    geography = constraints.get("geography", "the region")

    base_phases = [
        {
            "name": "Assessment & Design",
            "duration": "Months 1-3",
            "description": f"Conduct needs assessment in {geography}, finalize coordination model design, secure initial stakeholder commitments",
            "milestones": [
                "Needs assessment complete",
                "Governance structure defined",
                "Stakeholder MOUs signed",
                "Budget finalized",
            ],
            "status": "not_started",
        },
        {
            "name": "Authority & Funding",
            "duration": "Months 3-6",
            "description": f"Secure regulatory authority ({model.authority_type}), establish funding streams, execute data sharing agreements",
            "milestones": [
                f"{model.authority_type} approval obtained",
                "Funding commitments secured",
                "Data sharing framework in place",
                "Legal review complete",
            ],
            "status": "not_started",
        },
        {
            "name": "Infrastructure Build",
            "duration": "Months 6-9",
            "description": "Build operational infrastructure: IT systems, staffing, training, physical space, provider network",
            "milestones": [
                "IT systems deployed",
                "Core staff hired and trained",
                "Provider network established",
                "Quality measures defined",
            ],
            "status": "not_started",
        },
        {
            "name": "Pilot Launch",
            "duration": "Months 9-12",
            "description": f"Launch pilot with initial cohort, monitor quality metrics, adjust operations based on early data",
            "milestones": [
                "First enrollees onboarded",
                "Care coordination active",
                "Initial quality data collected",
                "Stakeholder feedback gathered",
            ],
            "status": "not_started",
        },
    ]

    if horizon in ("3yr", "5yr"):
        base_phases.extend([
            {
                "name": "Scale & Optimize",
                "duration": "Year 2",
                "description": "Expand enrollment, optimize workflows, integrate additional services, refine quality programs",
                "milestones": [
                    "Enrollment doubled from pilot",
                    "Quality benchmarks met",
                    "Cost savings documented",
                    "Workforce fully staffed",
                ],
                "status": "not_started",
            },
            {
                "name": "Full Operation",
                "duration": "Year 3",
                "description": "Full-scale operations, outcome reporting, financial sustainability assessment, model refinement",
                "milestones": [
                    "Target population reached",
                    "Outcome data published",
                    "Financial model sustainable",
                    "Replication plan developed",
                ],
                "status": "not_started",
            },
        ])

    if horizon == "5yr":
        base_phases.extend([
            {
                "name": "Mature & Replicate",
                "duration": "Years 4-5",
                "description": "Mature operations, publish outcomes, support replication in other geographies, advocate for policy changes",
                "milestones": [
                    "Multi-year outcomes published",
                    "Replication sites launched",
                    "Policy recommendations issued",
                    "Long-term sustainability secured",
                ],
                "status": "not_started",
            },
        ])

    return base_phases


def _generate_stakeholders(model: CoordinationModel, constraints: dict) -> list:
    """Generate stakeholder map based on model and domains."""
    domains = constraints.get("domains", [])
    geography = constraints.get("geography", "the jurisdiction")

    stakeholders = [
        {
            "name": "Government Executive",
            "role": "champion",
            "influence": "high",
            "interest": "high",
            "description": f"Mayor/County Executive of {geography} — authorizes funding and political cover",
            "engagement_strategy": "Regular briefings, visible wins, political credit",
        },
        {
            "name": "Lead Agency Director",
            "role": "owner",
            "influence": "high",
            "interest": "high",
            "description": "Director of lead implementing agency — operational authority",
            "engagement_strategy": "Co-design process, operational authority, performance incentives",
        },
        {
            "name": "Community Advocates",
            "role": "advisor",
            "influence": "moderate",
            "interest": "high",
            "description": "Advocacy organizations and community leaders — voice of affected populations",
            "engagement_strategy": "Advisory board seats, community forums, transparent reporting",
        },
    ]

    domain_stakeholders = {
        "health": {"name": "Health Department", "role": "partner", "influence": "high", "interest": "high",
                    "description": "Public health authority — regulatory oversight, data, workforce",
                    "engagement_strategy": "Data sharing agreements, co-governance, shared metrics"},
        "justice": {"name": "Courts / District Attorney", "role": "partner", "influence": "high", "interest": "moderate",
                    "description": "Justice system actors — diversion programs, data sharing, policy alignment",
                    "engagement_strategy": "Joint protocols, outcome data, cost savings evidence"},
        "housing": {"name": "Housing Authority", "role": "partner", "influence": "moderate", "interest": "high",
                    "description": "Public housing and homelessness services — housing-first integration",
                    "engagement_strategy": "Preference agreements, coordinated entry, shared case management"},
        "income": {"name": "Economic Development / DHS", "role": "partner", "influence": "moderate", "interest": "moderate",
                   "description": "Benefits, employment, and economic programs — income stability services",
                   "engagement_strategy": "Benefits enrollment integration, employment pipeline, data sharing"},
        "education": {"name": "School District", "role": "partner", "influence": "moderate", "interest": "moderate",
                      "description": "K-12 education system — early identification, student services, data",
                      "engagement_strategy": "FERPA-compliant data sharing, co-located services, joint interventions"},
        "child_welfare": {"name": "Child Welfare Agency", "role": "partner", "influence": "high", "interest": "high",
                          "description": "Child protective services, foster care, family support — child safety integration",
                          "engagement_strategy": "Shared case plans, co-investigation, family team meetings"},
    }

    for d in domains:
        if d in domain_stakeholders:
            stakeholders.append(domain_stakeholders[d])

    stakeholders.extend([
        {
            "name": "Provider Organizations",
            "role": "implementer",
            "influence": "moderate",
            "interest": "high",
            "description": "Service providers who will deliver coordinated care — FQHCs, hospitals, CBOs",
            "engagement_strategy": "Network agreements, incentive alignment, training, feedback loops",
        },
        {
            "name": "Payers / Insurers",
            "role": "funder",
            "influence": "high",
            "interest": "moderate",
            "description": "Medicaid MCOs, Medicare, commercial payers — funding and data",
            "engagement_strategy": "Value-based contracts, shared savings, data partnerships",
        },
    ])

    return stakeholders


def _generate_budget(model: CoordinationModel, constraints: dict) -> dict:
    """Generate budget breakdown."""
    total = constraints.get("annual_budget", 0)
    if total <= 0:
        total = 5000000  # default assumption

    return {
        "total_annual": total,
        "categories": [
            {"name": "Personnel & Workforce", "percentage": 45, "amount": round(total * 0.45), "description": "Staff salaries, benefits, training"},
            {"name": "Technology & Data", "percentage": 15, "amount": round(total * 0.15), "description": "IT systems, data integration, analytics platforms"},
            {"name": "Operations & Facilities", "percentage": 12, "amount": round(total * 0.12), "description": "Office space, transportation, supplies"},
            {"name": "Provider Payments", "percentage": 15, "amount": round(total * 0.15), "description": "Service delivery contracts, incentive payments"},
            {"name": "Administration & Governance", "percentage": 8, "amount": round(total * 0.08), "description": "Management, legal, compliance, reporting"},
            {"name": "Contingency & Innovation", "percentage": 5, "amount": round(total * 0.05), "description": "Reserves, pilot programs, quality improvement"},
        ],
        "funding_sources": json.loads(model.funding_sources or "[]"),
    }


def _generate_risks(model: CoordinationModel, constraints: dict) -> list:
    """Generate risk register."""
    political = constraints.get("political_context", "neutral")

    risks = [
        {
            "category": "political",
            "description": "Loss of political champion or change in administration",
            "likelihood": "high" if political in ("resistant", "hostile") else "moderate",
            "impact": "high",
            "mitigation": "Build bipartisan support, embed in legislation/regulation, demonstrate early wins",
        },
        {
            "category": "financial",
            "description": "Funding shortfall or delayed reimbursement",
            "likelihood": "moderate",
            "impact": "high",
            "mitigation": "Diversify funding sources, build reserves, phased implementation to match cash flow",
        },
        {
            "category": "operational",
            "description": "Workforce recruitment and retention challenges",
            "likelihood": "high",
            "impact": "moderate",
            "mitigation": "Competitive compensation, career pathways, partnerships with training programs",
        },
        {
            "category": "technical",
            "description": "Data integration failures or privacy breaches",
            "likelihood": "moderate",
            "impact": "high",
            "mitigation": "Phased data integration, robust security framework, privacy officer, incident response plan",
        },
        {
            "category": "regulatory",
            "description": "Regulatory approval delays or compliance issues",
            "likelihood": "moderate" if model.authority_type == "local_agreement" else "high",
            "impact": "moderate",
            "mitigation": "Early engagement with regulators, legal counsel, compliance monitoring",
        },
        {
            "category": "stakeholder",
            "description": "Agency resistance to coordination or data sharing",
            "likelihood": "high",
            "impact": "moderate",
            "mitigation": "Executive mandates, shared governance, demonstrate mutual benefit, start with willing partners",
        },
        {
            "category": "community",
            "description": "Community distrust or opposition to program",
            "likelihood": "moderate",
            "impact": "moderate",
            "mitigation": "Community advisory board, transparent communication, cultural competency, community health workers",
        },
    ]

    return risks


def _generate_workforce(model: CoordinationModel, constraints: dict) -> dict:
    """Generate workforce plan."""
    staffing = json.loads(model.staffing_model or "{}")
    population = constraints.get("population_size", 1000)

    roles = []
    for role, ratio in staffing.items():
        clean_role = role.replace("_", " ").title()
        roles.append({
            "title": clean_role,
            "ratio": ratio,
            "estimated_fte": _estimate_fte(ratio, population),
            "recruitment_timeline": "Months 4-8",
            "training_required": "40-80 hours initial + ongoing",
        })

    return {
        "total_estimated_fte": sum(r["estimated_fte"] for r in roles),
        "roles": roles,
        "training_approach": "Phased onboarding with cross-system orientation, model-specific certification, ongoing supervision",
        "retention_strategy": "Competitive salary, career ladders, peer support, manageable caseloads",
    }


def _estimate_fte(ratio: str, population: int) -> int:
    """Estimate FTEs from ratio string like '1:200 patients' or '1 per hub'."""
    import re
    s = str(ratio).lower()
    # "1 per hub" or "1 per site" => fixed count
    if "per hub" in s or "per site" in s or "per aco" in s or "per ccr" in s or "per sib" in s:
        nums = re.findall(r"\d+", s)
        return int(nums[0]) if nums else 1
    # "Independent third party" or non-numeric
    nums = re.findall(r"\d+", s)
    if not nums:
        return 1
    # If ratio references staff roles (CHWs, facilitators, etc.), it's a staff-to-staff ratio
    # e.g., "1:6-8 CHWs" means 1 supervisor per 6-8 CHWs, not per 6 population
    staff_refs = ["chw", "facilitator", "worker", "staff", "member"]
    is_staff_ratio = any(ref in s for ref in staff_refs)
    if len(nums) >= 2:
        staff = int(nums[0])
        per = int(nums[1])
        if per > 0:
            if is_staff_ratio:
                # Estimate based on a reasonable number of front-line workers, not population
                estimated_frontline = max(10, population // 75)
                return max(1, round(estimated_frontline / per * staff))
            return max(1, round(population / per * staff))
    elif len(nums) == 1:
        return int(nums[0])
    return 1


def _generate_authority_map(model: CoordinationModel, constraints: dict) -> dict:
    """Generate authority map — what authority is needed from whom."""
    authority_type = model.authority_type
    reqs = json.loads(model.regulatory_requirements or "[]")

    entries = []
    if authority_type == "federal_waiver":
        entries.append({
            "authority": "Federal CMS Approval",
            "grantor": "Centers for Medicare & Medicaid Services",
            "type": "Waiver/State Plan Amendment",
            "timeline": "6-12 months",
            "requirements": [r for r in reqs if "CMS" in r or "federal" in r.lower()],
            "status": "not_started",
        })
    if authority_type in ("federal_waiver", "state_plan"):
        entries.append({
            "authority": "State Medicaid Authority",
            "grantor": "State Medicaid Agency",
            "type": "State Plan Amendment or Waiver",
            "timeline": "3-9 months",
            "requirements": [r for r in reqs if "state" in r.lower() or "plan" in r.lower()],
            "status": "not_started",
        })

    entries.append({
        "authority": "Local Government Authorization",
        "grantor": "City/County Government",
        "type": "Executive order, ordinance, or budget appropriation",
        "timeline": "1-3 months",
        "requirements": ["Budget appropriation", "Agency designation"],
        "status": "not_started",
    })

    entries.append({
        "authority": "Data Sharing Authority",
        "grantor": "Participating agencies",
        "type": "Inter-agency data sharing agreements",
        "timeline": "2-6 months",
        "requirements": ["HIPAA BAA", "42 CFR Part 2 consent", "FERPA agreements", "CJIS compliance"],
        "status": "not_started",
    })

    entries.append({
        "authority": "Provider Network Authority",
        "grantor": "Provider organizations",
        "type": "Network participation agreements",
        "timeline": "3-6 months",
        "requirements": ["Credentialing", "Quality standards", "Reporting requirements"],
        "status": "not_started",
    })

    return {
        "primary_authority_type": authority_type,
        "entries": entries,
    }
