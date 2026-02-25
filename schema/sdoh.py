"""
BATHS Dome — Social Determinants of Health (SDOH) Standards Mapping

The BATHS Dome: A Whole-Person Digital Twin Architecture
Layers 5-9 map to SDOH standards.

This module maps two standard SDOH screening instruments to specific
dome layer fields:

1. PRAPARE (Protocol for Responding to and Assessing Patients' Assets,
   Risks, and Experiences) — developed by NACHC
   Reference: https://prapare.org

2. AHC-HRSN (Accountable Health Communities Health-Related Social Needs)
   — developed by CMS
   Reference: https://innovation.cms.gov/innovation-models/ahcm

The mapping is bidirectional:
- SDOH screening data → dome layers (ingest)
- Dome layer data → SDOH screening responses (export)

This means a dome can be populated FROM standardized screenings,
and a dome can PRODUCE screening-compatible data for integration
with health systems.

Coding system: LOINC codes for SDOH observations
(http://hl7.org/fhir/us/sdoh-clinicalcare/STU2.1/)
"""

from typing import Optional, Dict, List, Any, Literal
from pydantic import BaseModel, Field
from enum import Enum


# ═══════════════════════════════════════════════════════════════
# PRAPARE — Protocol for Responding to and Assessing Patients'
# Assets, Risks, and Experiences
# ═══════════════════════════════════════════════════════════════

class PRAPAREDomain(str, Enum):
    """PRAPARE screening domains."""
    PERSONAL_CHARACTERISTICS = "personal_characteristics"
    FAMILY_AND_HOME = "family_and_home"
    MONEY_AND_RESOURCES = "money_and_resources"
    SOCIAL_AND_EMOTIONAL_HEALTH = "social_and_emotional_health"
    OPTIONAL_MEASURES = "optional_measures"


class PRAPAREItem(BaseModel):
    """A single PRAPARE screening item with dome layer mapping."""
    item_id: str
    domain: PRAPAREDomain
    question: str
    loinc_code: str             # LOINC code for this screening item
    response: Optional[str] = None
    response_code: Optional[str] = None
    # Dome mapping
    dome_layer: int             # Which dome layer (1-12) this maps to
    dome_field: str             # Which field in that layer
    risk_level: Optional[Literal["low", "moderate", "high", "critical"]] = None


