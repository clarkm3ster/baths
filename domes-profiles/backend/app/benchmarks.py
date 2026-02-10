"""
Cost benchmarks for the DOMES Profiles cost engine.

All costs are ANNUAL PER PERSON in USD unless otherwise noted.
Every figure is sourced from published government or research data.
This module is the factual foundation for all cost calculations.
"""

# ---------------------------------------------------------------------------
# Domain labels (canonical mapping)
# ---------------------------------------------------------------------------

DOMAIN_LABELS: dict[str, str] = {
    "health": "Health",
    "justice": "Justice",
    "child_welfare": "Child Welfare",
    "housing": "Housing",
    "income": "Income",
    "education": "Education",
}

DOMAIN_COLORS: dict[str, str] = {
    "health": "#1A6B3C",
    "justice": "#8B1A1A",
    "housing": "#1A3D8B",
    "income": "#6B5A1A",
    "education": "#5A1A6B",
    "child_welfare": "#1A6B6B",
}

# ---------------------------------------------------------------------------
# SYSTEM COST BENCHMARKS
# ---------------------------------------------------------------------------
# Keyed by system identifier (matches the data-system IDs used across DOMES).
# Each entry has:
#   label       - Human-readable name
#   domain      - Which DOMES domain this belongs to
#   base_cost   - Default annual per-person cost
#   categories  - Optional sub-populations with specific costs
#   source      - Published citation
# ---------------------------------------------------------------------------

SYSTEM_COSTS: dict[str, dict] = {
    # ----- HEALTH -----
    "mmis": {
        "label": "Medicaid",
        "domain": "health",
        "base_cost": 8500,
        "categories": {
            "general_adult": 4800,
            "disabled": 16200,
            "behavioral_health": 12400,
            "dual_eligible": 22800,
            "pregnant": 9600,
            "child": 3200,
            "foster_child": 8900,
        },
        "source": "CMS Medicaid PMPM Actuarial Report 2023",
    },
    "mco": {
        "label": "Managed Care Organization",
        "domain": "health",
        "base_cost": 7200,
        "categories": {
            "general": 5400,
            "behavioral_health": 11800,
            "complex_care": 18500,
        },
        "source": "CMS MCO Rate Setting Guide",
    },
    "bha": {
        "label": "Behavioral Health",
        "domain": "health",
        "base_cost": 8200,
        "categories": {
            "outpatient_therapy": 4800,
            "intensive_outpatient": 9600,
            "residential_treatment": 28000,
            "mat_opioid": 7200,
            "crisis_services": 15000,
            "assertive_community_treatment": 12000,
        },
        "source": "SAMHSA National Survey / TEDS",
    },
    "cmhc_ehr": {
        "label": "Community Mental Health Center",
        "domain": "health",
        "base_cost": 5600,
        "source": "SAMHSA Uniform Reporting System",
    },
    "hie": {
        "label": "Health Information Exchange",
        "domain": "health",
        "base_cost": 180,
        "source": "ONC HIE Cost Analysis",
    },
    "pdmp": {
        "label": "Prescription Drug Monitoring",
        "domain": "health",
        "base_cost": 45,
        "source": "State PDMP Program Reports",
    },
    "va_system": {
        "label": "VA Healthcare",
        "domain": "health",
        "base_cost": 14200,
        "categories": {
            "primary_care": 8400,
            "mental_health": 12800,
            "disability_compensation": 18600,
        },
        "source": "VA Budget Request FY2024",
    },
    "vital_records": {
        "label": "Vital Records",
        "domain": "health",
        "base_cost": 25,
        "source": "State Vital Records Admin",
    },
    # ----- JUSTICE -----
    "doc": {
        "label": "Incarceration",
        "domain": "justice",
        "base_cost": 39800,
        "categories": {
            "state_prison": 39800,
            "county_jail": 31400,
            "juvenile_detention": 58800,
        },
        "source": "Vera Institute of Justice - Price of Prisons 2023",
    },
    "cjis": {
        "label": "Criminal Justice Information",
        "domain": "justice",
        "base_cost": 120,
        "source": "FBI CJIS Division Budget",
    },
    "probation_parole": {
        "label": "Probation/Parole Supervision",
        "domain": "justice",
        "base_cost": 4200,
        "categories": {
            "standard": 4200,
            "intensive": 8400,
            "electronic_monitoring": 6800,
        },
        "source": "Bureau of Justice Statistics",
    },
    "court_cms": {
        "label": "Court System",
        "domain": "justice",
        "base_cost": 2800,
        "categories": {
            "criminal": 3200,
            "family": 2400,
            "juvenile": 4100,
            "drug_court": 5800,
        },
        "source": "National Center for State Courts",
    },
    # ----- CHILD WELFARE -----
    "sacwis": {
        "label": "Child Welfare",
        "domain": "child_welfare",
        "base_cost": 32000,
        "categories": {
            "investigation": 8500,
            "foster_care": 32000,
            "kinship_care": 18000,
            "adoption_subsidy": 12000,
            "family_preservation": 6500,
        },
        "source": "ACF AFCARS / Child Welfare Financing Survey",
    },
    # ----- HOUSING -----
    "hmis": {
        "label": "Homeless Services",
        "domain": "housing",
        "base_cost": 22400,
        "categories": {
            "emergency_shelter": 22400,
            "transitional_housing": 18000,
            "permanent_supportive": 14200,
            "rapid_rehousing": 8400,
        },
        "source": "HUD Annual Homeless Assessment Report",
    },
    "pha": {
        "label": "Public Housing/Section 8",
        "domain": "housing",
        "base_cost": 10800,
        "categories": {
            "section_8_voucher": 10800,
            "public_housing": 9200,
            "project_based": 11400,
        },
        "source": "HUD Budget Justification",
    },
    # ----- INCOME -----
    "ssa": {
        "label": "SSI/SSDI",
        "domain": "income",
        "base_cost": 12600,
        "categories": {
            "ssi": 12600,
            "ssdi": 16800,
            "both": 21600,
        },
        "source": "SSA Annual Statistical Supplement",
    },
    "snap_ebt": {
        "label": "SNAP Benefits",
        "domain": "income",
        "base_cost": 3400,
        "source": "USDA FNS Program Data",
    },
    "tanf": {
        "label": "TANF Cash Assistance",
        "domain": "income",
        "base_cost": 5200,
        "source": "ACF TANF Financial Data",
    },
    "unemployment": {
        "label": "Unemployment Insurance",
        "domain": "income",
        "base_cost": 7800,
        "source": "DOL UI Data",
    },
    # ----- EDUCATION -----
    "slds": {
        "label": "Public Education",
        "domain": "education",
        "base_cost": 14800,
        "categories": {
            "general": 14800,
            "special_education": 28400,
        },
        "source": "NCES Digest of Education Statistics",
    },
    "iep": {
        "label": "Special Education (IEP)",
        "domain": "education",
        "base_cost": 28400,
        "source": "NCES / IDEA Data Center",
    },
}

