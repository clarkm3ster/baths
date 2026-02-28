"""
DOMES v2 — Initial Schema Migration

Revision: 001
Created: 2026-02-27
Author: DOMES v2 Build System

Creates all core tables in dependency order:
    1. Enums (PostgreSQL native ENUM types)
    2. government_system (reference table, no FKs)
    3. person (primary entity)
    4. consent + consent_audit_entry
    5. fragment
    6. data_gap + provision
    7. observation + encounter + condition + medication + assessment + enrollment
    8. biometric_reading + environment_reading
    9. dome + flourishing_score

TimescaleDB note:
    After running this migration, call setup_timescaledb() from domes.database
    to convert biometric_reading and environment_reading to hypertables.
    This cannot be done inside a standard migration because create_hypertable()
    requires the table to be empty at call time.

Downgrade note:
    The downgrade() function drops ALL tables and ALL custom enum types.
    This is a complete schema teardown — use with care.
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# Revision identifiers — used by Alembic
revision: str = "001_initial_schema"
down_revision: str | None = None  # This is the first migration
branch_labels: str | None = None
depends_on: str | None = None


# ---------------------------------------------------------------------------
# Enum type definitions
# ---------------------------------------------------------------------------

# We pre-define all PostgreSQL ENUM types to avoid SQLAlchemy creating them
# piecemeal. All enums use CREATE TYPE IF NOT EXISTS.

ENUM_DEFS: list[tuple[str, list[str]]] = [
    ("housing_status_enum", ["housed", "sheltered", "unsheltered", "institutional", "doubled_up", "unknown"]),
    ("employment_status_enum", ["employed_full_time", "employed_part_time", "unemployed", "unable_to_work", "not_in_labor_force", "unknown"]),
    ("gender_enum", ["woman", "man", "non_binary", "transgender_woman", "transgender_man", "culturally_specific", "different_identity", "questioning", "unknown"]),
    ("immigration_status_enum", ["us_citizen", "lawful_permanent_resident", "refugee", "asylum_seeker", "daca", "undocumented", "visa_holder", "unknown"]),
    ("race_enum", ["american_indian_alaska_native", "asian", "black_african_american", "hispanic_latina_latinx", "middle_eastern_north_african", "native_hawaiian_pacific_islander", "white", "multiracial", "other", "unknown"]),
    ("ethnicity_enum", ["hispanic_or_latino", "not_hispanic_or_latino", "unknown"]),
    ("data_domain_enum", ["health", "behavioral_health", "substance_use", "criminal_justice", "housing", "education", "financial", "child_welfare", "biometric", "environmental", "all"]),
    ("consent_purpose_enum", ["treatment", "payment", "healthcare_operations", "care_coordination", "research", "public_health", "emergency", "legal"]),
    ("grantor_relationship_enum", ["self", "guardian", "parent", "healthcare_proxy", "power_of_attorney", "court_appointed", "other"]),
    ("consent_audit_action_enum", ["granted", "viewed", "data_accessed", "shared", "revoked", "expired", "amended"]),
    ("fragment_source_type_enum", ["census", "fhir", "hmis", "ehr", "wearable", "cgm", "environmental", "claims", "criminal_justice", "benefits", "pharmacy", "manual", "unknown"]),
    ("observation_category_enum", ["vital-signs", "laboratory", "social-history", "survey", "activity", "sdoh", "imaging", "procedure"]),
    ("observation_status_enum", ["registered", "preliminary", "final", "amended", "corrected", "cancelled", "entered-in-error", "unknown"]),
    ("code_system_enum", ["http://loinc.org", "http://snomed.info/sct", "http://hl7.org/fhir/sid/icd-10-cm", "http://www.cms.gov/Medicare/Coding/ICD10", "http://www.ama-assn.org/go/cpt", "http://www.nlm.nih.gov/research/umls/rxnorm", "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets", "http://hl7.org/fhir/sid/cvx", "http://hl7.org/fhir/sid/ndc", "custom"]),
    ("encounter_class_enum", ["AMB", "IMP", "EMER", "HH", "VR", "OBSENC", "SS", "FLD", "SHELTER", "PRISON", "CRISIS"]),
    ("encounter_status_enum", ["planned", "in-progress", "on-hold", "discharged", "completed", "cancelled", "entered-in-error"]),
    ("encounter_type_enum", ["er_visit", "psychiatric_hospitalization", "medical_hospitalization", "outpatient_clinic", "behavioral_health_clinic", "act_team_contact", "mobile_crisis_response", "shelter_stay", "jail_booking", "court_appearance", "probation_check_in", "home_visit", "telehealth", "crisis_line_call", "case_management", "street_outreach", "pharmacy_visit"]),
    ("condition_clinical_status_enum", ["active", "recurrence", "relapse", "inactive", "remission", "resolved"]),
    ("condition_verification_status_enum", ["unconfirmed", "provisional", "differential", "confirmed", "refuted", "entered-in-error"]),
    ("condition_category_enum", ["problem-list-item", "encounter-diagnosis", "health-concern", "sdoh-condition", "disability"]),
    ("condition_severity_enum", ["mild", "moderate", "severe", "critical"]),
    ("medication_status_enum", ["active", "on-hold", "cancelled", "completed", "entered-in-error", "stopped", "draft", "unknown"]),
    ("medication_category_enum", ["antipsychotic", "mood_stabilizer", "antidepressant", "anxiolytic", "medication_assisted_treatment", "antidiabetic", "cardiovascular", "pain_management", "anticonvulsant", "other"]),
    ("adherence_status_enum", ["adherent", "partially_adherent", "non_adherent", "unable_to_assess"]),
    ("assessment_type_enum", ["phq_9", "phq_2", "gad_7", "audit_c", "audit", "dast_10", "c_ssrs", "vi_spdat", "spdat", "locus", "asam", "basis_32", "gaf", "panss", "bprs", "lace", "hmis_comprehensive", "custom"]),
    ("assessment_status_enum", ["scheduled", "in_progress", "completed", "refused", "unable_to_complete"]),
    ("program_type_enum", ["medicaid", "medicare", "chip", "va_health", "act_team", "cmhc", "sud_treatment", "mat_program", "section_8_hcv", "public_housing", "emergency_shelter", "transitional_housing", "permanent_supportive_housing", "rapid_rehousing", "ssi", "ssdi", "snap", "tanf", "wic", "unemployment_insurance", "general_assistance", "eitc", "probation", "parole", "drug_court", "foster_care", "early_intervention", "iep", "va_disability", "hudvash", "ssvf", "liheap", "head_start", "pace", "ltss", "custom"]),
    ("enrollment_status_enum", ["active", "pending", "waitlisted", "disenrolled", "suspended", "completed", "denied"]),
    ("exit_destination_enum", ["permanent_housing", "rental_no_subsidy", "rental_with_subsidy", "owned", "staying_with_family", "staying_with_friends", "transitional_housing", "emergency_shelter", "place_not_for_habitation", "hospital_non_psych", "psychiatric_facility", "substance_use_facility", "jail_prison", "long_term_care", "foster_care", "deceased", "other", "unknown"]),
    ("biometric_metric_enum", ["heart_rate", "hrv_rmssd", "hrv_sdnn", "blood_glucose", "spo2", "respiratory_rate", "bp_systolic", "bp_diastolic", "temperature_body", "temperature_wrist", "steps", "active_energy", "sleep_stage", "weight", "bmi", "vo2_max", "resting_heart_rate", "walking_speed", "electrodermal_activity", "skin_temperature", "readiness_score", "blood_alcohol"]),
    ("biometric_device_enum", ["apple_watch", "oura_ring", "whoop", "fitbit", "garmin", "withings", "samsung", "dexcom_cgm", "libre_cgm", "eversense_cgm", "omron", "manual", "ehr", "unknown"]),
    ("cgm_trend_enum", ["double_up", "single_up", "forty_five_up", "flat", "forty_five_down", "single_down", "double_down", "not_computable", "rate_out_of_range"]),
    ("environment_metric_enum", ["pm2_5", "pm10", "pm1", "aqi", "temp_ambient", "humidity", "uv_index", "noise_level", "light_level", "heat_index", "wind_speed", "precipitation", "pressure", "dew_point"]),
    ("environment_source_enum", ["purpleair", "epa_aqs", "openweathermap", "tomorrow_io", "noaa", "sensor_direct", "manual"]),
    ("dome_trigger_enum", ["scheduled", "new_data", "consent_change", "manual", "crisis_event", "enrollment_change", "condition_change"]),
    ("risk_level_enum", ["low", "moderate", "high", "critical", "unknown"]),
    ("flourishing_domain_enum", ["health_vitality", "economic_prosperity", "community_belonging", "environmental_harmony", "creative_expression", "intellectual_growth", "physical_space_beauty", "play_joy", "spiritual_depth", "love_relationships", "purpose_meaning", "legacy_contribution"]),
    ("system_domain_enum", ["health", "behavioral_health", "housing", "income", "justice", "child_welfare", "education", "veterans", "immigration", "other"]),
    ("system_privacy_law_enum", ["HIPAA", "42_CFR_Part_2", "FERPA", "CAPTA", "CJIS", "Privacy_Act", "HITECH", "HMIS_Privacy", "State_Law", "38_USC_5705"]),
    ("system_api_availability_enum", ["public", "limited", "partner_only", "none"]),
    ("gap_type_enum", ["legal", "technical", "political", "structural", "resource"]),
    ("gap_severity_enum", ["critical", "high", "moderate", "low"]),
    ("provision_type_enum", ["right", "protection", "obligation", "enforcement"]),
    ("provision_domain_enum", ["health", "civil_rights", "housing", "income", "education", "justice", "substance_use", "veterans", "immigration"]),
]


def _create_enum(name: str, values: list[str]) -> None:
    """Create a PostgreSQL ENUM type if it doesn't exist."""
    values_sql = ", ".join(f"'{v}'" for v in values)
    op.execute(f"CREATE TYPE IF NOT EXISTS {name} AS ENUM ({values_sql})")


