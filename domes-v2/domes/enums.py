"""
DOMES v2 — System-wide Enumerations

All enumerations used across the data model. Organized by domain.
"""
from __future__ import annotations

import enum


# ---------------------------------------------------------------------------
# Person / Demographics
# ---------------------------------------------------------------------------

class HousingStatus(str, enum.Enum):
    """Current housing situation — aligned with HUD HMIS housing categories."""
    HOUSED = "housed"                   # Stable, permanent housing
    SHELTERED = "sheltered"             # Emergency shelter or transitional housing
    UNSHELTERED = "unsheltered"         # Street / places not meant for habitation
    INSTITUTIONAL = "institutional"     # Jail, hospital, nursing facility, etc.
    DOUBLED_UP = "doubled_up"           # Couch surfing / doubled-up (precariously housed)
    UNKNOWN = "unknown"


class EmploymentStatus(str, enum.Enum):
    """Employment status — aligned with HMIS EmploymentStatus data element."""
    EMPLOYED_FULL_TIME = "employed_full_time"
    EMPLOYED_PART_TIME = "employed_part_time"
    UNEMPLOYED = "unemployed"
    UNABLE_TO_WORK = "unable_to_work"
    NOT_IN_LABOR_FORCE = "not_in_labor_force"
    UNKNOWN = "unknown"


class Gender(str, enum.Enum):
    """Gender identity — aligned with HMIS gender list 3.06.1 and FHIR extensions."""
    WOMAN = "woman"
    MAN = "man"
    NON_BINARY = "non_binary"
    TRANSGENDER_WOMAN = "transgender_woman"
    TRANSGENDER_MAN = "transgender_man"
    CULTURALLY_SPECIFIC = "culturally_specific"
    DIFFERENT_IDENTITY = "different_identity"
    QUESTIONING = "questioning"
    UNKNOWN = "unknown"


class ImmigrationStatus(str, enum.Enum):
    US_CITIZEN = "us_citizen"
    LAWFUL_PERMANENT_RESIDENT = "lawful_permanent_resident"
    REFUGEE = "refugee"
    ASYLUM_SEEKER = "asylum_seeker"
    DACA = "daca"
    UNDOCUMENTED = "undocumented"
    VISA_HOLDER = "visa_holder"
    UNKNOWN = "unknown"


class Race(str, enum.Enum):
    """Race categories — aligned with HMIS and US Core FHIR extensions (OMB)."""
    AMERICAN_INDIAN_ALASKA_NATIVE = "american_indian_alaska_native"
    ASIAN = "asian"
    BLACK_AFRICAN_AMERICAN = "black_african_american"
    HISPANIC_LATINA_LATINX = "hispanic_latina_latinx"
    MIDDLE_EASTERN_NORTH_AFRICAN = "middle_eastern_north_african"
    NATIVE_HAWAIIAN_PACIFIC_ISLANDER = "native_hawaiian_pacific_islander"
    WHITE = "white"
    MULTIRACIAL = "multiracial"
    OTHER = "other"
    UNKNOWN = "unknown"


class Ethnicity(str, enum.Enum):
    """Hispanic/Latino ethnicity (separate from race per OMB standards)."""
    HISPANIC_OR_LATINO = "hispanic_or_latino"
    NOT_HISPANIC_OR_LATINO = "not_hispanic_or_latino"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Consent / Privacy
# ---------------------------------------------------------------------------

class DataDomain(str, enum.Enum):
    """Data sensitivity domains — drives consent requirements and access control."""
    HEALTH = "health"
    BEHAVIORAL_HEALTH = "behavioral_health"
    SUBSTANCE_USE = "substance_use"       # 42 CFR Part 2 — strictest protection
    CRIMINAL_JUSTICE = "criminal_justice"  # CJIS-protected
    HOUSING = "housing"
    EDUCATION = "education"               # FERPA-protected
    FINANCIAL = "financial"               # Privacy Act
    CHILD_WELFARE = "child_welfare"       # CAPTA/SACWIS
    BIOMETRIC = "biometric"
    ENVIRONMENTAL = "environmental"
    ALL = "all"


