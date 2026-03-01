"""
BATHS Data Engine — Federal Performance Indicators (APP/APR/CAP/APG)

Ingests the FY2026 master list of citizen-facing federal performance metrics
from three authoritative sources:

1. Performance.gov CAP/APG goals — Cross-Agency Priority Goals and Agency
   Priority Goals from the President's Management Agenda.

2. Agency APP/APR publications — machine-readable Annual Performance Plans
   and Annual Performance Reports required by GPRA Modernization Act of 2010
   (31 USC §1115-1116).  Each publication contains Performance Goals →
   Performance Indicators → Targets/Actuals.

3. Citizen-metric filter — keeps indicators whose beneficiary_population is
   the public (people, households, patients, students, travelers, veterans,
   taxpayers) and excludes purely internal enablers unless they explicitly
   measure a public service level or outcome.

API sources (all public, no auth):
  - Performance.gov API (performance.gov)
  - Agency APR/APP pages (machine-readable JSON/XML when available)
  - MAX.gov GPRA performance data feeds
  - USASpending.gov program-level performance links

The citizen-metric filter classifies each indicator by testing:
  - beneficiary_population: must name a public group, not an internal process
  - indicator_name: must describe a public outcome or service level
  - Excludes: workforce training completion, IT uptime, procurement speed,
    hiring targets, internal audit compliance, etc.
"""

import logging
import re
from typing import Any

from .scraper import BaseScraper
from .store import DataStore, get_store

logger = logging.getLogger("baths.performance")


# ══════════════════════════════════════════════════════════════════════════════
# CITIZEN-METRIC FILTER
# ══════════════════════════════════════════════════════════════════════════════

# Populations that are "the public" — if an indicator's beneficiary matches
# any of these, it passes the citizen filter.
CITIZEN_POPULATIONS = {
    "people", "persons", "individuals", "americans", "residents",
    "households", "families", "children", "infants", "youth", "adolescents",
    "adults", "elderly", "seniors", "older adults",
    "patients", "beneficiaries", "enrollees", "recipients", "claimants",
    "students", "learners", "graduates",
    "veterans", "service members", "military families",
    "travelers", "passengers", "drivers", "motorists", "pedestrians",
    "taxpayers", "filers", "small businesses", "farmers", "ranchers",
    "homeowners", "renters", "tenants", "homeless persons",
    "workers", "employees", "job seekers", "unemployed",
    "immigrants", "refugees", "asylum seekers",
    "victims", "survivors",
    "communities", "tribes", "tribal members",
    "consumers", "borrowers",
    "disabled persons", "persons with disabilities",
}

# Internal-enabler keywords — if the indicator name contains these AND the
# beneficiary is not a public group, it's an internal enabler.
INTERNAL_ENABLER_PATTERNS = [
    r"\bworkforce\s+training\b",
    r"\bIT\s+uptime\b",
    r"\bsystem\s+availability\b",
    r"\bprocurement\s+(?:speed|cycle|time)\b",
    r"\bhiring\s+(?:target|timeline|speed)\b",
    r"\binternal\s+audit\b",
    r"\bstaff\s+(?:retention|turnover|satisfaction)\b",
    r"\bFTE\s+(?:count|utilization)\b",
    r"\bcontract\s+(?:award|obligation)\s+(?:rate|time)\b",
    r"\badministrative\s+(?:cost|overhead|efficiency)\b",
    r"\bEO\s+compliance\b",
    r"\bcybersecurity\s+(?:score|posture)\b",
    r"\bdata\s+center\s+(?:consolidation|migration)\b",
    r"\bcustomer\s+experience\s+(?:of\s+)?(?:agency\s+)?staff\b",
]
_INTERNAL_RE = re.compile("|".join(INTERNAL_ENABLER_PATTERNS), re.IGNORECASE)

# Public-outcome keywords — if indicator name contains these, it's likely
# citizen-facing even if the beneficiary field is ambiguous.
PUBLIC_OUTCOME_PATTERNS = [
    r"\bmortality\b", r"\blife\s+expectancy\b", r"\binfant\s+death\b",
    r"\bpoverty\s+rate\b", r"\bhomelessness\b", r"\bfood\s+(?:insecurity|security)\b",
    r"\buninsured\s+rate\b", r"\bvaccination\s+(?:rate|coverage)\b",
    r"\bliteracy\b", r"\bgraduation\s+rate\b", r"\bdropout\b",
    r"\bunemployment\s+rate\b", r"\bcrime\s+rate\b", r"\brecidivism\b",
    r"\bwait(?:ing)?\s+time\b", r"\baccess\s+to\b", r"\bservice\s+level\b",
    r"\bbenefits?\s+(?:processing|determination|decision)\s+time\b",
    r"\bclaims?\s+(?:processing|backlog|pending)\b",
    r"\bwater\s+quality\b", r"\bair\s+quality\b", r"\bsuperfund\b",
    r"\bdisaster\s+(?:response|recovery|assistance)\b",
    r"\bhospital\s+(?:readmission|infection|acquired)\b",
    r"\bopioid\b", r"\boverdose\b", r"\bsubstance\s+(?:use|abuse)\b",
    r"\bhousing\s+(?:voucher|assistance|affordab)\b",
    r"\bSNAP\b", r"\bWIC\b", r"\bMedicaid\b", r"\bMedicare\b",
    r"\bSocial\s+Security\b", r"\bSSI\b", r"\bSSA\b",
    r"\btax\s+(?:refund|filing|gap|compliance)\b",
    r"\bbroadband\b", r"\binternet\s+access\b",
]
_PUBLIC_RE = re.compile("|".join(PUBLIC_OUTCOME_PATTERNS), re.IGNORECASE)


def is_citizen_facing(indicator_name: str, beneficiary_population: str | None,
                      goal_name: str = "") -> bool:
    """Determine whether a performance indicator is citizen-facing.

    Rules:
      1. If beneficiary_population names a public group → citizen-facing.
      2. If indicator_name matches a public-outcome pattern → citizen-facing.
      3. If indicator_name matches an internal-enabler pattern AND
         beneficiary is not public → NOT citizen-facing.
      4. Default: not citizen-facing (conservative).
    """
    beneficiary = (beneficiary_population or "").lower().strip()

    # Rule 1: explicit public beneficiary
    if beneficiary:
        tokens = set(re.split(r"[,;/\s]+", beneficiary))
        if tokens & CITIZEN_POPULATIONS:
            # But check if it's actually internal despite public-sounding name
            if _INTERNAL_RE.search(indicator_name):
                return False
            return True

    # Rule 2: public-outcome keyword in indicator or goal
    combined = f"{indicator_name} {goal_name}"
    if _PUBLIC_RE.search(combined):
        return True

    # Rule 3: internal enabler
    if _INTERNAL_RE.search(indicator_name):
        return False

    # Rule 4: conservative default
    return False


