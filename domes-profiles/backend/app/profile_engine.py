"""
Profile Engine for DOMES Profiles.

Generates complete person profiles by aggregating data from upstream services
(domes-legal, domes-datamap, domes-profile-research) and local cost benchmarks.
Falls back to local benchmark data when upstreams are unavailable.
"""

import logging
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from . import upstream
from .models import Profile, ProfileDomain, ProfileVersion

logger = logging.getLogger(__name__)


# ===========================================================================
# Domain metadata
# ===========================================================================

DOMAIN_META: dict[str, dict] = {
    "health": {"label": "Health", "color": "#1A6B3C"},
    "justice": {"label": "Justice", "color": "#8B1A1A"},
    "housing": {"label": "Housing", "color": "#1A3D8B"},
    "income": {"label": "Income", "color": "#6B5A1A"},
    "education": {"label": "Education", "color": "#5A1A6B"},
    "child_welfare": {"label": "Child Welfare", "color": "#1A6B6B"},
}


# ===========================================================================
# Local benchmark cost data (used when upstreams are down)
# Per-system annual cost ranges and coordination savings percentages
# ===========================================================================

SYSTEM_BENCHMARKS: dict[str, dict] = {
    # Health
    "medicaid": {"domain": "health", "label": "Medicaid", "annual_cost": 12000, "coord_savings": 0.35},
    "bha": {"domain": "health", "label": "Behavioral Health", "annual_cost": 18000, "coord_savings": 0.45},
    "hie": {"domain": "health", "label": "Health Info Exchange", "annual_cost": 2000, "coord_savings": 0.60},
    "pdmp": {"domain": "health", "label": "Prescription Drug Monitoring", "annual_cost": 1500, "coord_savings": 0.50},
    "mco": {"domain": "health", "label": "Managed Care Org", "annual_cost": 14000, "coord_savings": 0.30},
    "va": {"domain": "health", "label": "VA Healthcare", "annual_cost": 22000, "coord_savings": 0.40},
    "er_frequent": {"domain": "health", "label": "Frequent ER Use", "annual_cost": 28000, "coord_savings": 0.65},
    # Justice
    "doc": {"domain": "justice", "label": "Dept of Corrections", "annual_cost": 15000, "coord_savings": 0.50},
    "probation": {"domain": "justice", "label": "Probation/Parole", "annual_cost": 5000, "coord_savings": 0.40},
    "court_cms": {"domain": "justice", "label": "Court Case Mgmt", "annual_cost": 3000, "coord_savings": 0.35},
    "juvenile_court": {"domain": "justice", "label": "Juvenile Court", "annual_cost": 8000, "coord_savings": 0.45},
    # Housing
    "hmis": {"domain": "housing", "label": "Homeless Info System", "annual_cost": 8000, "coord_savings": 0.55},
    "pha": {"domain": "housing", "label": "Public Housing Auth", "annual_cost": 9600, "coord_savings": 0.25},
    "shelter": {"domain": "housing", "label": "Emergency Shelter", "annual_cost": 12000, "coord_savings": 0.60},
    # Income
    "tanf": {"domain": "income", "label": "TANF", "annual_cost": 7200, "coord_savings": 0.30},
    "snap": {"domain": "income", "label": "SNAP", "annual_cost": 3600, "coord_savings": 0.20},
    "ssi": {"domain": "income", "label": "SSI", "annual_cost": 10200, "coord_savings": 0.25},
    "ssdi": {"domain": "income", "label": "SSDI", "annual_cost": 14400, "coord_savings": 0.25},
    "ssa": {"domain": "income", "label": "Social Security Admin", "annual_cost": 10200, "coord_savings": 0.25},
    "unemployment": {"domain": "income", "label": "Unemployment Comp", "annual_cost": 6000, "coord_savings": 0.30},
    # Education
    "iep": {"domain": "education", "label": "IEP / Special Ed", "annual_cost": 12000, "coord_savings": 0.35},
    "slds": {"domain": "education", "label": "Student Longitudinal Data", "annual_cost": 1500, "coord_savings": 0.50},
    # Child Welfare
    "sacwis": {"domain": "child_welfare", "label": "Child Welfare Info System", "annual_cost": 18000, "coord_savings": 0.45},
    "foster_care": {"domain": "child_welfare", "label": "Foster Care", "annual_cost": 22000, "coord_savings": 0.40},
}