class ConsentPurpose(str, enum.Enum):
    """Purpose of consent — aligned with FHIR Consent.provision.purpose (ActReason)."""
    TREATMENT = "treatment"
    PAYMENT = "payment"
    HEALTHCARE_OPERATIONS = "healthcare_operations"
    CARE_COORDINATION = "care_coordination"
    RESEARCH = "research"
    PUBLIC_HEALTH = "public_health"
    EMERGENCY = "emergency"
    LEGAL = "legal"


class GrantorRelationship(str, enum.Enum):
    """Relationship of consent signer to the person."""
    SELF = "self"
    GUARDIAN = "guardian"
    PARENT = "parent"
    HEALTHCARE_PROXY = "healthcare_proxy"
    POWER_OF_ATTORNEY = "power_of_attorney"
    COURT_APPOINTED = "court_appointed"
    OTHER = "other"


class ConsentAuditAction(str, enum.Enum):
    """Actions recorded in the consent audit trail."""
    GRANTED = "granted"
    VIEWED = "viewed"
    DATA_ACCESSED = "data_accessed"
    SHARED = "shared"
    REVOKED = "revoked"
    EXPIRED = "expired"
    AMENDED = "amended"


# ---------------------------------------------------------------------------
# Fragment / Ingestion
# ---------------------------------------------------------------------------

class FragmentSourceType(str, enum.Enum):
    """Origin system type for raw data fragments."""
    CENSUS = "census"
    FHIR = "fhir"
    HMIS = "hmis"
    EHR = "ehr"
    WEARABLE = "wearable"
    CGM = "cgm"             # Continuous glucose monitor
    ENVIRONMENTAL = "environmental"
    CLAIMS = "claims"
    CRIMINAL_JUSTICE = "criminal_justice"
    BENEFITS = "benefits"
    PHARMACY = "pharmacy"
    MANUAL = "manual"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Observation / FHIR
# ---------------------------------------------------------------------------

class ObservationCategory(str, enum.Enum):
    """FHIR observation categories — http://terminology.hl7.org/CodeSystem/observation-category"""
    VITAL_SIGNS = "vital-signs"
    LABORATORY = "laboratory"
    SOCIAL_HISTORY = "social-history"
    SURVEY = "survey"
    ACTIVITY = "activity"
    SDOH = "sdoh"            # Social determinants of health (Gravity Project)
    IMAGING = "imaging"
    PROCEDURE = "procedure"


class ObservationStatus(str, enum.Enum):
    """FHIR Observation.status value set."""
    REGISTERED = "registered"
    PRELIMINARY = "preliminary"
    FINAL = "final"
    AMENDED = "amended"
    CORRECTED = "corrected"
    CANCELLED = "cancelled"
    ENTERED_IN_ERROR = "entered-in-error"
    UNKNOWN = "unknown"


class CodeSystem(str, enum.Enum):
    """Standard medical coding systems."""
    LOINC = "http://loinc.org"
    SNOMED_CT = "http://snomed.info/sct"
    ICD_10_CM = "http://hl7.org/fhir/sid/icd-10-cm"
    ICD_10_PCS = "http://www.cms.gov/Medicare/Coding/ICD10"
    CPT = "http://www.ama-assn.org/go/cpt"
    RXNORM = "http://www.nlm.nih.gov/research/umls/rxnorm"
    HCPCS = "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets"
    CVX = "http://hl7.org/fhir/sid/cvx"
    NDC = "http://hl7.org/fhir/sid/ndc"
    CUSTOM = "custom"


# ---------------------------------------------------------------------------
# Encounter
# ---------------------------------------------------------------------------

class EncounterClass(str, enum.Enum):
    """FHIR v3-ActCode ActEncounterCode values — encounter setting."""
    AMBULATORY = "AMB"         # Outpatient / clinic
    INPATIENT = "IMP"          # Inpatient admission
    EMERGENCY = "EMER"         # Emergency department
    HOME_HEALTH = "HH"         # Home health
    VIRTUAL = "VR"             # Telehealth / phone
    OBSERVATION = "OBSENC"     # Observation (not yet admitted)
    SHORT_STAY = "SS"          # Short stay / 23-hour
    FIELD = "FLD"              # Mobile outreach / street
    SHELTER = "SHELTER"        # Custom: shelter stay
    PRISON = "PRISON"          # Custom: incarceration
    CRISIS_LINE = "CRISIS"     # Custom: 988/crisis line