# Complete PRAPARE instrument with dome layer mappings
PRAPARE_INSTRUMENT: List[PRAPAREItem] = [
    # ── Personal Characteristics ────────────────────────────────
    PRAPAREItem(
        item_id="prapare_race",
        domain=PRAPAREDomain.PERSONAL_CHARACTERISTICS,
        question="Are you Hispanic or Latino?",
        loinc_code="56051-6",
        dome_layer=4,  # Health — demographics
        dome_field="patient.race",
    ),
    PRAPAREItem(
        item_id="prapare_ethnicity",
        domain=PRAPAREDomain.PERSONAL_CHARACTERISTICS,
        question="Which race(s) are you?",
        loinc_code="32624-9",
        dome_layer=4,
        dome_field="patient.ethnicity",
    ),
    PRAPAREItem(
        item_id="prapare_farmworker",
        domain=PRAPAREDomain.PERSONAL_CHARACTERISTICS,
        question="At any point in the past 2 years, has season or migrant farm work been your or your family's main source of income?",
        loinc_code="93035-4",
        dome_layer=6,  # Economic
        dome_field="employment_type",
    ),
    PRAPAREItem(
        item_id="prapare_veteran",
        domain=PRAPAREDomain.PERSONAL_CHARACTERISTICS,
        question="Have you been discharged from the armed forces of the United States?",
        loinc_code="93034-7",
        dome_layer=1,  # Legal — veteran entitlements
        dome_field="veteran_status",
    ),
    PRAPAREItem(
        item_id="prapare_language",
        domain=PRAPAREDomain.PERSONAL_CHARACTERISTICS,
        question="What language are you most comfortable speaking?",
        loinc_code="54899-0",
        dome_layer=4,
        dome_field="patient.communication",
    ),

    # ── Family and Home ─────────────────────────────────────────
    PRAPAREItem(
        item_id="prapare_household_size",
        domain=PRAPAREDomain.FAMILY_AND_HOME,
        question="How many family members, including yourself, do you currently live with?",
        loinc_code="63512-8",
        dome_layer=8,  # Community — household
        dome_field="household_size",
    ),
    PRAPAREItem(
        item_id="prapare_housing_status",
        domain=PRAPAREDomain.FAMILY_AND_HOME,
        question="What is your housing situation today?",
        loinc_code="71802-3",
        dome_layer=5,  # Housing
        dome_field="current_housing.tenure",
    ),
    PRAPAREItem(
        item_id="prapare_housing_worry",
        domain=PRAPAREDomain.FAMILY_AND_HOME,
        question="Are you worried about losing your housing?",
        loinc_code="93033-9",
        dome_layer=5,
        dome_field="housing_stability_score",
    ),
    PRAPAREItem(
        item_id="prapare_address",
        domain=PRAPAREDomain.FAMILY_AND_HOME,
        question="What address do you live at?",
        loinc_code="56799-0",
        dome_layer=5,
        dome_field="current_housing.address",
    ),

    # ── Money and Resources ─────────────────────────────────────
    PRAPAREItem(
        item_id="prapare_education",
        domain=PRAPAREDomain.MONEY_AND_RESOURCES,
        question="What is the highest level of school that you have finished?",
        loinc_code="82589-3",
        dome_layer=7,  # Education
        dome_field="highest_level",
    ),
    PRAPAREItem(
        item_id="prapare_employment",
        domain=PRAPAREDomain.MONEY_AND_RESOURCES,
        question="What is your current work situation?",
        loinc_code="67875-5",
        dome_layer=6,  # Economic
        dome_field="current_employment.employment_type",
    ),
    PRAPAREItem(
        item_id="prapare_insurance",
        domain=PRAPAREDomain.MONEY_AND_RESOURCES,
        question="What is your main insurance?",
        loinc_code="76437-3",
        dome_layer=4,  # Health → Coverage
        dome_field="coverages",
    ),
    PRAPAREItem(
        item_id="prapare_food",
        domain=PRAPAREDomain.MONEY_AND_RESOURCES,
        question="In the past year, have you or any family members you live with been unable to get any of the following when it was really needed? (Food)",
        loinc_code="88122-7",
        dome_layer=9,  # Environment — food access
        dome_field="food_access_score",
    ),
    PRAPAREItem(
        item_id="prapare_utilities",
        domain=PRAPAREDomain.MONEY_AND_RESOURCES,
        question="In the past year, have you or any family members you live with been unable to get any of the following when it was really needed? (Utilities)",
        loinc_code="93031-3",
        dome_layer=3,  # Fiscal
        dome_field="utility_difficulty",
    ),
    PRAPAREItem(
        item_id="prapare_childcare",
        domain=PRAPAREDomain.MONEY_AND_RESOURCES,
        question="In the past year, have you or any family members you live with been unable to get any of the following when it was really needed? (Child care)",
        loinc_code="93030-5",
        dome_layer=8,  # Community — childcare
        dome_field="childcare_access",
    ),
    PRAPAREItem(
        item_id="prapare_transportation",
        domain=PRAPAREDomain.MONEY_AND_RESOURCES,
        question="Has lack of transportation kept you from medical appointments, meetings, work, or from getting things needed for daily living?",
        loinc_code="93030-4",
        dome_layer=2,  # Systems — access barrier
        dome_field="transportation_barrier",
    ),

    # ── Social and Emotional Health ─────────────────────────────
    PRAPAREItem(
        item_id="prapare_social_integration",
        domain=PRAPAREDomain.SOCIAL_AND_EMOTIONAL_HEALTH,
        question="How often do you see or talk to people that you care about and feel close to?",
        loinc_code="93029-7",
        dome_layer=8,  # Community
        dome_field="isolation_risk_score",
    ),
    PRAPAREItem(
        item_id="prapare_stress",
        domain=PRAPAREDomain.SOCIAL_AND_EMOTIONAL_HEALTH,
        question="Stress is when someone feels tense, nervous, anxious or can't sleep at night because their mind is troubled. How stressed are you?",
        loinc_code="93038-8",
        dome_layer=4,  # Health — mental health
        dome_field="stress_level",
    ),

    # ── Optional Measures ───────────────────────────────────────
    PRAPAREItem(
        item_id="prapare_safety",
        domain=PRAPAREDomain.OPTIONAL_MEASURES,
        question="In the past year, have you been afraid of your partner or ex-partner?",
        loinc_code="93028-9",
        dome_layer=8,  # Community — safety
        dome_field="interpersonal_safety",
    ),
    PRAPAREItem(
        item_id="prapare_refugee",
        domain=PRAPAREDomain.OPTIONAL_MEASURES,
        question="Are you a refugee?",
        loinc_code="93027-1",
        dome_layer=1,  # Legal — immigration status
        dome_field="refugee_status",
    ),
    PRAPAREItem(
        item_id="prapare_incarceration",
        domain=PRAPAREDomain.OPTIONAL_MEASURES,
        question="In the past year, have you spent more than 2 nights in a row in a jail, prison, detention center, or juvenile correction facility?",
        loinc_code="93026-3",
        dome_layer=1,  # Legal — justice involvement
        dome_field="justice_involvement",
    ),
]