# Map circumstance flags to relevant system IDs
CIRCUMSTANCE_SYSTEMS: dict[str, list[str]] = {
    "is_homeless": ["hmis", "shelter"],
    "has_housing_instability": ["hmis"],
    "is_section_8": ["pha"],
    "is_in_shelter": ["shelter"],
    "has_substance_use": ["bha", "pdmp"],
    "has_mental_illness": ["bha"],
    "has_chronic_health": ["hie", "mco"],
    "is_frequent_er": ["er_frequent", "hie"],
    "is_on_medicaid": ["medicaid", "mco"],
    "is_va_healthcare": ["va"],
    "is_dual_eligible": ["va", "medicaid"],
    "has_disability": ["ssa"],
    "is_incarcerated": ["doc"],
    "is_recently_released": ["doc", "probation"],
    "is_on_probation": ["probation"],
    "is_on_parole": ["probation"],
    "is_juvenile_justice": ["juvenile_court", "court_cms"],
    "has_dv_history": ["court_cms"],
    "is_on_tanf": ["tanf"],
    "is_on_snap": ["snap"],
    "is_on_ssi": ["ssi"],
    "is_on_ssdi": ["ssdi"],
    "is_unemployed": ["unemployment"],
    "is_in_foster_care": ["sacwis", "foster_care"],
    "has_child_in_foster": ["sacwis"],
    "is_aging_out_foster": ["sacwis", "foster_care"],
    "has_iep": ["iep", "slds"],
    "is_in_special_ed": ["iep"],
    "has_truancy": ["slds"],
    "is_school_age": ["slds"],
}


# Default gaps by domain
DEFAULT_GAPS: dict[str, list[dict]] = {
    "health": [
        {"id": "gap_health_1", "label": "No shared care plan across BH and primary care", "severity": "high"},
        {"id": "gap_health_2", "label": "ER visit data not linked to outpatient records", "severity": "high"},
        {"id": "gap_health_3", "label": "MCO authorization not visible to BH provider", "severity": "medium"},
    ],
    "justice": [
        {"id": "gap_justice_1", "label": "Reentry plan not shared with community providers", "severity": "high"},
        {"id": "gap_justice_2", "label": "Court dates not visible to housing or employment services", "severity": "medium"},
    ],
    "housing": [
        {"id": "gap_housing_1", "label": "HMIS and Medicaid not linked for housing-health coordination", "severity": "high"},
        {"id": "gap_housing_2", "label": "Section 8 status invisible to healthcare providers", "severity": "medium"},
    ],
    "income": [
        {"id": "gap_income_1", "label": "Benefits eligibility not cross-checked across programs", "severity": "high"},
        {"id": "gap_income_2", "label": "Employment data siloed from benefits systems", "severity": "medium"},
    ],
    "education": [
        {"id": "gap_education_1", "label": "IEP data not shared with behavioral health", "severity": "high"},
        {"id": "gap_education_2", "label": "School attendance not linked to child welfare", "severity": "medium"},
    ],
    "child_welfare": [
        {"id": "gap_cw_1", "label": "Foster placement data not shared with education system", "severity": "high"},
        {"id": "gap_cw_2", "label": "Child welfare history invisible at health encounters", "severity": "high"},
        {"id": "gap_cw_3", "label": "Court proceedings not linked to service plans", "severity": "medium"},
    ],
}