class EncounterStatus(str, enum.Enum):
    """FHIR Encounter.status values."""
    PLANNED = "planned"
    IN_PROGRESS = "in-progress"
    ON_HOLD = "on-hold"
    DISCHARGED = "discharged"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ENTERED_IN_ERROR = "entered-in-error"


class EncounterType(str, enum.Enum):
    """DOMES-specific encounter type taxonomy."""
    ER_VISIT = "er_visit"
    PSYCHIATRIC_HOSPITALIZATION = "psychiatric_hospitalization"
    MEDICAL_HOSPITALIZATION = "medical_hospitalization"
    OUTPATIENT_CLINIC = "outpatient_clinic"
    BEHAVIORAL_HEALTH_CLINIC = "behavioral_health_clinic"
    ACT_TEAM_CONTACT = "act_team_contact"
    MOBILE_CRISIS_RESPONSE = "mobile_crisis_response"
    SHELTER_STAY = "shelter_stay"
    JAIL_BOOKING = "jail_booking"
    COURT_APPEARANCE = "court_appearance"
    PROBATION_CHECK_IN = "probation_check_in"
    HOME_VISIT = "home_visit"
    TELEHEALTH = "telehealth"
    CRISIS_LINE_CALL = "crisis_line_call"
    CASE_MANAGEMENT = "case_management"
    STREET_OUTREACH = "street_outreach"
    PHARMACY_VISIT = "pharmacy_visit"


# ---------------------------------------------------------------------------
# Condition
# ---------------------------------------------------------------------------

class ConditionClinicalStatus(str, enum.Enum):
    """FHIR condition-clinical value set."""
    ACTIVE = "active"
    RECURRENCE = "recurrence"
    RELAPSE = "relapse"
    INACTIVE = "inactive"
    REMISSION = "remission"
    RESOLVED = "resolved"


class ConditionVerificationStatus(str, enum.Enum):
    """FHIR condition-ver-status value set."""
    UNCONFIRMED = "unconfirmed"
    PROVISIONAL = "provisional"
    DIFFERENTIAL = "differential"
    CONFIRMED = "confirmed"
    REFUTED = "refuted"
    ENTERED_IN_ERROR = "entered-in-error"


class ConditionCategory(str, enum.Enum):
    """FHIR condition-category + SDOH extensions."""
    PROBLEM_LIST_ITEM = "problem-list-item"
    ENCOUNTER_DIAGNOSIS = "encounter-diagnosis"
    HEALTH_CONCERN = "health-concern"
    SDOH_CONDITION = "sdoh-condition"        # Gravity Project SDOH
    DISABILITY = "disability"


class ConditionSeverity(str, enum.Enum):
    """Condition severity."""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Medication
# ---------------------------------------------------------------------------

class MedicationStatus(str, enum.Enum):
    """FHIR MedicationRequest.status values."""
    ACTIVE = "active"
    ON_HOLD = "on-hold"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    ENTERED_IN_ERROR = "entered-in-error"
    STOPPED = "stopped"
    DRAFT = "draft"
    UNKNOWN = "unknown"


class MedicationCategory(str, enum.Enum):
    """High-level medication category for DOMES analysis."""
    ANTIPSYCHOTIC = "antipsychotic"
    MOOD_STABILIZER = "mood_stabilizer"
    ANTIDEPRESSANT = "antidepressant"
    ANXIOLYTIC = "anxiolytic"
    MAT = "medication_assisted_treatment"  # Methadone, buprenorphine, naltrexone
    ANTIDIABETIC = "antidiabetic"
    CARDIOVASCULAR = "cardiovascular"
    PAIN_MANAGEMENT = "pain_management"
    ANTICONVULSANT = "anticonvulsant"
    OTHER = "other"


class AdherenceStatus(str, enum.Enum):
    """Medication adherence classification."""
    ADHERENT = "adherent"           # Taking as prescribed
    PARTIALLY_ADHERENT = "partially_adherent"
    NON_ADHERENT = "non_adherent"
    UNABLE_TO_ASSESS = "unable_to_assess"