# Map agency to dome dimension(s)
AGENCY_DOME_MAP = {
    "HHS": "health",
    "CMS": "health",
    "CDC": "health",
    "FDA": "health",
    "NIH": "health",
    "SAMHSA": "health",
    "HRSA": "health",
    "IHS": "health",
    "ACF": "health",
    "HUD": "housing",
    "ED": "education",
    "DOL": "economics",
    "ETA": "economics",
    "SSA": "economics",
    "USDA": "nutrition",
    "FNS": "nutrition",
    "VA": "health",
    "VBA": "economics",
    "VHA": "health",
    "DOJ": "safety",
    "BOP": "safety",
    "DOT": "transportation",
    "FHWA": "transportation",
    "FAA": "transportation",
    "FTA": "transportation",
    "EPA": "environment",
    "DOE": "infrastructure",
    "IRS": "economics",
    "Treasury": "economics",
    "SBA": "economics",
    "DHS": "safety",
    "FEMA": "safety",
    "USCIS": "legal",
    "DOI": "environment",
    "USDA-FS": "environment",
    "USDA-NRCS": "environment",
    "OPM": None,  # purely internal
    "GSA": None,
    "OMB": None,
}


def _dome_dimension_for(agency_code: str, indicator_name: str) -> str | None:
    """Infer dome dimension from agency + indicator text."""
    dim = AGENCY_DOME_MAP.get(agency_code)
    if dim:
        return dim

    text = indicator_name.lower()
    keyword_map = {
        "health": ["health", "medical", "hospital", "vaccination", "disease",
                    "mortality", "opioid", "overdose", "mental health"],
        "housing": ["housing", "homeless", "shelter", "rent", "voucher", "HUD"],
        "education": ["education", "school", "student", "graduation", "literacy",
                       "Pell", "FAFSA", "college"],
        "economics": ["employment", "unemployment", "poverty", "income", "wage",
                        "job", "workforce", "benefits", "SSI", "SNAP", "tax"],
        "nutrition": ["food", "nutrition", "hunger", "WIC", "SNAP", "meal"],
        "safety": ["crime", "violence", "recidivism", "incarceration", "victim",
                    "disaster", "emergency"],
        "transportation": ["transit", "highway", "traffic", "fatality", "aviation"],
        "environment": ["air quality", "water quality", "pollution", "superfund",
                         "emissions", "climate", "conservation"],
        "infrastructure": ["broadband", "internet", "energy", "grid", "telecom"],
        "legal": ["immigration", "asylum", "citizenship", "civil rights",
                   "disability rights", "ADA"],
        "community": ["community", "tribal", "civic", "volunteer", "nonprofit"],
    }

    for domain, keywords in keyword_map.items():
        for kw in keywords:
            if kw.lower() in text:
                return domain

    return None


# ══════════════════════════════════════════════════════════════════════════════
# FY2026 SEED DATA — Authoritative federal performance indicators
#
# Sources:
#   - Performance.gov CAP Goals (President's Management Agenda FY2022-2026)
#   - Published Agency Priority Goals (APGs) for FY2024-2025
#   - Major agency APP/APR indicators from FY2025 publications
#
# Each record follows the schema: goal → indicator → target/actual.
# The citizen_facing flag is computed by is_citizen_facing() at seed time.
# ══════════════════════════════════════════════════════════════════════════════

