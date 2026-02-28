"""
DOMES v2 — Seed Data

Populates the database with 5 archetypal characters representing the full
range of DOMES use cases, plus reference data (government systems).

The 5 characters:
    1. Robert Jackson (45)  — The Permanent Crisis
       Chronically homeless 7+ years, schizoaffective disorder,
       47 ER visits/year, 9 simultaneous systems, $112,100 fragmented cost

    2. Marcus Thompson (34) — The Revolving Door
       Post-incarceration, SUD, newly homeless, $87,400 fragmented cost

    3. Sarah Chen (28)      — The Split Family
       Domestic violence survivor, split custody, $72,200 fragmented cost

    4. James Williams (52)  — The Forgotten Veteran
       Combat PTSD, Type 2 diabetes, housing instability, $94,100 fragmented cost

    5. Maria Rodriguez (16) — The System Child
       Foster care, juvenile justice, unaccompanied, $68,200 fragmented cost

Usage:
    python -m domes.seed                         # Run seed against configured DB
    DOMES_DATABASE_URL=... python -m domes.seed  # Override DB URL

For testing:
    from domes.seed import run_seed
    await run_seed(session)  # Pass your test session
"""
from __future__ import annotations

import asyncio
import hashlib
import logging
import uuid
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from domes.database import AsyncSessionLocal
from domes.enums import (
    AdherenceStatus,
    AssessmentStatus,
    AssessmentType,
    BiometricDevice,
    BiometricMetric,
    ConditionClinicalStatus,
    ConditionVerificationStatus,
    ConditionCategory,
    ConditionSeverity,
    DataDomain,
    DomeTrigger,
    EmploymentStatus,
    EncounterClass,
    EncounterStatus,
    EncounterType,
    EnrollmentStatus,
    Ethnicity,
    ExitDestination,
    FlourishingDomain,
    FragmentSourceType,
    Gender,
    GrantorRelationship,
    HousingStatus,
    MedicationCategory,
    MedicationStatus,
    ObservationCategory,
    ObservationStatus,
    ProgramType,
    Race,
    RiskLevel,
    SystemAPIAvailability,
    SystemDomain,
)
from domes.models.assessment import Assessment
from domes.models.biometric import BiometricReading
from domes.models.condition import Condition
from domes.models.consent import Consent, ConsentAuditEntry
from domes.models.dome import Dome
from domes.models.encounter import Encounter
from domes.models.enrollment import Enrollment
from domes.models.flourishing import FlourishingScore
from domes.models.fragment import Fragment
from domes.models.medication import Medication
from domes.models.observation import Observation
from domes.models.person import Person
from domes.models.system import GovernmentSystem

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Deterministic UUIDs for seed data (stable across re-runs)
# ---------------------------------------------------------------------------

def _seed_uuid(name: str) -> uuid.UUID:
    """Generate a deterministic UUID from a seed name using SHA-1."""
    return uuid.uuid5(uuid.NAMESPACE_DNS, f"domes.v2.seed.{name}")


# Character UUIDs
ROBERT_JACKSON_ID = _seed_uuid("robert.jackson")
MARCUS_THOMPSON_ID = _seed_uuid("marcus.thompson")
SARAH_CHEN_ID = _seed_uuid("sarah.chen")
JAMES_WILLIAMS_ID = _seed_uuid("james.williams")
MARIA_RODRIGUEZ_ID = _seed_uuid("maria.rodriguez")

# Government system UUIDs
SYS_HMIS_ID = _seed_uuid("system.hmis")
SYS_BHA_ID = _seed_uuid("system.bha")
SYS_MMIS_ID = _seed_uuid("system.mmis")
SYS_SUD_ID = _seed_uuid("system.sud_treatment")
SYS_CRISIS_ID = _seed_uuid("system.mobile_crisis")
SYS_HOSPITAL_ID = _seed_uuid("system.hospital")
SYS_SHELTER_ID = _seed_uuid("system.shelter")
SYS_HOUSING_ID = _seed_uuid("system.housing_authority")
SYS_PROBATION_ID = _seed_uuid("system.probation")
SYS_VA_ID = _seed_uuid("system.va_health")
SYS_CHILD_WELFARE_ID = _seed_uuid("system.child_welfare")
SYS_SNAP_ID = _seed_uuid("system.snap_fns")

# ---------------------------------------------------------------------------
# Helper: now() with tz
# ---------------------------------------------------------------------------

def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _days_ago(n: int) -> datetime:
    return _utcnow() - timedelta(days=n)


def _ssn_hash(ssn_digits: str) -> str:
    """Return SHA-256 hash of SSN (9 digits, no dashes)."""
    return hashlib.sha256(ssn_digits.encode()).hexdigest()


# ===========================================================================
# GOVERNMENT SYSTEMS (reference data)
# ===========================================================================

def _build_government_systems() -> list[GovernmentSystem]:
    """Build the 12 seed government systems."""
    return [
        GovernmentSystem(
            id=SYS_HMIS_ID,
            system_code="HMIS",
            system_name="Homeless Management Information System",
            agency="HUD / Local CoC",
            domain=SystemDomain.HOUSING,
            api_availability=SystemAPIAvailability.PARTNER_ONLY,
            privacy_laws=["HMIS_Privacy", "Privacy_Act"],
            fhir_base_url=None,
            api_base_url="https://hmis.hudexchange.info/api",
            is_active=True,
            notes="HMIS FY2024 CSV format; Clarity HMIS API. Primary housing data source for CoC.",
        ),
        GovernmentSystem(
            id=SYS_BHA_ID,
            system_code="BHA",
            system_name="Behavioral Health Authority",
            agency="State Behavioral Health Authority",
            domain=SystemDomain.BEHAVIORAL_HEALTH,
            api_availability=SystemAPIAvailability.PARTNER_ONLY,
            privacy_laws=["HIPAA", "42_CFR_Part_2", "State_Law"],
            fhir_base_url=None,
            api_base_url=None,
            is_active=True,
            notes="State BHA — mental health and SUD treatment records. 42 CFR Part 2 applies to SUD data.",
        ),
        GovernmentSystem(
            id=SYS_MMIS_ID,
            system_code="MMIS",
            system_name="Medicaid Management Information System",
            agency="CMS / State Medicaid Agency",
            domain=SystemDomain.HEALTH,
            api_availability=SystemAPIAvailability.LIMITED,
            privacy_laws=["HIPAA", "Privacy_Act"],
            fhir_base_url="https://medicaid.cms.gov/fhir/R4",
            api_base_url="https://medicaid.gov/api",
            is_active=True,
            notes="Claims data + enrollment. CMS Interoperability Rule requires FHIR R4 APIs by 2027.",
        ),
        GovernmentSystem(
            id=SYS_SUD_ID,
            system_code="SUD_TX",
            system_name="Substance Use Disorder Treatment Program",
            agency="SAMHSA / State BHA",
            domain=SystemDomain.BEHAVIORAL_HEALTH,
            api_availability=SystemAPIAvailability.NONE,
            privacy_laws=["42_CFR_Part_2", "HIPAA"],
            fhir_base_url=None,
            api_base_url=None,
            is_active=True,
            notes="Opioid treatment programs, MAT clinics, residential SUD. Strictest 42 CFR Part 2 protections.",
        ),
        GovernmentSystem(
            id=SYS_CRISIS_ID,
            system_code="MOBILE_CRISIS",
            system_name="Mobile Crisis Response Team",
            agency="988 / County Mental Health",
            domain=SystemDomain.BEHAVIORAL_HEALTH,
            api_availability=SystemAPIAvailability.LIMITED,
            privacy_laws=["HIPAA", "State_Law"],
            fhir_base_url=None,
            api_base_url=None,
            is_active=True,
            notes="988 Suicide & Crisis Lifeline dispatch and mobile crisis team. Crisis encounter records.",
        ),
        GovernmentSystem(
            id=SYS_HOSPITAL_ID,
            system_code="HOSPITAL_EHR",
            system_name="Hospital / EHR System",
            agency="Hospital Network",
            domain=SystemDomain.HEALTH,
            api_availability=SystemAPIAvailability.LIMITED,
            privacy_laws=["HIPAA", "HITECH"],
            fhir_base_url="https://hospital.example.org/fhir/R4",
            api_base_url=None,
            is_active=True,
            notes="Epic EHR FHIR R4 endpoint. ER visits, inpatient, discharge records.",
        ),
        GovernmentSystem(
            id=SYS_SHELTER_ID,
            system_code="SHELTER",
            system_name="Emergency Shelter / Transitional Housing",
            agency="Local CoC / Shelter Operator",
            domain=SystemDomain.HOUSING,
            api_availability=SystemAPIAvailability.PARTNER_ONLY,
            privacy_laws=["HMIS_Privacy"],
            fhir_base_url=None,
            api_base_url=None,
            is_active=True,
            notes="HMIS-connected shelter system. Bed availability, entry/exit dates.",
        ),
        GovernmentSystem(
            id=SYS_HOUSING_ID,
            system_code="HOUSING_AUTH",
            system_name="Public Housing Authority",
            agency="HUD / Local Housing Authority",
            domain=SystemDomain.HOUSING,
            api_availability=SystemAPIAvailability.NONE,
            privacy_laws=["Privacy_Act", "HMIS_Privacy"],
            fhir_base_url=None,
            api_base_url=None,
            is_active=True,
            notes="Section 8 HCV, Public Housing. Waitlist often 5-10 years for PSH units.",
        ),
        GovernmentSystem(
            id=SYS_PROBATION_ID,
            system_code="PROBATION",
            system_name="Probation / Parole System",
            agency="County Probation Department",
            domain=SystemDomain.JUSTICE,
            api_availability=SystemAPIAvailability.NONE,
            privacy_laws=["CJIS", "State_Law"],
            fhir_base_url=None,
            api_base_url=None,
            is_active=True,
            notes="CJIS-protected. Probation terms, check-in records, violations.",
        ),
        GovernmentSystem(
            id=SYS_VA_ID,
            system_code="VA_HEALTH",
            system_name="Veterans Affairs Health System",
            agency="U.S. Department of Veterans Affairs",
            domain=SystemDomain.VETERANS,
            api_availability=SystemAPIAvailability.LIMITED,
            privacy_laws=["HIPAA", "38_USC_5705", "Privacy_Act"],
            fhir_base_url="https://sandbox.api.va.gov/services/fhir/v0/R4",
            api_base_url="https://api.va.gov",
            is_active=True,
            notes="VA Lighthouse FHIR R4 API. VistA EHR. Mental health under 38 USC 5705 extra protection.",
        ),
        GovernmentSystem(
            id=SYS_CHILD_WELFARE_ID,
            system_code="CHILD_WELFARE",
            system_name="Child Welfare / DCFS",
            agency="State DCFS",
            domain=SystemDomain.CHILD_WELFARE,
            api_availability=SystemAPIAvailability.NONE,
            privacy_laws=["CAPTA", "FERPA", "State_Law"],
            fhir_base_url=None,
            api_base_url=None,
            is_active=True,
            notes="Foster care, DCFS case records, placement history. CAPTA protects abuse/neglect records.",
        ),
        GovernmentSystem(
            id=SYS_SNAP_ID,
            system_code="SNAP_FNS",
            system_name="SNAP / Food and Nutrition Service",
            agency="USDA / FNS",
            domain=SystemDomain.INCOME,
            api_availability=SystemAPIAvailability.NONE,
            privacy_laws=["Privacy_Act"],
            fhir_base_url=None,
            api_base_url=None,
            is_active=True,
            notes="SNAP benefits enrollment and eligibility. Batch data sharing only.",
        ),
    ]