# ---------------------------------------------------------------------------
# Assessment
# ---------------------------------------------------------------------------

class AssessmentType(str, enum.Enum):
    """Standardized assessment tool types."""
    PHQ_9 = "phq_9"               # Depression — 9 items, 0-27
    PHQ_2 = "phq_2"               # Depression screen — 2 items
    GAD_7 = "gad_7"               # Anxiety — 7 items, 0-21
    AUDIT_C = "audit_c"           # Alcohol use — 3 items, 0-12
    AUDIT = "audit"               # Alcohol use — 10 items, 0-40
    DAST_10 = "dast_10"           # Drug abuse — 10 items, 0-10
    CSSRS = "c_ssrs"              # Columbia suicide severity rating scale
    VI_SPDAT = "vi_spdat"         # Housing vulnerability index
    SPDAT = "spdat"               # Full service prioritization assessment
    LOCUS = "locus"               # Level of care utilization
    ASAM = "asam"                 # Addiction severity / level of care
    BASIS_32 = "basis_32"         # Behavior and symptom
    GAF = "gaf"                   # Global assessment of functioning
    PANSS = "panss"               # Positive and negative syndrome scale
    BPRS = "bprs"                 # Brief psychiatric rating scale
    LACE = "lace"                 # 30-day readmission risk
    HMIS_COMPREHENSIVE = "hmis_comprehensive"
    CUSTOM = "custom"


class AssessmentStatus(str, enum.Enum):
    """Assessment completion status."""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REFUSED = "refused"
    UNABLE_TO_COMPLETE = "unable_to_complete"


# ---------------------------------------------------------------------------
# Enrollment
# ---------------------------------------------------------------------------

class ProgramType(str, enum.Enum):
    """Government program / enrollment types — covers all 30 DOMES systems."""
    MEDICAID = "medicaid"
    MEDICARE = "medicare"
    CHIP = "chip"
    VA_HEALTH = "va_health"
    # Behavioral health
    ACT_TEAM = "act_team"
    CMHC = "cmhc"                  # Community mental health center
    SUD_TREATMENT = "sud_treatment"
    MAT_PROGRAM = "mat_program"
    # Housing
    SECTION_8_HCV = "section_8_hcv"
    PUBLIC_HOUSING = "public_housing"
    EMERGENCY_SHELTER = "emergency_shelter"
    TRANSITIONAL_HOUSING = "transitional_housing"
    PERMANENT_SUPPORTIVE_HOUSING = "permanent_supportive_housing"
    RAPID_REHOUSING = "rapid_rehousing"
    # Income
    SSI = "ssi"
    SSDI = "ssdi"
    SNAP = "snap"
    TANF = "tanf"
    WIC = "wic"
    UNEMPLOYMENT_INSURANCE = "unemployment_insurance"
    GENERAL_ASSISTANCE = "general_assistance"
    EITC = "eitc"
    # Justice
    PROBATION = "probation"
    PAROLE = "parole"
    DRUG_COURT = "drug_court"
    # Child welfare
    FOSTER_CARE = "foster_care"
    EARLY_INTERVENTION = "early_intervention"
    IEP = "iep"
    # Veterans
    VA_DISABILITY = "va_disability"
    HUDVASH = "hudvash"
    SSVF = "ssvf"
    # Other
    LIHEAP = "liheap"
    HEAD_START = "head_start"
    PACE = "pace"
    LTSS = "ltss"
    CUSTOM = "custom"


class EnrollmentStatus(str, enum.Enum):
    """Program enrollment status."""
    ACTIVE = "active"
    PENDING = "pending"
    WAITLISTED = "waitlisted"
    DISENROLLED = "disenrolled"
    SUSPENDED = "suspended"
    COMPLETED = "completed"
    DENIED = "denied"