# Default bridges by domain
DEFAULT_BRIDGES: dict[str, list[dict]] = {
    "health": [
        {"id": "bridge_health_1", "label": "42 CFR Part 2 consent for SUD records sharing", "type": "consent", "impact": "high"},
        {"id": "bridge_health_2", "label": "HIE opt-in for cross-provider data access", "type": "consent", "impact": "high"},
    ],
    "justice": [
        {"id": "bridge_justice_1", "label": "Reentry data-sharing MOU between DOC and community providers", "type": "policy", "impact": "high"},
        {"id": "bridge_justice_2", "label": "Unified case management across justice and social services", "type": "technical", "impact": "medium"},
    ],
    "housing": [
        {"id": "bridge_housing_1", "label": "Coordinated entry with Medicaid enrollment linkage", "type": "technical", "impact": "high"},
        {"id": "bridge_housing_2", "label": "Housing status flag in healthcare EHR", "type": "technical", "impact": "medium"},
    ],
    "income": [
        {"id": "bridge_income_1", "label": "Automated benefits cross-enrollment (SNAP/TANF/Medicaid)", "type": "technical", "impact": "high"},
        {"id": "bridge_income_2", "label": "SSA data sharing agreement for disability determination", "type": "policy", "impact": "medium"},
    ],
    "education": [
        {"id": "bridge_education_1", "label": "IEP-BH data sharing consent under FERPA/HIPAA alignment", "type": "consent", "impact": "high"},
        {"id": "bridge_education_2", "label": "Student longitudinal data linked to workforce systems", "type": "technical", "impact": "medium"},
    ],
    "child_welfare": [
        {"id": "bridge_cw_1", "label": "Child welfare-education data match under ESSA provisions", "type": "policy", "impact": "high"},
        {"id": "bridge_cw_2", "label": "Unified family services plan shared across agencies", "type": "technical", "impact": "high"},
    ],
}


# Default provisions by domain (used when domes-legal is down)
DEFAULT_PROVISIONS: dict[str, list[dict]] = {
    "health": [
        {"id": "prov_h1", "title": "42 CFR Part 2 - SUD Record Confidentiality", "type": "federal"},
        {"id": "prov_h2", "title": "HIPAA Privacy Rule - Treatment/Payment/Operations", "type": "federal"},
        {"id": "prov_h3", "title": "ACA Section 2703 - Health Home Services", "type": "federal"},
        {"id": "prov_h4", "title": "Medicaid 1115 Waiver - SUD Treatment Coverage", "type": "state"},
    ],
    "justice": [
        {"id": "prov_j1", "title": "Second Chance Act - Reentry Programs", "type": "federal"},
        {"id": "prov_j2", "title": "CJRA - Criminal Justice Reform Act", "type": "federal"},
        {"id": "prov_j3", "title": "Medicaid Inmate Exclusion Policy - Suspension vs Termination", "type": "federal"},
    ],
    "housing": [
        {"id": "prov_ho1", "title": "McKinney-Vento Act - Homeless Assistance", "type": "federal"},
        {"id": "prov_ho2", "title": "HEARTH Act - Continuum of Care", "type": "federal"},
        {"id": "prov_ho3", "title": "Section 8 Housing Choice Voucher Program", "type": "federal"},
    ],
    "income": [
        {"id": "prov_i1", "title": "TANF Block Grant - Temporary Assistance", "type": "federal"},
        {"id": "prov_i2", "title": "SNAP - Supplemental Nutrition Assistance", "type": "federal"},
        {"id": "prov_i3", "title": "SSI/SSDI - Disability Benefits", "type": "federal"},
    ],
    "education": [
        {"id": "prov_e1", "title": "IDEA - Individuals with Disabilities Education Act", "type": "federal"},
        {"id": "prov_e2", "title": "FERPA - Student Records Privacy", "type": "federal"},
        {"id": "prov_e3", "title": "ESSA - Every Student Succeeds Act", "type": "federal"},
    ],
    "child_welfare": [
        {"id": "prov_cw1", "title": "Title IV-E - Foster Care Assistance", "type": "federal"},
        {"id": "prov_cw2", "title": "Title IV-B - Child & Family Services", "type": "federal"},
        {"id": "prov_cw3", "title": "CAPTA - Child Abuse Prevention & Treatment Act", "type": "federal"},
        {"id": "prov_cw4", "title": "ICWA - Indian Child Welfare Act", "type": "federal"},
    ],
}


# ===========================================================================
# Available circumstances registry
# ===========================================================================