# ===========================================================================
# CHARACTER 1: ROBERT JACKSON
# ===========================================================================

def _build_robert_jackson() -> Person:
    """
    Robert Jackson — The Permanent Crisis

    Age 45. Chronically homeless 7+ years. Schizoaffective disorder (F25.0).
    47 ER visits/year. 9 active government systems. Annual fragmented cost $112,100.
    DOB: 1980-03-15 (adjusted for current age ~45). Chicago, IL.
    """
    return Person(
        id=ROBERT_JACKSON_ID,
        first_name="Robert",
        last_name="Jackson",
        preferred_name="Bobby",
        date_of_birth=date(1980, 3, 15),
        gender=Gender.MAN,
        race=Race.BLACK_AFRICAN_AMERICAN,
        ethnicity=Ethnicity.NOT_HISPANIC_OR_LATINO,
        primary_language="en",
        # No fixed address — unsheltered
        city="Chicago",
        state="IL",
        county="Cook",
        census_tract="170310601001",  # Lower West Side / Grant Park area
        housing_status=HousingStatus.UNSHELTERED,
        housing_status_since=date(2017, 4, 1),  # 7+ years
        employment_status=EmploymentStatus.UNABLE_TO_WORK,
        veteran=False,
        chronic_homelessness=True,
        years_homeless=Decimal("7.8"),
        # Government IDs
        medicaid_id="IL-MCAID-RJ-48291",
        hmis_client_id="HMIS-COOK-00847291",
        probation_case_number="COOK-PROB-2019-8834",
        ssn_hash=_ssn_hash("412837462"),  # Fictional SSN
        fhir_resource_type="Patient",
        fhir_resource_id="rj-epic-patient-001",
        fhir_system="https://hospital.example.org/fhir/R4",
        created_by="seed_v2",
    )


def _build_robert_jackson_consent() -> Consent:
    """Robert's primary 42 CFR Part 2 compliant consent."""
    return Consent(
        id=_seed_uuid("robert.jackson.consent.primary"),
        person_id=ROBERT_JACKSON_ID,
        granting_person_id=ROBERT_JACKSON_ID,
        grantor_relationship=GrantorRelationship.SELF,
        receiving_organization_id=SYS_HMIS_ID,
        purpose="care_coordination",
        data_categories=[
            DataDomain.HEALTH.value,
            DataDomain.BEHAVIORAL_HEALTH.value,
            DataDomain.SUBSTANCE_USE.value,
            DataDomain.HOUSING.value,
            DataDomain.CRIMINAL_JUSTICE.value,
        ],
        is_42cfr_protected=True,
        cfr42_compliant=True,
        cfr42_disclosing_program="Chicago Continuum of Care HMIS",
        cfr42_information_description=(
            "Mental health treatment records, substance use disorder treatment records, "
            "housing history, emergency shelter utilization, and crisis response records."
        ),
        cfr42_right_to_revoke_stated=True,
        cfr42_signed=True,
        cfr42_signature_method="electronic",
        cfr42_date_signed=datetime(2024, 1, 15, 10, 30, tzinfo=timezone.utc),
        cfr42_expiration_event="Upon termination of care coordination services",
        is_active=True,
        expires_at=datetime(2025, 1, 15, tzinfo=timezone.utc),
        witness_name="Maria Gutierrez (Case Manager)",
        notes="Signed at Pacific Garden Mission intake. Verbal consent confirmed in English.",
        fhir_resource_type="Consent",
        created_by="seed_v2",
    )


def _build_robert_jackson_conditions() -> list[Condition]:
    """Robert's active diagnoses — schizoaffective, alcohol use disorder."""
    return [
        Condition(
            id=_seed_uuid("rj.condition.f25"),
            person_id=ROBERT_JACKSON_ID,
            clinical_status=ConditionClinicalStatus.ACTIVE,
            verification_status=ConditionVerificationStatus.CONFIRMED,
            category=ConditionCategory.PROBLEM_LIST_ITEM,
            severity=ConditionSeverity.SEVERE,
            icd10_code="F25.0",
            code_display="Schizoaffective disorder, bipolar type",
            onset_date=date(2008, 6, 1),
            is_chronic=True,
            is_42cfr_protected=False,
            sensitivity_label=None,
            asserter_name="Dr. Patricia Nguyen, MD",
            asserter_role="Psychiatrist",
            note=(
                "Long-standing schizoaffective disorder with bipolar features. "
                "Medication non-adherent due to housing instability. "
                "47 ER visits in CY2024 — primarily psychiatric crises. "
                "Has history of LAI (long-acting injectable) antipsychotic but lapsed 2022."
            ),
            source_system_id=SYS_BHA_ID,
            fhir_resource_type="Condition",
            created_by="seed_v2",
        ),
        Condition(
            id=_seed_uuid("rj.condition.z59"),
            person_id=ROBERT_JACKSON_ID,
            clinical_status=ConditionClinicalStatus.ACTIVE,
            verification_status=ConditionVerificationStatus.CONFIRMED,
            category=ConditionCategory.SDOH_CONDITION,
            severity=ConditionSeverity.SEVERE,
            icd10_code="Z59.0",
            code_display="Homelessness",
            onset_date=date(2017, 4, 1),
            is_chronic=True,
            is_42cfr_protected=False,
            note="Chronically homeless 7+ years. Primarily unsheltered — Grant Park, Lower Wacker Drive.",
            source_system_id=SYS_HMIS_ID,
            fhir_resource_type="Condition",
            created_by="seed_v2",
        ),
        Condition(
            id=_seed_uuid("rj.condition.f10"),
            person_id=ROBERT_JACKSON_ID,
            clinical_status=ConditionClinicalStatus.ACTIVE,
            verification_status=ConditionVerificationStatus.CONFIRMED,
            category=ConditionCategory.PROBLEM_LIST_ITEM,
            severity=ConditionSeverity.MODERATE,
            icd10_code="F10.20",
            code_display="Alcohol use disorder, moderate",
            onset_date=date(2015, 1, 1),
            is_chronic=True,
            is_42cfr_protected=True,  # F10-F19 = 42 CFR Part 2
            sensitivity_label="ETHUD",
            note="Co-occurring AUD. Has attempted SBIRT twice. Drinking as self-medication for psychotic symptoms.",
            source_system_id=SYS_BHA_ID,
            fhir_resource_type="Condition",
            created_by="seed_v2",
        ),
        Condition(
            id=_seed_uuid("rj.condition.z65"),
            person_id=ROBERT_JACKSON_ID,
            clinical_status=ConditionClinicalStatus.ACTIVE,
            verification_status=ConditionVerificationStatus.CONFIRMED,
            category=ConditionCategory.SDOH_CONDITION,
            icd10_code="Z65.3",
            code_display="Problems related to other legal circumstances",
            onset_date=date(2019, 8, 15),
            is_chronic=False,
            is_42cfr_protected=False,
            note="Probation for misdemeanor trespass. Active probation supervision.",
            source_system_id=SYS_PROBATION_ID,
            fhir_resource_type="Condition",
            created_by="seed_v2",
        ),
    ]