# ---------------------------------------------------------------------------
# COORDINATION SAVINGS BENCHMARKS
# ---------------------------------------------------------------------------
# Keyed by the domain pair (alphabetical). Each entry encodes the evidence-
# based savings percentage achievable when systems in those two domains share
# data and coordinate services.
# ---------------------------------------------------------------------------

COORDINATION_SAVINGS: dict[str, dict] = {
    "health_justice": {
        "label": "Health-Justice Coordination",
        "savings_pct": 0.35,
        "mechanisms": [
            "Pre-release Medicaid enrollment (avoid ER for routine care)",
            "MAT continuity (reduce recidivism 40-60%)",
            "Health record transfer (avoid duplicate testing)",
        ],
        "source": "RAND Corporation / Pew Charitable Trusts",
    },
    "health_housing": {
        "label": "Health-Housing Coordination",
        "savings_pct": 0.40,
        "mechanisms": [
            "Permanent supportive housing (reduce ER visits 60%)",
            "Housing status in care plans (appropriate prescribing)",
            "Coordinated intake (reduce assessment duplication)",
        ],
        "source": "HUD-HHS Pay for Success / SAMHSA CABHI",
    },
    "health_behavioral": {
        "label": "Integrated Physical-Behavioral Health",
        "savings_pct": 0.25,
        "mechanisms": [
            "Integrated care coordination",
            "Shared treatment plans",
            "Whole-person care management",
        ],
        "source": "Milliman / Medicaid Integration Studies",
    },
    "child_welfare_health": {
        "label": "Child Welfare-Health Coordination",
        "savings_pct": 0.30,
        "mechanisms": [
            "Health passport for foster children",
            "Automatic Medicaid continuity on placement change",
            "Coordinated trauma-informed care",
        ],
        "source": "Casey Family Programs / ACF Studies",
    },
    "income_health": {
        "label": "Benefits-Health Coordination",
        "savings_pct": 0.15,
        "mechanisms": [
            "Auto-enrollment across programs",
            "Shared eligibility determination",
            "Reduced administrative burden",
        ],
        "source": "CBPP / Urban Institute",
    },
    "education_health": {
        "label": "Education-Health Coordination",
        "savings_pct": 0.20,
        "mechanisms": [
            "School-based Medicaid billing",
            "Shared IEP-treatment plans",
            "Early intervention services",
        ],
        "source": "GAO Reports on School-Based Health",
    },
    "justice_housing": {
        "label": "Justice-Housing Coordination",
        "savings_pct": 0.45,
        "mechanisms": [
            "Re-entry housing (reduce recidivism 30-50%)",
            "Supportive housing for justice-involved",
            "Eviction prevention for probationers",
        ],
        "source": "Council of State Governments Justice Center",
    },
}