# ═══════════════════════════════════════════════════════════════
# AHC-HRSN — Accountable Health Communities
# Health-Related Social Needs Screening Tool
# ═══════════════════════════════════════════════════════════════

class AHCDomain(str, Enum):
    """AHC-HRSN screening domains — 5 core + supplemental."""
    # Core domains (required)
    HOUSING_INSTABILITY = "housing_instability"
    FOOD_INSECURITY = "food_insecurity"
    TRANSPORTATION_PROBLEMS = "transportation_problems"
    UTILITY_HELP_NEEDS = "utility_help_needs"
    INTERPERSONAL_SAFETY = "interpersonal_safety"
    # Supplemental domains
    FINANCIAL_STRAIN = "financial_strain"
    EMPLOYMENT = "employment"
    FAMILY_COMMUNITY_SUPPORT = "family_community_support"
    EDUCATION = "education"
    PHYSICAL_ACTIVITY = "physical_activity"
    SUBSTANCE_USE = "substance_use"
    MENTAL_HEALTH = "mental_health"
    DISABILITIES = "disabilities"


class AHCScreeningItem(BaseModel):
    """A single AHC-HRSN screening item with dome layer mapping."""
    item_id: str
    domain: AHCDomain
    question: str
    loinc_code: str
    response: Optional[str] = None
    positive_screen: bool = False      # True if response indicates need
    # Dome mapping
    dome_layer: int
    dome_field: str
    severity: Optional[Literal["none", "mild", "moderate", "severe"]] = None