def _build_robert_jackson_encounters() -> list[Encounter]:
    """Sample ER encounters (representing 47/year) + mobile crisis."""
    encounters = []

    # 6 sample ER visits (of 47/year)
    er_dates = [
        _days_ago(12), _days_ago(34), _days_ago(67),
        _days_ago(98), _days_ago(134), _days_ago(178),
    ]
    for i, dt in enumerate(er_dates):
        enc = Encounter(
            id=_seed_uuid(f"rj.encounter.er.{i}"),
            person_id=ROBERT_JACKSON_ID,
            encounter_class=EncounterClass.EMERGENCY,
            encounter_type=EncounterType.ER_VISIT,
            status=EncounterStatus.COMPLETED,
            started_at=dt,
            ended_at=dt + timedelta(hours=8),
            duration_hours=8.0,
            primary_diagnosis_code="F25.0",
            primary_diagnosis_display="Schizoaffective disorder, bipolar type",
            reason_codes=["psychiatric_crisis", "medication_lapse"],
            facility_name="Cook County Health ED",
            facility_type="emergency_department",
            facility_city="Chicago",
            facility_state="IL",
            is_preventable=True,
            is_high_utilizer_event=True,
            is_42cfr_protected=False,
            estimated_cost=Decimal("1500.00"),
            actual_cost=Decimal("1487.50"),
            payer="Medicaid",
            source_system_id=SYS_HOSPITAL_ID,
            fhir_resource_type="Encounter",
            created_by="seed_v2",
        )
        encounters.append(enc)

    # Mobile crisis encounter
    crisis_enc = Encounter(
        id=_seed_uuid("rj.encounter.crisis.1"),
        person_id=ROBERT_JACKSON_ID,
        encounter_class=EncounterClass.FIELD,
        encounter_type=EncounterType.MOBILE_CRISIS_RESPONSE,
        status=EncounterStatus.COMPLETED,
        started_at=_days_ago(22),
        ended_at=_days_ago(22) + timedelta(hours=2),
        duration_hours=2.0,
        primary_diagnosis_code="F25.0",
        reason_codes=["988_dispatch", "public_disturbance", "medication_lapse"],
        facility_name="Chicago CARE Team",
        facility_type="mobile_crisis",
        facility_city="Chicago",
        facility_state="IL",
        is_high_utilizer_event=True,
        estimated_cost=Decimal("450.00"),
        payer="Medicaid",
        source_system_id=SYS_CRISIS_ID,
        fhir_resource_type="Encounter",
        created_by="seed_v2",
    )
    encounters.append(crisis_enc)

    # Shelter stay
    shelter_enc = Encounter(
        id=_seed_uuid("rj.encounter.shelter.1"),
        person_id=ROBERT_JACKSON_ID,
        encounter_class=EncounterClass.SHELTER,
        encounter_type=EncounterType.SHELTER_STAY,
        status=EncounterStatus.COMPLETED,
        started_at=_days_ago(90),
        ended_at=_days_ago(60),
        duration_hours=720.0,  # 30 days
        facility_name="Pacific Garden Mission",
        facility_type="emergency_shelter",
        facility_city="Chicago",
        facility_state="IL",
        estimated_cost=Decimal("3600.00"),  # $40/night x 30
        payer="HMIS_CoC",
        source_system_id=SYS_SHELTER_ID,
        fhir_resource_type="Encounter",
        created_by="seed_v2",
    )
    encounters.append(shelter_enc)

    return encounters


def _build_robert_jackson_medications() -> list[Medication]:
    """Robert's medications — primarily antipsychotics with poor adherence."""
    return [
        Medication(
            id=_seed_uuid("rj.medication.olanzapine"),
            person_id=ROBERT_JACKSON_ID,
            status=MedicationStatus.ACTIVE,
            medication_category=MedicationCategory.ANTIPSYCHOTIC,
            rxnorm_code="2059017",
            medication_name="Olanzapine",
            generic_name="olanzapine",
            brand_name="Zyprexa",
            dosage_text="10 mg orally once daily",
            dose_quantity=Decimal("10"),
            dose_unit="mg",
            frequency="QD",
            route="oral",
            start_date=date(2023, 8, 1),
            days_supply=30,
            refills_authorized=11,
            refills_remaining=3,
            is_mat=False,
            is_controlled=False,
            is_42cfr_protected=False,
            adherence_status=AdherenceStatus.NON_ADHERENT,
            adherence_pct=0.23,  # Only 23% adherent — major clinical concern
            last_filled_date=date(2024, 9, 12),
            prescriber_name="Dr. Patricia Nguyen, MD",
            prescriber_npi="1234567890",
            pharmacy_name="Walgreens - Lower West Side",
            source_system_id=SYS_MMIS_ID,
            fhir_resource_type="MedicationRequest",
            notes=(
                "CRITICAL: 23% adherence rate. Robert frequently loses or sells medication. "
                "ACT team recommend long-acting injectable (LAI) — Aristada monthly injection "
                "when housing stable. Last IM injection attempt Dec 2022 — no follow-through."
            ),
            created_by="seed_v2",
        ),
        Medication(
            id=_seed_uuid("rj.medication.valproate"),
            person_id=ROBERT_JACKSON_ID,
            status=MedicationStatus.STOPPED,
            medication_category=MedicationCategory.MOOD_STABILIZER,
            rxnorm_code="11118",
            medication_name="Valproate",
            generic_name="valproic acid",
            brand_name="Depakote",
            dosage_text="500 mg orally twice daily",
            dose_quantity=Decimal("500"),
            dose_unit="mg",
            frequency="BID",
            route="oral",
            start_date=date(2022, 1, 15),
            end_date=date(2023, 3, 1),
            is_mat=False,
            is_controlled=False,
            is_42cfr_protected=False,
            adherence_status=AdherenceStatus.NON_ADHERENT,
            adherence_pct=0.10,
            prescriber_name="Dr. Patricia Nguyen, MD",
            source_system_id=SYS_BHA_ID,
            fhir_resource_type="MedicationRequest",
            notes="Discontinued — unable to maintain consistent dosing while unsheltered.",
            created_by="seed_v2",
        ),
    ]


def _build_robert_jackson_assessments() -> list[Assessment]:
    """Robert's most recent standardized assessments."""
    return [
        Assessment(
            id=_seed_uuid("rj.assessment.vispdat.2024"),
            person_id=ROBERT_JACKSON_ID,
            assessment_type=AssessmentType.VI_SPDAT,
            assessment_status=AssessmentStatus.COMPLETED,
            administered_at=_days_ago(45),
            total_score=Decimal("16"),
            score_interpretation=(
                "Score 16/17: High acuity — Permanent Supportive Housing (PSH) indicated. "
                "Prioritized for CoC PSH waitlist. Estimated wait: 14-18 months."
            ),
            risk_level=RiskLevel.CRITICAL,
            item_responses={
                "history_of_homelessness": 2,
                "risk_of_harm": 2,
                "emergency_service_use": 3,
                "risk_of_legal_issues": 1,
                "risk_of_exploitation": 2,
                "social_relationships": 2,
                "wellness": 4,
            },
            administered_by_name="James Carter",
            administered_by_role="Outreach Case Manager",
            administered_by_organization="Chicago CoC",
            is_42cfr_protected=False,
            source_system_id=SYS_HMIS_ID,
            fhir_resource_type="QuestionnaireResponse",
            notes="Administered at Lower Wacker camp site. Robert was cooperative but showed psychotic symptoms.",
            created_by="seed_v2",
        ),
        Assessment(
            id=_seed_uuid("rj.assessment.phq9.2024"),
            person_id=ROBERT_JACKSON_ID,
            assessment_type=AssessmentType.PHQ_9,
            assessment_status=AssessmentStatus.COMPLETED,
            administered_at=_days_ago(67),
            total_score=Decimal("21"),
            score_interpretation="Score 21/27: Severe depression",
            risk_level=RiskLevel.CRITICAL,
            item_responses={
                "q1_anhedonia": 3,
                "q2_depressed_mood": 3,
                "q3_sleep": 3,
                "q4_fatigue": 3,
                "q5_appetite": 2,
                "q6_worthlessness": 2,
                "q7_concentration": 2,
                "q8_psychomotor": 2,
                "q9_suicidal_ideation": 1,  # Passive SI without plan
            },
            administered_by_name="Dr. Patricia Nguyen, MD",
            administered_by_role="Psychiatrist",
            administered_by_organization="Cook County BHC",
            is_42cfr_protected=False,
            source_system_id=SYS_BHA_ID,
            fhir_resource_type="QuestionnaireResponse",
            notes="PHQ-9 item 9 = 1 (passive SI). C-SSRS follow-up completed — no active plan.",
            created_by="seed_v2",
        ),
    ]