SEED_PERFORMANCE_INDICATORS: list[dict[str, Any]] = [

    # ──────────────────────────────────────────────────────────────────────
    # CROSS-AGENCY PRIORITY (CAP) GOALS — Performance.gov
    # ──────────────────────────────────────────────────────────────────────

    # CAP Goal: Improving Customer Experience
    {
        "indicator_id": "CAP-CX-trust",
        "agency_code": "OMB", "agency_name": "Office of Management and Budget",
        "fiscal_year": 2026, "source_type": "cap_goal",
        "goal_name": "Improving Customer Experience and Service Delivery (CAP Goal)",
        "goal_id": "CAP-CX", "strategic_objective": "President's Management Agenda",
        "indicator_name": "Percentage of designated High-Impact Service Providers (HISPs) that improve customer trust scores",
        "indicator_unit": "%", "target_value": 75, "actual_value": 62,
        "actual_year": 2024, "baseline_value": 50, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "people",
        "data_source": "OMB HISP Trust Score Survey",
        "publication_url": "https://www.performance.gov/cx/",
        "tags": ["customer_experience", "trust", "service_delivery"],
    },
    {
        "indicator_id": "CAP-CX-digital",
        "agency_code": "OMB", "agency_name": "Office of Management and Budget",
        "fiscal_year": 2026, "source_type": "cap_goal",
        "goal_name": "Improving Customer Experience and Service Delivery (CAP Goal)",
        "goal_id": "CAP-CX", "strategic_objective": "President's Management Agenda",
        "indicator_name": "Number of life experiences with redesigned federal service delivery",
        "indicator_unit": "count", "target_value": 36, "actual_value": 28,
        "actual_year": 2024, "baseline_value": 0, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "people",
        "data_source": "OMB Life Experience Design Tracker",
        "publication_url": "https://www.performance.gov/cx/",
        "tags": ["customer_experience", "digital", "life_experiences"],
    },

    # CAP Goal: Equity
    {
        "indicator_id": "CAP-EQ-access",
        "agency_code": "OMB", "agency_name": "Office of Management and Budget",
        "fiscal_year": 2026, "source_type": "cap_goal",
        "goal_name": "Advancing Equity (CAP Goal)",
        "goal_id": "CAP-EQ", "strategic_objective": "President's Management Agenda",
        "indicator_name": "Percentage of equity action plans with measurable outcomes for underserved communities",
        "indicator_unit": "%", "target_value": 100, "actual_value": 75,
        "actual_year": 2024, "baseline_value": 0, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "communities",
        "data_source": "Agency Equity Action Plans",
        "publication_url": "https://www.performance.gov/equity/",
        "tags": ["equity", "underserved", "access"],
    },

    # ──────────────────────────────────────────────────────────────────────
    # HHS — Health and Human Services
    # ──────────────────────────────────────────────────────────────────────

    # APG: Reduce Opioid Overdose Deaths
    {
        "indicator_id": "HHS-APG-opioid-deaths",
        "agency_code": "HHS", "agency_name": "Department of Health and Human Services",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Reduce opioid overdose deaths through prevention, treatment, and recovery",
        "goal_id": "HHS-APG-5.1", "strategic_objective": "SO 5.1: Combat opioid crisis",
        "indicator_name": "Number of opioid overdose deaths (annual)",
        "indicator_unit": "count", "target_value": 70000, "actual_value": 81083,
        "actual_year": 2024, "baseline_value": 80411, "baseline_year": 2021,
        "trend": "improving",
        "beneficiary_population": "people",
        "data_source": "CDC WONDER Provisional Mortality",
        "publication_url": "https://www.performance.gov/agencies/hhs/",
        "tags": ["opioid", "overdose", "mortality", "substance_use"],
    },
    {
        "indicator_id": "HHS-APG-naloxone",
        "agency_code": "HHS", "agency_name": "Department of Health and Human Services",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Reduce opioid overdose deaths through prevention, treatment, and recovery",
        "goal_id": "HHS-APG-5.1", "strategic_objective": "SO 5.1: Combat opioid crisis",
        "indicator_name": "Number of naloxone kits distributed through SAMHSA-funded programs",
        "indicator_unit": "count", "target_value": 1500000, "actual_value": 1107000,
        "actual_year": 2024, "baseline_value": 680000, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "people",
        "data_source": "SAMHSA Grant Reporting",
        "publication_url": "https://www.performance.gov/agencies/hhs/",
        "tags": ["opioid", "naloxone", "harm_reduction"],
    },

    # APG: Maternal Health
    {
        "indicator_id": "HHS-APG-maternal-mortality",
        "agency_code": "HHS", "agency_name": "Department of Health and Human Services",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Reduce maternal mortality and morbidity",
        "goal_id": "HHS-APG-1.4", "strategic_objective": "SO 1.4: Maternal health",
        "indicator_name": "Maternal mortality rate per 100,000 live births",
        "indicator_unit": "rate per 100,000", "target_value": 17.0, "actual_value": 22.3,
        "actual_year": 2023, "baseline_value": 23.8, "baseline_year": 2020,
        "trend": "improving",
        "beneficiary_population": "patients",
        "data_source": "CDC NCHS Vital Statistics",
        "publication_url": "https://www.performance.gov/agencies/hhs/",
        "tags": ["maternal_health", "mortality", "births"],
    },

    # APP indicators: health coverage, behavioral health
    {
        "indicator_id": "HHS-APP-uninsured",
        "agency_code": "HHS", "agency_name": "Department of Health and Human Services",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Expand access to comprehensive health coverage",
        "goal_id": "HHS-SO-1.1", "strategic_objective": "SO 1.1: Health coverage",
        "indicator_name": "Uninsured rate among the US population",
        "indicator_unit": "%", "target_value": 7.5, "actual_value": 7.9,
        "actual_year": 2024, "baseline_value": 10.2, "baseline_year": 2020,
        "trend": "improving",
        "beneficiary_population": "people",
        "data_source": "Census CPS ASEC / National Health Interview Survey",
        "publication_url": "https://www.hhs.gov/about/budget/fy2026/performance/index.html",
        "tags": ["health_coverage", "uninsured", "ACA"],
    },
    {
        "indicator_id": "HHS-APP-marketplace",
        "agency_code": "HHS", "agency_name": "Department of Health and Human Services",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Expand access to comprehensive health coverage",
        "goal_id": "HHS-SO-1.1", "strategic_objective": "SO 1.1: Health coverage",
        "indicator_name": "Number of individuals enrolled in Marketplace coverage",
        "indicator_unit": "count", "target_value": 22000000, "actual_value": 21300000,
        "actual_year": 2025, "baseline_value": 14800000, "baseline_year": 2021,
        "trend": "improving",
        "beneficiary_population": "enrollees",
        "data_source": "CMS Marketplace Open Enrollment Reports",
        "publication_url": "https://www.hhs.gov/about/budget/fy2026/performance/index.html",
        "tags": ["marketplace", "ACA", "enrollment"],
    },
    {
        "indicator_id": "HHS-APP-cmhc",
        "agency_code": "HHS", "agency_name": "Department of Health and Human Services",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Strengthen mental health and substance use disorder services",
        "goal_id": "HHS-SO-5.2", "strategic_objective": "SO 5.2: Behavioral health",
        "indicator_name": "Number of people served by Certified Community Behavioral Health Clinics (CCBHCs)",
        "indicator_unit": "count", "target_value": 5000000, "actual_value": 3200000,
        "actual_year": 2024, "baseline_value": 2200000, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "patients",
        "data_source": "SAMHSA CCBHC Reporting",
        "publication_url": "https://www.hhs.gov/about/budget/fy2026/performance/index.html",
        "tags": ["behavioral_health", "CCBHC", "mental_health"],
    },
    {
        "indicator_id": "HHS-APP-childhood-vaccination",
        "agency_code": "HHS", "agency_name": "Department of Health and Human Services",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Protect Americans from infectious disease",
        "goal_id": "HHS-SO-3.1", "strategic_objective": "SO 3.1: Infectious disease",
        "indicator_name": "Percentage of children 19-35 months receiving combined 7-vaccine series",
        "indicator_unit": "%", "target_value": 72, "actual_value": 69.9,
        "actual_year": 2023, "baseline_value": 70.4, "baseline_year": 2020,
        "trend": "flat",
        "beneficiary_population": "children",
        "data_source": "CDC National Immunization Survey",
        "publication_url": "https://www.hhs.gov/about/budget/fy2026/performance/index.html",
        "tags": ["vaccination", "immunization", "children"],
    },

    # ──────────────────────────────────────────────────────────────────────
    # HUD — Housing and Urban Development
    # ──────────────────────────────────────────────────────────────────────

    {
        "indicator_id": "HUD-APG-homelessness",
        "agency_code": "HUD", "agency_name": "Department of Housing and Urban Development",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Reduce homelessness",
        "goal_id": "HUD-APG-3.1", "strategic_objective": "SO 3: End homelessness",
        "indicator_name": "Point-in-Time count of people experiencing homelessness",
        "indicator_unit": "count", "target_value": 550000, "actual_value": 653104,
        "actual_year": 2024, "baseline_value": 580466, "baseline_year": 2020,
        "trend": "declining",
        "beneficiary_population": "homeless persons",
        "data_source": "HUD Annual Homeless Assessment Report (AHAR)",
        "publication_url": "https://www.performance.gov/agencies/hud/",
        "tags": ["homelessness", "PIT_count", "shelter"],
    },
    {
        "indicator_id": "HUD-APG-veteran-homelessness",
        "agency_code": "HUD", "agency_name": "Department of Housing and Urban Development",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Reduce veteran homelessness",
        "goal_id": "HUD-APG-3.2", "strategic_objective": "SO 3: End homelessness",
        "indicator_name": "Point-in-Time count of veterans experiencing homelessness",
        "indicator_unit": "count", "target_value": 28000, "actual_value": 35574,
        "actual_year": 2024, "baseline_value": 37252, "baseline_year": 2020,
        "trend": "improving",
        "beneficiary_population": "veterans",
        "data_source": "HUD Annual Homeless Assessment Report (AHAR)",
        "publication_url": "https://www.performance.gov/agencies/hud/",
        "tags": ["homelessness", "veterans", "HUD-VASH"],
    },
    {
        "indicator_id": "HUD-APP-voucher-utilization",
        "agency_code": "HUD", "agency_name": "Department of Housing and Urban Development",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Increase utilization of Housing Choice Vouchers",
        "goal_id": "HUD-SO-1.3", "strategic_objective": "SO 1: Affordable housing",
        "indicator_name": "Housing Choice Voucher utilization rate",
        "indicator_unit": "%", "target_value": 98, "actual_value": 93,
        "actual_year": 2024, "baseline_value": 87, "baseline_year": 2021,
        "trend": "improving",
        "beneficiary_population": "households",
        "data_source": "HUD Picture of Subsidized Households",
        "publication_url": "https://www.hud.gov/program_offices/cfo/reports/fy2026_app",
        "tags": ["voucher", "section_8", "utilization"],
    },
    {
        "indicator_id": "HUD-APP-cost-burdened",
        "agency_code": "HUD", "agency_name": "Department of Housing and Urban Development",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Reduce housing cost burden for low-income renters",
        "goal_id": "HUD-SO-1.1", "strategic_objective": "SO 1: Affordable housing",
        "indicator_name": "Percentage of very low-income renters who are severely cost-burdened (paying >50% of income)",
        "indicator_unit": "%", "target_value": 22, "actual_value": 26.3,
        "actual_year": 2023, "baseline_value": 25.9, "baseline_year": 2020,
        "trend": "declining",
        "beneficiary_population": "renters",
        "data_source": "Census ACS / Harvard JCHS",
        "publication_url": "https://www.hud.gov/program_offices/cfo/reports/fy2026_app",
        "tags": ["cost_burden", "rent", "affordability"],
    },
    {
        "indicator_id": "HUD-APP-lead-hazard",
        "agency_code": "HUD", "agency_name": "Department of Housing and Urban Development",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Protect families from lead-based paint and other housing hazards",
        "goal_id": "HUD-SO-4.1", "strategic_objective": "SO 4: Healthy homes",
        "indicator_name": "Number of housing units made lead-safe",
        "indicator_unit": "count", "target_value": 25000, "actual_value": 18500,
        "actual_year": 2024, "baseline_value": 12000, "baseline_year": 2021,
        "trend": "improving",
        "beneficiary_population": "families",
        "data_source": "HUD Office of Lead Hazard Control",
        "publication_url": "https://www.hud.gov/program_offices/cfo/reports/fy2026_app",
        "tags": ["lead_paint", "healthy_homes", "children"],
    },

    # ──────────────────────────────────────────────────────────────────────
    # SSA — Social Security Administration
    # ──────────────────────────────────────────────────────────────────────

    {
        "indicator_id": "SSA-APG-initial-disability",
        "agency_code": "SSA", "agency_name": "Social Security Administration",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Improve timely access to disability benefits",
        "goal_id": "SSA-APG-1.1", "strategic_objective": "SO 1: Deliver quality services",
        "indicator_name": "Average processing time for initial disability claims (days)",
        "indicator_unit": "days", "target_value": 185, "actual_value": 213,
        "actual_year": 2024, "baseline_value": 225, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "claimants",
        "data_source": "SSA Workload Data",
        "publication_url": "https://www.performance.gov/agencies/ssa/",
        "tags": ["disability", "processing_time", "backlog"],
    },
    {
        "indicator_id": "SSA-APG-disability-backlog",
        "agency_code": "SSA", "agency_name": "Social Security Administration",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Improve timely access to disability benefits",
        "goal_id": "SSA-APG-1.1", "strategic_objective": "SO 1: Deliver quality services",
        "indicator_name": "Number of pending initial disability claims",
        "indicator_unit": "count", "target_value": 800000, "actual_value": 1090000,
        "actual_year": 2024, "baseline_value": 1130000, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "claimants",
        "data_source": "SSA Workload Data",
        "publication_url": "https://www.performance.gov/agencies/ssa/",
        "tags": ["disability", "backlog", "pending_claims"],
    },
    {
        "indicator_id": "SSA-APP-retirement-online",
        "agency_code": "SSA", "agency_name": "Social Security Administration",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Increase online self-service for benefit applications",
        "goal_id": "SSA-SO-2.3", "strategic_objective": "SO 2: Improve customer experience",
        "indicator_name": "Percentage of retirement claims filed online",
        "indicator_unit": "%", "target_value": 72, "actual_value": 65,
        "actual_year": 2024, "baseline_value": 58, "baseline_year": 2021,
        "trend": "improving",
        "beneficiary_population": "beneficiaries",
        "data_source": "SSA IT Workload Reports",
        "publication_url": "https://www.ssa.gov/agency/performance/",
        "tags": ["online_services", "retirement", "digital"],
    },

    # ──────────────────────────────────────────────────────────────────────
    # VA — Department of Veterans Affairs
    # ──────────────────────────────────────────────────────────────────────

    {
        "indicator_id": "VA-APG-claims-processing",
        "agency_code": "VA", "agency_name": "Department of Veterans Affairs",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Reduce veteran disability claims processing time",
        "goal_id": "VA-APG-2.1", "strategic_objective": "SO 2: Benefits delivery",
        "indicator_name": "Average days to complete disability compensation claims",
        "indicator_unit": "days", "target_value": 100, "actual_value": 128,
        "actual_year": 2024, "baseline_value": 152, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "veterans",
        "data_source": "VBA Monday Morning Workload Report",
        "publication_url": "https://www.performance.gov/agencies/va/",
        "tags": ["disability_claims", "processing_time", "veterans"],
    },
    {
        "indicator_id": "VA-APG-veteran-suicide",
        "agency_code": "VA", "agency_name": "Department of Veterans Affairs",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Reduce veteran suicide",
        "goal_id": "VA-APG-4.1", "strategic_objective": "SO 4: Suicide prevention",
        "indicator_name": "Veteran suicide rate per 100,000",
        "indicator_unit": "rate per 100,000", "target_value": 28, "actual_value": 31.7,
        "actual_year": 2022, "baseline_value": 32.4, "baseline_year": 2019,
        "trend": "improving",
        "beneficiary_population": "veterans",
        "data_source": "VA National Suicide Data Report",
        "publication_url": "https://www.performance.gov/agencies/va/",
        "tags": ["suicide_prevention", "mental_health", "veterans"],
    },
    {
        "indicator_id": "VA-APP-wait-time-primary",
        "agency_code": "VA", "agency_name": "Department of Veterans Affairs",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Ensure timely access to health care",
        "goal_id": "VA-SO-1.2", "strategic_objective": "SO 1: Health care access",
        "indicator_name": "Average wait time for new patient primary care appointment (days)",
        "indicator_unit": "days", "target_value": 20, "actual_value": 26.3,
        "actual_year": 2024, "baseline_value": 28.1, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "veterans",
        "data_source": "VHA Access and Wait Time Data",
        "publication_url": "https://www.va.gov/performance/",
        "tags": ["wait_time", "primary_care", "access"],
    },
    {
        "indicator_id": "VA-APP-homelessness",
        "agency_code": "VA", "agency_name": "Department of Veterans Affairs",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "End veteran homelessness",
        "goal_id": "VA-SO-3.1", "strategic_objective": "SO 3: Housing stability",
        "indicator_name": "Number of veterans permanently housed through HUD-VASH and SSVF",
        "indicator_unit": "count", "target_value": 40000, "actual_value": 38000,
        "actual_year": 2024, "baseline_value": 35000, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "veterans",
        "data_source": "VA Homeless Programs Office",
        "publication_url": "https://www.va.gov/performance/",
        "tags": ["homelessness", "HUD-VASH", "permanent_housing"],
    },

    # ──────────────────────────────────────────────────────────────────────
    # ED — Department of Education
    # ──────────────────────────────────────────────────────────────────────

    {
        "indicator_id": "ED-APG-fafsa",
        "agency_code": "ED", "agency_name": "Department of Education",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Increase FAFSA completion and Pell Grant accessibility",
        "goal_id": "ED-APG-1.1", "strategic_objective": "SO 1: Postsecondary access",
        "indicator_name": "Number of FAFSA applications completed (annual)",
        "indicator_unit": "count", "target_value": 18000000, "actual_value": 16100000,
        "actual_year": 2024, "baseline_value": 17300000, "baseline_year": 2022,
        "trend": "declining",
        "beneficiary_population": "students",
        "data_source": "Federal Student Aid Data Center",
        "publication_url": "https://www.performance.gov/agencies/ed/",
        "tags": ["FAFSA", "financial_aid", "postsecondary"],
    },
    {
        "indicator_id": "ED-APG-student-loan-default",
        "agency_code": "ED", "agency_name": "Department of Education",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Reduce student loan default and improve repayment outcomes",
        "goal_id": "ED-APG-2.1", "strategic_objective": "SO 2: Student loan outcomes",
        "indicator_name": "Cohort default rate on federal student loans",
        "indicator_unit": "%", "target_value": 7.0, "actual_value": 10.1,
        "actual_year": 2022, "baseline_value": 7.3, "baseline_year": 2019,
        "trend": "declining",
        "beneficiary_population": "borrowers",
        "data_source": "Federal Student Aid CDR Reports",
        "publication_url": "https://www.performance.gov/agencies/ed/",
        "tags": ["student_loans", "default_rate", "repayment"],
    },
    {
        "indicator_id": "ED-APP-high-school-graduation",
        "agency_code": "ED", "agency_name": "Department of Education",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Increase high school graduation rates",
        "goal_id": "ED-SO-3.1", "strategic_objective": "SO 3: K-12 outcomes",
        "indicator_name": "Adjusted cohort high school graduation rate (ACGR)",
        "indicator_unit": "%", "target_value": 88.5, "actual_value": 87.0,
        "actual_year": 2023, "baseline_value": 86.0, "baseline_year": 2020,
        "trend": "improving",
        "beneficiary_population": "students",
        "data_source": "NCES Common Core of Data",
        "publication_url": "https://www.ed.gov/about/budget/fy2026",
        "tags": ["graduation_rate", "K-12", "high_school"],
    },
    {
        "indicator_id": "ED-APP-pell-recipients",
        "agency_code": "ED", "agency_name": "Department of Education",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Increase Pell Grant access for low-income students",
        "goal_id": "ED-SO-1.2", "strategic_objective": "SO 1: Postsecondary access",
        "indicator_name": "Number of Pell Grant recipients (annual)",
        "indicator_unit": "count", "target_value": 7000000, "actual_value": 6700000,
        "actual_year": 2024, "baseline_value": 6300000, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "students",
        "data_source": "Federal Student Aid Data Center",
        "publication_url": "https://www.ed.gov/about/budget/fy2026",
        "tags": ["Pell_Grant", "financial_aid", "low_income"],
    },

    # ──────────────────────────────────────────────────────────────────────
    # DOL — Department of Labor
    # ──────────────────────────────────────────────────────────────────────

    {
        "indicator_id": "DOL-APG-ui-first-payment",
        "agency_code": "DOL", "agency_name": "Department of Labor",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Improve timeliness of unemployment insurance payments",
        "goal_id": "DOL-APG-2.1", "strategic_objective": "SO 2: UI modernization",
        "indicator_name": "Percentage of UI first payments made within 21 days",
        "indicator_unit": "%", "target_value": 87, "actual_value": 78,
        "actual_year": 2024, "baseline_value": 72, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "unemployed",
        "data_source": "DOL ETA UI Data Summary",
        "publication_url": "https://www.performance.gov/agencies/dol/",
        "tags": ["unemployment_insurance", "timeliness", "first_payment"],
    },
    {
        "indicator_id": "DOL-APP-training-employment",
        "agency_code": "DOL", "agency_name": "Department of Labor",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Increase employment outcomes for workforce training participants",
        "goal_id": "DOL-SO-1.1", "strategic_objective": "SO 1: Workforce development",
        "indicator_name": "Employment rate of WIOA Adult program exiters (Q2 after exit)",
        "indicator_unit": "%", "target_value": 74, "actual_value": 70.1,
        "actual_year": 2024, "baseline_value": 68.5, "baseline_year": 2021,
        "trend": "improving",
        "beneficiary_population": "job seekers",
        "data_source": "DOL ETA WIOA Annual Report",
        "publication_url": "https://www.dol.gov/agencies/eta/performance",
        "tags": ["WIOA", "workforce", "employment_outcome"],
    },
    {
        "indicator_id": "DOL-APP-workplace-fatality",
        "agency_code": "DOL", "agency_name": "Department of Labor",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Reduce workplace fatalities and injuries",
        "goal_id": "DOL-SO-3.1", "strategic_objective": "SO 3: Worker safety",
        "indicator_name": "Workplace fatality rate per 100,000 full-time equivalent workers",
        "indicator_unit": "rate per 100,000", "target_value": 3.3, "actual_value": 3.5,
        "actual_year": 2023, "baseline_value": 3.4, "baseline_year": 2020,
        "trend": "flat",
        "beneficiary_population": "workers",
        "data_source": "BLS Census of Fatal Occupational Injuries",
        "publication_url": "https://www.dol.gov/agencies/osha/data",
        "tags": ["workplace_safety", "fatality", "OSHA"],
    },

    # ──────────────────────────────────────────────────────────────────────
    # USDA — Agriculture (nutrition focus)
    # ──────────────────────────────────────────────────────────────────────

    {
        "indicator_id": "USDA-APG-food-insecurity",
        "agency_code": "USDA", "agency_name": "Department of Agriculture",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Reduce food insecurity in America",
        "goal_id": "USDA-APG-4.1", "strategic_objective": "SO 4: Nutrition security",
        "indicator_name": "Prevalence of food insecurity among US households",
        "indicator_unit": "%", "target_value": 10, "actual_value": 13.5,
        "actual_year": 2023, "baseline_value": 10.2, "baseline_year": 2021,
        "trend": "declining",
        "beneficiary_population": "households",
        "data_source": "USDA ERS Household Food Security Report",
        "publication_url": "https://www.performance.gov/agencies/usda/",
        "tags": ["food_insecurity", "SNAP", "nutrition"],
    },
    {
        "indicator_id": "USDA-APP-snap-participation",
        "agency_code": "USDA", "agency_name": "Department of Agriculture",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Increase SNAP participation among eligible individuals",
        "goal_id": "USDA-SO-4.2", "strategic_objective": "SO 4: Nutrition security",
        "indicator_name": "SNAP participation rate among eligible individuals",
        "indicator_unit": "%", "target_value": 85, "actual_value": 82,
        "actual_year": 2023, "baseline_value": 82, "baseline_year": 2021,
        "trend": "flat",
        "beneficiary_population": "individuals",
        "data_source": "USDA FNS SNAP QC",
        "publication_url": "https://www.usda.gov/our-agency/about-usda/performance",
        "tags": ["SNAP", "participation_rate", "benefits_access"],
    },
    {
        "indicator_id": "USDA-APP-wic-coverage",
        "agency_code": "USDA", "agency_name": "Department of Agriculture",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Increase WIC coverage among eligible infants and children",
        "goal_id": "USDA-SO-4.3", "strategic_objective": "SO 4: Nutrition security",
        "indicator_name": "WIC coverage rate among eligible infants",
        "indicator_unit": "%", "target_value": 92, "actual_value": 84,
        "actual_year": 2023, "baseline_value": 88, "baseline_year": 2020,
        "trend": "declining",
        "beneficiary_population": "infants",
        "data_source": "USDA FNS WIC Eligibility and Coverage Reports",
        "publication_url": "https://www.usda.gov/our-agency/about-usda/performance",
        "tags": ["WIC", "infants", "nutrition", "coverage"],
    },
    {
        "indicator_id": "USDA-APP-school-meals",
        "agency_code": "USDA", "agency_name": "Department of Agriculture",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Expand access to school nutrition programs",
        "goal_id": "USDA-SO-4.4", "strategic_objective": "SO 4: Nutrition security",
        "indicator_name": "Number of children receiving free or reduced-price school lunch daily",
        "indicator_unit": "count", "target_value": 22500000, "actual_value": 21800000,
        "actual_year": 2024, "baseline_value": 20500000, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "children",
        "data_source": "USDA FNS Program Data",
        "publication_url": "https://www.usda.gov/our-agency/about-usda/performance",
        "tags": ["school_lunch", "nutrition", "children"],
    },

    # ──────────────────────────────────────────────────────────────────────
    # EPA — Environmental Protection Agency
    # ──────────────────────────────────────────────────────────────────────

    {
        "indicator_id": "EPA-APG-lead-drinking-water",
        "agency_code": "EPA", "agency_name": "Environmental Protection Agency",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Reduce lead in drinking water",
        "goal_id": "EPA-APG-1.2", "strategic_objective": "SO 1: Clean and safe water",
        "indicator_name": "Number of community water systems exceeding lead action level",
        "indicator_unit": "count", "target_value": 1000, "actual_value": 1450,
        "actual_year": 2024, "baseline_value": 1600, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "communities",
        "data_source": "EPA SDWIS Federal Reporting",
        "publication_url": "https://www.performance.gov/agencies/epa/",
        "tags": ["lead", "drinking_water", "public_health"],
    },
    {
        "indicator_id": "EPA-APP-superfund-sites",
        "agency_code": "EPA", "agency_name": "Environmental Protection Agency",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Accelerate Superfund cleanups in disadvantaged communities",
        "goal_id": "EPA-SO-3.1", "strategic_objective": "SO 3: Remediate contamination",
        "indicator_name": "Number of Superfund sites with human exposure under control",
        "indicator_unit": "count", "target_value": 1500, "actual_value": 1430,
        "actual_year": 2024, "baseline_value": 1375, "baseline_year": 2021,
        "trend": "improving",
        "beneficiary_population": "communities",
        "data_source": "EPA CERCLIS/Superfund Program Reports",
        "publication_url": "https://www.epa.gov/planandbudget/fy2026",
        "tags": ["superfund", "contamination", "cleanup"],
    },
    {
        "indicator_id": "EPA-APP-air-quality",
        "agency_code": "EPA", "agency_name": "Environmental Protection Agency",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Improve air quality in nonattainment areas",
        "goal_id": "EPA-SO-4.1", "strategic_objective": "SO 4: Clean air",
        "indicator_name": "Percentage of US population living in areas meeting all NAAQS",
        "indicator_unit": "%", "target_value": 80, "actual_value": 74,
        "actual_year": 2023, "baseline_value": 71, "baseline_year": 2020,
        "trend": "improving",
        "beneficiary_population": "people",
        "data_source": "EPA Air Quality System (AQS)",
        "publication_url": "https://www.epa.gov/planandbudget/fy2026",
        "tags": ["air_quality", "NAAQS", "public_health"],
    },

    # ──────────────────────────────────────────────────────────────────────
    # DOT — Department of Transportation
    # ──────────────────────────────────────────────────────────────────────

    {
        "indicator_id": "DOT-APG-traffic-fatalities",
        "agency_code": "DOT", "agency_name": "Department of Transportation",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Reduce roadway fatalities toward zero (Safe System approach)",
        "goal_id": "DOT-APG-1.1", "strategic_objective": "SO 1: Safety",
        "indicator_name": "Number of roadway fatalities (annual)",
        "indicator_unit": "count", "target_value": 37000, "actual_value": 40990,
        "actual_year": 2023, "baseline_value": 42939, "baseline_year": 2021,
        "trend": "improving",
        "beneficiary_population": "travelers",
        "data_source": "NHTSA FARS",
        "publication_url": "https://www.performance.gov/agencies/dot/",
        "tags": ["traffic_fatalities", "roadway_safety", "Safe_System"],
    },
    {
        "indicator_id": "DOT-APP-transit-ridership",
        "agency_code": "DOT", "agency_name": "Department of Transportation",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Increase public transit ridership and accessibility",
        "goal_id": "DOT-SO-4.1", "strategic_objective": "SO 4: Climate and sustainability",
        "indicator_name": "Annual unlinked transit trips (billions)",
        "indicator_unit": "billions", "target_value": 10.0, "actual_value": 9.1,
        "actual_year": 2024, "baseline_value": 7.4, "baseline_year": 2021,
        "trend": "improving",
        "beneficiary_population": "passengers",
        "data_source": "FTA National Transit Database",
        "publication_url": "https://www.transportation.gov/budget/fy2026-performance",
        "tags": ["transit", "ridership", "public_transportation"],
    },

    # ──────────────────────────────────────────────────────────────────────
    # DHS / FEMA — Homeland Security / Disaster
    # ──────────────────────────────────────────────────────────────────────

    {
        "indicator_id": "FEMA-APG-disaster-assistance",
        "agency_code": "DHS", "agency_name": "Department of Homeland Security",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Improve speed and equity of disaster assistance delivery",
        "goal_id": "DHS-APG-3.1", "strategic_objective": "SO 3: Resilience",
        "indicator_name": "Average days from disaster declaration to Individual Assistance payment",
        "indicator_unit": "days", "target_value": 14, "actual_value": 21,
        "actual_year": 2024, "baseline_value": 25, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "individuals",
        "data_source": "FEMA Individual Assistance Program",
        "publication_url": "https://www.performance.gov/agencies/dhs/",
        "tags": ["disaster", "FEMA", "individual_assistance"],
    },

    # ──────────────────────────────────────────────────────────────────────
    # IRS / Treasury — Tax administration
    # ──────────────────────────────────────────────────────────────────────

    {
        "indicator_id": "IRS-APG-phone-service",
        "agency_code": "IRS", "agency_name": "Internal Revenue Service",
        "fiscal_year": 2026, "source_type": "apg",
        "goal_name": "Improve IRS customer service and reduce wait times",
        "goal_id": "IRS-APG-CX", "strategic_objective": "IRA Implementation",
        "indicator_name": "IRS phone Level of Service (percentage of calls answered)",
        "indicator_unit": "%", "target_value": 85, "actual_value": 88,
        "actual_year": 2024, "baseline_value": 15, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "taxpayers",
        "data_source": "IRS Databook / Filing Season Statistics",
        "publication_url": "https://www.performance.gov/agencies/treasury/",
        "tags": ["IRS", "phone_service", "customer_experience"],
    },
    {
        "indicator_id": "IRS-APP-refund-timeliness",
        "agency_code": "IRS", "agency_name": "Internal Revenue Service",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Process tax refunds timely and accurately",
        "goal_id": "IRS-SO-1.2", "strategic_objective": "Filing and payment",
        "indicator_name": "Percentage of e-filed refunds issued within 21 days",
        "indicator_unit": "%", "target_value": 95, "actual_value": 93,
        "actual_year": 2024, "baseline_value": 89, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "filers",
        "data_source": "IRS Filing Season Statistics",
        "publication_url": "https://www.irs.gov/statistics/soi-tax-stats-irs-data-book",
        "tags": ["refund", "timeliness", "e-file"],
    },
    {
        "indicator_id": "IRS-APP-eitc-participation",
        "agency_code": "IRS", "agency_name": "Internal Revenue Service",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Increase Earned Income Tax Credit participation",
        "goal_id": "IRS-SO-3.1", "strategic_objective": "Compliance and outreach",
        "indicator_name": "EITC participation rate among eligible filers",
        "indicator_unit": "%", "target_value": 80, "actual_value": 78,
        "actual_year": 2023, "baseline_value": 78, "baseline_year": 2021,
        "trend": "flat",
        "beneficiary_population": "filers",
        "data_source": "IRS SOI / CBPP Estimates",
        "publication_url": "https://www.irs.gov/statistics/soi-tax-stats-irs-data-book",
        "tags": ["EITC", "participation", "tax_credits", "poverty"],
    },

    # ──────────────────────────────────────────────────────────────────────
    # SBA — Small Business Administration
    # ──────────────────────────────────────────────────────────────────────

    {
        "indicator_id": "SBA-APP-7a-loans",
        "agency_code": "SBA", "agency_name": "Small Business Administration",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Expand access to capital for underserved small businesses",
        "goal_id": "SBA-SO-1.1", "strategic_objective": "SO 1: Capital access",
        "indicator_name": "Percentage of 7(a) loan dollars to underserved markets (women, minority, veteran, rural)",
        "indicator_unit": "%", "target_value": 42, "actual_value": 38,
        "actual_year": 2024, "baseline_value": 35, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "small businesses",
        "data_source": "SBA Lending Statistics",
        "publication_url": "https://www.sba.gov/about-sba/sba-performance",
        "tags": ["SBA_7a", "capital_access", "underserved"],
    },

    # ──────────────────────────────────────────────────────────────────────
    # USCIS / DHS — Immigration services
    # ──────────────────────────────────────────────────────────────────────

    {
        "indicator_id": "USCIS-APP-naturalization-time",
        "agency_code": "USCIS", "agency_name": "U.S. Citizenship and Immigration Services",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Reduce immigration application processing times",
        "goal_id": "DHS-SO-5.1", "strategic_objective": "SO 5: Immigration services",
        "indicator_name": "Median processing time for N-400 naturalization applications (months)",
        "indicator_unit": "months", "target_value": 7.0, "actual_value": 8.5,
        "actual_year": 2024, "baseline_value": 10.5, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": "immigrants",
        "data_source": "USCIS Processing Time Data",
        "publication_url": "https://www.uscis.gov/tools/processing-times",
        "tags": ["naturalization", "processing_time", "immigration"],
    },

    # ──────────────────────────────────────────────────────────────────────
    # INTERNAL ENABLERS (should be filtered OUT by citizen-metric filter)
    # Included to validate the filter works correctly.
    # ──────────────────────────────────────────────────────────────────────

    {
        "indicator_id": "OPM-INT-hiring-timeline",
        "agency_code": "OPM", "agency_name": "Office of Personnel Management",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Improve federal hiring speed",
        "goal_id": "OPM-SO-1.1", "strategic_objective": "SO 1: Federal workforce",
        "indicator_name": "Average time-to-hire for federal competitive service positions (days)",
        "indicator_unit": "days", "target_value": 80, "actual_value": 98,
        "actual_year": 2024, "baseline_value": 101, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": None,
        "data_source": "OPM HR Solutions Dashboard",
        "publication_url": "https://www.opm.gov/policy-data-oversight/",
        "tags": ["hiring", "federal_workforce", "internal"],
    },
    {
        "indicator_id": "GSA-INT-it-modernization",
        "agency_code": "GSA", "agency_name": "General Services Administration",
        "fiscal_year": 2026, "source_type": "app_goal",
        "goal_name": "Accelerate IT modernization across government",
        "goal_id": "GSA-SO-2.1", "strategic_objective": "SO 2: Technology",
        "indicator_name": "Percentage of agency systems migrated to cloud (data center consolidation)",
        "indicator_unit": "%", "target_value": 60, "actual_value": 45,
        "actual_year": 2024, "baseline_value": 35, "baseline_year": 2022,
        "trend": "improving",
        "beneficiary_population": None,
        "data_source": "GSA Data Center Optimization Initiative",
        "publication_url": "https://www.gsa.gov/about-us/budget-performance",
        "tags": ["cloud_migration", "data_center", "IT_modernization", "internal"],
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# SEED FUNCTION
# ══════════════════════════════════════════════════════════════════════════════

def seed_performance_indicators(store: DataStore | None = None):
    """Seed the performance_indicators table with FY2026 authoritative data.

    For each indicator, computes citizen_facing and dome_dimension before storing.
    """
    store = store or get_store()
    added = 0

    for ind in SEED_PERFORMANCE_INDICATORS:
        # Compute citizen_facing
        citizen = is_citizen_facing(
            ind["indicator_name"],
            ind.get("beneficiary_population"),
            ind.get("goal_name", ""),
        )
        ind["citizen_facing"] = 1 if citizen else 0

        # Compute dome_dimension if not set
        if not ind.get("dome_dimension"):
            ind["dome_dimension"] = _dome_dimension_for(
                ind["agency_code"], ind["indicator_name"]
            )

        store.upsert_performance_indicator(**ind)
        added += 1

    logger.info(f"Seeded {added} performance indicators "
                f"({sum(1 for i in SEED_PERFORMANCE_INDICATORS if is_citizen_facing(i['indicator_name'], i.get('beneficiary_population'), i.get('goal_name', '')))} citizen-facing)")
    return added


# ══════════════════════════════════════════════════════════════════════════════
# SCRAPERS — Performance.gov API + Agency APP/APR machine-readable feeds
# ══════════════════════════════════════════════════════════════════════════════

class PerformanceGovScraper(BaseScraper):
    """Scrapes Performance.gov for CAP Goals and Agency Priority Goals.

    Performance.gov publishes structured goal data at:
      - https://www.performance.gov/api/goals/apg.json  (APGs)
      - https://www.performance.gov/api/goals/cap.json  (CAP Goals)
      - https://www.performance.gov/api/agencies.json   (Agency list)

    When the API is unavailable (it's intermittent), seed data serves as floor.
    """

    engine_name = "performance"
    source_name = "performance_gov"

    PERF_API = "https://www.performance.gov"

    async def scrape(self) -> dict:
        added = 0
        updated = 0

        # Try CAP goals
        cap_data = await self._fetch(f"{self.PERF_API}/api/goals/cap.json")
        if cap_data and isinstance(cap_data, list):
            for goal in cap_data:
                result = self._process_performance_gov_goal(goal, "cap_goal")
                added += result.get("added", 0)
                updated += result.get("updated", 0)

        # Try APG goals
        apg_data = await self._fetch(f"{self.PERF_API}/api/goals/apg.json")
        if apg_data and isinstance(apg_data, list):
            for goal in apg_data:
                result = self._process_performance_gov_goal(goal, "apg")
                added += result.get("added", 0)
                updated += result.get("updated", 0)

        return {"added": added, "updated": updated}

    def _process_performance_gov_goal(self, goal: dict, source_type: str) -> dict:
        added = 0
        updated = 0

        agency_code = goal.get("agency_abbreviation", goal.get("agency", ""))
        agency_name = goal.get("agency_name", "")
        goal_name = goal.get("goal_statement", goal.get("title", ""))
        goal_id = goal.get("id", "")

        indicators = goal.get("indicators", goal.get("metrics", []))
        if not indicators and goal_name:
            # Some goals have the metric embedded in the goal statement
            indicators = [{"name": goal_name, "target": goal.get("target"),
                           "actual": goal.get("actual")}]

        for i, ind in enumerate(indicators):
            ind_name = ind.get("name", ind.get("description", f"Indicator {i+1}"))
            slug = re.sub(r'[^a-z0-9]+', '-', ind_name.lower())[:50]
            indicator_id = f"{agency_code}-{source_type}-{slug}"

            citizen = is_citizen_facing(ind_name, ind.get("population"), goal_name)
            dome_dim = _dome_dimension_for(agency_code, ind_name)

            try:
                self.store.upsert_performance_indicator(
                    indicator_id=indicator_id,
                    agency_code=agency_code,
                    agency_name=agency_name,
                    fiscal_year=2026,
                    source_type=source_type,
                    goal_name=goal_name,
                    goal_id=str(goal_id),
                    strategic_objective=goal.get("strategic_objective", ""),
                    indicator_name=ind_name,
                    indicator_unit=ind.get("unit", ""),
                    target_value=ind.get("target"),
                    actual_value=ind.get("actual"),
                    actual_year=ind.get("actual_year"),
                    baseline_value=ind.get("baseline"),
                    baseline_year=ind.get("baseline_year"),
                    trend=ind.get("trend"),
                    citizen_facing=1 if citizen else 0,
                    beneficiary_population=ind.get("population"),
                    dome_dimension=dome_dim,
                    data_source=ind.get("data_source", "Performance.gov"),
                    publication_url=f"{self.PERF_API}/agencies/{agency_code.lower()}/",
                    tags=ind.get("tags", []),
                )
                added += 1
            except Exception as e:
                logger.warning(f"Failed to upsert indicator {indicator_id}: {e}")

        return {"added": added, "updated": updated}


class AgencyAPRScraper(BaseScraper):
    """Scrapes machine-readable APP/APR publications from individual agencies.

    Each CFO Act agency publishes its APP/APR alongside the budget justification.
    Some publish structured data (JSON/XML); most publish PDF with tables.

    This scraper targets the machine-readable feeds where available:
      - HHS: JSON performance appendix
      - VA: XML performance data
      - ED: JSON performance tables
      - SSA: annual performance report data tables

    For agencies without machine-readable formats, the seed data provides the
    authoritative baseline, and this scraper enriches with any new data found
    in structured feeds linked from agency /budget/ or /performance/ pages.
    """

    engine_name = "performance"
    source_name = "agency_apr"

    # Agencies with known machine-readable APP/APR endpoints
    AGENCY_FEEDS: list[dict] = [
        {
            "agency_code": "HHS",
            "url": "https://www.hhs.gov/about/budget/fy2026/performance/index.html",
            "format": "html_with_links",
        },
        {
            "agency_code": "VA",
            "url": "https://www.va.gov/performance/",
            "format": "html_with_links",
        },
        {
            "agency_code": "ED",
            "url": "https://www2.ed.gov/about/reports/annual/index.html",
            "format": "html_with_links",
        },
        {
            "agency_code": "SSA",
            "url": "https://www.ssa.gov/agency/performance/",
            "format": "html_with_links",
        },
        {
            "agency_code": "DOL",
            "url": "https://www.dol.gov/general/aboutdol/budget",
            "format": "html_with_links",
        },
        {
            "agency_code": "HUD",
            "url": "https://www.hud.gov/program_offices/cfo/reports",
            "format": "html_with_links",
        },
        {
            "agency_code": "USDA",
            "url": "https://www.usda.gov/our-agency/about-usda/performance",
            "format": "html_with_links",
        },
        {
            "agency_code": "EPA",
            "url": "https://www.epa.gov/planandbudget/strategicplan",
            "format": "html_with_links",
        },
        {
            "agency_code": "DOT",
            "url": "https://www.transportation.gov/mission/budget/fy2026-budget-estimates",
            "format": "html_with_links",
        },
    ]

    async def scrape(self) -> dict:
        added = 0
        updated = 0

        for feed in self.AGENCY_FEEDS:
            result = await self._scrape_agency(feed)
            added += result.get("added", 0)
            updated += result.get("updated", 0)

        return {"added": added, "updated": updated}

    async def _scrape_agency(self, feed: dict) -> dict:
        """Try to fetch and parse an agency's performance data.

        Currently most agencies don't expose true JSON APIs for APP/APR data.
        This attempts to fetch the page and look for linked JSON/CSV/XML
        performance data files.  When none are found, returns 0 (seed data
        remains the floor).
        """
        data = await self._fetch(feed["url"], timeout=15.0)
        if not data:
            return {"added": 0, "updated": 0}

        added = 0

        # If the response contains raw HTML, look for links to structured data
        raw = data.get("_raw", "") if isinstance(data, dict) else ""
        if raw:
            # Extract links to .json, .csv, .xml performance files
            import re as _re
            links = _re.findall(
                r'href=["\']([^"\']*(?:performance|apr|app)[^"\']*\.(?:json|csv|xml))',
                raw, _re.IGNORECASE
            )
            for link in links[:5]:  # cap at 5 to avoid runaway
                if not link.startswith("http"):
                    from urllib.parse import urljoin
                    link = urljoin(feed["url"], link)
                sub_data = await self._fetch(link, timeout=15.0)
                if sub_data and isinstance(sub_data, (list, dict)):
                    result = self._ingest_structured_apr(
                        feed["agency_code"], sub_data
                    )
                    added += result

        return {"added": added, "updated": 0}

    def _ingest_structured_apr(self, agency_code: str, data: Any) -> int:
        """Ingest structured APP/APR data (JSON array of goals/indicators)."""
        added = 0
        items = data if isinstance(data, list) else data.get("goals", data.get("indicators", []))

        for item in items:
            if not isinstance(item, dict):
                continue

            goal_name = item.get("goal", item.get("name", item.get("title", "")))
            indicators = item.get("indicators", item.get("metrics", [item]))

            for ind in indicators:
                ind_name = ind.get("indicator", ind.get("metric", ind.get("name", "")))
                if not ind_name:
                    continue

                slug = re.sub(r'[^a-z0-9]+', '-', ind_name.lower())[:50]
                indicator_id = f"{agency_code}-apr-{slug}"

                citizen = is_citizen_facing(ind_name, ind.get("population"), goal_name)
                dome_dim = _dome_dimension_for(agency_code, ind_name)

                try:
                    self.store.upsert_performance_indicator(
                        indicator_id=indicator_id,
                        agency_code=agency_code,
                        agency_name=ind.get("agency_name", agency_code),
                        fiscal_year=ind.get("fiscal_year", 2026),
                        source_type="apr_result",
                        goal_name=goal_name,
                        goal_id=ind.get("goal_id"),
                        strategic_objective=ind.get("strategic_objective"),
                        indicator_name=ind_name,
                        indicator_unit=ind.get("unit"),
                        target_value=ind.get("target"),
                        actual_value=ind.get("actual"),
                        actual_year=ind.get("actual_year"),
                        baseline_value=ind.get("baseline"),
                        baseline_year=ind.get("baseline_year"),
                        trend=ind.get("trend"),
                        citizen_facing=1 if citizen else 0,
                        beneficiary_population=ind.get("population"),
                        dome_dimension=dome_dim,
                        data_source=ind.get("data_source", "Agency APR"),
                        publication_url=ind.get("url"),
                        tags=ind.get("tags", []),
                    )
                    added += 1
                except Exception as e:
                    logger.warning(f"Failed to ingest APR indicator: {e}")

        return added