AVAILABLE_CIRCUMSTANCES: list[dict] = [
    # Housing
    {"key": "is_homeless", "label": "Currently Homeless", "category": "housing"},
    {"key": "has_housing_instability", "label": "Housing Instability", "category": "housing"},
    {"key": "is_section_8", "label": "Section 8 Voucher", "category": "housing"},
    {"key": "is_in_shelter", "label": "In Emergency Shelter", "category": "housing"},
    # Health
    {"key": "has_substance_use", "label": "Substance Use Disorder", "category": "health"},
    {"key": "has_mental_illness", "label": "Serious Mental Illness", "category": "health"},
    {"key": "has_chronic_health", "label": "Chronic Health Conditions", "category": "health"},
    {"key": "is_frequent_er", "label": "Frequent ER Utilizer", "category": "health"},
    {"key": "is_on_medicaid", "label": "On Medicaid", "category": "health"},
    {"key": "is_va_healthcare", "label": "VA Healthcare", "category": "health"},
    {"key": "is_dual_eligible", "label": "Dual Eligible (Medicare+Medicaid)", "category": "health"},
    {"key": "has_disability", "label": "Has Disability", "category": "health"},
    # Justice
    {"key": "is_incarcerated", "label": "Currently Incarcerated", "category": "justice"},
    {"key": "is_recently_released", "label": "Recently Released from Incarceration", "category": "justice"},
    {"key": "is_on_probation", "label": "On Probation", "category": "justice"},
    {"key": "is_on_parole", "label": "On Parole", "category": "justice"},
    {"key": "is_juvenile_justice", "label": "Juvenile Justice Involved", "category": "justice"},
    {"key": "has_dv_history", "label": "Domestic Violence History", "category": "justice"},
    # Income
    {"key": "is_on_tanf", "label": "Receiving TANF", "category": "income"},
    {"key": "is_on_snap", "label": "Receiving SNAP", "category": "income"},
    {"key": "is_on_ssi", "label": "Receiving SSI", "category": "income"},
    {"key": "is_on_ssdi", "label": "Receiving SSDI", "category": "income"},
    {"key": "is_unemployed", "label": "Unemployed", "category": "income"},
    # Child Welfare
    {"key": "is_in_foster_care", "label": "In Foster Care", "category": "child_welfare"},
    {"key": "has_child_in_foster", "label": "Child in Foster Care", "category": "child_welfare"},
    {"key": "is_aging_out_foster", "label": "Aging Out of Foster Care", "category": "child_welfare"},
    # Education
    {"key": "has_iep", "label": "Has IEP", "category": "education"},
    {"key": "is_in_special_ed", "label": "In Special Education", "category": "education"},
    {"key": "has_truancy", "label": "Truancy Issues", "category": "education"},
    {"key": "is_school_age", "label": "School Age", "category": "education"},
]


# ===========================================================================
# Narrative generation (local fallback)
# ===========================================================================

def _build_narrative(name: str, circumstances: dict, systems: list[str], total_cost: float, savings: float) -> str:
    """Build a human-readable narrative about this person's profile."""
    active = [c["label"] for c in AVAILABLE_CIRCUMSTANCES if circumstances.get(c["key"])]
    domains_involved = set()
    for c in AVAILABLE_CIRCUMSTANCES:
        if circumstances.get(c["key"]):
            domains_involved.add(c["category"])

    n_systems = len(systems)
    n_domains = len(domains_involved)
    domain_labels = sorted([DOMAIN_META.get(d, {}).get("label", d) for d in domains_involved])

    lines = []
    lines.append(
        f"{name} is currently navigating {n_systems} separate government systems "
        f"across {n_domains} domains: {', '.join(domain_labels)}."
    )

    if active:
        lines.append(
            f"Key circumstances include: {', '.join(active[:6])}{'...' if len(active) > 6 else ''}."
        )

    lines.append(
        f"The estimated annual cost of serving {name} in today's fragmented system is "
        f"${total_cost:,.0f}. With coordinated data sharing and integrated case management, "
        f"that cost could be reduced by ${savings:,.0f} per year — a "
        f"{(savings / total_cost * 100):.0f}% reduction." if total_cost > 0 else
        f"Cost data is being calculated."
    )

    lines.append(
        "Each of these systems maintains its own records, its own intake process, "
        "and its own eligibility rules — creating redundancy, delay, and risk of "
        "people falling through the cracks."
    )

    return " ".join(lines)