def _build_robert_jackson_enrollments() -> list[Enrollment]:
    """Robert's active program enrollments (9 systems)."""
    return [
        Enrollment(
            id=_seed_uuid("rj.enrollment.medicaid"),
            person_id=ROBERT_JACKSON_ID,
            system_id=SYS_MMIS_ID,
            program_type=ProgramType.MEDICAID,
            status=EnrollmentStatus.ACTIVE,
            program_name="Illinois Medicaid",
            program_id="IL-MEDICAID",
            entry_date=date(2018, 6, 1),
            monthly_benefit_amount=Decimal("0"),
            annual_benefit_amount=Decimal("0"),
            notes="FFS Medicaid — not enrolled in MCO. Annual Medicaid spend $71,400 (ER-heavy).",
            created_by="seed_v2",
        ),
        Enrollment(
            id=_seed_uuid("rj.enrollment.hmis"),
            person_id=ROBERT_JACKSON_ID,
            system_id=SYS_HMIS_ID,
            program_type=ProgramType.EMERGENCY_SHELTER,
            status=EnrollmentStatus.ACTIVE,
            program_name="Chicago CoC HMIS — Street Outreach",
            program_id="COOK-CoC-0047",
            entry_date=date(2019, 3, 10),
            hmis_enrollment_id="ENR-2019-847291-001",
            hmis_project_type=4,  # Street outreach
            notes="Active in HMIS. VI-SPDAT score 16 — on PSH priority waitlist.",
            created_by="seed_v2",
        ),
        Enrollment(
            id=_seed_uuid("rj.enrollment.snap"),
            person_id=ROBERT_JACKSON_ID,
            system_id=SYS_SNAP_ID,
            program_type=ProgramType.SNAP,
            status=EnrollmentStatus.ACTIVE,
            program_name="SNAP / Food Stamps",
            entry_date=date(2020, 1, 1),
            monthly_benefit_amount=Decimal("281"),
            annual_benefit_amount=Decimal("3372"),
            created_by="seed_v2",
        ),
        Enrollment(
            id=_seed_uuid("rj.enrollment.probation"),
            person_id=ROBERT_JACKSON_ID,
            system_id=SYS_PROBATION_ID,
            program_type=ProgramType.PROBATION,
            status=EnrollmentStatus.ACTIVE,
            program_name="Cook County Probation",
            program_id=f"COOK-PROB-2019-8834",
            entry_date=date(2019, 10, 1),
            notes="12-month probation for trespass. Check-in weekly by phone; often misses.",
            created_by="seed_v2",
        ),
        Enrollment(
            id=_seed_uuid("rj.enrollment.bha"),
            person_id=ROBERT_JACKSON_ID,
            system_id=SYS_BHA_ID,
            program_type=ProgramType.CMHC,
            status=EnrollmentStatus.ACTIVE,
            program_name="Cook County Behavioral Health Clinic",
            program_id="CCBHC-NW-012",
            entry_date=date(2021, 2, 15),
            notes="ACT team referral pending. Currently case managed, not ACT enrolled.",
            created_by="seed_v2",
        ),
    ]


def _build_robert_jackson_biometrics() -> list[BiometricReading]:
    """Sample biometric readings for Robert — elevated HR, no CGM."""
    readings = []
    # 7 days of daily resting heart rate (elevated — stress, schizo meds)
    for i in range(7):
        readings.append(BiometricReading(
            id=_seed_uuid(f"rj.biometric.rhr.{i}"),
            person_id=ROBERT_JACKSON_ID,
            timestamp=_days_ago(i),
            metric=BiometricMetric.RESTING_HEART_RATE,
            value=Decimal(str(88 + (i % 5))),  # 88-92 bpm — elevated
            unit="bpm",
            loinc_code="40443-4",
            device=BiometricDevice.MANUAL,
            data_domain=DataDomain.BIOMETRIC,
            quality_score=0.85,
            is_anomaly=False,
            interval_seconds=86400,
            metadata_={"source": "shelter_intake_vitals"},
            created_by="seed_v2",
        ))
    return readings


def _build_robert_jackson_dome() -> tuple[Dome, list[FlourishingScore]]:
    """Robert's current DOMES snapshot — critical across all domains."""
    dome = Dome(
        id=_seed_uuid("rj.dome.current"),
        person_id=ROBERT_JACKSON_ID,
        assembled_at=_days_ago(1),
        is_current=True,
        trigger=DomeTrigger.SCHEDULED,
        assembly_version="2.0.0",
        cosm_score=Decimal("11.2"),
        cosm_label="Crisis",
        cosm_delta=Decimal("-2.1"),
        risk_scores={
            "crisis_30d": {"score": 0.94, "level": "critical", "drivers": [
                "47_annual_er_visits", "medication_nonadherence_0.23",
                "unsheltered_7_years", "active_psychosis", "probation_noncompliance"
            ]},
            "readmission_30d": {"score": 0.89, "level": "critical", "drivers": [
                "frequent_er_utilizer", "no_pcp", "no_stable_housing"
            ]},
            "housing_loss_90d": {"score": 0.95, "level": "critical", "drivers": [
                "already_unsheltered", "no_subsidy", "psh_waitlist_14mo"
            ]},
            "substance_relapse_30d": {"score": 0.72, "level": "high", "drivers": [
                "co_occurring_aud", "no_sud_treatment", "street_environment"
            ]},
            "medication_nonadherence_7d": {"score": 0.93, "level": "critical", "drivers": [
                "23pct_adherence", "no_stable_storage", "lacks_daily_structure"
            ]},
        },
        overall_risk_level=RiskLevel.CRITICAL,
        domain_scores={
            "health_vitality": {"score": 8, "trend": "declining", "threats": ["active_psychosis", "med_nonadherence", "47_er_annual"], "supports": ["medicaid_enrolled"]},
            "economic_prosperity": {"score": 12, "trend": "stable", "threats": ["no_income", "unable_to_work"], "supports": ["snap_active", "ssi_pending"]},
            "community_belonging": {"score": 10, "trend": "declining", "threats": ["social_isolation", "distrust_of_services"], "supports": ["outreach_worker_relationship"]},
            "environmental_harmony": {"score": 5, "trend": "declining", "threats": ["unsheltered", "extreme_weather_exposure", "pm25_elevated"], "supports": []},
            "creative_expression": {"score": 20, "trend": "stable", "threats": ["cognitive_impairment"], "supports": ["history_of_music"]},
            "intellectual_growth": {"score": 18, "trend": "stable", "threats": ["untreated_psychosis"], "supports": []},
            "physical_space_beauty": {"score": 3, "trend": "declining", "threats": ["no_private_space", "tent_dwelling"], "supports": []},
            "play_joy": {"score": 12, "trend": "stable", "threats": ["depression", "anhedonia"], "supports": []},
            "spiritual_depth": {"score": 25, "trend": "stable", "threats": [], "supports": ["pacific_garden_chapel_attendance"]},
            "love_relationships": {"score": 14, "trend": "declining", "threats": ["family_estrangement_12yr"], "supports": []},
            "purpose_meaning": {"score": 15, "trend": "declining", "threats": ["active_psychosis", "hopelessness"], "supports": ["past_employment_janitorial"]},
            "legacy_contribution": {"score": 10, "trend": "stable", "threats": ["active_crisis"], "supports": []},
        },
        fragmented_annual_cost=Decimal("112100.00"),
        coordinated_annual_cost=Decimal("41200.00"),
        delta=Decimal("70900.00"),
        lifetime_cost_estimate=Decimal("1446360.00"),
        cost_methodology=(
            "Fragmented: 47 ER visits @ $1,500 avg ($70,500) + shelter stays ($9,600) "
            "+ probation supervision ($4,200) + BHC outpatient ($7,800) + SNAP ($3,372) "
            "+ mobile crisis ($2,700) + medications ($2,400) + other ($11,528). "
            "Coordinated: PSH unit ($18,000) + ACT team ($14,400) + MCO managed Medicaid ($8,800). "
            "50-year lifetime projection at fragmented rate."
        ),
        systems_represented=["HMIS", "BHA", "MMIS", "SUD_TX", "MOBILE_CRISIS", "HOSPITAL_EHR", "SHELTER", "HOUSING_AUTH", "PROBATION"],
        systems_missing=["VA_HEALTH", "CHILD_WELFARE"],
        fragment_count=89,
        recommendations=[
            {"priority": 1, "domain": "health_vitality", "action": "Enroll in ACT (Assertive Community Treatment) team", "rationale": "47 ER visits preventable with intensive outreach", "urgency": "immediate", "estimated_impact": "$45,000+ annual savings", "system_responsible": "BHA"},
            {"priority": 2, "domain": "physical_space_beauty", "action": "Fast-track to top of PSH waitlist under CoC priority", "rationale": "VI-SPDAT 16 — highest acuity; homelessness is primary driver of all other crises", "urgency": "immediate", "estimated_impact": "Eliminates 60% of ER visits within 12 months of housing", "system_responsible": "HMIS/CoC"},
            {"priority": 3, "domain": "health_vitality", "action": "Switch to long-acting injectable antipsychotic (Aristada monthly)", "rationale": "23% oral adherence vs ~80% LAI adherence evidence base", "urgency": "soon", "estimated_impact": "Reduces psychiatric crises by ~70%", "system_responsible": "BHA"},
            {"priority": 4, "domain": "economic_prosperity", "action": "File SSI/SSDI application immediately (disabled, unable to work)", "rationale": "Robert meets disability criteria — estimated $894/month + Medicaid upgrade", "urgency": "soon", "estimated_impact": "$10,728 annual income + housing voucher eligibility", "system_responsible": "SSA"},
        ],
        crisis_flags=[
            "medication_nonadherence_severe",
            "47_annual_er_visits",
            "unsheltered_7_years",
            "phq9_21_severe_depression",
            "passive_suicidal_ideation",
        ],
        assembly_duration_ms=847,
        narrative_summary=(
            "Robert Jackson is a 45-year-old Black man experiencing his 7th year of chronic "
            "unsheltered homelessness in Chicago. He has schizoaffective disorder (bipolar type) "
            "and co-occurring alcohol use disorder, and is currently taking olanzapine with only "
            "23% adherence — primarily because he has no stable place to store medications or "
            "maintain daily routines. He made 47 emergency department visits in the last 12 months, "
            "each costing an average of $1,500 — a total of $70,500 in emergency costs alone. "
            "The system is spending $112,100 per year on reactive, fragmented care that is not "
            "treating the underlying cause: he needs a home. "
            "With Permanent Supportive Housing and an ACT team, his annual cost would drop to "
            "$41,200 — saving $70,900 per year — and his quality of life would improve dramatically. "
            "IMMEDIATE PRIORITIES: (1) ACT team enrollment today, (2) PSH fast-track, "
            "(3) Switch to monthly injectable antipsychotic, (4) SSI/SSDI filing."
        ),
        created_by="seed_v2",
    )

    # 12 flourishing scores tied to this dome
    domain_layer_map = {
        FlourishingDomain.HEALTH_VITALITY: (1, True),
        FlourishingDomain.ECONOMIC_PROSPERITY: (1, True),
        FlourishingDomain.COMMUNITY_BELONGING: (1, True),
        FlourishingDomain.ENVIRONMENTAL_HARMONY: (1, False),  # score <50
        FlourishingDomain.CREATIVE_EXPRESSION: (2, None),
        FlourishingDomain.INTELLECTUAL_GROWTH: (2, None),
        FlourishingDomain.PHYSICAL_SPACE_BEAUTY: (2, None),
        FlourishingDomain.PLAY_JOY: (2, None),
        FlourishingDomain.SPIRITUAL_DEPTH: (3, None),
        FlourishingDomain.LOVE_RELATIONSHIPS: (3, None),
        FlourishingDomain.PURPOSE_MEANING: (3, None),
        FlourishingDomain.LEGACY_CONTRIBUTION: (3, None),
    }

    scores_data = dome.domain_scores or {}
    flourishing_scores = []

    for domain, (layer, foundation_met) in domain_layer_map.items():
        ds = scores_data.get(domain.value, {})
        raw_score = ds.get("score", 15)
        risk = RiskLevel.CRITICAL if raw_score < 25 else (RiskLevel.HIGH if raw_score < 50 else RiskLevel.MODERATE)

        fs = FlourishingScore(
            id=_seed_uuid(f"rj.flourishing.{domain.value}"),
            person_id=ROBERT_JACKSON_ID,
            dome_id=dome.id,
            domain=domain,
            scored_at=dome.assembled_at,
            score=Decimal(str(raw_score)),
            trend=ds.get("trend", "declining"),
            risk_level=risk,
            threats=ds.get("threats"),
            supports=ds.get("supports"),
            domain_layer=layer,
            is_foundation_met=foundation_met,
            evidence_sources=["hmis_enrollment", "encounter_count", "assessment_phq9", "assessment_vispdat"],
            confidence=0.91,
            narrative=f"Robert's {domain.value.replace('_', ' ')} domain is at {raw_score}/100.",
            created_by="seed_v2",
        )
        flourishing_scores.append(fs)

    return dome, flourishing_scores