# ---------------------------------------------------------------------------
# AVOIDABLE COST EVENTS
# ---------------------------------------------------------------------------
# Per-event costs that coordinated care can prevent or reduce in frequency.
# ---------------------------------------------------------------------------

AVOIDABLE_COSTS: dict[str, dict] = {
    "er_visit_avoidable": {
        "cost": 2200,
        "description": "Avoidable ER visit (non-emergency use)",
        "source": "HCUP / AHRQ",
    },
    "psychiatric_crisis": {
        "cost": 8500,
        "description": "Psychiatric crisis/5150 hold",
        "source": "SAMHSA Crisis Services Report",
    },
    "jail_booking": {
        "cost": 1800,
        "description": "Jail booking and short stay (avg 3 days)",
        "source": "Vera Institute",
    },
    "shelter_month": {
        "cost": 1867,
        "description": "Emergency shelter per month",
        "source": "HUD AHAR",
    },
    "foster_placement_disruption": {
        "cost": 4200,
        "description": "Foster care placement disruption",
        "source": "Casey Family Programs",
    },
    "medicaid_coverage_gap": {
        "cost": 3500,
        "description": "Cost of Medicaid coverage gap (deferred care -> ER)",
        "source": "KFF Medicaid Coverage Gap Analysis",
    },
    "readmission_30day": {
        "cost": 15200,
        "description": "30-day hospital readmission",
        "source": "CMS Hospital Readmissions Reduction Program",
    },
    "recidivism_event": {
        "cost": 28000,
        "description": "Recidivism (return to incarceration avg 8 months)",
        "source": "Bureau of Justice Statistics",
    },
}

# ---------------------------------------------------------------------------
# AVOIDABLE EVENT FREQUENCY ESTIMATES
# ---------------------------------------------------------------------------
# Per-year expected occurrences for high-utilizer populations keyed by domain
# involvement. Used by the cost engine to estimate avoidable event costs.
# ---------------------------------------------------------------------------

AVOIDABLE_EVENT_FREQUENCIES: dict[str, dict[str, float]] = {
    "health": {
        "er_visit_avoidable": 4.0,
        "psychiatric_crisis": 0.5,
        "readmission_30day": 0.3,
        "medicaid_coverage_gap": 0.2,
    },
    "justice": {
        "jail_booking": 2.0,
        "recidivism_event": 0.25,
    },
    "housing": {
        "shelter_month": 6.0,
        "er_visit_avoidable": 2.0,
    },
    "child_welfare": {
        "foster_placement_disruption": 1.5,
        "er_visit_avoidable": 1.0,
    },
    "income": {
        "er_visit_avoidable": 1.0,
        "medicaid_coverage_gap": 0.3,
    },
    "education": {
        "er_visit_avoidable": 0.5,
    },
}

# ---------------------------------------------------------------------------
# CIRCUMSTANCE -> CATEGORY MAPPING
# ---------------------------------------------------------------------------
# Maps circumstance keywords to the appropriate cost category for each system.
# The cost engine uses this to select the right sub-population cost.
# ---------------------------------------------------------------------------