# ===========================================================================
# Core engine functions
# ===========================================================================

def _resolve_systems(circumstances: dict) -> list[str]:
    """Determine which system IDs are relevant given circumstances."""
    system_ids: set[str] = set()
    for key, value in circumstances.items():
        if value and key in CIRCUMSTANCE_SYSTEMS:
            for sid in CIRCUMSTANCE_SYSTEMS[key]:
                system_ids.add(sid)
    return sorted(system_ids)


def _aggregate_by_domain(
    system_ids: list[str],
    upstream_provisions: dict[str, list[dict]],
    upstream_gaps: list[dict],
    upstream_bridges: list[dict],
    consent_pathways: list[dict],
) -> dict[str, dict]:
    """
    Group systems, costs, provisions, gaps, and bridges by domain.
    Returns {domain: {systems, annual_cost, coordinated_cost, provisions, gaps, bridges}}.
    """
    domain_data: dict[str, dict] = {}

    # Initialize from system benchmarks
    for sid in system_ids:
        bench = SYSTEM_BENCHMARKS.get(sid)
        if not bench:
            continue
        domain = bench["domain"]
        if domain not in domain_data:
            domain_data[domain] = {
                "systems": [],
                "annual_cost": 0.0,
                "coordinated_cost": 0.0,
                "provisions": [],
                "gaps": [],
                "bridges": [],
            }
        entry = domain_data[domain]
        entry["systems"].append({
            "id": sid,
            "label": bench["label"],
            "annual_cost": bench["annual_cost"],
            "coord_savings_pct": bench["coord_savings"],
        })
        entry["annual_cost"] += bench["annual_cost"]
        coordinated = bench["annual_cost"] * (1 - bench["coord_savings"])
        entry["coordinated_cost"] += coordinated

    # Add provisions from upstream or defaults
    for domain in domain_data:
        if domain in upstream_provisions and upstream_provisions[domain]:
            domain_data[domain]["provisions"] = upstream_provisions[domain][:5]
        else:
            domain_data[domain]["provisions"] = DEFAULT_PROVISIONS.get(domain, [])

    # Add gaps from upstream or defaults
    if upstream_gaps:
        for gap in upstream_gaps:
            gap_domain = gap.get("domain", "health")
            if gap_domain in domain_data:
                domain_data[gap_domain]["gaps"].append(gap)
    else:
        for domain in domain_data:
            domain_data[domain]["gaps"] = DEFAULT_GAPS.get(domain, [])[:2]

    # Add bridges from upstream or defaults, plus consent pathways
    if upstream_bridges:
        for bridge in upstream_bridges:
            b_domain = bridge.get("domain", "health")
            if b_domain in domain_data:
                domain_data[b_domain]["bridges"].append(bridge)
    else:
        for domain in domain_data:
            domain_data[domain]["bridges"] = DEFAULT_BRIDGES.get(domain, [])[:2]

    # Merge consent pathways into bridges
    for pathway in consent_pathways:
        p_domain = pathway.get("domain", "health")
        if p_domain in domain_data:
            domain_data[p_domain]["bridges"].append({
                "id": pathway.get("id", f"consent_{p_domain}"),
                "label": pathway.get("label", pathway.get("description", "Consent pathway")),
                "type": "consent",
                "impact": pathway.get("impact", "high"),
            })

    return domain_data