# ===========================================================================
# CHARACTER 2: MARCUS THOMPSON
# ===========================================================================

def _build_marcus_thompson() -> Person:
    """
    Marcus Thompson — The Revolving Door

    Age 34. Recently released from Cook County Jail (6-month sentence).
    Opioid use disorder (on buprenorphine MAT). Newly homeless post-release.
    $87,400 fragmented annual cost. Detroit, MI background; now Chicago.
    """
    return Person(
        id=MARCUS_THOMPSON_ID,
        first_name="Marcus",
        last_name="Thompson",
        date_of_birth=date(1991, 11, 8),
        gender=Gender.MAN,
        race=Race.BLACK_AFRICAN_AMERICAN,
        ethnicity=Ethnicity.NOT_HISPANIC_OR_LATINO,
        primary_language="en",
        city="Chicago",
        state="IL",
        county="Cook",
        housing_status=HousingStatus.SHELTERED,
        housing_status_since=date(2024, 8, 15),
        employment_status=EmploymentStatus.UNEMPLOYED,
        veteran=False,
        chronic_homelessness=False,
        years_homeless=Decimal("0.5"),
        medicaid_id="IL-MCAID-MT-29371",
        hmis_client_id="HMIS-COOK-00294871",
        probation_case_number="COOK-PAROLE-2024-2291",
        ssn_hash=_ssn_hash("531284917"),
        fhir_resource_type="Patient",
        created_by="seed_v2",
    )


def _build_marcus_thompson_conditions() -> list[Condition]:
    return [
        Condition(
            id=_seed_uuid("mt.condition.f11"),
            person_id=MARCUS_THOMPSON_ID,
            clinical_status=ConditionClinicalStatus.ACTIVE,
            verification_status=ConditionVerificationStatus.CONFIRMED,
            category=ConditionCategory.PROBLEM_LIST_ITEM,
            severity=ConditionSeverity.MODERATE,
            icd10_code="F11.20",
            code_display="Opioid use disorder, moderate",
            onset_date=date(2019, 3, 1),
            is_chronic=True,
            is_42cfr_protected=True,
            sensitivity_label="OPIOIDUD",
            note="OUD — currently on buprenorphine MAT. Stable while incarcerated; at risk post-release.",
            source_system_id=SYS_SUD_ID,
            fhir_resource_type="Condition",
            created_by="seed_v2",
        ),
        Condition(
            id=_seed_uuid("mt.condition.z59"),
            person_id=MARCUS_THOMPSON_ID,
            clinical_status=ConditionClinicalStatus.ACTIVE,
            verification_status=ConditionVerificationStatus.CONFIRMED,
            category=ConditionCategory.SDOH_CONDITION,
            icd10_code="Z59.0",
            code_display="Homelessness",
            onset_date=date(2024, 8, 15),
            is_chronic=False,
            note="Newly homeless post-release. Staying at Hilda's Place transitional shelter.",
            source_system_id=SYS_HMIS_ID,
            fhir_resource_type="Condition",
            created_by="seed_v2",
        ),
    ]


def _build_marcus_thompson_medications() -> list[Medication]:
    return [
        Medication(
            id=_seed_uuid("mt.medication.buprenorphine"),
            person_id=MARCUS_THOMPSON_ID,
            status=MedicationStatus.ACTIVE,
            medication_category=MedicationCategory.MAT,
            rxnorm_code="1864412",
            medication_name="Buprenorphine/Naloxone",
            generic_name="buprenorphine/naloxone",
            brand_name="Suboxone",
            dosage_text="16 mg/4 mg sublingual film once daily",
            dose_quantity=Decimal("16"),
            dose_unit="mg",
            frequency="QD",
            route="sublingual",
            start_date=date(2024, 8, 20),
            days_supply=30,
            refills_authorized=5,
            refills_remaining=4,
            is_mat=True,
            is_controlled=True,
            dea_schedule=3,
            is_42cfr_protected=True,
            adherence_status=AdherenceStatus.ADHERENT,
            adherence_pct=0.87,
            last_filled_date=date(2024, 10, 1),
            prescriber_name="Dr. Keisha Johnson, DO",
            source_system_id=SYS_SUD_ID,
            fhir_resource_type="MedicationRequest",
            notes="MOUD via SUD clinic. Doing well — needs stable housing to maintain.",
            created_by="seed_v2",
        ),
    ]


def _build_marcus_thompson_dome() -> tuple[Dome, list[FlourishingScore]]:
    """Marcus Thompson's current dome snapshot."""
    dome = Dome(
        id=_seed_uuid("mt.dome.current"),
        person_id=MARCUS_THOMPSON_ID,
        assembled_at=_days_ago(1),
        is_current=True,
        trigger=DomeTrigger.ENROLLMENT_CHANGE,
        assembly_version="2.0.0",
        cosm_score=Decimal("31.5"),
        cosm_label="Fragile",
        cosm_delta=Decimal("8.2"),  # Improving since release
        risk_scores={
            "substance_relapse_30d": {"score": 0.74, "level": "high", "drivers": ["post_incarceration", "housing_instability", "peer_network"]},
            "housing_loss_90d": {"score": 0.61, "level": "high", "drivers": ["emergency_shelter", "no_income", "felony_record"]},
            "crisis_30d": {"score": 0.45, "level": "moderate", "drivers": ["transition_stress", "sud_history"]},
        },
        overall_risk_level=RiskLevel.HIGH,
        fragmented_annual_cost=Decimal("87400.00"),
        coordinated_annual_cost=Decimal("28600.00"),
        delta=Decimal("58800.00"),
        systems_represented=["HMIS", "SUD_TX", "PROBATION", "MMIS", "SNAP_FNS"],
        systems_missing=["HOSPITAL_EHR", "VA_HEALTH"],
        fragment_count=34,
        recommendations=[
            {"priority": 1, "action": "Rapid rehousing within 90 days", "urgency": "immediate", "system_responsible": "HMIS/CoC"},
            {"priority": 2, "action": "Employment readiness program enrollment", "urgency": "soon", "system_responsible": "WorkForce"},
            {"priority": 3, "action": "Continue MAT; schedule 90-day MOUD follow-up", "urgency": "soon", "system_responsible": "SUD_TX"},
        ],
        crisis_flags=["post_incarceration_transition_high_risk"],
        assembly_duration_ms=412,
        narrative_summary=(
            "Marcus Thompson (34) was released from Cook County Jail 60 days ago after a "
            "6-month sentence for drug possession. He is currently on buprenorphine MAT and "
            "showing strong adherence (87%). He is staying at a transitional shelter and "
            "actively engaging with his probation officer. His COSM score of 31.5 reflects "
            "a fragile but improving situation. The highest risk is relapse if he loses "
            "shelter access — the 30-day relapse risk is 74% in that scenario. "
            "PRIORITY: Rapid rehousing within 90 days and employment placement."
        ),
        created_by="seed_v2",
    )

    flourishing_scores = []
    domain_scores = [
        (FlourishingDomain.HEALTH_VITALITY, 45, 1, True),
        (FlourishingDomain.ECONOMIC_PROSPERITY, 22, 1, False),
        (FlourishingDomain.COMMUNITY_BELONGING, 30, 1, False),
        (FlourishingDomain.ENVIRONMENTAL_HARMONY, 35, 1, False),
        (FlourishingDomain.CREATIVE_EXPRESSION, 40, 2, None),
        (FlourishingDomain.INTELLECTUAL_GROWTH, 38, 2, None),
        (FlourishingDomain.PHYSICAL_SPACE_BEAUTY, 28, 2, None),
        (FlourishingDomain.PLAY_JOY, 32, 2, None),
        (FlourishingDomain.SPIRITUAL_DEPTH, 35, 3, None),
        (FlourishingDomain.LOVE_RELATIONSHIPS, 25, 3, None),
        (FlourishingDomain.PURPOSE_MEANING, 28, 3, None),
        (FlourishingDomain.LEGACY_CONTRIBUTION, 20, 3, None),
    ]

    for domain, score, layer, foundation_met in domain_scores:
        risk = RiskLevel.CRITICAL if score < 25 else (RiskLevel.HIGH if score < 50 else RiskLevel.MODERATE)
        flourishing_scores.append(FlourishingScore(
            id=_seed_uuid(f"mt.flourishing.{domain.value}"),
            person_id=MARCUS_THOMPSON_ID,
            dome_id=dome.id,
            domain=domain,
            scored_at=dome.assembled_at,
            score=Decimal(str(score)),
            trend="improving",
            risk_level=risk,
            domain_layer=layer,
            is_foundation_met=foundation_met,
            confidence=0.78,
            created_by="seed_v2",
        ))

    return dome, flourishing_scores