class ExitDestination(str, enum.Enum):
    """HMIS-aligned exit destination codes (list 3.12)."""
    PERMANENT_HOUSING = "permanent_housing"
    RENTAL_NO_SUBSIDY = "rental_no_subsidy"
    RENTAL_WITH_SUBSIDY = "rental_with_subsidy"
    OWNED = "owned"
    STAYING_WITH_FAMILY = "staying_with_family"
    STAYING_WITH_FRIENDS = "staying_with_friends"
    TRANSITIONAL_HOUSING = "transitional_housing"
    EMERGENCY_SHELTER = "emergency_shelter"
    PLACE_NOT_FOR_HABITATION = "place_not_for_habitation"
    HOSPITAL_NON_PSYCH = "hospital_non_psych"
    PSYCHIATRIC_FACILITY = "psychiatric_facility"
    SUBSTANCE_USE_FACILITY = "substance_use_facility"
    JAIL_PRISON = "jail_prison"
    LONG_TERM_CARE = "long_term_care"
    FOSTER_CARE = "foster_care"
    DECEASED = "deceased"
    OTHER = "other"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Biometric / Wearable
# ---------------------------------------------------------------------------

class BiometricMetric(str, enum.Enum):
    """Biometric measurement types — TimescaleDB hypertable metric column."""
    HEART_RATE = "heart_rate"                   # BPM
    HRV_RMSSD = "hrv_rmssd"                     # Heart rate variability (RMSSD, ms)
    HRV_SDNN = "hrv_sdnn"                       # HRV (SDNN, ms) — Apple Watch metric
    BLOOD_GLUCOSE = "blood_glucose"             # mg/dL
    SPO2 = "spo2"                               # Oxygen saturation (%)
    RESPIRATORY_RATE = "respiratory_rate"       # Breaths/min
    BLOOD_PRESSURE_SYSTOLIC = "bp_systolic"     # mmHg
    BLOOD_PRESSURE_DIASTOLIC = "bp_diastolic"   # mmHg
    TEMPERATURE_BODY = "temperature_body"       # °F
    TEMPERATURE_WRIST = "temperature_wrist"     # °C (wearable-derived)
    STEPS = "steps"                             # Count (cumulative per interval)
    ACTIVE_ENERGY = "active_energy"             # kcal
    SLEEP_STAGE = "sleep_stage"                 # Encoded (see SleepStage enum)
    WEIGHT = "weight"                           # kg
    BMI = "bmi"
    VO2_MAX = "vo2_max"                         # mL/kg/min
    RESTING_HEART_RATE = "resting_heart_rate"   # BPM (daily)
    WALKING_SPEED = "walking_speed"             # m/s
    ELECTRODERMAL_ACTIVITY = "electrodermal_activity"  # µS (stress proxy)
    SKIN_TEMPERATURE = "skin_temperature"       # °C (Whoop/Oura)
    READINESS_SCORE = "readiness_score"         # 0-100 (Oura/Whoop)
    BLOOD_ALCOHOL = "blood_alcohol"             # % (0.0-1.0)


class SleepStage(str, enum.Enum):
    """Sleep stage values — stored as string in biometric metadata."""
    IN_BED = "in_bed"
    AWAKE = "awake"
    LIGHT = "light"        # NREM 1-2 / Apple Watch "core"
    DEEP = "deep"          # NREM 3 / slow-wave
    REM = "rem"
    UNSPECIFIED = "unspecified"


class BiometricDevice(str, enum.Enum):
    """Source wearable device."""
    APPLE_WATCH = "apple_watch"
    OURA_RING = "oura_ring"
    WHOOP = "whoop"
    FITBIT = "fitbit"
    GARMIN = "garmin"
    WITHINGS = "withings"
    SAMSUNG = "samsung"
    DEXCOM_CGM = "dexcom_cgm"      # Continuous glucose monitor
    LIBRE_CGM = "libre_cgm"
    EVERSENSE_CGM = "eversense_cgm"
    OMRON = "omron"                # Blood pressure cuff
    MANUAL = "manual"
    EHR = "ehr"
    UNKNOWN = "unknown"