async def generate_profile(
    circumstances: dict,
    db: Session,
    name: str | None = None,
) -> Profile:
    """
    Generate a complete profile from circumstances.
    Calls upstream services and falls back to local benchmarks on failure.
    """
    # 1. Determine systems from circumstances
    system_ids = _resolve_systems(circumstances)
    circ_list = upstream.circumstances_to_list(circumstances)

    # 2. Call upstream services (all tolerant of failure)
    person_map = await upstream.fetch_person_map(circ_list)
    composite = await upstream.fetch_composite_profile(circumstances)
    provisions_by_domain = await upstream.fetch_provisions_for_profile(circumstances)
    consent_pathways = await upstream.fetch_consent_pathways(circ_list)

    # Merge upstream systems with local resolution
    upstream_systems = person_map.get("systems", [])
    if upstream_systems:
        for s in upstream_systems:
            sid = s.get("id", "")
            if sid and sid not in system_ids:
                system_ids.append(sid)

    upstream_gaps = person_map.get("gaps", [])
    upstream_bridges = person_map.get("bridges", [])

    # 3. Aggregate by domain
    domain_data = _aggregate_by_domain(
        system_ids, provisions_by_domain, upstream_gaps, upstream_bridges, consent_pathways
    )

    # 4. Calculate totals
    total_annual = sum(d["annual_cost"] for d in domain_data.values())
    total_coordinated = sum(d["coordinated_cost"] for d in domain_data.values())
    total_savings = total_annual - total_coordinated

    # Use upstream cost data if available and reasonable
    if composite.get("total_annual_cost") and composite["total_annual_cost"] > 0:
        total_annual = composite["total_annual_cost"]
    if composite.get("coordinated_annual_cost") and composite["coordinated_annual_cost"] > 0:
        total_coordinated = composite["coordinated_annual_cost"]
        total_savings = total_annual - total_coordinated

    five_year = total_savings * 5
    # Lifetime estimate: assume 20-year horizon with 2% annual growth
    lifetime = total_savings * 20 * 1.02

    # 5. Build narrative
    narrative = composite.get("narrative", "")
    if not narrative:
        profile_name = name or "This person"
        narrative = _build_narrative(profile_name, circumstances, system_ids, total_annual, total_savings)

    # 6. Create Profile record
    profile = Profile(
        id=str(uuid.uuid4()),
        name=name or "Unnamed Profile",
        version=1,
        circumstances=circumstances,
        systems_involved=system_ids,
        total_annual_cost=round(total_annual, 2),
        coordinated_annual_cost=round(total_coordinated, 2),
        savings_annual=round(total_savings, 2),
        five_year_projection=round(five_year, 2),
        lifetime_estimate=round(lifetime, 2),
        narrative=narrative,
        is_sample=False,
    )
    db.add(profile)

    # 7. Create ProfileDomain records
    for domain_key, data in domain_data.items():
        meta = DOMAIN_META.get(domain_key, {"label": domain_key.title()})
        pd = ProfileDomain(
            profile_id=profile.id,
            domain=domain_key,
            domain_label=meta["label"],
            systems=data["systems"],
            provisions_count=len(data["provisions"]),
            annual_cost=round(data["annual_cost"], 2),
            coordinated_cost=round(data["coordinated_cost"], 2),
            savings=round(data["annual_cost"] - data["coordinated_cost"], 2),
            top_provisions=data["provisions"],
            gaps=data["gaps"],
            bridges=data["bridges"],
        )
        db.add(pd)

    db.commit()
    db.refresh(profile)
    return profile