# ===========================================================================
# CHARACTER 3: SARAH CHEN
# ===========================================================================

def _build_sarah_chen() -> Person:
    """
    Sarah Chen — The Split Family

    Age 28. DV survivor fleeing abuser. Children in temporary foster care
    while Sarah is in DV shelter. Navigating DCFS, housing, healthcare
    simultaneously. $72,200 fragmented annual cost. San Francisco, CA.
    """
    return Person(
        id=SARAH_CHEN_ID,
        first_name="Sarah",
        last_name="Chen",
        date_of_birth=date(1997, 7, 22),
        gender=Gender.WOMAN,
        race=Race.ASIAN,
        ethnicity=Ethnicity.NOT_HISPANIC_OR_LATINO,
        primary_language="en",
        secondary_languages=["zh-Cantonese"],
        city="San Francisco",
        state="CA",
        county="San Francisco",
        housing_status=HousingStatus.SHELTERED,
        housing_status_since=date(2024, 6, 3),
        employment_status=EmploymentStatus.UNEMPLOYED,
        veteran=False,
        chronic_homelessness=False,
        years_homeless=Decimal("0.6"),
        medicaid_id="CA-MCAID-SC-88421",
        hmis_client_id="HMIS-SF-00388421",
        child_welfare_case_number="DCFS-SF-2024-4421",
        ssn_hash=_ssn_hash("629381047"),
        fhir_resource_type="Patient",
        created_by="seed_v2",
    )


def _build_sarah_chen_conditions() -> list[Condition]:
    return [
        Condition(
            id=_seed_uuid("sc.condition.ptsd"),
            person_id=SARAH_CHEN_ID,
            clinical_status=ConditionClinicalStatus.ACTIVE,
            verification_status=ConditionVerificationStatus.CONFIRMED,
            category=ConditionCategory.PROBLEM_LIST_ITEM,
            severity=ConditionSeverity.MODERATE,
            icd10_code="F43.10",
            code_display="Post-traumatic stress disorder, unspecified",
            onset_date=date(2024, 5, 1),
            is_chronic=False,
            is_42cfr_protected=False,
            note="PTSD from intimate partner violence (IPV). In trauma-informed CBT.",
            source_system_id=SYS_BHA_ID,
            fhir_resource_type="Condition",
            created_by="seed_v2",
        ),
        Condition(
            id=_seed_uuid("sc.condition.z63"),
            person_id=SARAH_CHEN_ID,
            clinical_status=ConditionClinicalStatus.ACTIVE,
            verification_status=ConditionVerificationStatus.CONFIRMED,
            category=ConditionCategory.SDOH_CONDITION,
            icd10_code="Z63.31",
            code_display="Absence of family member due to child being placed in foster care",
            onset_date=date(2024, 6, 3),
            is_chronic=False,
            note="Two children (ages 4 and 6) placed in foster care while Sarah in DV shelter.",
            source_system_id=SYS_CHILD_WELFARE_ID,
            fhir_resource_type="Condition",
            created_by="seed_v2",
        ),
    ]


def _build_sarah_chen_dome() -> tuple[Dome, list[FlourishingScore]]:
    dome = Dome(
        id=_seed_uuid("sc.dome.current"),
        person_id=SARAH_CHEN_ID,
        assembled_at=_days_ago(1),
        is_current=True,
        trigger=DomeTrigger.NEW_DATA,
        assembly_version="2.0.0",
        cosm_score=Decimal("38.4"),
        cosm_label="Fragile",
        cosm_delta=Decimal("5.1"),
        risk_scores={
            "crisis_30d": {"score": 0.52, "level": "moderate", "drivers": ["family_separation", "ptsd_active"]},
            "housing_loss_90d": {"score": 0.48, "level": "moderate", "drivers": ["dv_shelter_60d_limit", "no_income"]},
        },
        overall_risk_level=RiskLevel.MODERATE,
        fragmented_annual_cost=Decimal("72200.00"),
        coordinated_annual_cost=Decimal("31800.00"),
        delta=Decimal("40400.00"),
        systems_represented=["HMIS", "CHILD_WELFARE", "BHA", "MMIS"],
        systems_missing=["SNAP_FNS", "SUD_TX"],
        fragment_count=28,
        recommendations=[
            {"priority": 1, "action": "Rapid reunification with children — DCFS family plan", "urgency": "immediate", "system_responsible": "CHILD_WELFARE"},
            {"priority": 2, "action": "Permanent housing with DV preference priority", "urgency": "soon", "system_responsible": "HMIS"},
            {"priority": 3, "action": "SNAP enrollment — currently unenrolled", "urgency": "soon", "system_responsible": "SNAP_FNS"},
        ],
        crisis_flags=["family_separation_active", "dv_shelter_time_limit_approaching"],
        assembly_duration_ms=318,
        narrative_summary=(
            "Sarah Chen (28) fled domestic violence 7 months ago with her two children (4 and 6). "
            "Her children are currently in temporary foster care while she stabilizes in a DV shelter. "
            "She is engaged in trauma-informed CBT and is highly motivated to reunify with her children. "
            "Her DV shelter placement has a 90-day limit expiring in 3 weeks — housing crisis imminent. "
            "PRIORITIES: Housing placement with DV preference, DCFS family reunification plan, SNAP enrollment."
        ),
        created_by="seed_v2",
    )

    flourishing_scores = []
    domain_scores = [
        (FlourishingDomain.HEALTH_VITALITY, 42, 1, True),
        (FlourishingDomain.ECONOMIC_PROSPERITY, 18, 1, False),
        (FlourishingDomain.COMMUNITY_BELONGING, 40, 1, True),
        (FlourishingDomain.ENVIRONMENTAL_HARMONY, 38, 1, False),
        (FlourishingDomain.CREATIVE_EXPRESSION, 55, 2, None),
        (FlourishingDomain.INTELLECTUAL_GROWTH, 60, 2, None),
        (FlourishingDomain.PHYSICAL_SPACE_BEAUTY, 25, 2, None),
        (FlourishingDomain.PLAY_JOY, 30, 2, None),
        (FlourishingDomain.SPIRITUAL_DEPTH, 50, 3, None),
        (FlourishingDomain.LOVE_RELATIONSHIPS, 35, 3, None),
        (FlourishingDomain.PURPOSE_MEANING, 48, 3, None),
        (FlourishingDomain.LEGACY_CONTRIBUTION, 45, 3, None),
    ]

    for domain, score, layer, foundation_met in domain_scores:
        risk = RiskLevel.CRITICAL if score < 25 else (RiskLevel.HIGH if score < 50 else RiskLevel.MODERATE)
        flourishing_scores.append(FlourishingScore(
            id=_seed_uuid(f"sc.flourishing.{domain.value}"),
            person_id=SARAH_CHEN_ID,
            dome_id=dome.id,
            domain=domain,
            scored_at=dome.assembled_at,
            score=Decimal(str(score)),
            trend="improving",
            risk_level=risk,
            domain_layer=layer,
            is_foundation_met=foundation_met,
            confidence=0.82,
            created_by="seed_v2",
        ))

    return dome, flourishing_scores


# ===========================================================================
# CHARACTER 4: JAMES WILLIAMS
# ===========================================================================

def _build_james_williams() -> Person:
    """
    James Williams — The Forgotten Veteran

    Age 52. Vietnam-era Navy veteran. Combat PTSD. Type 2 diabetes (poorly controlled).
    Lost housing after divorce. Navigating VA + civilian systems.
    $94,100 fragmented annual cost. Atlanta, GA.
    """
    return Person(
        id=JAMES_WILLIAMS_ID,
        first_name="James",
        last_name="Williams",
        preferred_name="Jim",
        date_of_birth=date(1973, 2, 28),
        gender=Gender.MAN,
        race=Race.BLACK_AFRICAN_AMERICAN,
        ethnicity=Ethnicity.NOT_HISPANIC_OR_LATINO,
        primary_language="en",
        city="Atlanta",
        state="GA",
        county="Fulton",
        housing_status=HousingStatus.SHELTERED,
        housing_status_since=date(2023, 11, 1),
        employment_status=EmploymentStatus.UNABLE_TO_WORK,
        veteran=True,
        chronic_homelessness=False,
        years_homeless=Decimal("1.2"),
        medicaid_id=None,
        medicare_id="1EG4-TE5-MK72",
        va_patient_id="VA-ATL-JW-00182744",
        hmis_client_id="HMIS-ATL-00182744",
        ssn_hash=_ssn_hash("734819265"),
        fhir_resource_type="Patient",
        fhir_resource_id="jw-va-patient-001",
        fhir_system="https://sandbox.api.va.gov/services/fhir/v0/R4",
        created_by="seed_v2",
    )