class CGMTrend(str, enum.Enum):
    """Dexcom CGM trend arrow values."""
    DOUBLE_UP = "double_up"           # >+3 mg/dL/min
    SINGLE_UP = "single_up"           # +2 to +3 mg/dL/min
    FORTY_FIVE_UP = "forty_five_up"   # +1 to +2 mg/dL/min
    FLAT = "flat"                     # -1 to +1 mg/dL/min
    FORTY_FIVE_DOWN = "forty_five_down"
    SINGLE_DOWN = "single_down"
    DOUBLE_DOWN = "double_down"       # <-3 mg/dL/min
    NOT_COMPUTABLE = "not_computable"
    RATE_OUT_OF_RANGE = "rate_out_of_range"


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

class EnvironmentMetric(str, enum.Enum):
    """Environmental monitoring metric types."""
    PM2_5 = "pm2_5"                    # Fine particulate matter (µg/m³)
    PM10 = "pm10"                       # Coarse particulate matter (µg/m³)
    PM1 = "pm1"                         # Ultrafine particles (µg/m³)
    AQI = "aqi"                         # Air Quality Index (EPA composite)
    TEMPERATURE_AMBIENT = "temp_ambient"  # °F
    HUMIDITY = "humidity"               # %
    UV_INDEX = "uv_index"              # 0-11+
    NOISE_LEVEL = "noise_level"        # dB(A)
    LIGHT_LEVEL = "light_level"        # Lux
    HEAT_INDEX = "heat_index"          # °F (apparent temperature)
    WIND_SPEED = "wind_speed"           # mph
    PRECIPITATION = "precipitation"    # mm/hr
    PRESSURE = "pressure"              # hPa
    DEW_POINT = "dew_point"            # °F


class EnvironmentSource(str, enum.Enum):
    """Environmental data source."""
    PURPLE_AIR = "purpleair"
    EPA_AQS = "epa_aqs"
    OPEN_WEATHER_MAP = "openweathermap"
    TOMORROW_IO = "tomorrow_io"
    NOAA = "noaa"
    SENSOR_DIRECT = "sensor_direct"    # On-device / local sensor
    MANUAL = "manual"


# ---------------------------------------------------------------------------
# Dome / Digital Twin
# ---------------------------------------------------------------------------

class DomeTrigger(str, enum.Enum):
    """What triggered a new dome assembly."""
    SCHEDULED = "scheduled"             # Regular scheduled assembly
    NEW_DATA = "new_data"               # New fragment arrived
    CONSENT_CHANGE = "consent_change"
    MANUAL = "manual"                   # User-requested
    CRISIS_EVENT = "crisis_event"       # Emergency trigger
    ENROLLMENT_CHANGE = "enrollment_change"
    CONDITION_CHANGE = "condition_change"