AHC_INSTRUMENT: List[AHCScreeningItem] = [
    # ── Core: Housing Instability ───────────────────────────────
    AHCScreeningItem(
        item_id="ahc_housing_1",
        domain=AHCDomain.HOUSING_INSTABILITY,
        question="What is your living situation today?",
        loinc_code="71802-3",
        dome_layer=5,
        dome_field="current_housing.tenure",
    ),
    AHCScreeningItem(
        item_id="ahc_housing_2",
        domain=AHCDomain.HOUSING_INSTABILITY,
        question="Think about the place you live. Do you have problems with any of the following? (pest infestations, mold, lead paint, inadequate heat/AC, water leaks, none)",
        loinc_code="93033-9",
        dome_layer=5,
        dome_field="current_housing.environmental_hazards",
    ),
    AHCScreeningItem(
        item_id="ahc_housing_3",
        domain=AHCDomain.HOUSING_INSTABILITY,
        question="In the past 12 months, was there a time when you were not able to pay the mortgage or rent on time?",
        loinc_code="93031-3",
        dome_layer=5,
        dome_field="housing_stability_score",
    ),

    # ── Core: Food Insecurity ───────────────────────────────────
    AHCScreeningItem(
        item_id="ahc_food_1",
        domain=AHCDomain.FOOD_INSECURITY,
        question="Within the past 12 months, you worried that your food would run out before you got money to buy more.",
        loinc_code="88122-7",
        dome_layer=9,
        dome_field="food_access_score",
    ),
    AHCScreeningItem(
        item_id="ahc_food_2",
        domain=AHCDomain.FOOD_INSECURITY,
        question="Within the past 12 months, the food you bought just didn't last and you didn't have money to get more.",
        loinc_code="88123-5",
        dome_layer=9,
        dome_field="food_access_score",
    ),

    # ── Core: Transportation Problems ───────────────────────────
    AHCScreeningItem(
        item_id="ahc_transport_1",
        domain=AHCDomain.TRANSPORTATION_PROBLEMS,
        question="In the past 12 months, has lack of reliable transportation kept you from medical appointments, meetings, work or from getting things needed for daily living?",
        loinc_code="93030-4",
        dome_layer=2,
        dome_field="transportation_barrier",
    ),

    # ── Core: Utility Help Needs ────────────────────────────────
    AHCScreeningItem(
        item_id="ahc_utility_1",
        domain=AHCDomain.UTILITY_HELP_NEEDS,
        question="In the past 12 months has the electric, gas, oil, or water company threatened to shut off services in your home?",
        loinc_code="93028-9",
        dome_layer=3,
        dome_field="utility_difficulty",
    ),

    # ── Core: Interpersonal Safety ──────────────────────────────
    AHCScreeningItem(
        item_id="ahc_safety_1",
        domain=AHCDomain.INTERPERSONAL_SAFETY,
        question="How often does anyone, including family and friends, physically hurt you?",
        loinc_code="93026-3",
        dome_layer=8,
        dome_field="interpersonal_safety",
    ),
    AHCScreeningItem(
        item_id="ahc_safety_2",
        domain=AHCDomain.INTERPERSONAL_SAFETY,
        question="How often does anyone, including family and friends, insult or talk down to you?",
        loinc_code="93025-5",
        dome_layer=8,
        dome_field="interpersonal_safety",
    ),
    AHCScreeningItem(
        item_id="ahc_safety_3",
        domain=AHCDomain.INTERPERSONAL_SAFETY,
        question="How often does anyone, including family and friends, threaten you with harm?",
        loinc_code="93024-8",
        dome_layer=8,
        dome_field="interpersonal_safety",
    ),
    AHCScreeningItem(
        item_id="ahc_safety_4",
        domain=AHCDomain.INTERPERSONAL_SAFETY,
        question="How often does anyone, including family and friends, scream or curse at you?",
        loinc_code="93023-0",
        dome_layer=8,
        dome_field="interpersonal_safety",
    ),

    # ── Supplemental: Financial Strain ──────────────────────────
    AHCScreeningItem(
        item_id="ahc_financial_1",
        domain=AHCDomain.FINANCIAL_STRAIN,
        question="How hard is it for you to pay for the very basics like food, housing, medical care, and heating?",
        loinc_code="76513-1",
        dome_layer=3,
        dome_field="financial_strain_level",
    ),

    # ── Supplemental: Employment ────────────────────────────────
    AHCScreeningItem(
        item_id="ahc_employment_1",
        domain=AHCDomain.EMPLOYMENT,
        question="Do you want help finding or keeping work or a job?",
        loinc_code="93028-9",
        dome_layer=6,
        dome_field="employment_assistance_need",
    ),

    # ── Supplemental: Family & Community Support ────────────────
    AHCScreeningItem(
        item_id="ahc_support_1",
        domain=AHCDomain.FAMILY_COMMUNITY_SUPPORT,
        question="If for any reason you need help with day-to-day activities such as bathing, preparing meals, shopping, managing finances, etc., do you get the help you need?",
        loinc_code="93027-1",
        dome_layer=8,
        dome_field="support_network_strength",
    ),
    AHCScreeningItem(
        item_id="ahc_support_2",
        domain=AHCDomain.FAMILY_COMMUNITY_SUPPORT,
        question="How often do you feel lonely or isolated from those around you?",
        loinc_code="93026-3",
        dome_layer=8,
        dome_field="isolation_risk_score",
    ),

    # ── Supplemental: Education ─────────────────────────────────
    AHCScreeningItem(
        item_id="ahc_education_1",
        domain=AHCDomain.EDUCATION,
        question="Do you want help with school or training? For example, starting or completing job training or getting a GED or equivalent.",
        loinc_code="93025-5",
        dome_layer=7,
        dome_field="education_assistance_need",
    ),

    # ── Supplemental: Substance Use ─────────────────────────────
    AHCScreeningItem(
        item_id="ahc_substance_1",
        domain=AHCDomain.SUBSTANCE_USE,
        question="How many times in the past 12 months have you had 5 or more drinks in a day (males) or 4 or more drinks in a day (females)?",
        loinc_code="93024-8",
        dome_layer=4,
        dome_field="substance_use_screen",
    ),
    AHCScreeningItem(
        item_id="ahc_substance_2",
        domain=AHCDomain.SUBSTANCE_USE,
        question="How many times in the past 12 months have you used tobacco products?",
        loinc_code="93023-0",
        dome_layer=4,
        dome_field="tobacco_use_screen",
    ),

    # ── Supplemental: Mental Health ─────────────────────────────
    AHCScreeningItem(
        item_id="ahc_mental_1",
        domain=AHCDomain.MENTAL_HEALTH,
        question="Over the past 2 weeks, how often have you been bothered by feeling down, depressed, or hopeless?",
        loinc_code="44255-8",  # PHQ-2 item
        dome_layer=4,
        dome_field="phq2_score",
    ),
    AHCScreeningItem(
        item_id="ahc_mental_2",
        domain=AHCDomain.MENTAL_HEALTH,
        question="Over the past 2 weeks, how often have you been bothered by little interest or pleasure in doing things?",
        loinc_code="44250-9",  # PHQ-2 item
        dome_layer=4,
        dome_field="phq2_score",
    ),

    # ── Supplemental: Disabilities ──────────────────────────────
    AHCScreeningItem(
        item_id="ahc_disability_1",
        domain=AHCDomain.DISABILITIES,
        question="Are you deaf, or do you have serious difficulty hearing?",
        loinc_code="93022-2",
        dome_layer=4,
        dome_field="disability_screen",
    ),
    AHCScreeningItem(
        item_id="ahc_disability_2",
        domain=AHCDomain.DISABILITIES,
        question="Are you blind, or do you have serious difficulty seeing, even when wearing glasses?",
        loinc_code="93021-4",
        dome_layer=4,
        dome_field="disability_screen",
    ),
    AHCScreeningItem(
        item_id="ahc_disability_3",
        domain=AHCDomain.DISABILITIES,
        question="Because of a physical, mental, or emotional condition, do you have difficulty doing errands alone such as visiting a doctor's office or shopping?",
        loinc_code="93020-6",
        dome_layer=10,  # Autonomy
        dome_field="functional_limitations",
    ),
]