def _build_james_williams_conditions() -> list[Condition]:
    return [
        Condition(
            id=_seed_uuid("jw.condition.ptsd"),
            person_id=JAMES_WILLIAMS_ID,
            clinical_status=ConditionClinicalStatus.ACTIVE,
            verification_status=ConditionVerificationStatus.CONFIRMED,
            category=ConditionCategory.PROBLEM_LIST_ITEM,
            severity=ConditionSeverity.SEVERE,
            icd10_code="F43.12",
            code_display="Post-traumatic stress disorder, chronic",
            onset_date=date(1995, 1, 1),
            is_chronic=True,
            is_42cfr_protected=False,
            asserter_name="VA Mental Health Clinic",
            source_system_id=SYS_VA_ID,
            fhir_resource_type="Condition",
            note="Service-connected PTSD, 70% VA disability rating. Treatment-resistant. Not engaged in VA PTSD program.",
            created_by="seed_v2",
        ),
        Condition(
            id=_seed_uuid("jw.condition.dm2"),
            person_id=JAMES_WILLIAMS_ID,
            clinical_status=ConditionClinicalStatus.ACTIVE,
            verification_status=ConditionVerificationStatus.CONFIRMED,
            category=ConditionCategory.PROBLEM_LIST_ITEM,
            severity=ConditionSeverity.MODERATE,
            icd10_code="E11.9",
            code_display="Type 2 diabetes mellitus without complications",
            onset_date=date(2015, 4, 1),
            is_chronic=True,
            is_42cfr_protected=False,
            note="HbA1c 9.8% — poorly controlled. No CGM. Metformin adherence poor without stable housing.",
            source_system_id=SYS_VA_ID,
            fhir_resource_type="Condition",
            created_by="seed_v2",
        ),
    ]


def _build_james_williams_dome() -> tuple[Dome, list[FlourishingScore]]:
    dome = Dome(
        id=_seed_uuid("jw.dome.current"),
        person_id=JAMES_WILLIAMS_ID,
        assembled_at=_days_ago(1),
        is_current=True,
        trigger=DomeTrigger.SCHEDULED,
        assembly_version="2.0.0",
        cosm_score=Decimal("29.7"),
        cosm_label="Fragile",
        cosm_delta=Decimal("-1.3"),
        risk_scores={
            "crisis_30d": {"score": 0.58, "level": "moderate", "drivers": ["ptsd_chronic", "social_isolation", "diabetes_uncontrolled"]},
            "diabetes_complication_90d": {"score": 0.71, "level": "high", "drivers": ["hba1c_9.8", "no_cgm", "medication_irregular"]},
            "housing_loss_90d": {"score": 0.44, "level": "moderate", "drivers": ["emergency_shelter"]},
        },
        overall_risk_level=RiskLevel.HIGH,
        fragmented_annual_cost=Decimal("94100.00"),
        coordinated_annual_cost=Decimal("38400.00"),
        delta=Decimal("55700.00"),
        systems_represented=["VA_HEALTH", "HMIS", "MMIS"],
        systems_missing=["SNAP_FNS", "PROBATION"],
        fragment_count=52,
        recommendations=[
            {"priority": 1, "action": "HUD-VASH voucher application (veteran housing preference)", "urgency": "immediate", "system_responsible": "VA/HUD"},
            {"priority": 2, "action": "VA diabetes management + CGM prescription", "urgency": "immediate", "system_responsible": "VA_HEALTH"},
            {"priority": 3, "action": "VA PTSD treatment enrollment (CPT or EMDR)", "urgency": "soon", "system_responsible": "VA_HEALTH"},
        ],
        crisis_flags=["diabetes_hba1c_critical_9.8", "ptsd_untreated_chronic"],
        assembly_duration_ms=589,
        narrative_summary=(
            "James Williams (52) is a Navy veteran with chronic PTSD (70% service-connected) and "
            "Type 2 diabetes with an HbA1c of 9.8% — dangerously uncontrolled. He became homeless "
            "14 months ago following a divorce. He is eligible for HUD-VASH (veteran housing voucher) "
            "but has not applied. His diabetes complications risk is HIGH within 90 days without "
            "intervention. PRIORITIES: HUD-VASH application immediately, CGM prescription, VA PTSD enrollment."
        ),
        created_by="seed_v2",
    )

    flourishing_scores = []
    domain_scores = [
        (FlourishingDomain.HEALTH_VITALITY, 25, 1, True),
        (FlourishingDomain.ECONOMIC_PROSPERITY, 35, 1, False),
        (FlourishingDomain.COMMUNITY_BELONGING, 28, 1, False),
        (FlourishingDomain.ENVIRONMENTAL_HARMONY, 32, 1, False),
        (FlourishingDomain.CREATIVE_EXPRESSION, 30, 2, None),
        (FlourishingDomain.INTELLECTUAL_GROWTH, 42, 2, None),
        (FlourishingDomain.PHYSICAL_SPACE_BEAUTY, 22, 2, None),
        (FlourishingDomain.PLAY_JOY, 25, 2, None),
        (FlourishingDomain.SPIRITUAL_DEPTH, 40, 3, None),
        (FlourishingDomain.LOVE_RELATIONSHIPS, 20, 3, None),
        (FlourishingDomain.PURPOSE_MEANING, 28, 3, None),
        (FlourishingDomain.LEGACY_CONTRIBUTION, 30, 3, None),
    ]

    for domain, score, layer, foundation_met in domain_scores:
        risk = RiskLevel.CRITICAL if score < 25 else (RiskLevel.HIGH if score < 50 else RiskLevel.MODERATE)
        flourishing_scores.append(FlourishingScore(
            id=_seed_uuid(f"jw.flourishing.{domain.value}"),
            person_id=JAMES_WILLIAMS_ID,
            dome_id=dome.id,
            domain=domain,
            scored_at=dome.assembled_at,
            score=Decimal(str(score)),
            trend="stable",
            risk_level=risk,
            domain_layer=layer,
            is_foundation_met=foundation_met,
            confidence=0.85,
            created_by="seed_v2",
        ))

    return dome, flourishing_scores


# ===========================================================================
# CHARACTER 5: MARIA RODRIGUEZ
# ===========================================================================

def _build_maria_rodriguez() -> Person:
    """
    Maria Rodriguez — The System Child

    Age 16. In foster care since age 11 (5 placements). Juvenile justice
    involvement (truancy, shoplifting). No stable adult attachment.
    Unaccompanied minor. $68,200 fragmented annual cost. Los Angeles, CA.
    """
    return Person(
        id=MARIA_RODRIGUEZ_ID,
        first_name="Maria",
        last_name="Rodriguez",
        date_of_birth=date(2009, 9, 14),
        gender=Gender.WOMAN,
        race=Race.HISPANIC_LATINA_LATINX,
        ethnicity=Ethnicity.HISPANIC_OR_LATINO,
        primary_language="en",
        secondary_languages=["es"],
        city="Los Angeles",
        state="CA",
        county="Los Angeles",
        housing_status=HousingStatus.INSTITUTIONAL,  # Foster care placement
        housing_status_since=date(2020, 3, 1),
        employment_status=EmploymentStatus.NOT_IN_LABOR_FORCE,
        veteran=False,
        chronic_homelessness=False,
        years_homeless=Decimal("0"),
        medicaid_id="CA-MCAID-MR-10039",
        child_welfare_case_number="DCFS-LA-2020-10039",
        hmis_client_id=None,  # Minor — separate HMIS handling
        ssn_hash=_ssn_hash("826492017"),
        fhir_resource_type="Patient",
        created_by="seed_v2",
    )


def _build_maria_rodriguez_conditions() -> list[Condition]:
    return [
        Condition(
            id=_seed_uuid("mr.condition.rad"),
            person_id=MARIA_RODRIGUEZ_ID,
            clinical_status=ConditionClinicalStatus.ACTIVE,
            verification_status=ConditionVerificationStatus.CONFIRMED,
            category=ConditionCategory.PROBLEM_LIST_ITEM,
            severity=ConditionSeverity.MODERATE,
            icd10_code="F94.1",
            code_display="Reactive attachment disorder of childhood",
            onset_date=date(2021, 6, 1),
            is_chronic=True,
            is_42cfr_protected=False,
            note="RAD from early neglect + 5 foster placement disruptions. In DBT skills group.",
            source_system_id=SYS_BHA_ID,
            fhir_resource_type="Condition",
            created_by="seed_v2",
        ),
        Condition(
            id=_seed_uuid("mr.condition.z62"),
            person_id=MARIA_RODRIGUEZ_ID,
            clinical_status=ConditionClinicalStatus.ACTIVE,
            verification_status=ConditionVerificationStatus.CONFIRMED,
            category=ConditionCategory.SDOH_CONDITION,
            icd10_code="Z62.29",
            code_display="Upbringing away from parents, other",
            onset_date=date(2020, 3, 1),
            is_chronic=True,
            note="5 foster placements since 2020. Current placement: therapeutic group home.",
            source_system_id=SYS_CHILD_WELFARE_ID,
            fhir_resource_type="Condition",
            created_by="seed_v2",
        ),
    ]