class RiskLevel(str, enum.Enum):
    """Risk severity levels for computed risk scores."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Flourishing
# ---------------------------------------------------------------------------

class FlourishingDomain(str, enum.Enum):
    """12 flourishing domains — from BATHS/DOMES flourishing architecture.

    Organized in 3 layers:
    - Foundation (L1): health_vitality, economic_prosperity, community_belonging,
      environmental_harmony
    - Aspiration (L2): creative_expression, intellectual_growth, physical_space_beauty,
      play_joy
    - Transcendence (L3): spiritual_depth, love_relationships, purpose_meaning,
      legacy_contribution
    """
    # Layer 1 — Foundation
    HEALTH_VITALITY = "health_vitality"
    ECONOMIC_PROSPERITY = "economic_prosperity"
    COMMUNITY_BELONGING = "community_belonging"
    ENVIRONMENTAL_HARMONY = "environmental_harmony"
    # Layer 2 — Aspiration
    CREATIVE_EXPRESSION = "creative_expression"
    INTELLECTUAL_GROWTH = "intellectual_growth"
    PHYSICAL_SPACE_BEAUTY = "physical_space_beauty"
    PLAY_JOY = "play_joy"
    # Layer 3 — Transcendence
    SPIRITUAL_DEPTH = "spiritual_depth"
    LOVE_RELATIONSHIPS = "love_relationships"
    PURPOSE_MEANING = "purpose_meaning"
    LEGACY_CONTRIBUTION = "legacy_contribution"


class PhilosophicalTradition(str, enum.Enum):
    """8 philosophical traditions for computing tradition-weighted flourishing scores.

    Each tradition assigns different weights to the 12 flourishing domains,
    reflecting its core conception of what it means for a human being to thrive.
    Traditions are not mutually exclusive — they offer complementary lenses
    on the same person's condition.
    """
    ARISTOTELIAN = "aristotelian"       # Eudaimonia — virtue, character, practical wisdom
    UTILITARIAN = "utilitarian"         # Greatest good — QALYs, welfare economics, pain calculus
    CAPABILITIES = "capabilities"       # Sen/Nussbaum — what can this person DO and BE?
    RAWLSIAN = "rawlsian"               # Justice as fairness — how does the least advantaged fare?
    UBUNTU = "ubuntu"                   # I am because we are — communal flourishing, relational identity
    BUDDHIST = "buddhist"               # Reduction of suffering — attachment, impermanence, compassion
    EXISTENTIALIST = "existentialist"   # Authentic existence — freedom, responsibility, meaning-creation
    INDIGENOUS = "indigenous"           # Connection to land/community — holistic wellness, seven generations


# ---------------------------------------------------------------------------
# Government Systems
# ---------------------------------------------------------------------------

class SystemDomain(str, enum.Enum):
    """Domain / sector of a government data system."""
    HEALTH = "health"
    BEHAVIORAL_HEALTH = "behavioral_health"
    HOUSING = "housing"
    INCOME = "income"
    JUSTICE = "justice"
    CHILD_WELFARE = "child_welfare"
    EDUCATION = "education"
    VETERANS = "veterans"
    IMMIGRATION = "immigration"
    OTHER = "other"


class SystemPrivacyLaw(str, enum.Enum):
    """Privacy laws that govern a system's data."""
    HIPAA = "HIPAA"
    CFR_42_PART_2 = "42_CFR_Part_2"    # SUD — strictest
    FERPA = "FERPA"
    CAPTA = "CAPTA"                     # Child abuse/neglect
    CJIS = "CJIS"                       # Criminal justice
    PRIVACY_ACT = "Privacy_Act"
    HITECH = "HITECH"
    HMIS_PRIVACY = "HMIS_Privacy"
    STATE_LAW = "State_Law"
    VA_5705 = "38_USC_5705"             # VA mental health records


class SystemAPIAvailability(str, enum.Enum):
    """API availability / interoperability level for a government system."""
    PUBLIC = "public"                   # Open API, no key required
    LIMITED = "limited"                 # API exists but restricted access
    PARTNER_ONLY = "partner_only"       # Requires formal data sharing agreement
    NONE = "none"                       # No API — batch/manual only


# ---------------------------------------------------------------------------
# Gap / Bridge
# ---------------------------------------------------------------------------

class GapType(str, enum.Enum):
    """Type of barrier causing a data gap between systems."""
    LEGAL = "legal"                     # Statutory prohibition (42 CFR Part 2, etc.)
    TECHNICAL = "technical"             # No API, incompatible formats
    POLITICAL = "political"             # Jurisdictional resistance
    STRUCTURAL = "structural"           # Policy design (e.g., Medicaid inmate exclusion)
    RESOURCE = "resource"               # Budget / staffing constraints


class GapSeverity(str, enum.Enum):
    """Impact severity of a data gap."""
    CRITICAL = "critical"              # Active patient harm; life safety implications
    HIGH = "high"                       # Significant service disruption
    MODERATE = "moderate"
    LOW = "low"


# ---------------------------------------------------------------------------
# Provision / Legal
# ---------------------------------------------------------------------------

class ProvisionType(str, enum.Enum):
    """Type of legal provision."""
    RIGHT = "right"
    PROTECTION = "protection"
    OBLIGATION = "obligation"
    ENFORCEMENT = "enforcement"


class ProvisionDomain(str, enum.Enum):
    """Legal domain of a provision — mirrors DOMES legal matching engine."""
    HEALTH = "health"
    CIVIL_RIGHTS = "civil_rights"
    HOUSING = "housing"
    INCOME = "income"
    EDUCATION = "education"
    JUSTICE = "justice"
    SUBSTANCE_USE = "substance_use"
    VETERANS = "veterans"
    IMMIGRATION = "immigration"