# ═══════════════════════════════════════════════════════════════
# SDOH ↔ DOME LAYER MAPPING
# ═══════════════════════════════════════════════════════════════

class SDOHLayerMapping(BaseModel):
    """Maps an SDOH domain to specific dome layers and fields."""
    sdoh_domain: str
    sdoh_instrument: str          # "PRAPARE" or "AHC-HRSN"
    primary_dome_layer: int
    secondary_dome_layers: List[int] = Field(default_factory=list)
    dome_fields: List[str] = Field(default_factory=list)
    scoring_weight: float = 1.0   # How much this domain contributes to layer completeness
    government_systems: List[str] = Field(default_factory=list)  # Related systems in Layer 2


# Complete SDOH → Dome mapping
SDOH_DOME_MAPPINGS: List[SDOHLayerMapping] = [
    SDOHLayerMapping(
        sdoh_domain="Housing Instability",
        sdoh_instrument="AHC-HRSN",
        primary_dome_layer=5,
        secondary_dome_layers=[3, 1],
        dome_fields=["current_housing", "housing_stability_score", "eviction_history"],
        scoring_weight=1.5,  # Housing instability affects nearly every other layer
        government_systems=["Section 8", "public housing", "rental assistance", "homelessness prevention"],
    ),
    SDOHLayerMapping(
        sdoh_domain="Food Insecurity",
        sdoh_instrument="AHC-HRSN",
        primary_dome_layer=9,
        secondary_dome_layers=[4, 3],
        dome_fields=["food_access_score"],
        scoring_weight=1.2,
        government_systems=["SNAP", "WIC", "school meal programs"],
    ),
    SDOHLayerMapping(
        sdoh_domain="Transportation Problems",
        sdoh_instrument="AHC-HRSN",
        primary_dome_layer=2,
        secondary_dome_layers=[6, 4],
        dome_fields=["transportation_barrier"],
        scoring_weight=1.0,
        government_systems=["transportation", "paratransit"],
    ),
    SDOHLayerMapping(
        sdoh_domain="Utility Help Needs",
        sdoh_instrument="AHC-HRSN",
        primary_dome_layer=3,
        secondary_dome_layers=[5],
        dome_fields=["utility_difficulty"],
        scoring_weight=0.8,
        government_systems=["LIHEAP", "utility assistance"],
    ),
    SDOHLayerMapping(
        sdoh_domain="Interpersonal Safety",
        sdoh_instrument="AHC-HRSN",
        primary_dome_layer=8,
        secondary_dome_layers=[4, 1, 5],
        dome_fields=["interpersonal_safety"],
        scoring_weight=1.5,
        government_systems=["family court", "domestic violence services", "victim services"],
    ),
    SDOHLayerMapping(
        sdoh_domain="Financial Strain",
        sdoh_instrument="AHC-HRSN",
        primary_dome_layer=3,
        secondary_dome_layers=[6, 1],
        dome_fields=["total_monthly_income", "total_monthly_expenses", "financial_strain_level"],
        scoring_weight=1.3,
        government_systems=["TANF", "EITC", "childcare subsidies"],
    ),
    SDOHLayerMapping(
        sdoh_domain="Employment",
        sdoh_instrument="AHC-HRSN",
        primary_dome_layer=6,
        secondary_dome_layers=[3, 7],
        dome_fields=["current_employment", "skills", "market_demand_match"],
        scoring_weight=1.2,
        government_systems=["employment services", "workforce development"],
    ),
    SDOHLayerMapping(
        sdoh_domain="Family & Community Support",
        sdoh_instrument="AHC-HRSN",
        primary_dome_layer=8,
        secondary_dome_layers=[10],
        dome_fields=["connections", "isolation_risk_score", "support_network_strength"],
        scoring_weight=1.1,
        government_systems=[],
    ),
    SDOHLayerMapping(
        sdoh_domain="Education",
        sdoh_instrument="AHC-HRSN",
        primary_dome_layer=7,
        secondary_dome_layers=[6],
        dome_fields=["highest_level", "credential_gaps", "personalized_pathways"],
        scoring_weight=1.0,
        government_systems=["public education", "Pell Grant", "workforce development"],
    ),
    SDOHLayerMapping(
        sdoh_domain="Personal Characteristics",
        sdoh_instrument="PRAPARE",
        primary_dome_layer=4,
        secondary_dome_layers=[1],
        dome_fields=["patient.race", "patient.ethnicity", "patient.communication"],
        scoring_weight=0.5,
        government_systems=[],
    ),
    SDOHLayerMapping(
        sdoh_domain="Mental Health",
        sdoh_instrument="AHC-HRSN",
        primary_dome_layer=4,
        secondary_dome_layers=[8, 10],
        dome_fields=["phq2_score", "conditions"],
        scoring_weight=1.3,
        government_systems=["substance abuse treatment", "Medicaid", "behavioral health"],
    ),
    SDOHLayerMapping(
        sdoh_domain="Substance Use",
        sdoh_instrument="AHC-HRSN",
        primary_dome_layer=4,
        secondary_dome_layers=[1, 6],
        dome_fields=["substance_use_screen", "tobacco_use_screen"],
        scoring_weight=1.1,
        government_systems=["substance abuse treatment", "Medicaid"],
    ),
    SDOHLayerMapping(
        sdoh_domain="Disabilities",
        sdoh_instrument="AHC-HRSN",
        primary_dome_layer=4,
        secondary_dome_layers=[10, 6, 5],
        dome_fields=["disability_screen", "functional_limitations"],
        scoring_weight=1.2,
        government_systems=["SSI", "SSDI", "vocational rehabilitation", "ADA services"],
    ),
]