async def update_profile(
    profile_id: str,
    new_circumstances: dict,
    db: Session,
) -> Profile:
    """
    Update a profile with new circumstances.
    Saves old version, increments version number, regenerates data.
    """
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise ValueError(f"Profile {profile_id} not found")

    # Save current version to history
    version_record = ProfileVersion(
        profile_id=profile.id,
        version=profile.version,
        circumstances=profile.circumstances,
        total_annual_cost=profile.total_annual_cost,
        coordinated_annual_cost=profile.coordinated_annual_cost,
        change_description=f"Version {profile.version} before update",
    )
    db.add(version_record)

    # Merge old + new circumstances
    merged = dict(profile.circumstances or {})
    merged.update(new_circumstances)

    # Regenerate system resolution and costs
    system_ids = _resolve_systems(merged)
    circ_list = upstream.circumstances_to_list(merged)

    person_map = await upstream.fetch_person_map(circ_list)
    composite = await upstream.fetch_composite_profile(merged)
    provisions_by_domain = await upstream.fetch_provisions_for_profile(merged)
    consent_pathways = await upstream.fetch_consent_pathways(circ_list)

    upstream_gaps = person_map.get("gaps", [])
    upstream_bridges = person_map.get("bridges", [])

    domain_data = _aggregate_by_domain(
        system_ids, provisions_by_domain, upstream_gaps, upstream_bridges, consent_pathways
    )

    total_annual = sum(d["annual_cost"] for d in domain_data.values())
    total_coordinated = sum(d["coordinated_cost"] for d in domain_data.values())
    total_savings = total_annual - total_coordinated

    if composite.get("total_annual_cost") and composite["total_annual_cost"] > 0:
        total_annual = composite["total_annual_cost"]
    if composite.get("coordinated_annual_cost") and composite["coordinated_annual_cost"] > 0:
        total_coordinated = composite["coordinated_annual_cost"]
        total_savings = total_annual - total_coordinated

    five_year = total_savings * 5
    lifetime = total_savings * 20 * 1.02

    narrative = composite.get("narrative", "")
    if not narrative:
        narrative = _build_narrative(profile.name, merged, system_ids, total_annual, total_savings)

    # Update profile
    profile.version += 1
    profile.circumstances = merged
    profile.systems_involved = system_ids
    profile.total_annual_cost = round(total_annual, 2)
    profile.coordinated_annual_cost = round(total_coordinated, 2)
    profile.savings_annual = round(total_savings, 2)
    profile.five_year_projection = round(five_year, 2)
    profile.lifetime_estimate = round(lifetime, 2)
    profile.narrative = narrative
    profile.updated_at = datetime.now(timezone.utc)

    # Replace domain records
    for old_domain in profile.domains:
        db.delete(old_domain)

    for domain_key, data in domain_data.items():
        meta = DOMAIN_META.get(domain_key, {"label": domain_key.title()})
        pd = ProfileDomain(
            profile_id=profile.id,
            domain=domain_key,
            domain_label=meta["label"],
            systems=data["systems"],
            provisions_count=len(data["provisions"]),
            annual_cost=round(data["annual_cost"], 2),
            coordinated_cost=round(data["coordinated_cost"], 2),
            savings=round(data["annual_cost"] - data["coordinated_cost"], 2),
            top_provisions=data["provisions"],
            gaps=data["gaps"],
            bridges=data["bridges"],
        )
        db.add(pd)

    db.commit()
    db.refresh(profile)
    return profile


def compare_profiles(profile_id_1: str, profile_id_2: str, db: Session) -> dict:
    """
    Side-by-side comparison of two profiles.
    Returns differences in systems, costs, gaps, and savings.
    """
    p1 = db.query(Profile).filter(Profile.id == profile_id_1).first()
    p2 = db.query(Profile).filter(Profile.id == profile_id_2).first()

    if not p1 or not p2:
        missing = []
        if not p1:
            missing.append(profile_id_1)
        if not p2:
            missing.append(profile_id_2)
        raise ValueError(f"Profile(s) not found: {', '.join(missing)}")

    def _profile_summary(p: Profile) -> dict:
        domains_dict = {}
        for d in p.domains:
            domains_dict[d.domain] = {
                "domain_label": d.domain_label,
                "systems_count": len(d.systems or []),
                "systems": [s.get("label", s.get("id", "")) for s in (d.systems or [])],
                "annual_cost": d.annual_cost,
                "coordinated_cost": d.coordinated_cost,
                "savings": d.savings,
                "provisions_count": d.provisions_count,
                "gaps_count": len(d.gaps or []),
                "bridges_count": len(d.bridges or []),
            }
        return {
            "id": p.id,
            "name": p.name,
            "circumstances": p.circumstances or {},
            "systems_involved": p.systems_involved or [],
            "total_annual_cost": p.total_annual_cost,
            "coordinated_annual_cost": p.coordinated_annual_cost,
            "savings_annual": p.savings_annual,
            "five_year_projection": p.five_year_projection,
            "lifetime_estimate": p.lifetime_estimate,
            "domains": domains_dict,
        }

    s1 = _profile_summary(p1)
    s2 = _profile_summary(p2)

    # Compute differences
    all_domains = sorted(set(list(s1["domains"].keys()) + list(s2["domains"].keys())))
    domain_diffs = {}
    for domain in all_domains:
        d1 = s1["domains"].get(domain)
        d2 = s2["domains"].get(domain)
        domain_diffs[domain] = {
            "profile_1": d1,
            "profile_2": d2,
            "cost_difference": (
                (d1["annual_cost"] if d1 else 0) - (d2["annual_cost"] if d2 else 0)
            ),
            "savings_difference": (
                (d1["savings"] if d1 else 0) - (d2["savings"] if d2 else 0)
            ),
        }

    systems_1 = set(s1["systems_involved"])
    systems_2 = set(s2["systems_involved"])

    return {
        "profile_1": s1,
        "profile_2": s2,
        "differences": {
            "cost_difference": s1["total_annual_cost"] - s2["total_annual_cost"],
            "savings_difference": s1["savings_annual"] - s2["savings_annual"],
            "systems_only_in_1": sorted(systems_1 - systems_2),
            "systems_only_in_2": sorted(systems_2 - systems_1),
            "systems_shared": sorted(systems_1 & systems_2),
            "domains": domain_diffs,
        },
    }