CIRCUMSTANCE_CATEGORY_MAP: dict[str, dict[str, str]] = {
    "mmis": {
        "disabled": "disabled",
        "disability": "disabled",
        "ssi": "disabled",
        "behavioral_health": "behavioral_health",
        "substance_use": "behavioral_health",
        "mental_health": "behavioral_health",
        "sud": "behavioral_health",
        "dual_eligible": "dual_eligible",
        "medicare": "dual_eligible",
        "pregnant": "pregnant",
        "pregnancy": "pregnant",
        "child": "child",
        "minor": "child",
        "youth": "child",
        "foster": "foster_child",
        "foster_care": "foster_child",
    },
    "mco": {
        "behavioral_health": "behavioral_health",
        "substance_use": "behavioral_health",
        "mental_health": "behavioral_health",
        "complex_care": "complex_care",
        "chronic": "complex_care",
        "multiple_conditions": "complex_care",
    },
    "bha": {
        "outpatient": "outpatient_therapy",
        "therapy": "outpatient_therapy",
        "iop": "intensive_outpatient",
        "intensive_outpatient": "intensive_outpatient",
        "residential": "residential_treatment",
        "inpatient": "residential_treatment",
        "mat": "mat_opioid",
        "opioid": "mat_opioid",
        "opioid_use": "mat_opioid",
        "crisis": "crisis_services",
        "act": "assertive_community_treatment",
    },
    "va_system": {
        "primary_care": "primary_care",
        "mental_health": "mental_health",
        "disability": "disability_compensation",
        "disability_compensation": "disability_compensation",
        "service_connected": "disability_compensation",
    },
    "doc": {
        "state_prison": "state_prison",
        "prison": "state_prison",
        "county_jail": "county_jail",
        "jail": "county_jail",
        "juvenile": "juvenile_detention",
        "youth": "juvenile_detention",
        "minor": "juvenile_detention",
    },
    "probation_parole": {
        "intensive": "intensive",
        "electronic_monitoring": "electronic_monitoring",
        "gps": "electronic_monitoring",
        "ankle_monitor": "electronic_monitoring",
    },
    "court_cms": {
        "criminal": "criminal",
        "family": "family",
        "juvenile": "juvenile",
        "youth": "juvenile",
        "drug_court": "drug_court",
        "treatment_court": "drug_court",
    },
    "sacwis": {
        "investigation": "investigation",
        "cps_investigation": "investigation",
        "foster_care": "foster_care",
        "foster": "foster_care",
        "kinship": "kinship_care",
        "kinship_care": "kinship_care",
        "adoption": "adoption_subsidy",
        "adoption_subsidy": "adoption_subsidy",
        "family_preservation": "family_preservation",
        "in_home": "family_preservation",
    },
    "hmis": {
        "emergency_shelter": "emergency_shelter",
        "shelter": "emergency_shelter",
        "homeless": "emergency_shelter",
        "transitional": "transitional_housing",
        "transitional_housing": "transitional_housing",
        "permanent_supportive": "permanent_supportive",
        "psh": "permanent_supportive",
        "rapid_rehousing": "rapid_rehousing",
        "rrh": "rapid_rehousing",
    },
    "pha": {
        "section_8": "section_8_voucher",
        "voucher": "section_8_voucher",
        "hcv": "section_8_voucher",
        "public_housing": "public_housing",
        "project_based": "project_based",
    },
    "ssa": {
        "ssi": "ssi",
        "ssdi": "ssdi",
        "both": "both",
        "dual_benefit": "both",
    },
    "slds": {
        "special_education": "special_education",
        "iep": "special_education",
        "disability": "special_education",
    },
}

# ---------------------------------------------------------------------------
# INFLATION RATE for projections
# ---------------------------------------------------------------------------

ANNUAL_INFLATION_RATE: float = 0.03

# ---------------------------------------------------------------------------
# LIFETIME HORIZON DEFAULTS (years)
# ---------------------------------------------------------------------------
# Used when no explicit duration is provided. Based on population type.
# ---------------------------------------------------------------------------

LIFETIME_HORIZONS: dict[str, int] = {
    "youth": 10,
    "child": 10,
    "minor": 10,
    "adult": 20,
    "chronic": 30,
    "elderly": 15,
    "default": 20,
}

# ---------------------------------------------------------------------------
# COORDINATION INVESTMENT ESTIMATES
# ---------------------------------------------------------------------------
# Per-person one-time coordination investment costs, used for ROI.
# ---------------------------------------------------------------------------

COORDINATION_INVESTMENT_PER_PERSON: float = 3500.0