# ═══════════════════════════════════════════════════════════════
# SDOH SCREENING INTEGRATION
# ═══════════════════════════════════════════════════════════════

class SDOHScreeningResult(BaseModel):
    """
    Complete SDOH screening result for a dome subject.
    Can be populated from PRAPARE, AHC-HRSN, or both.

    This is the bridge between standard healthcare screenings
    and the dome's 12-layer architecture.
    """
    screening_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    instrument: str                    # "PRAPARE", "AHC-HRSN", "both"
    screening_date: Optional[str] = None
    screener: Optional[str] = None     # Who administered the screening

    # Responses
    prapare_responses: List[PRAPAREItem] = Field(default_factory=list)
    ahc_responses: List[AHCScreeningItem] = Field(default_factory=list)

    # Computed needs summary
    positive_screens: List[str] = Field(default_factory=list)
    # e.g., ["housing_instability", "food_insecurity", "interpersonal_safety"]
    risk_score: float = 0.0            # Aggregate risk (0-100)
    priority_domains: List[str] = Field(default_factory=list)

    # Dome layer impact mapping
    layer_impacts: Dict[int, float] = Field(default_factory=dict)
    # Layer number → risk severity (0-1). e.g., {5: 0.8, 3: 0.6, 8: 0.9}

    def compute_layer_impacts(self) -> Dict[int, float]:
        """
        Compute which dome layers are most affected by this person's
        social determinants. Used by the dome scoring system.
        """
        impacts: Dict[int, float] = {}

        for mapping in SDOH_DOME_MAPPINGS:
            domain_risk = 0.0
            # Check PRAPARE responses
            for item in self.prapare_responses:
                if item.risk_level in ("high", "critical"):
                    if item.dome_layer == mapping.primary_dome_layer:
                        domain_risk = max(domain_risk, 0.8 if item.risk_level == "high" else 1.0)
                elif item.risk_level == "moderate":
                    if item.dome_layer == mapping.primary_dome_layer:
                        domain_risk = max(domain_risk, 0.5)

            # Check AHC responses
            for item in self.ahc_responses:
                if item.positive_screen:
                    if item.dome_layer == mapping.primary_dome_layer:
                        severity_map = {"none": 0, "mild": 0.3, "moderate": 0.6, "severe": 0.9}
                        domain_risk = max(
                            domain_risk,
                            severity_map.get(item.severity or "moderate", 0.5),
                        )

            if domain_risk > 0:
                # Apply to primary layer
                layer = mapping.primary_dome_layer
                weighted = domain_risk * mapping.scoring_weight
                impacts[layer] = max(impacts.get(layer, 0), weighted)

                # Apply reduced impact to secondary layers
                for sec_layer in mapping.secondary_dome_layers:
                    sec_impact = domain_risk * 0.4 * mapping.scoring_weight
                    impacts[sec_layer] = max(impacts.get(sec_layer, 0), sec_impact)

        self.layer_impacts = impacts
        return impacts


import uuid  # noqa: E402 — needed for SDOHScreeningResult default