def get_dome(profile_id: str, db: Session) -> dict:
    """
    Build the full Dome visualization structure for a profile.
    """
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise ValueError(f"Profile {profile_id} not found")

    domains_list = []
    total_gaps = 0
    total_consent_closable = 0
    total_systems = 0

    for d in profile.domains:
        meta = DOMAIN_META.get(d.domain, {"label": d.domain.title(), "color": "#666666"})
        gaps = d.gaps or []
        bridges = d.bridges or []
        consent_bridges = [b for b in bridges if b.get("type") == "consent"]

        total_gaps += len(gaps)
        total_consent_closable += len(consent_bridges)
        total_systems += len(d.systems or [])

        domains_list.append({
            "domain": d.domain,
            "label": meta["label"],
            "color": meta["color"],
            "systems": d.systems or [],
            "provisions": d.top_provisions or [],
            "gaps": gaps,
            "bridges": bridges,
            "annual_cost": d.annual_cost,
            "coordinated_cost": d.coordinated_cost,
            "savings": d.savings,
        })

    # Build cross-domain connections (systems that appear in multiple domains)
    system_domains: dict[str, list[str]] = {}
    for d in profile.domains:
        for s in (d.systems or []):
            sid = s.get("id", "")
            if sid:
                system_domains.setdefault(sid, []).append(d.domain)
    connections = []
    for sid, domains in system_domains.items():
        if len(domains) > 1:
            for i in range(len(domains)):
                for j in range(i + 1, len(domains)):
                    connections.append({
                        "source_domain": domains[i],
                        "target_domain": domains[j],
                        "system": sid,
                        "label": SYSTEM_BENCHMARKS.get(sid, {}).get("label", sid),
                    })

    # Build consent pathways from consent-type bridges
    consent_pathways = []
    for d in domains_list:
        for b in d.get("bridges", []):
            if b.get("type") == "consent":
                consent_pathways.append({
                    "domain": d["domain"],
                    "bridge_id": b.get("id", ""),
                    "label": b.get("label", ""),
                    "impact": b.get("impact", "medium"),
                })

    return {
        "profile": profile.to_full(),
        "domains": domains_list,
        "totals": {
            "annual_cost": profile.total_annual_cost,
            "coordinated_cost": profile.coordinated_annual_cost,
            "savings": profile.savings_annual,
            "five_year": profile.five_year_projection,
            "lifetime": profile.lifetime_estimate,
            "systems_count": total_systems,
            "gaps_count": total_gaps,
            "consent_closable": total_consent_closable,
        },
        "connections": connections,
        "consent_pathways": consent_pathways,
    }