def _build_maria_rodriguez_dome() -> tuple[Dome, list[FlourishingScore]]:
    dome = Dome(
        id=_seed_uuid("mr.dome.current"),
        person_id=MARIA_RODRIGUEZ_ID,
        assembled_at=_days_ago(1),
        is_current=True,
        trigger=DomeTrigger.SCHEDULED,
        assembly_version="2.0.0",
        cosm_score=Decimal("34.8"),
        cosm_label="Fragile",
        cosm_delta=Decimal("3.2"),
        risk_scores={
            "aging_out_risk": {"score": 0.81, "level": "high", "drivers": ["5_placements", "no_adult_connection", "2_years_to_18"]},
            "juvenile_justice_escalation_30d": {"score": 0.38, "level": "moderate", "drivers": ["truancy", "group_home_instability"]},
        },
        overall_risk_level=RiskLevel.HIGH,
        fragmented_annual_cost=Decimal("68200.00"),
        coordinated_annual_cost=Decimal("24800.00"),
        delta=Decimal("43400.00"),
        systems_represented=["CHILD_WELFARE", "BHA", "MMIS"],
        systems_missing=["HMIS", "SNAP_FNS", "PROBATION"],
        fragment_count=41,
        recommendations=[
            {"priority": 1, "action": "Assign CASA (Court Appointed Special Advocate) immediately", "urgency": "immediate", "system_responsible": "CHILD_WELFARE"},
            {"priority": 2, "action": "Extended foster care agreement to age 21 — begin planning NOW (2 years out)", "urgency": "soon", "system_responsible": "CHILD_WELFARE"},
            {"priority": 3, "action": "Stable therapeutic foster home (not group home)", "urgency": "immediate", "system_responsible": "CHILD_WELFARE"},
        ],
        crisis_flags=["aging_out_in_2_years_no_plan", "5_placement_disruptions"],
        assembly_duration_ms=276,
        narrative_summary=(
            "Maria Rodriguez (16) has been in the foster care system since age 11 with 5 placement "
            "disruptions. She is currently in a therapeutic group home in Los Angeles. She has "
            "reactive attachment disorder and is in DBT skills group. Without intervention, she will "
            "age out of foster care in 2 years with no family connection, no housing plan, and no "
            "income — the highest risk pathway to adult homelessness. "
            "PRIORITIES: CASA assignment, extended foster care agreement, stable family-style placement."
        ),
        created_by="seed_v2",
    )

    flourishing_scores = []
    domain_scores = [
        (FlourishingDomain.HEALTH_VITALITY, 48, 1, True),
        (FlourishingDomain.ECONOMIC_PROSPERITY, 15, 1, False),
        (FlourishingDomain.COMMUNITY_BELONGING, 30, 1, False),
        (FlourishingDomain.ENVIRONMENTAL_HARMONY, 42, 1, True),
        (FlourishingDomain.CREATIVE_EXPRESSION, 60, 2, None),
        (FlourishingDomain.INTELLECTUAL_GROWTH, 52, 2, None),
        (FlourishingDomain.PHYSICAL_SPACE_BEAUTY, 38, 2, None),
        (FlourishingDomain.PLAY_JOY, 45, 2, None),
        (FlourishingDomain.SPIRITUAL_DEPTH, 38, 3, None),
        (FlourishingDomain.LOVE_RELATIONSHIPS, 18, 3, None),
        (FlourishingDomain.PURPOSE_MEANING, 42, 3, None),
        (FlourishingDomain.LEGACY_CONTRIBUTION, 35, 3, None),
    ]

    for domain, score, layer, foundation_met in domain_scores:
        risk = RiskLevel.CRITICAL if score < 25 else (RiskLevel.HIGH if score < 50 else RiskLevel.MODERATE)
        flourishing_scores.append(FlourishingScore(
            id=_seed_uuid(f"mr.flourishing.{domain.value}"),
            person_id=MARIA_RODRIGUEZ_ID,
            dome_id=dome.id,
            domain=domain,
            scored_at=dome.assembled_at,
            score=Decimal(str(score)),
            trend="stable",
            risk_level=risk,
            domain_layer=layer,
            is_foundation_met=foundation_met,
            confidence=0.80,
            created_by="seed_v2",
        ))

    return dome, flourishing_scores


# ===========================================================================
# MAIN SEED FUNCTION
# ===========================================================================

async def run_seed(session: AsyncSession) -> None:
    """
    Execute the full DOMES v2 seed against the provided session.

    Idempotent — uses merge (upsert-by-PK) so re-running is safe.
    All objects use deterministic UUIDs.
    """
    logger.info("Starting DOMES v2 seed data load...")

    # ------------------------------------------------------------------
    # 1. Government systems
    # ------------------------------------------------------------------
    logger.info("Seeding government systems...")
    for system in _build_government_systems():
        await session.merge(system)

    await session.flush()

    # ------------------------------------------------------------------
    # 2. Character: Robert Jackson (The Permanent Crisis)
    # ------------------------------------------------------------------
    logger.info("Seeding Robert Jackson (The Permanent Crisis)...")

    rj = _build_robert_jackson()
    await session.merge(rj)
    await session.flush()

    await session.merge(_build_robert_jackson_consent())

    for condition in _build_robert_jackson_conditions():
        await session.merge(condition)

    for encounter in _build_robert_jackson_encounters():
        await session.merge(encounter)

    for medication in _build_robert_jackson_medications():
        await session.merge(medication)

    for assessment in _build_robert_jackson_assessments():
        await session.merge(assessment)

    for enrollment in _build_robert_jackson_enrollments():
        await session.merge(enrollment)

    for biometric in _build_robert_jackson_biometrics():
        await session.merge(biometric)

    rj_dome, rj_flourishing = _build_robert_jackson_dome()
    await session.merge(rj_dome)
    for fs in rj_flourishing:
        await session.merge(fs)

    await session.flush()

    # ------------------------------------------------------------------
    # 3. Character: Marcus Thompson (The Revolving Door)
    # ------------------------------------------------------------------
    logger.info("Seeding Marcus Thompson (The Revolving Door)...")

    mt = _build_marcus_thompson()
    await session.merge(mt)
    await session.flush()

    for condition in _build_marcus_thompson_conditions():
        await session.merge(condition)

    for medication in _build_marcus_thompson_medications():
        await session.merge(medication)

    mt_dome, mt_flourishing = _build_marcus_thompson_dome()
    await session.merge(mt_dome)
    for fs in mt_flourishing:
        await session.merge(fs)

    await session.flush()

    # ------------------------------------------------------------------
    # 4. Character: Sarah Chen (The Split Family)
    # ------------------------------------------------------------------
    logger.info("Seeding Sarah Chen (The Split Family)...")

    sc = _build_sarah_chen()
    await session.merge(sc)
    await session.flush()

    for condition in _build_sarah_chen_conditions():
        await session.merge(condition)

    sc_dome, sc_flourishing = _build_sarah_chen_dome()
    await session.merge(sc_dome)
    for fs in sc_flourishing:
        await session.merge(fs)

    await session.flush()

    # ------------------------------------------------------------------
    # 5. Character: James Williams (The Forgotten Veteran)
    # ------------------------------------------------------------------
    logger.info("Seeding James Williams (The Forgotten Veteran)...")

    jw = _build_james_williams()
    await session.merge(jw)
    await session.flush()

    for condition in _build_james_williams_conditions():
        await session.merge(condition)

    jw_dome, jw_flourishing = _build_james_williams_dome()
    await session.merge(jw_dome)
    for fs in jw_flourishing:
        await session.merge(fs)

    await session.flush()

    # ------------------------------------------------------------------
    # 6. Character: Maria Rodriguez (The System Child)
    # ------------------------------------------------------------------
    logger.info("Seeding Maria Rodriguez (The System Child)...")

    mr = _build_maria_rodriguez()
    await session.merge(mr)
    await session.flush()

    for condition in _build_maria_rodriguez_conditions():
        await session.merge(condition)

    mr_dome, mr_flourishing = _build_maria_rodriguez_dome()
    await session.merge(mr_dome)
    for fs in mr_flourishing:
        await session.merge(fs)

    await session.commit()

    logger.info(
        "DOMES v2 seed complete. "
        "Seeded: 12 government systems, 5 persons, 5 domes, 60 flourishing scores, "
        "conditions, encounters, medications, assessments, enrollments, biometrics."
    )
    logger.info("Character summary:")
    logger.info("  Robert Jackson (45) — COSM 11.2 (Crisis) — $112,100 fragmented — $70,900 savings")
    logger.info("  Marcus Thompson (34) — COSM 31.5 (Fragile) — $87,400 fragmented — $58,800 savings")
    logger.info("  Sarah Chen (28) — COSM 38.4 (Fragile) — $72,200 fragmented — $40,400 savings")
    logger.info("  James Williams (52) — COSM 29.7 (Fragile) — $94,100 fragmented — $55,700 savings")
    logger.info("  Maria Rodriguez (16) — COSM 34.8 (Fragile) — $68,200 fragmented — $43,400 savings")
    logger.info("  TOTAL SYSTEM SAVINGS IF COORDINATED: $269,200/year across 5 characters")


async def main() -> None:
    """CLI entry point: python -m domes.seed"""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    async with AsyncSessionLocal() as session:
        await run_seed(session)


if __name__ == "__main__":
    asyncio.run(main())