def _drop_enum(name: str) -> None:
    """Drop a PostgreSQL ENUM type if it exists."""
    op.execute(f"DROP TYPE IF EXISTS {name} CASCADE")


# ---------------------------------------------------------------------------
# Upgrade
# ---------------------------------------------------------------------------

def upgrade() -> None:
    """Create complete DOMES v2 schema."""

    # ------------------------------------------------------------------
    # 1. Create all ENUM types
    # ------------------------------------------------------------------
    for name, values in ENUM_DEFS:
        _create_enum(name, values)

    # ------------------------------------------------------------------
    # 2. government_system — reference table (no FKs)
    # ------------------------------------------------------------------
    op.create_table(
        "government_system",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("system_code", sa.String(64), nullable=False, unique=True),
        sa.Column("system_name", sa.String(255), nullable=False),
        sa.Column("agency", sa.String(255), nullable=True),
        sa.Column("domain", sa.Enum(name="system_domain_enum", create_type=False), nullable=False),
        sa.Column("api_availability", sa.Enum(name="system_api_availability_enum", create_type=False), nullable=False),
        sa.Column("privacy_laws", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("fhir_base_url", sa.String(512), nullable=True),
        sa.Column("api_base_url", sa.String(512), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("notes", sa.Text(), nullable=True),
        # FHIR mixin
        sa.Column("fhir_resource_type", sa.String(64), nullable=True),
        sa.Column("fhir_resource_id", sa.String(255), nullable=True),
        sa.Column("fhir_system", sa.String(512), nullable=True),
        # Timestamps
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        # Audit
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        comment="Reference table of government data systems (30+ systems)",
    )
    op.create_index("idx_government_system_code", "government_system", ["system_code"], unique=True)
    op.create_index("idx_government_system_domain", "government_system", ["domain"])

    # ------------------------------------------------------------------
    # 3. person — primary entity
    # ------------------------------------------------------------------
    op.create_table(
        "person",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        # Name
        sa.Column("first_name", sa.String(100), nullable=True),
        sa.Column("middle_name", sa.String(100), nullable=True),
        sa.Column("last_name", sa.String(100), nullable=True),
        sa.Column("preferred_name", sa.String(100), nullable=True),
        sa.Column("name_suffix", sa.String(20), nullable=True),
        # Demographics
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("gender", sa.Enum(name="gender_enum", create_type=False), nullable=True),
        sa.Column("race", sa.Enum(name="race_enum", create_type=False), nullable=True),
        sa.Column("ethnicity", sa.Enum(name="ethnicity_enum", create_type=False), nullable=True),
        sa.Column("primary_language", sa.String(32), nullable=True),
        sa.Column("secondary_languages", postgresql.ARRAY(sa.String()), nullable=True),
        # Identity
        sa.Column("ssn_hash", sa.String(64), nullable=True, unique=True),
        # Location
        sa.Column("address_line1", sa.String(255), nullable=True),
        sa.Column("address_line2", sa.String(255), nullable=True),
        sa.Column("city", sa.String(100), nullable=True),
        sa.Column("state", sa.String(2), nullable=True),
        sa.Column("county", sa.String(100), nullable=True),
        sa.Column("zip_code", sa.String(10), nullable=True),
        sa.Column("census_tract", sa.String(16), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        # Situational
        sa.Column("housing_status", sa.Enum(name="housing_status_enum", create_type=False), nullable=True),
        sa.Column("housing_status_since", sa.Date(), nullable=True),
        sa.Column("employment_status", sa.Enum(name="employment_status_enum", create_type=False), nullable=True),
        sa.Column("immigration_status", sa.Enum(name="immigration_status_enum", create_type=False), nullable=True),
        sa.Column("veteran", sa.Boolean(), nullable=True),
        sa.Column("chronic_homelessness", sa.Boolean(), nullable=True),
        sa.Column("years_homeless", sa.Numeric(5, 2), nullable=True),
        sa.Column("immigration_status", sa.Enum(name="immigration_status_enum", create_type=False), nullable=True),
        # Government IDs
        sa.Column("medicaid_id", sa.String(50), nullable=True),
        sa.Column("medicare_id", sa.String(50), nullable=True),
        sa.Column("snap_case_number", sa.String(50), nullable=True),
        sa.Column("va_patient_id", sa.String(50), nullable=True),
        sa.Column("hmis_client_id", sa.String(50), nullable=True),
        sa.Column("probation_case_number", sa.String(50), nullable=True),
        sa.Column("child_welfare_case_number", sa.String(50), nullable=True),
        sa.Column("dob_approximate", sa.Boolean(), nullable=True, server_default="false"),
        # FHIR
        sa.Column("fhir_resource_type", sa.String(64), nullable=True),
        sa.Column("fhir_resource_id", sa.String(255), nullable=True),
        sa.Column("fhir_system", sa.String(512), nullable=True),
        # Timestamps
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_reason", sa.String(500), nullable=True),
        # Audit
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        comment="Core person entity — primary key of the DOMES universe",
    )
    op.create_index("idx_person_last_first", "person", ["last_name", "first_name"])
    op.create_index("idx_person_dob", "person", ["date_of_birth"])
    op.create_index("idx_person_housing_status", "person", ["housing_status"])
    op.create_index("idx_person_hmis", "person", ["hmis_client_id"])
    op.create_index("idx_person_medicaid", "person", ["medicaid_id"])
    op.create_index("idx_person_ssn_hash", "person", ["ssn_hash"], unique=True, postgresql_where="ssn_hash IS NOT NULL")

    # ------------------------------------------------------------------
    # 4. consent + consent_audit_entry
    # ------------------------------------------------------------------
    op.create_table(
        "consent",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("person.id", ondelete="CASCADE"), nullable=False),
        sa.Column("granting_person_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("grantor_relationship", sa.Enum(name="grantor_relationship_enum", create_type=False), nullable=True),
        sa.Column("receiving_organization_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("government_system.id", ondelete="SET NULL"), nullable=True),
        sa.Column("purpose", sa.Enum(name="consent_purpose_enum", create_type=False), nullable=True),
        sa.Column("data_categories", postgresql.ARRAY(sa.String()), nullable=True),
        # 42 CFR Part 2 elements
        sa.Column("is_42cfr_protected", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("cfr42_compliant", sa.Boolean(), nullable=True),
        sa.Column("cfr42_disclosing_program", sa.String(255), nullable=True),
        sa.Column("cfr42_information_description", sa.String(1000), nullable=True),
        sa.Column("cfr42_right_to_revoke_stated", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("cfr42_signed", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("cfr42_signature_method", sa.String(64), nullable=True),
        sa.Column("cfr42_date_signed", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cfr42_expiration_event", sa.String(255), nullable=True),
        # Status
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revocation_reason", sa.String(500), nullable=True),
        sa.Column("witness_name", sa.String(255), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        # FHIR
        sa.Column("fhir_resource_type", sa.String(64), nullable=True),
        sa.Column("fhir_resource_id", sa.String(255), nullable=True),
        sa.Column("fhir_system", sa.String(512), nullable=True),
        # Timestamps
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        comment="42 CFR Part 2 compliant consent records",
    )
    op.create_index("idx_consent_person_active", "consent", ["person_id", "is_active"])
    op.create_index("idx_consent_42cfr", "consent", ["person_id"], postgresql_where="is_42cfr_protected = true")

    op.create_table(
        "consent_audit_entry",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("consent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("consent.id", ondelete="CASCADE"), nullable=False),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("person.id", ondelete="CASCADE"), nullable=False),
        sa.Column("action", sa.Enum(name="consent_audit_action_enum", create_type=False), nullable=False),
        sa.Column("actor_id", sa.String(255), nullable=True),
        sa.Column("actor_name", sa.String(255), nullable=True),
        sa.Column("actor_role", sa.String(128), nullable=True),
        sa.Column("actor_organization", sa.String(255), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("data_category_accessed", sa.Enum(name="data_domain_enum", create_type=False), nullable=True),
        sa.Column("action_timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        comment="Immutable append-only consent audit log",
    )
    op.create_index("idx_consent_audit_consent", "consent_audit_entry", ["consent_id"])
    op.create_index("idx_consent_audit_person_time", "consent_audit_entry", ["person_id", "action_timestamp"])

    # ------------------------------------------------------------------
    # 5. fragment
    # ------------------------------------------------------------------
    op.create_table(
        "fragment",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("person.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_system_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("government_system.id", ondelete="SET NULL"), nullable=True),
        sa.Column("source_type", sa.Enum(name="fragment_source_type_enum", create_type=False), nullable=False),
        sa.Column("data_domain", sa.Enum(name="data_domain_enum", create_type=False), nullable=False),
        sa.Column("external_id", sa.String(255), nullable=True),
        sa.Column("external_version", sa.String(64), nullable=True),
        # Lifecycle
        sa.Column("ingested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("validated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("normalized_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("assembled_at", sa.DateTime(timezone=True), nullable=True),
        # Status
        sa.Column("validation_status", sa.String(32), nullable=True),
        sa.Column("validation_errors", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("normalization_status", sa.String(32), nullable=True),
        sa.Column("is_superseded", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("superseded_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        # Content
        sa.Column("source_format", sa.String(64), nullable=True),
        sa.Column("is_42cfr_protected", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_pii", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("consent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("consent.id", ondelete="SET NULL"), nullable=True),
        sa.Column("raw_payload", postgresql.JSONB(), nullable=False),
        sa.Column("normalized_payload", postgresql.JSONB(), nullable=True),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        # Timestamps + Audit
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        comment="Raw ingest boundary — immutable fragments from source systems",
    )
    op.create_index("idx_fragment_person_domain", "fragment", ["person_id", "data_domain"])
    op.create_index("idx_fragment_person_ingested", "fragment", ["person_id", "ingested_at"])
    op.create_index("idx_fragment_external_id", "fragment", ["external_id"], postgresql_where="external_id IS NOT NULL")
    op.create_index("idx_fragment_active", "fragment", ["person_id"], postgresql_where="is_superseded = false")

    # ------------------------------------------------------------------
    # 6. data_gap + provision
    # ------------------------------------------------------------------
    op.create_table(
        "data_gap",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("person.id", ondelete="CASCADE"), nullable=True),
        sa.Column("system_a_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("government_system.id", ondelete="CASCADE"), nullable=False),
        sa.Column("system_b_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("government_system.id", ondelete="CASCADE"), nullable=True),
        sa.Column("gap_type", sa.Enum(name="gap_type_enum", create_type=False), nullable=False),
        sa.Column("severity", sa.Enum(name="gap_severity_enum", create_type=False), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("affected_data_domains", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("is_resolved", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("resolution_notes", sa.Text(), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        comment="Data gaps between government systems",
    )
    op.create_index("idx_data_gap_person", "data_gap", ["person_id"])
    op.create_index("idx_data_gap_severity", "data_gap", ["severity"])

    op.create_table(
        "provision",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("gap_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("data_gap.id", ondelete="CASCADE"), nullable=True),
        sa.Column("provision_type", sa.Enum(name="provision_type_enum", create_type=False), nullable=False),
        sa.Column("domain", sa.Enum(name="provision_domain_enum", create_type=False), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("citation", sa.String(255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("applies_when", postgresql.JSONB(), nullable=True),
        sa.Column("enforcement_mechanisms", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("cross_references", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        comment="Legal provisions and rights — matched to data gaps",
    )
    op.create_index("idx_provision_gap", "provision", ["gap_id"])
    op.create_index("idx_provision_domain", "provision", ["domain"])

    # ------------------------------------------------------------------
    # 7. observation
    # ------------------------------------------------------------------
    op.create_table(
        "observation",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("person.id", ondelete="CASCADE"), nullable=False),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), nullable=True),  # FK added after encounter table
        sa.Column("status", sa.Enum(name="observation_status_enum", create_type=False), nullable=False),
        sa.Column("category", sa.Enum(name="observation_category_enum", create_type=False), nullable=True),
        sa.Column("code", sa.String(64), nullable=True),
        sa.Column("code_system", sa.Enum(name="code_system_enum", create_type=False), nullable=True),
        sa.Column("code_display", sa.String(255), nullable=True),
        sa.Column("effective_datetime", sa.DateTime(timezone=True), nullable=True),
        sa.Column("issued", sa.DateTime(timezone=True), nullable=True),
        sa.Column("value_quantity", sa.Numeric(12, 4), nullable=True),
        sa.Column("value_unit", sa.String(32), nullable=True),
        sa.Column("value_string", sa.String(500), nullable=True),
        sa.Column("value_boolean", sa.Boolean(), nullable=True),
        sa.Column("value_integer", sa.Integer(), nullable=True),
        sa.Column("value_codeable_concept", sa.String(64), nullable=True),
        sa.Column("reference_range_low", sa.Numeric(12, 4), nullable=True),
        sa.Column("reference_range_high", sa.Numeric(12, 4), nullable=True),
        sa.Column("interpretation", sa.String(64), nullable=True),
        sa.Column("source_system_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("government_system.id", ondelete="SET NULL"), nullable=True),
        sa.Column("source_fragment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fragment.id", ondelete="SET NULL"), nullable=True),
        sa.Column("performer_name", sa.String(255), nullable=True),
        sa.Column("performer_role", sa.String(128), nullable=True),
        sa.Column("performer_organization", sa.String(255), nullable=True),
        sa.Column("is_42cfr_protected", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_sensitive", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        comment="FHIR-aligned Observations — vitals, labs, assessments, SDOH",
    )
    op.create_index("idx_observation_person_time", "observation", ["person_id", "effective_datetime"])
    op.create_index("idx_observation_code", "observation", ["code", "code_system"])
    op.create_index("idx_observation_category", "observation", ["category"])

    # ------------------------------------------------------------------
    # 8. encounter
    # ------------------------------------------------------------------
    op.create_table(
        "encounter",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("person.id", ondelete="CASCADE"), nullable=False),
        sa.Column("class_", sa.Enum(name="encounter_class_enum", create_type=False), nullable=False),
        sa.Column("encounter_type", sa.Enum(name="encounter_type_enum", create_type=False), nullable=False),
        sa.Column("status", sa.Enum(name="encounter_status_enum", create_type=False), nullable=False),
        sa.Column("period_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("period_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("location_name", sa.String(255), nullable=True),
        sa.Column("location_city", sa.String(100), nullable=True),
        sa.Column("location_state", sa.String(2), nullable=True),
        sa.Column("location_zip", sa.String(10), nullable=True),
        sa.Column("location_type", sa.String(64), nullable=True),
        sa.Column("reason_code", sa.String(64), nullable=True),
        sa.Column("reason_code_system", sa.Enum(name="code_system_enum", create_type=False), nullable=True),
        sa.Column("reason_display", sa.String(500), nullable=True),
        sa.Column("discharge_disposition", sa.String(64), nullable=True),
        sa.Column("is_42cfr_protected", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("source_system_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("government_system.id", ondelete="SET NULL"), nullable=True),
        sa.Column("source_fragment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fragment.id", ondelete="SET NULL"), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        # FHIR
        sa.Column("fhir_resource_type", sa.String(64), nullable=True),
        sa.Column("fhir_resource_id", sa.String(255), nullable=True),
        sa.Column("fhir_system", sa.String(512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        comment="Clinical, shelter, justice, and social encounters",
    )
    op.create_index("idx_encounter_person_time", "encounter", ["person_id", "period_start"])
    op.create_index("idx_encounter_type", "encounter", ["encounter_type"])

    # Add FK from observation to encounter now that encounter table exists
    op.create_foreign_key(
        "fk_observation_encounter",
        "observation", "encounter",
        ["encounter_id"], ["id"],
        ondelete="SET NULL",
    )

    # ------------------------------------------------------------------
    # 9. condition
    # ------------------------------------------------------------------
    op.create_table(
        "condition",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("person.id", ondelete="CASCADE"), nullable=False),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("encounter.id", ondelete="SET NULL"), nullable=True),
        sa.Column("clinical_status", sa.Enum(name="condition_clinical_status_enum", create_type=False), nullable=True),
        sa.Column("verification_status", sa.Enum(name="condition_verification_status_enum", create_type=False), nullable=True),
        sa.Column("category", sa.Enum(name="condition_category_enum", create_type=False), nullable=True),
        sa.Column("severity", sa.Enum(name="condition_severity_enum", create_type=False), nullable=True),
        sa.Column("code", sa.String(64), nullable=True),
        sa.Column("code_system", sa.Enum(name="code_system_enum", create_type=False), nullable=True),
        sa.Column("code_display", sa.String(255), nullable=True),
        sa.Column("onset_datetime", sa.DateTime(timezone=True), nullable=True),
        sa.Column("onset_date", sa.Date(), nullable=True),
        sa.Column("abatement_datetime", sa.DateTime(timezone=True), nullable=True),
        sa.Column("abatement_date", sa.Date(), nullable=True),
        sa.Column("recorded_date", sa.Date(), nullable=True),
        sa.Column("is_42cfr_protected", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("source_system_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("government_system.id", ondelete="SET NULL"), nullable=True),
        sa.Column("source_fragment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fragment.id", ondelete="SET NULL"), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        # FHIR
        sa.Column("fhir_resource_type", sa.String(64), nullable=True),
        sa.Column("fhir_resource_id", sa.String(255), nullable=True),
        sa.Column("fhir_system", sa.String(512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        comment="FHIR-aligned diagnoses, problem list items, SDOH conditions",
    )
    op.create_index("idx_condition_person_clinical", "condition", ["person_id", "clinical_status"])
    op.create_index("idx_condition_code", "condition", ["code", "code_system"])

    # ------------------------------------------------------------------
    # 10. medication
    # ------------------------------------------------------------------
    op.create_table(
        "medication",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("person.id", ondelete="CASCADE"), nullable=False),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("encounter.id", ondelete="SET NULL"), nullable=True),
        sa.Column("status", sa.Enum(name="medication_status_enum", create_type=False), nullable=False),
        sa.Column("category", sa.Enum(name="medication_category_enum", create_type=False), nullable=True),
        sa.Column("medication_code", sa.String(64), nullable=True),
        sa.Column("medication_code_system", sa.Enum(name="code_system_enum", create_type=False), nullable=True),
        sa.Column("medication_display", sa.String(255), nullable=True),
        sa.Column("generic_name", sa.String(255), nullable=True),
        sa.Column("brand_name", sa.String(255), nullable=True),
        sa.Column("dosage_value", sa.Numeric(10, 3), nullable=True),
        sa.Column("dosage_unit", sa.String(32), nullable=True),
        sa.Column("dosage_form", sa.String(64), nullable=True),
        sa.Column("route", sa.String(64), nullable=True),
        sa.Column("frequency", sa.String(64), nullable=True),
        sa.Column("authored_on", sa.Date(), nullable=True),
        sa.Column("effective_date_start", sa.Date(), nullable=True),
        sa.Column("effective_date_end", sa.Date(), nullable=True),
        sa.Column("prescriber_name", sa.String(255), nullable=True),
        sa.Column("prescriber_npi", sa.String(10), nullable=True),
        sa.Column("dispense_quantity", sa.Numeric(10, 2), nullable=True),
        sa.Column("days_supply", sa.Integer(), nullable=True),
        sa.Column("refills_authorized", sa.Integer(), nullable=True),
        sa.Column("adherence_status", sa.Enum(name="adherence_status_enum", create_type=False), nullable=True),
        sa.Column("is_mat", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_42cfr_protected", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("source_system_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("government_system.id", ondelete="SET NULL"), nullable=True),
        sa.Column("source_fragment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fragment.id", ondelete="SET NULL"), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        # FHIR
        sa.Column("fhir_resource_type", sa.String(64), nullable=True),
        sa.Column("fhir_resource_id", sa.String(255), nullable=True),
        sa.Column("fhir_system", sa.String(512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        comment="Medication records — prescriptions, fills, adherence (MAT flagged)",
    )
    op.create_index("idx_medication_person_status", "medication", ["person_id", "status"])
    op.create_index("idx_medication_mat", "medication", ["person_id"], postgresql_where="is_mat = true")

    # ------------------------------------------------------------------
    # 11. assessment
    # ------------------------------------------------------------------
    op.create_table(
        "assessment",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("person.id", ondelete="CASCADE"), nullable=False),
        sa.Column("encounter_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("encounter.id", ondelete="SET NULL"), nullable=True),
        sa.Column("assessment_type", sa.Enum(name="assessment_type_enum", create_type=False), nullable=False),
        sa.Column("status", sa.Enum(name="assessment_status_enum", create_type=False), nullable=False),
        sa.Column("administered_date", sa.Date(), nullable=True),
        sa.Column("administered_by", sa.String(255), nullable=True),
        sa.Column("administering_organization", sa.String(255), nullable=True),
        sa.Column("score", sa.Numeric(6, 2), nullable=True),
        sa.Column("max_score", sa.Numeric(6, 2), nullable=True),
        sa.Column("severity_label", sa.String(64), nullable=True),
        sa.Column("score_interpretation", sa.Text(), nullable=True),
        sa.Column("subscores", postgresql.JSONB(), nullable=True),
        sa.Column("item_responses", postgresql.JSONB(), nullable=True),
        sa.Column("risk_flags", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("followup_recommended", sa.Boolean(), nullable=True),
        sa.Column("is_42cfr_protected", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("source_system_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("government_system.id", ondelete="SET NULL"), nullable=True),
        sa.Column("source_fragment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fragment.id", ondelete="SET NULL"), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        comment="Standardized assessments: PHQ-9, GAD-7, AUDIT-C, VI-SPDAT, LOCUS, ASAM",
    )
    op.create_index("idx_assessment_person_type", "assessment", ["person_id", "assessment_type"])
    op.create_index("idx_assessment_date", "assessment", ["administered_date"])

    # ------------------------------------------------------------------
    # 12. enrollment
    # ------------------------------------------------------------------
    op.create_table(
        "enrollment",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("person.id", ondelete="CASCADE"), nullable=False),
        sa.Column("program_system_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("government_system.id", ondelete="SET NULL"), nullable=True),
        sa.Column("program_type", sa.Enum(name="program_type_enum", create_type=False), nullable=False),
        sa.Column("status", sa.Enum(name="enrollment_status_enum", create_type=False), nullable=False),
        sa.Column("entry_date", sa.Date(), nullable=False),
        sa.Column("exit_date", sa.Date(), nullable=True),
        sa.Column("exit_destination", sa.Enum(name="exit_destination_enum", create_type=False), nullable=True),
        sa.Column("exit_reason", sa.String(500), nullable=True),
        sa.Column("eligibility_determination_date", sa.Date(), nullable=True),
        sa.Column("program_name", sa.String(255), nullable=True),
        sa.Column("program_subtype", sa.String(64), nullable=True),
        sa.Column("benefit_amount_monthly", sa.Numeric(10, 2), nullable=True),
        sa.Column("benefit_unit", sa.String(32), nullable=True),
        sa.Column("case_manager_name", sa.String(255), nullable=True),
        sa.Column("case_manager_id", sa.String(128), nullable=True),
        sa.Column("case_number", sa.String(128), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("source_system_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("government_system.id", ondelete="SET NULL"), nullable=True),
        sa.Column("source_fragment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fragment.id", ondelete="SET NULL"), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        comment="Program enrollments: Medicaid, SNAP, HMIS, housing, justice, etc.",
    )
    op.create_index("idx_enrollment_person_program", "enrollment", ["person_id", "program_type"])
    op.create_index("idx_enrollment_active", "enrollment", ["person_id"], postgresql_where="is_active = true")
    op.create_index("idx_enrollment_entry_date", "enrollment", ["entry_date"])

    # ------------------------------------------------------------------
    # 13. biometric_reading
    # ------------------------------------------------------------------
    op.create_table(
        "biometric_reading",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("person.id", ondelete="CASCADE"), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("metric", sa.Enum(name="biometric_metric_enum", create_type=False), nullable=False),
        sa.Column("value", sa.Numeric(12, 4), nullable=False),
        sa.Column("unit", sa.String(32), nullable=True),
        sa.Column("device", sa.Enum(name="biometric_device_enum", create_type=False), nullable=True),
        sa.Column("device_id", sa.String(128), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("is_estimated", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("cgm_trend", sa.Enum(name="cgm_trend_enum", create_type=False), nullable=True),
        sa.Column("source_fragment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fragment.id", ondelete="SET NULL"), nullable=True),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        comment="TimescaleDB hypertable — continuous wearable and device biometric data",
    )
    op.create_index("idx_biometric_person_metric_time", "biometric_reading", ["person_id", "metric", "timestamp"])
    op.create_index("idx_biometric_device_time", "biometric_reading", ["device", "timestamp"])

    # ------------------------------------------------------------------
    # 14. environment_reading
    # ------------------------------------------------------------------
    op.create_table(
        "environment_reading",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("person.id", ondelete="CASCADE"), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("metric", sa.Enum(name="environment_metric_enum", create_type=False), nullable=False),
        sa.Column("value", sa.Numeric(12, 4), nullable=False),
        sa.Column("unit", sa.String(32), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("location_description", sa.String(255), nullable=True),
        sa.Column("census_tract", sa.String(16), nullable=True),
        sa.Column("source", sa.Enum(name="environment_source_enum", create_type=False), nullable=False),
        sa.Column("sensor_id", sa.String(128), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("is_estimated", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("exceeds_who_guideline", sa.Boolean(), nullable=True),
        sa.Column("exceeds_epa_standard", sa.Boolean(), nullable=True),
        sa.Column("source_fragment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("fragment.id", ondelete="SET NULL"), nullable=True),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        comment="TimescaleDB hypertable — environmental readings linked to person-location-time.",
    )
    op.create_index("idx_env_person_metric_time", "environment_reading", ["person_id", "metric", "timestamp"])
    op.create_index("idx_env_source_time", "environment_reading", ["source", "timestamp"])

    # ------------------------------------------------------------------
    # 15. dome
    # ------------------------------------------------------------------
    op.create_table(
        "dome",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("person.id", ondelete="CASCADE"), nullable=False),
        sa.Column("assembled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_current", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("trigger", sa.Enum(name="dome_trigger_enum", create_type=False), nullable=False),
        sa.Column("assembly_version", sa.String(32), nullable=False, server_default="2.0.0"),
        sa.Column("cosm_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("cosm_label", sa.String(32), nullable=True),
        sa.Column("cosm_delta", sa.Numeric(5, 2), nullable=True),
        sa.Column("risk_scores", postgresql.JSONB(), nullable=True),
        sa.Column("overall_risk_level", sa.Enum(name="risk_level_enum", create_type=False), nullable=False, server_default="unknown"),
        sa.Column("domain_scores", postgresql.JSONB(), nullable=True),
        sa.Column("fragmented_annual_cost", sa.Numeric(12, 2), nullable=True),
        sa.Column("coordinated_annual_cost", sa.Numeric(12, 2), nullable=True),
        sa.Column("delta", sa.Numeric(12, 2), nullable=True),
        sa.Column("lifetime_cost_estimate", sa.Numeric(15, 2), nullable=True),
        sa.Column("cost_methodology", sa.String(255), nullable=True),
        sa.Column("systems_represented", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("systems_missing", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("fragment_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("recommendations", postgresql.JSONB(), nullable=True),
        sa.Column("crisis_flags", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("assembly_duration_ms", sa.Integer(), nullable=True),
        sa.Column("assembly_errors", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("assembly_metadata", postgresql.JSONB(), nullable=True),
        sa.Column("narrative_summary", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        comment="Assembled digital twin snapshots — one current per person, full history retained",
    )
    op.create_index("idx_dome_person_current", "dome", ["person_id"], unique=True, postgresql_where="is_current = true")
    op.create_index("idx_dome_person_assembled", "dome", ["person_id", "assembled_at"])
    op.create_index("idx_dome_cosm", "dome", ["cosm_score"])
    op.create_index("idx_dome_crisis", "dome", ["overall_risk_level"], postgresql_where="overall_risk_level = 'critical'")

    # ------------------------------------------------------------------
    # 16. flourishing_score
    # ------------------------------------------------------------------
    op.create_table(
        "flourishing_score",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("person.id", ondelete="CASCADE"), nullable=False),
        sa.Column("dome_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("dome.id", ondelete="SET NULL"), nullable=True),
        sa.Column("domain", sa.Enum(name="flourishing_domain_enum", create_type=False), nullable=False),
        sa.Column("scored_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("score", sa.Numeric(5, 2), nullable=False),
        sa.Column("score_delta", sa.Numeric(5, 2), nullable=True),
        sa.Column("trend", sa.String(32), nullable=True),
        sa.Column("risk_level", sa.Enum(name="risk_level_enum", create_type=False), nullable=False, server_default="unknown"),
        sa.Column("threats", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("supports", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("domain_layer", sa.Integer(), nullable=True),
        sa.Column("is_foundation_met", sa.Boolean(), nullable=True),
        sa.Column("evidence_sources", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("domain_data", postgresql.JSONB(), nullable=True),
        sa.Column("recommendations", postgresql.JSONB(), nullable=True),
        sa.Column("narrative", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        comment="12-domain flourishing scores per person per dome assembly",
    )
    op.create_index("idx_flourishing_person_domain_time", "flourishing_score", ["person_id", "domain", "scored_at"])
    op.create_index("idx_flourishing_dome", "flourishing_score", ["dome_id"])
    op.create_index("idx_flourishing_critical", "flourishing_score", ["domain", "risk_level"], postgresql_where="risk_level = 'critical'")


# ---------------------------------------------------------------------------
# Downgrade
# ---------------------------------------------------------------------------

def downgrade() -> None:
    """Drop ALL DOMES v2 tables and enum types — COMPLETE TEARDOWN."""

    # Drop in reverse dependency order
    tables = [
        "flourishing_score",
        "dome",
        "environment_reading",
        "biometric_reading",
        "enrollment",
        "assessment",
        "medication",
        "condition",
        "observation",
        "encounter",
        "provision",
        "data_gap",
        "fragment",
        "consent_audit_entry",
        "consent",
        "person",
        "government_system",
    ]

    for table in tables:
        op.drop_table(table)

    # Drop all custom enum types
    for name, _ in reversed(ENUM_DEFS):
        _drop_enum(name)
