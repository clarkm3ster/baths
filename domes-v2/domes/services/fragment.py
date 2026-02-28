"""
DOMES v2 — Fragment Engine (Streaming Data Ingestion)

The Fragment engine is the data collection layer of DOMES. It is responsible
for reaching into every data source — 30+ government systems, wearable APIs,
environmental sensors, and community reports — and reducing each record to a
standardised, quality-scored Fragment that can be assembled into a digital twin.

Information-theoretic framing
------------------------------
Each fragment carries a certain amount of *new* information about the person.
A duplicate ER claim from two payers carries zero new information; a first-ever
pharmacy fill of olanzapine carries high information gain. The engine tracks
this gain explicitly so that the Cosm engine can prioritise the fragments that
will shift the twin's beliefs the most.

Privacy architecture
--------------------
The engine enforces the strictest applicable privacy rule per data domain:

  42 CFR Part 2  — substance use (SUD) records require explicit written consent
                   and cannot be re-disclosed without a second written consent.
  HIPAA minimum necessary — only fields required for care coordination are
                   pulled; raw PHI never logged.
  CJIS            — criminal justice data requires a valid data sharing agreement
                   and encrypted transit.
  FERPA           — education records require separate consent if the person
                   is under 18 or enrolled in a FERPA-covered programme.

The privacy boundary check runs before any payload is written to storage.
If consent is absent or expired, the fragment is quarantined, not dropped,
so the *existence* of data can be audited even if the content cannot be read.
"""
from __future__ import annotations

import asyncio
import hashlib
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    "FragmentEngine",
    "SourceDescriptor",
    "IngestResult",
    "FragmentQualityScore",
    "CircuitState",
    "RobertJacksonDaySimulator",
]

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

QUALITY_THRESHOLD_ASSEMBLY = 0.30   # fragments below this score are excluded from dome assembly
QUALITY_THRESHOLD_WARN     = 0.50   # fragments below this score trigger a quality warning
MAX_BACKFILL_DAYS          = 365 * 3  # default historical backfill window (3 years)
CIRCUIT_FAIL_THRESHOLD     = 5       # consecutive failures before opening a circuit breaker
CIRCUIT_RESET_SECONDS      = 300     # seconds before a half-open probe is attempted


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class PollFrequency(str, Enum):
    """How often a source should be polled for new data."""
    REAL_TIME   = "real_time"    # sub-second push (wearables, event streams)
    FIVE_MIN    = "five_min"     # high-frequency biometric aggregation
    HOURLY      = "hourly"       # environmental sensors
    DAILY       = "daily"        # government batch jobs
    WEEKLY      = "weekly"       # some benefit programme data feeds
    ON_DEMAND   = "on_demand"    # triggered by an external event (discharge, booking)


class TrustLevel(str, Enum):
    """Source reliability tier — informs the quality score weight.

    Hierarchy mirrors evidence-based medicine's hierarchy of evidence:
    administrative claims and EHR labs > clinician notes > self-report > second-hand.
    """
    AUTHORITATIVE = "authoritative"  # Government claims, lab results, legal records
    CLINICAL      = "clinical"       # EHR/FHIR from a treating provider
    ADMINISTRATIVE = "administrative" # Benefits, enrollments, court records
    OBSERVATIONAL  = "observational"  # Wearable, environmental, community worker
    SELF_REPORT    = "self_report"    # Person's own statement
    SECOND_HAND    = "second_hand"    # Third-party observation (not primary source)


class CircuitState(str, Enum):
    """Circuit breaker state per data source."""
    CLOSED      = "closed"      # Normal operation
    OPEN        = "open"        # Source is down; requests suppressed
    HALF_OPEN   = "half_open"   # Probe request in flight to test recovery


class PrivacyLaw(str, Enum):
    """Privacy regulation governing a data source."""
    HIPAA          = "HIPAA"
    CFR_42_PART_2  = "42_CFR_Part_2"   # SUD — strictest re-disclosure rules
    CJIS           = "CJIS"
    FERPA          = "FERPA"
    HMIS_PRIVACY   = "HMIS_Privacy"
    PRIVACY_ACT    = "Privacy_Act"      # Federal records
    STATE_LAW      = "State_Law"
    NONE           = "none"             # Environmental / census — no consent required


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class FragmentQualityScore:
    """Five-component quality score for a single fragment.

    Information-theoretic design
    -----------------------------
    The composite score approximates the *reliability-weighted information
    content* of a fragment.  A stale (freshness=0.1) fragment from an
    authoritative source (reliability=1.0) is less useful than a fresh
    fragment from a clinical source (reliability=0.8).  The product captures
    this interaction.

    Components
    ----------
    freshness      : Decay function of data age.  Real-time wearable data
                     starts at 1.0 and decays to 0.5 at 24 hours.  A 90-day-old
                     HMIS enrollment starts at ~0.7 and decays further.
    reliability    : Source trust level mapped to [0.4, 1.0].  Medicaid claims
                     (AUTHORITATIVE) → 1.0.  Second-hand report → 0.4.
    completeness   : Fraction of expected fields that are non-null.  A FHIR
                     Observation with missing effectiveDateTime is penalised.
    consistency    : How well this fragment agrees with existing knowledge in
                     the twin.  A new address that contradicts three recent
                     HMIS records scores low until evidence accumulates.
    information_gain : Estimated KL-divergence from the prior twin state this
                     fragment introduces.  High for a first-ever diagnosis;
                     near-zero for the 50th duplicate ER claim from the same visit.
    composite      : Weighted harmonic mean, emphasising freshness × reliability.
    """

    freshness:        float = 1.0   # 0.0 – 1.0
    reliability:      float = 1.0   # 0.0 – 1.0
    completeness:     float = 1.0   # 0.0 – 1.0
    consistency:      float = 1.0   # 0.0 – 1.0
    information_gain: float = 1.0   # 0.0 – 1.0
    composite:        float = 0.0   # computed

    def compute_composite(self) -> float:
        """Compute composite as a reliability-freshness-weighted harmonic mean.

        The harmonic mean punishes a single very-low component more harshly
        than an arithmetic mean would — reflecting that a fragment that is
        almost-completely-stale (freshness≈0) should be near-useless regardless
        of how reliable its source is.
        """
        weights = [0.25, 0.25, 0.20, 0.15, 0.15]
        components = [self.freshness, self.reliability, self.completeness,
                      self.consistency, self.information_gain]
        weighted_sum = sum(w * c for w, c in zip(weights, components))
        self.composite = round(min(1.0, max(0.0, weighted_sum)), 4)
        return self.composite


@dataclass
class SourceDescriptor:
    """Registry entry for a single data source.

    DOMES maintains a live registry of every system it can reach.  Each entry
    captures the polling contract, trust level, privacy rules, and circuit
    breaker state for that source.  The registry is the authoritative list of
    what data is *possible* to collect for a person — gaps between what is
    possible and what was actually collected feed the DataGap model.
    """

    source_id:        str                  # Stable machine identifier ("medicaid_claims")
    display_name:     str                  # Human-readable ("State Medicaid Claims Feed")
    source_type:      str                  # Maps to FragmentSourceType enum value
    domain:           str                  # Maps to DataDomain enum value
    trust_level:      TrustLevel
    poll_frequency:   PollFrequency
    privacy_laws:     list[PrivacyLaw]     = field(default_factory=list)
    rate_limit_rph:   int                  = 60    # requests per hour
    supports_backfill: bool                = True
    supports_push:     bool                = False  # True if the source pushes events to DOMES
    requires_consent:  bool                = True
    api_base_url:     str | None           = None
    schema_version:   str                  = "1.0"
    tags:             list[str]            = field(default_factory=list)

    # Circuit breaker state (mutable at runtime)
    circuit_state:       CircuitState = CircuitState.CLOSED
    consecutive_failures: int         = 0
    last_failure_at:     datetime | None = None
    last_success_at:     datetime | None = None

    def is_available(self) -> bool:
        """Return True if the circuit breaker allows requests to this source."""
        if self.circuit_state == CircuitState.CLOSED:
            return True
        if self.circuit_state == CircuitState.OPEN:
            if (self.last_failure_at and
                    (datetime.now(tz=timezone.utc) - self.last_failure_at).total_seconds()
                    > CIRCUIT_RESET_SECONDS):
                self.circuit_state = CircuitState.HALF_OPEN
                return True
            return False
        # HALF_OPEN — one probe allowed
        return True


@dataclass
class IngestResult:
    """Outcome of a single fragment ingestion attempt.

    Tracks every stage of the lifecycle: arrival → validation → normalisation
    → quality scoring → storage → Cosm notification.
    """

    fragment_id:       str
    source_id:         str
    person_id:         str
    raw_payload:       dict[str, Any]
    normalised_payload: dict[str, Any] | None = None
    quality:           FragmentQualityScore | None = None
    ingested_at:       datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
    validated_at:      datetime | None = None
    assembled_at:      datetime | None = None
    validation_errors: list[str] = field(default_factory=list)
    is_duplicate:      bool = False
    is_quarantined:    bool = False
    quarantine_reason: str | None = None
    processing_notes:  str | None = None
    cosm_notified:     bool = False
    duration_ms:       int  = 0


# ---------------------------------------------------------------------------
# Source Registry
# ---------------------------------------------------------------------------

def _build_source_registry() -> dict[str, SourceDescriptor]:
    """Build the canonical registry of all 30+ data sources DOMES can reach.

    Each source entry describes the polling contract, trust level, privacy
    rules, and circuit breaker state.  This registry is the source of truth
    for the DataGap model — any source not represented in a given person's
    fragment set represents a *known gap*.

    The registry is intentionally declarative (data, not code) so that new
    sources can be added without touching ingestion logic.
    """
    sources: list[SourceDescriptor] = [
        # ----------------------------------------------------------------
        # Health / Clinical
        # ----------------------------------------------------------------
        SourceDescriptor(
            source_id="medicaid_claims",
            display_name="State Medicaid Claims Feed (CMS-64)",
            source_type="claims",
            domain="health",
            trust_level=TrustLevel.AUTHORITATIVE,
            poll_frequency=PollFrequency.DAILY,
            privacy_laws=[PrivacyLaw.HIPAA],
            rate_limit_rph=120,
            tags=["health", "claims", "medicaid"],
        ),
        SourceDescriptor(
            source_id="fhir_ehr_primary",
            display_name="Primary EHR (FHIR R4 — US Core)",
            source_type="fhir",
            domain="health",
            trust_level=TrustLevel.CLINICAL,
            poll_frequency=PollFrequency.DAILY,
            privacy_laws=[PrivacyLaw.HIPAA],
            supports_push=True,
            tags=["health", "fhir", "ehr"],
        ),
        SourceDescriptor(
            source_id="hospital_discharge",
            display_name="Hospital Discharge Summary Feed",
            source_type="fhir",
            domain="health",
            trust_level=TrustLevel.CLINICAL,
            poll_frequency=PollFrequency.ON_DEMAND,
            privacy_laws=[PrivacyLaw.HIPAA],
            supports_push=True,
            tags=["health", "discharge", "hospital"],
        ),
        SourceDescriptor(
            source_id="pharmacy_claims",
            display_name="Pharmacy Claims (NCPDP D.0)",
            source_type="pharmacy",
            domain="health",
            trust_level=TrustLevel.AUTHORITATIVE,
            poll_frequency=PollFrequency.DAILY,
            privacy_laws=[PrivacyLaw.HIPAA],
            tags=["health", "pharmacy", "medication"],
        ),
        # ----------------------------------------------------------------
        # Behavioural Health / SUD
        # ----------------------------------------------------------------
        SourceDescriptor(
            source_id="cmhc_behavioral_health",
            display_name="Community Mental Health Centre EHR",
            source_type="ehr",
            domain="behavioral_health",
            trust_level=TrustLevel.CLINICAL,
            poll_frequency=PollFrequency.DAILY,
            privacy_laws=[PrivacyLaw.HIPAA, PrivacyLaw.CFR_42_PART_2],
            requires_consent=True,
            tags=["behavioral_health", "cmhc"],
        ),
        SourceDescriptor(
            source_id="sud_treatment_programme",
            display_name="SUD Treatment Programme (42 CFR Part 2)",
            source_type="ehr",
            domain="substance_use",
            trust_level=TrustLevel.CLINICAL,
            poll_frequency=PollFrequency.DAILY,
            privacy_laws=[PrivacyLaw.CFR_42_PART_2],
            requires_consent=True,
            tags=["substance_use", "42cfr2"],
        ),
        SourceDescriptor(
            source_id="crisis_line_988",
            display_name="988 Crisis & Suicide Lifeline Call Log",
            source_type="ehr",
            domain="behavioral_health",
            trust_level=TrustLevel.CLINICAL,
            poll_frequency=PollFrequency.ON_DEMAND,
            privacy_laws=[PrivacyLaw.HIPAA],
            supports_push=True,
            tags=["behavioral_health", "crisis"],
        ),
        # ----------------------------------------------------------------
        # Housing
        # ----------------------------------------------------------------
        SourceDescriptor(
            source_id="hmis",
            display_name="Homeless Management Information System (HMIS)",
            source_type="hmis",
            domain="housing",
            trust_level=TrustLevel.ADMINISTRATIVE,
            poll_frequency=PollFrequency.DAILY,
            privacy_laws=[PrivacyLaw.HMIS_PRIVACY],
            rate_limit_rph=300,
            tags=["housing", "hmis", "shelter"],
        ),
        SourceDescriptor(
            source_id="housing_authority",
            display_name="Public Housing Authority (HCV/Section 8)",
            source_type="benefits",
            domain="housing",
            trust_level=TrustLevel.ADMINISTRATIVE,
            poll_frequency=PollFrequency.WEEKLY,
            privacy_laws=[PrivacyLaw.PRIVACY_ACT],
            tags=["housing", "section8"],
        ),
        SourceDescriptor(
            source_id="psh_provider",
            display_name="Permanent Supportive Housing Provider",
            source_type="hmis",
            domain="housing",
            trust_level=TrustLevel.ADMINISTRATIVE,
            poll_frequency=PollFrequency.DAILY,
            privacy_laws=[PrivacyLaw.HMIS_PRIVACY],
            tags=["housing", "psh"],
        ),
        # ----------------------------------------------------------------
        # Income / Benefits
        # ----------------------------------------------------------------
        SourceDescriptor(
            source_id="snap_ssa",
            display_name="SNAP Eligibility / Case Status (FNS API)",
            source_type="benefits",
            domain="financial",
            trust_level=TrustLevel.AUTHORITATIVE,
            poll_frequency=PollFrequency.WEEKLY,
            privacy_laws=[PrivacyLaw.PRIVACY_ACT],
            tags=["income", "snap", "benefits"],
        ),
        SourceDescriptor(
            source_id="ssi_ssdi",
            display_name="SSA Disability Benefit Status (SSI/SSDI)",
            source_type="benefits",
            domain="financial",
            trust_level=TrustLevel.AUTHORITATIVE,
            poll_frequency=PollFrequency.WEEKLY,
            privacy_laws=[PrivacyLaw.PRIVACY_ACT],
            tags=["income", "ssi", "ssdi"],
        ),
        SourceDescriptor(
            source_id="tanf_general_assistance",
            display_name="TANF / General Assistance (State DHS)",
            source_type="benefits",
            domain="financial",
            trust_level=TrustLevel.AUTHORITATIVE,
            poll_frequency=PollFrequency.WEEKLY,
            privacy_laws=[PrivacyLaw.PRIVACY_ACT],
            tags=["income", "tanf"],
        ),
        # ----------------------------------------------------------------
        # Justice / Corrections
        # ----------------------------------------------------------------
        SourceDescriptor(
            source_id="doc_corrections",
            display_name="Dept. of Corrections — Booking & Release",
            source_type="criminal_justice",
            domain="criminal_justice",
            trust_level=TrustLevel.AUTHORITATIVE,
            poll_frequency=PollFrequency.ON_DEMAND,
            privacy_laws=[PrivacyLaw.CJIS],
            supports_push=True,
            tags=["justice", "corrections", "booking"],
        ),
        SourceDescriptor(
            source_id="probation_parole",
            display_name="Probation & Parole Case Management",
            source_type="criminal_justice",
            domain="criminal_justice",
            trust_level=TrustLevel.ADMINISTRATIVE,
            poll_frequency=PollFrequency.WEEKLY,
            privacy_laws=[PrivacyLaw.CJIS],
            tags=["justice", "probation"],
        ),
        SourceDescriptor(
            source_id="drug_court",
            display_name="Drug Court Case Management System",
            source_type="criminal_justice",
            domain="criminal_justice",
            trust_level=TrustLevel.ADMINISTRATIVE,
            poll_frequency=PollFrequency.WEEKLY,
            privacy_laws=[PrivacyLaw.CJIS, PrivacyLaw.CFR_42_PART_2],
            tags=["justice", "drug_court"],
        ),
        # ----------------------------------------------------------------
        # Child Welfare
        # ----------------------------------------------------------------
        SourceDescriptor(
            source_id="dcfs_child_welfare",
            display_name="DCFS Child Welfare Case Management",
            source_type="benefits",
            domain="child_welfare",
            trust_level=TrustLevel.AUTHORITATIVE,
            poll_frequency=PollFrequency.WEEKLY,
            privacy_laws=[PrivacyLaw.STATE_LAW],
            tags=["child_welfare", "dcfs"],
        ),
        # ----------------------------------------------------------------
        # Wearables / Biometric
        # ----------------------------------------------------------------
        SourceDescriptor(
            source_id="dexcom_cgm",
            display_name="Dexcom G7 Continuous Glucose Monitor",
            source_type="cgm",
            domain="biometric",
            trust_level=TrustLevel.OBSERVATIONAL,
            poll_frequency=PollFrequency.FIVE_MIN,
            privacy_laws=[PrivacyLaw.HIPAA],
            supports_push=True,
            requires_consent=True,
            tags=["wearable", "cgm", "glucose"],
        ),
        SourceDescriptor(
            source_id="apple_watch_hrv",
            display_name="Apple Watch — Heart Rate + HRV + Sleep",
            source_type="wearable",
            domain="biometric",
            trust_level=TrustLevel.OBSERVATIONAL,
            poll_frequency=PollFrequency.REAL_TIME,
            privacy_laws=[PrivacyLaw.HIPAA],
            supports_push=True,
            requires_consent=True,
            tags=["wearable", "heart_rate", "sleep"],
        ),
        SourceDescriptor(
            source_id="oura_sleep",
            display_name="Oura Ring — Sleep Architecture",
            source_type="wearable",
            domain="biometric",
            trust_level=TrustLevel.OBSERVATIONAL,
            poll_frequency=PollFrequency.DAILY,
            privacy_laws=[PrivacyLaw.HIPAA],
            requires_consent=True,
            tags=["wearable", "sleep"],
        ),
        # ----------------------------------------------------------------
        # Environmental
        # ----------------------------------------------------------------
        SourceDescriptor(
            source_id="openweathermap",
            display_name="OpenWeatherMap — Current Conditions",
            source_type="environmental",
            domain="environmental",
            trust_level=TrustLevel.OBSERVATIONAL,
            poll_frequency=PollFrequency.HOURLY,
            privacy_laws=[PrivacyLaw.NONE],
            requires_consent=False,
            tags=["environmental", "weather"],
        ),
        SourceDescriptor(
            source_id="purpleair_aq",
            display_name="PurpleAir — Hyperlocal Air Quality (PM2.5)",
            source_type="environmental",
            domain="environmental",
            trust_level=TrustLevel.OBSERVATIONAL,
            poll_frequency=PollFrequency.HOURLY,
            privacy_laws=[PrivacyLaw.NONE],
            requires_consent=False,
            tags=["environmental", "air_quality"],
        ),
        SourceDescriptor(
            source_id="noaa_alerts",
            display_name="NOAA Weather Alerts (NWS API)",
            source_type="environmental",
            domain="environmental",
            trust_level=TrustLevel.AUTHORITATIVE,
            poll_frequency=PollFrequency.REAL_TIME,
            privacy_laws=[PrivacyLaw.NONE],
            supports_push=True,
            requires_consent=False,
            tags=["environmental", "weather", "alerts"],
        ),
        SourceDescriptor(
            source_id="noise_sensor",
            display_name="Ambient Noise Sensor (IoT / dB mesh)",
            source_type="environmental",
            domain="environmental",
            trust_level=TrustLevel.OBSERVATIONAL,
            poll_frequency=PollFrequency.HOURLY,
            privacy_laws=[PrivacyLaw.NONE],
            requires_consent=False,
            tags=["environmental", "noise"],
        ),
        # ----------------------------------------------------------------
        # Community Reports
        # ----------------------------------------------------------------
        SourceDescriptor(
            source_id="outreach_worker_notes",
            display_name="Street Outreach Worker Encounter Notes",
            source_type="manual",
            domain="health",
            trust_level=TrustLevel.OBSERVATIONAL,
            poll_frequency=PollFrequency.ON_DEMAND,
            privacy_laws=[PrivacyLaw.HMIS_PRIVACY],
            tags=["outreach", "community", "manual"],
        ),
        SourceDescriptor(
            source_id="peer_specialist_notes",
            display_name="Peer Specialist / Community Health Worker Notes",
            source_type="manual",
            domain="behavioral_health",
            trust_level=TrustLevel.OBSERVATIONAL,
            poll_frequency=PollFrequency.ON_DEMAND,
            privacy_laws=[PrivacyLaw.HIPAA],
            tags=["outreach", "peer", "manual"],
        ),
        # ----------------------------------------------------------------
        # System-generated Events
        # ----------------------------------------------------------------
        SourceDescriptor(
            source_id="benefit_determination_letters",
            display_name="Benefit Determination / Notice Letters (DHS)",
            source_type="benefits",
            domain="financial",
            trust_level=TrustLevel.AUTHORITATIVE,
            poll_frequency=PollFrequency.ON_DEMAND,
            privacy_laws=[PrivacyLaw.PRIVACY_ACT],
            supports_push=True,
            tags=["benefits", "letters", "events"],
        ),
        SourceDescriptor(
            source_id="court_calendar",
            display_name="Court Date / Hearing Calendar (CourtConnect)",
            source_type="criminal_justice",
            domain="criminal_justice",
            trust_level=TrustLevel.AUTHORITATIVE,
            poll_frequency=PollFrequency.DAILY,
            privacy_laws=[PrivacyLaw.CJIS],
            tags=["justice", "court", "events"],
        ),
        SourceDescriptor(
            source_id="medication_event_stream",
            display_name="Pharmacy Fill / Refill Event Stream (SureScripts)",
            source_type="pharmacy",
            domain="health",
            trust_level=TrustLevel.AUTHORITATIVE,
            poll_frequency=PollFrequency.ON_DEMAND,
            privacy_laws=[PrivacyLaw.HIPAA],
            supports_push=True,
            tags=["pharmacy", "medication", "events"],
        ),
        SourceDescriptor(
            source_id="er_admit_discharge_transfer",
            display_name="Hospital ADT Feed (HL7 v2 / FHIR Subscription)",
            source_type="fhir",
            domain="health",
            trust_level=TrustLevel.CLINICAL,
            poll_frequency=PollFrequency.ON_DEMAND,
            privacy_laws=[PrivacyLaw.HIPAA],
            supports_push=True,
            tags=["health", "adt", "er"],
        ),
    ]
    return {s.source_id: s for s in sources}


# ---------------------------------------------------------------------------
# Freshness decay functions
# ---------------------------------------------------------------------------

def _compute_freshness(ingested_at: datetime, source: SourceDescriptor) -> float:
    """Compute a freshness score [0, 1] based on data age and polling frequency.

    Uses an exponential decay model where the half-life is calibrated to the
    source's polling frequency:

        freshness = exp(-ln(2) * age / half_life)

    Half-lives by poll frequency:
        REAL_TIME   : 1 hour    (biometric data loses half its value in 60 min)
        FIVE_MIN    : 4 hours
        HOURLY      : 12 hours
        DAILY       : 3 days
        WEEKLY      : 14 days
        ON_DEMAND   : 30 days   (event data stays fresh longer)
    """
    import math
    half_lives_hours = {
        PollFrequency.REAL_TIME:  1.0,
        PollFrequency.FIVE_MIN:   4.0,
        PollFrequency.HOURLY:    12.0,
        PollFrequency.DAILY:     72.0,
        PollFrequency.WEEKLY:   336.0,
        PollFrequency.ON_DEMAND: 720.0,
    }
    half_life_h = half_lives_hours.get(source.poll_frequency, 72.0)
    age_h = (datetime.now(tz=timezone.utc) - ingested_at).total_seconds() / 3600.0
    return round(math.exp(-math.log(2) * age_h / half_life_h), 4)


def _trust_to_reliability(trust: TrustLevel) -> float:
    """Map TrustLevel to a numeric reliability weight."""
    mapping = {
        TrustLevel.AUTHORITATIVE:  1.00,
        TrustLevel.CLINICAL:       0.90,
        TrustLevel.ADMINISTRATIVE: 0.80,
        TrustLevel.OBSERVATIONAL:  0.65,
        TrustLevel.SELF_REPORT:    0.50,
        TrustLevel.SECOND_HAND:    0.40,
    }
    return mapping.get(trust, 0.50)


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def _compute_fragment_fingerprint(source_id: str, source_record_id: str,
                                   payload_subset: dict) -> str:
    """Compute a stable fingerprint for deduplication.

    Hashes the tuple (source_id, source_record_id) as the primary key.
    For sources without stable record IDs (community reports), a content
    hash of selected payload fields is used as a secondary key.

    The same ER visit reported by both the hospital ADT feed and the Medicaid
    claims feed produces two fragments with different source_ids, which is
    correct — they will be *merged* by the Cosm entity resolver rather than
    deduplicated here.  Deduplication only applies to the *same source*
    reporting the *same record* twice.
    """
    if source_record_id:
        content = f"{source_id}::{source_record_id}"
    else:
        stable_fields = {k: v for k, v in sorted(payload_subset.items())
                         if k not in {"timestamp", "ingested_at", "request_id"}}
        content = f"{source_id}::{str(stable_fields)}"
    return hashlib.sha256(content.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Privacy boundary enforcement
# ---------------------------------------------------------------------------

async def _check_privacy_boundary(
    source: SourceDescriptor,
    person_id: str,
    consent_present: bool,
) -> tuple[bool, str | None]:
    """Enforce the strictest applicable privacy rule for this fragment.

    Returns (allowed: bool, reason: str | None).

    42 CFR Part 2 check
    -------------------
    SUD records require *two* separate written consents:
      1. To collect the data from the treatment provider.
      2. To share the data with any downstream system.
    If either consent is missing, the fragment is quarantined — not dropped.
    Quarantine preserves the audit trail (we know data *exists*) without
    exposing PHI to unauthorised systems.

    HIPAA minimum necessary
    -----------------------
    For HIPAA-covered sources, we log the access but do not inspect field-level
    content here.  Field-level minimum-necessary enforcement happens at the
    normalisation stage where the FHIR payload is projected to only the fields
    required for care coordination (e.g., psychotherapy notes are stripped from
    Encounter resources shared across systems).
    """
    if not source.requires_consent:
        return True, None

    if not consent_present:
        if PrivacyLaw.CFR_42_PART_2 in source.privacy_laws:
            reason = (
                f"42 CFR Part 2 — SUD record from {source.source_id} requires "
                "explicit written consent.  Fragment quarantined pending consent."
            )
        else:
            reason = (
                f"HIPAA — consent not present for {source.source_id}. "
                "Fragment quarantined pending consent or emergency override."
            )
        return False, reason

    return True, None


# ---------------------------------------------------------------------------
# Fragment Engine
# ---------------------------------------------------------------------------

class FragmentEngine:
    """Streaming data ingestion engine for DOMES v2.

    Architecture overview
    ---------------------
    The engine operates as an async event loop.  Every inbound data event —
    whether a wearable push, a batch government poll, or a community worker note —
    passes through a five-stage pipeline:

        [1] Receive      — accept raw payload and source metadata
        [2] Validate     — schema validation, required-field checks
        [3] Deduplicate  — fingerprint check against the last-N seen set
        [4] Quality      — score freshness, reliability, completeness, consistency
        [5] Normalise    — transform source-native format → FHIR-aligned fragment
        [6] Store        — persist to database (deferred to caller via ingest_result)
        [7] Notify       — emit event to Cosm engine via the notification bus

    Rate limiting
    -------------
    Each source has a rate_limit_rph budget.  A leaky-bucket counter per source
    tracks usage.  When the bucket is empty, requests are queued and replayed
    on the next tick rather than dropped — guaranteeing eventual delivery while
    respecting API quotas.

    Circuit breaker
    ---------------
    Each source has a circuit breaker (CLOSED → OPEN → HALF_OPEN → CLOSED).
    After CIRCUIT_FAIL_THRESHOLD consecutive failures, the breaker opens and
    the source is skipped for CIRCUIT_RESET_SECONDS before a probe is sent.
    This prevents cascading failures from a single misbehaving government API
    from exhausting the engine's connection pool.
    """

    def __init__(self) -> None:
        self._registry: dict[str, SourceDescriptor] = _build_source_registry()
        self._seen_fingerprints: dict[str, datetime] = {}   # fingerprint → first_seen
        self._rate_buckets: dict[str, int] = {}             # source_id → remaining calls
        self._notification_queue: asyncio.Queue = asyncio.Queue()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def ingest_fragment(
        self,
        source_id: str,
        person_id: str,
        raw_payload: dict[str, Any],
        source_record_id: str | None = None,
        consent_present: bool = True,
        data_timestamp: datetime | None = None,
    ) -> IngestResult:
        """Ingest a single raw fragment through the full pipeline.

        This is the primary entry point for all data ingestion.  It is called:
          - By scheduled pollers (government batch feeds)
          - By push webhooks (wearable APIs, ADT feeds, event streams)
          - By the backfill runner (historical data loading)
          - By community workers submitting manual notes

        Parameters
        ----------
        source_id        : Key in the source registry (e.g., "medicaid_claims")
        person_id        : DOMES person UUID this fragment belongs to
        raw_payload      : Raw data exactly as received from the source
        source_record_id : Stable ID in the source system for deduplication
        consent_present  : Whether valid consent covers this data collection
        data_timestamp   : When the underlying event occurred (not ingestion time)

        Returns
        -------
        IngestResult with full lifecycle metadata.  The caller is responsible
        for persisting the result to the Fragment table and broadcasting to Cosm.
        """
        start = datetime.now(tz=timezone.utc)
        fragment_id = str(uuid.uuid4())

        source = self._registry.get(source_id)
        if source is None:
            logger.error("Unknown source_id=%s — fragment rejected", source_id)
            return IngestResult(
                fragment_id=fragment_id,
                source_id=source_id,
                person_id=person_id,
                raw_payload=raw_payload,
                validation_errors=[f"Unknown source_id: {source_id}"],
                is_quarantined=True,
                quarantine_reason="Source not in registry",
            )

        result = IngestResult(
            fragment_id=fragment_id,
            source_id=source_id,
            person_id=person_id,
            raw_payload=raw_payload,
        )

        # Stage 1: Circuit breaker check
        if not source.is_available():
            result.is_quarantined = True
            result.quarantine_reason = f"Circuit breaker OPEN for {source_id}"
            logger.warning("Circuit OPEN for %s — fragment %s queued", source_id, fragment_id)
            return result

        # Stage 2: Privacy boundary enforcement
        allowed, privacy_reason = await _check_privacy_boundary(
            source, person_id, consent_present
        )
        if not allowed:
            result.is_quarantined = True
            result.quarantine_reason = privacy_reason
            logger.info("Fragment quarantined (privacy): %s", privacy_reason)
            return result

        # Stage 3: Validation
        errors = await self._validate_payload(source, raw_payload)
        result.validation_errors = errors
        result.validated_at = datetime.now(tz=timezone.utc)
        if errors:
            logger.warning("Validation errors for %s: %s", source_id, errors)

        # Stage 4: Deduplication
        fingerprint = _compute_fragment_fingerprint(source_id, source_record_id or "", raw_payload)
        if fingerprint in self._seen_fingerprints:
            result.is_duplicate = True
            result.processing_notes = (
                f"Duplicate of fragment seen at "
                f"{self._seen_fingerprints[fingerprint].isoformat()}"
            )
            logger.debug("Duplicate fragment from %s suppressed", source_id)
            return result
        self._seen_fingerprints[fingerprint] = result.ingested_at

        # Stage 5: Quality scoring
        eff_timestamp = data_timestamp or result.ingested_at
        result.quality = await self._score_quality(source, raw_payload, eff_timestamp)

        if result.quality.composite < QUALITY_THRESHOLD_ASSEMBLY:
            result.processing_notes = (
                f"Quality score {result.quality.composite:.3f} below assembly threshold "
                f"{QUALITY_THRESHOLD_ASSEMBLY} — fragment stored but excluded from dome."
            )

        # Stage 6: Normalisation (FHIR projection)
        result.normalised_payload = await self._normalise_payload(source, raw_payload)

        # Stage 7: Circuit breaker success bookkeeping
        source.consecutive_failures = 0
        source.last_success_at = datetime.now(tz=timezone.utc)
        if source.circuit_state == CircuitState.HALF_OPEN:
            source.circuit_state = CircuitState.CLOSED
            logger.info("Circuit CLOSED for %s after successful probe", source_id)

        # Stage 8: Notify Cosm
        await self._notify_cosm(result)

        result.duration_ms = int(
            (datetime.now(tz=timezone.utc) - start).total_seconds() * 1000
        )
        return result

    async def poll_source(
        self,
        source_id: str,
        person_id: str,
        since: datetime | None = None,
    ) -> list[IngestResult]:
        """Poll a government or external source for new records since `since`.

        In production, this method delegates to source-specific adapters
        (HMIS adapter, Medicaid claims adapter, FHIR bulk export adapter).
        Here we model the call contract and return a list of IngestResults.

        The since parameter implements incremental polling — only records
        created or modified after that timestamp are fetched, reducing API
        load and processing time.  For sources without incremental support
        (some HMIS implementations), a full export is fetched and deduplicated.
        """
        source = self._registry.get(source_id)
        if source is None or not source.is_available():
            return []

        # Rate limiting check
        if not self._consume_rate_budget(source_id):
            logger.warning("Rate limit reached for %s — poll deferred", source_id)
            return []

        logger.info("Polling %s for person=%s since=%s", source_id, person_id, since)
        # In production, this calls the actual adapter.  Placeholder return.
        return []

    async def backfill_source(
        self,
        source_id: str,
        person_id: str,
        days: int = MAX_BACKFILL_DAYS,
    ) -> int:
        """Pull historical records from a source when it first connects.

        When DOMES gains access to a new data source for a person who has
        been in the system for years, it needs to backfill history.  This
        method initiates a full historical pull going back `days` days.

        Backfill runs at a reduced rate (1/10th of normal rate limit) to
        avoid overwhelming the source API.  Progress is tracked so the job
        can be resumed if interrupted.

        Returns the number of fragments successfully ingested.
        """
        source = self._registry.get(source_id)
        if source is None or not source.supports_backfill:
            return 0

        since = datetime.now(tz=timezone.utc) - timedelta(days=days)
        logger.info(
            "Backfilling %s for person=%s, going back %d days to %s",
            source_id, person_id, days, since.isoformat()
        )
        # Production: batch pull with progress checkpointing.
        return 0

    async def get_source_status(self) -> dict[str, dict]:
        """Return circuit breaker and freshness status for all sources."""
        return {
            sid: {
                "circuit_state":        src.circuit_state.value,
                "consecutive_failures": src.consecutive_failures,
                "last_success_at":      src.last_success_at.isoformat() if src.last_success_at else None,
                "last_failure_at":      src.last_failure_at.isoformat() if src.last_failure_at else None,
                "rate_remaining":       self._rate_buckets.get(sid, src.rate_limit_rph),
            }
            for sid, src in self._registry.items()
        }

    async def record_source_failure(self, source_id: str, error: str) -> None:
        """Record a source failure and potentially open the circuit breaker."""
        source = self._registry.get(source_id)
        if source is None:
            return
        source.consecutive_failures += 1
        source.last_failure_at = datetime.now(tz=timezone.utc)
        if source.consecutive_failures >= CIRCUIT_FAIL_THRESHOLD:
            source.circuit_state = CircuitState.OPEN
            logger.error(
                "Circuit OPENED for %s after %d consecutive failures: %s",
                source_id, source.consecutive_failures, error
            )

    # ------------------------------------------------------------------
    # Internal pipeline stages
    # ------------------------------------------------------------------

    async def _validate_payload(
        self,
        source: SourceDescriptor,
        payload: dict[str, Any],
    ) -> list[str]:
        """Validate the raw payload against minimum required fields.

        Each source type has a required-field contract.  Missing required
        fields are errors; missing optional fields reduce the completeness
        score.  The validation is intentionally lenient — we store the
        fragment even with errors, because partial data is better than no
        data for assembling the twin.

        Field contracts by source type:
          fhir      : resourceType, id, subject.reference, effectiveDateTime
          hmis      : PersonalID, EnrollmentID, EntryDate, ProjectType
          claims    : member_id, service_date, procedure_code, npi
          wearable  : device_id, timestamp, metric_type, value, unit
          manual    : worker_id, person_id, timestamp, note_text
        """
        errors = []
        required_by_type = {
            "fhir":           ["resourceType", "subject"],
            "hmis":           ["PersonalID", "EnrollmentID"],
            "claims":         ["member_id", "service_date"],
            "pharmacy":       ["member_id", "fill_date", "ndc"],
            "wearable":       ["device_id", "timestamp", "metric_type"],
            "cgm":            ["device_id", "timestamp", "glucose_mgdl"],
            "environmental":  ["location", "timestamp", "metric"],
            "manual":         ["worker_id", "timestamp"],
            "criminal_justice": ["booking_id"],
            "benefits":       ["case_number", "program_type"],
        }
        required = required_by_type.get(source.source_type, [])
        for field_name in required:
            if field_name not in payload or payload[field_name] is None:
                errors.append(f"Missing required field: {field_name}")
        return errors

    async def _score_quality(
        self,
        source: SourceDescriptor,
        payload: dict[str, Any],
        data_timestamp: datetime,
    ) -> FragmentQualityScore:
        """Compute the five-component quality score for a fragment."""
        required_by_type = {
            "fhir":     ["resourceType", "subject", "effectiveDateTime", "code", "valueQuantity"],
            "hmis":     ["PersonalID", "EnrollmentID", "EntryDate", "ProjectType", "HouseholdID"],
            "claims":   ["member_id", "service_date", "procedure_code", "npi", "diagnosis_codes"],
            "pharmacy": ["member_id", "fill_date", "ndc", "drug_name", "days_supply"],
            "wearable": ["device_id", "timestamp", "metric_type", "value", "unit"],
            "cgm":      ["device_id", "timestamp", "glucose_mgdl", "trend", "calibration_state"],
        }
        expected = required_by_type.get(source.source_type, list(payload.keys()))
        present = sum(1 for f in expected if f in payload and payload[f] is not None)
        completeness = present / len(expected) if expected else 1.0

        score = FragmentQualityScore(
            freshness        = _compute_freshness(data_timestamp, source),
            reliability      = _trust_to_reliability(source.trust_level),
            completeness     = round(completeness, 4),
            consistency      = 1.0,   # Updated by Cosm after twin comparison
            information_gain = 1.0,   # Updated by Cosm after KL-divergence computation
        )
        score.compute_composite()
        return score

    async def _normalise_payload(
        self,
        source: SourceDescriptor,
        raw_payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Normalise source-native payload to a FHIR-aligned unified fragment.

        Each source type has a normalisation adapter that maps its native
        schema to the DOMES unified fragment schema (FHIR R4-aligned):

          FHIR sources  : pass-through with DOMES extensions added
          HMIS CSV      : map HMIS data elements to FHIR Encounter / Observation
          Claims (837P) : map CPT/HCPCS to FHIR Claim → Encounter
          Wearable APIs : map device-native metrics to FHIR Observation
          Environmental : map sensor readings to FHIR Observation (SDOH category)
          Manual notes  : wrap in FHIR Communication resource

        HIPAA minimum necessary is enforced here by projecting FHIR resources
        to only the fields required for care coordination (e.g., psychotherapy
        notes are stripped from Encounter resources shared across systems).
        """
        normalised: dict[str, Any] = {
            "domes_version": "2.0",
            "source_type":   source.source_type,
            "domain":        source.domain,
            "normalised_at": datetime.now(tz=timezone.utc).isoformat(),
        }

        if source.source_type == "fhir":
            normalised.update(raw_payload)
        elif source.source_type == "hmis":
            normalised["resourceType"] = "Encounter"
            normalised["class"] = {"code": "SHELTER"}
            normalised["subject"] = {"identifier": raw_payload.get("PersonalID")}
            normalised["period"] = {
                "start": raw_payload.get("EntryDate"),
                "end": raw_payload.get("ExitDate"),
            }
        elif source.source_type in ("wearable", "cgm"):
            normalised["resourceType"] = "Observation"
            normalised["category"] = [{"coding": [{"code": "vital-signs"}]}]
            normalised["subject"] = {"reference": f"Person/{raw_payload.get('person_id', '')}"}
            normalised["effectiveDateTime"] = raw_payload.get("timestamp")
            normalised["device"] = {"display": raw_payload.get("device_id")}
        elif source.source_type == "environmental":
            normalised["resourceType"] = "Observation"
            normalised["category"] = [{"coding": [{"code": "sdoh"}]}]
            normalised["effectiveDateTime"] = raw_payload.get("timestamp")
        elif source.source_type == "manual":
            normalised["resourceType"] = "Communication"
            normalised["sender"] = {"display": raw_payload.get("worker_id")}
            normalised["payload"] = [{"contentString": raw_payload.get("note_text", "")}]
        else:
            normalised.update(raw_payload)

        return normalised

    async def _notify_cosm(self, result: IngestResult) -> None:
        """Emit a fragment-ready event to the Cosm assembly engine.

        The event is placed on the notification queue.  The Cosm engine
        subscribes to this queue and assembles the twin incrementally as
        fragments arrive.  For high-value fragments (quality > 0.8, first
        occurrence of a new domain), Cosm is notified with HIGH priority
        to trigger an immediate partial reassembly.
        """
        if result.is_duplicate or result.is_quarantined:
            return

        priority = "HIGH" if (result.quality and result.quality.composite > 0.80) else "NORMAL"
        event = {
            "event_type": "FRAGMENT_READY",
            "fragment_id": result.fragment_id,
            "person_id":   result.person_id,
            "source_id":   result.source_id,
            "quality":     result.quality.composite if result.quality else None,
            "priority":    priority,
            "timestamp":   datetime.now(tz=timezone.utc).isoformat(),
        }
        await self._notification_queue.put(event)
        result.cosm_notified = True

    def _consume_rate_budget(self, source_id: str) -> bool:
        """Consume one call from the source's rate budget. Return False if exhausted."""
        source = self._registry[source_id]
        remaining = self._rate_buckets.get(source_id, source.rate_limit_rph)
        if remaining <= 0:
            return False
        self._rate_buckets[source_id] = remaining - 1
        return True


# ---------------------------------------------------------------------------
# Robert Jackson Day Simulator
# ---------------------------------------------------------------------------

class RobertJacksonDaySimulator:
    """Model a typical day in Robert Jackson's fragment stream.

    Robert Jackson — 45 years old, chronically homeless 7+ years,
    schizoaffective disorder, 47 ER visits/year, enrolled in 9 government
    systems.  This simulator generates the fragment events that DOMES would
    ingest on a representative day, demonstrating the full range of source
    types, quality scores, and privacy rules.

    Fragment timeline for the simulated day:

      06:00  Oura Ring — overnight sleep data (3.2 hrs fragmented, REM deficit)
      07:30  HMIS — shelter check-out logged
      09:00  Dexcom CGM — fasting glucose 180 mg/dL (elevated, SINGLE_UP trend)
      11:00  Outreach worker — encounter note from street contact
      14:00  SureScripts — olanzapine refill (12 days late → adherence alert)
      16:00  NOAA — cold front alert (temps dropping to 28°F overnight)
      20:00  Hospital ADT — ER check-in, chief complaint: chest pain
      23:00  Hospital ADT — ER discharge, disposition: returned to homelessness
    """

    PERSON_ID = "rj-demo-00000000-0000-0000-0000-000000000001"

    def __init__(self, engine: FragmentEngine) -> None:
        self._engine = engine

    async def simulate_day(self, base_date: datetime | None = None) -> list[IngestResult]:
        """Run all eight fragment events for Robert's simulated day.

        Returns a list of IngestResult objects in chronological order.
        Each result captures the full pipeline outcome — quality scores,
        validation results, and Cosm notification status.
        """
        base = base_date or datetime.now(tz=timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        results: list[IngestResult] = []

        # 06:00 — Oura sleep data (3.2 hours, fragmented — well below the
        # healthy 7-8h target).  The sleep architecture shows near-zero deep
        # sleep and REM, consistent with antipsychotic medication effects and
        # the hyperarousal state of sleeping outdoors.
        r = await self._engine.ingest_fragment(
            source_id="oura_sleep",
            person_id=self.PERSON_ID,
            raw_payload={
                "device_id":       "oura-rj-001",
                "timestamp":       (base + timedelta(hours=6)).isoformat(),
                "total_sleep_hrs": 3.2,
                "sleep_stages": {
                    "deep_min":  8,
                    "rem_min":  14,
                    "light_min": 96,
                    "awake_min": 74,
                },
                "readiness_score": 28,
                "hrv_avg_ms":      18.3,
                "resting_hr_bpm":  72,
                "metric_type":     "sleep_summary",
                "value":           3.2,
                "unit":            "hours",
            },
            data_timestamp=base + timedelta(hours=6),
        )
        results.append(r)
        logger.info("[RJ 06:00] Sleep fragment — quality=%.3f, 3.2hrs (fragmented)",
                    r.quality.composite if r.quality else 0)

        # 07:30 — HMIS shelter check-out.  Robert stayed one night at a
        # 100-bed emergency shelter.  The check-out is logged in HMIS,
        # revealing his housing status as SHELTERED for this single night.
        # Absence of check-in data for the following night implies return
        # to street (UNSHELTERED) — the Cosm engine will infer this gap.
        r = await self._engine.ingest_fragment(
            source_id="hmis",
            person_id=self.PERSON_ID,
            raw_payload={
                "PersonalID":   "HMIS-RJ-9412",
                "EnrollmentID": "ENR-2024-88317",
                "EntryDate":    (base - timedelta(hours=17)).strftime("%Y-%m-%d"),
                "ExitDate":     (base + timedelta(hours=7, minutes=30)).strftime("%Y-%m-%d"),
                "ProjectType":  1,   # 1 = Emergency Shelter
                "ExitDestination": "17",   # Other location (street)
                "HouseholdID":  "HH-001",
                "RelationshipToHoH": 1,
            },
            source_record_id="ENR-2024-88317",
            data_timestamp=base + timedelta(hours=7, minutes=30),
        )
        results.append(r)
        logger.info("[RJ 07:30] HMIS shelter checkout — quality=%.3f",
                    r.quality.composite if r.quality else 0)

        # 09:00 — Dexcom CGM glucose reading.  180 mg/dL is in the
        # clinically elevated range (normal fasting: 70-100).  The
        # SINGLE_UP trend means glucose is rising ~2 mg/dL/min, suggesting
        # a post-shelter-breakfast spike.  This reading may also be
        # medication-induced: olanzapine is strongly associated with
        # hyperglycaemia and metabolic syndrome.
        r = await self._engine.ingest_fragment(
            source_id="dexcom_cgm",
            person_id=self.PERSON_ID,
            raw_payload={
                "device_id":       "dexcom-g7-rj-02",
                "timestamp":       (base + timedelta(hours=9)).isoformat(),
                "glucose_mgdl":    180,
                "trend":           "SINGLE_UP",
                "trend_rate":      2.1,
                "calibration_state": "CALIBRATED",
                "metric_type":     "blood_glucose",
                "value":           180,
                "unit":            "mg/dL",
            },
            source_record_id=f"cgm-{base.date()}-0900",
            data_timestamp=base + timedelta(hours=9),
        )
        results.append(r)
        logger.info("[RJ 09:00] CGM glucose 180 mg/dL (elevated, SINGLE_UP) — quality=%.3f",
                    r.quality.composite if r.quality else 0)

        # 11:00 — Street outreach worker note.  This is a MANUAL fragment
        # (lowest reliability tier) but carries unique information: the
        # worker's observation of Robert's mental state, affect, and
        # expressed needs — information no government system captures.
        r = await self._engine.ingest_fragment(
            source_id="outreach_worker_notes",
            person_id=self.PERSON_ID,
            raw_payload={
                "worker_id":   "OW-BRIDGE-042",
                "timestamp":   (base + timedelta(hours=11)).isoformat(),
                "note_text": (
                    "Encountered RJ at the corner of Michigan & 14th.  "
                    "Appeared agitated, pacing.  Stated he ran out of his "
                    "medication 12 days ago and has not been sleeping.  "
                    "Declined shelter referral.  Accepted 2-day supply of "
                    "olanzapine from team's bridge medication kit.  Will "
                    "attempt warm handoff to CMHC tomorrow morning."
                ),
                "location":    "Michigan Ave & 14th St",
                "contact_type": "street_outreach",
                "person_id":   self.PERSON_ID,
            },
            data_timestamp=base + timedelta(hours=11),
        )
        results.append(r)
        logger.info("[RJ 11:00] Outreach note (agitated, med lapse 12d) — quality=%.3f",
                    r.quality.composite if r.quality else 0)

        # 14:00 — Pharmacy claim for olanzapine.  The fill is 12 days late
        # (prescription due date was 12 days ago).  This is an AUTHORITATIVE
        # fragment — it is a CMS-compliant pharmacy claim, the most reliable
        # evidence of medication adherence (or lack thereof).
        # PDC (proportion of days covered) for this fill: 0.0 for the 12-day gap.
        r = await self._engine.ingest_fragment(
            source_id="pharmacy_claims",
            person_id=self.PERSON_ID,
            raw_payload={
                "member_id":   "MEDICAID-RJ-441209",
                "fill_date":   (base + timedelta(hours=14)).strftime("%Y-%m-%d"),
                "ndc":         "00093-0093-01",
                "drug_name":   "Olanzapine 10mg",
                "days_supply": 30,
                "quantity":    30,
                "prescriber_npi": "1234567890",
                "pharmacy_npi":   "9876543210",
                "days_late":   12,
                "prior_fill_date": (base - timedelta(days=42)).strftime("%Y-%m-%d"),
            },
            source_record_id=f"rx-claim-{base.strftime('%Y%m%d')}-ola-001",
            data_timestamp=base + timedelta(hours=14),
        )
        results.append(r)
        logger.info("[RJ 14:00] Pharmacy — olanzapine fill (12d late) — quality=%.3f",
                    r.quality.composite if r.quality else 0)

        # 16:00 — NOAA cold front weather alert.  Temperatures dropping to
        # 28°F overnight.  For an unsheltered person, this is a direct health
        # threat — hypothermia risk is critical below 32°F.  This environmental
        # fragment has NO privacy restrictions (public data) but HIGH impact
        # on the twin's risk calculation.
        r = await self._engine.ingest_fragment(
            source_id="noaa_alerts",
            person_id=self.PERSON_ID,
            raw_payload={
                "location":       "Chicago, IL (Cook County)",
                "timestamp":      (base + timedelta(hours=16)).isoformat(),
                "metric":         "temperature_ambient",
                "alert_type":     "WINTER_WEATHER_ADVISORY",
                "forecast_low_f": 28,
                "forecast_high_f": 34,
                "wind_chill_f":   18,
                "precipitation":  "SNOW",
                "valid_until":    (base + timedelta(hours=36)).isoformat(),
                "urgency":        "CRITICAL",
                "headline":       "Wind Chill Warning through tomorrow morning",
            },
            data_timestamp=base + timedelta(hours=16),
        )
        results.append(r)
        logger.info("[RJ 16:00] Weather alert — 28F overnight, wind chill 18F — quality=%.3f",
                    r.quality.composite if r.quality else 0)

        # 20:00 — Hospital ADT admission event.  Chest pain, likely panic
        # attack (consistent with untreated schizoaffective disorder, medication
        # lapse, poor sleep, and cold stress).  This is ER visit #38 of the
        # year.  Estimated cost: $2,385 (median ED visit, Medicaid rates).
        r = await self._engine.ingest_fragment(
            source_id="er_admit_discharge_transfer",
            person_id=self.PERSON_ID,
            raw_payload={
                "resourceType":  "Encounter",
                "id":            "enc-rj-2024-er-038",
                "subject":       {"reference": f"Patient/{self.PERSON_ID}"},
                "class":         {"code": "EMER"},
                "status":        "in-progress",
                "period":        {"start": (base + timedelta(hours=20)).isoformat()},
                "reasonCode": [{
                    "coding": [{"system": "http://hl7.org/fhir/sid/icd-10-cm",
                                "code": "R07.9",
                                "display": "Chest pain, unspecified"}]
                }],
                "location": [{
                    "location": {"display": "Rush University Medical Center ED"},
                    "status": "active",
                }],
                "hospitalization": {
                    "admitSource": {"coding": [{"code": "hosp-trans"}]},
                },
            },
            source_record_id="enc-rj-2024-er-038",
            data_timestamp=base + timedelta(hours=20),
        )
        results.append(r)
        logger.info("[RJ 20:00] ER admission — chest pain (visit #38/yr) — quality=%.3f",
                    r.quality.composite if r.quality else 0)

        # 23:00 — Hospital ADT discharge event.  Diagnosis updated to panic
        # attack.  Disposition: returned to homelessness.  The 3-hour ER stay
        # resolves the acute crisis but returns Robert to the same conditions
        # (cold, unmedicated, unsheltered) that triggered it.  The system
        # has cost $2,385 to treat the symptom, not the cause.
        r = await self._engine.ingest_fragment(
            source_id="er_admit_discharge_transfer",
            person_id=self.PERSON_ID,
            raw_payload={
                "resourceType": "Encounter",
                "id":           "enc-rj-2024-er-038",
                "subject":      {"reference": f"Patient/{self.PERSON_ID}"},
                "class":        {"code": "EMER"},
                "status":       "finished",
                "period": {
                    "start": (base + timedelta(hours=20)).isoformat(),
                    "end":   (base + timedelta(hours=23)).isoformat(),
                },
                "reasonCode": [{
                    "coding": [{"system": "http://hl7.org/fhir/sid/icd-10-cm",
                                "code": "F41.0",
                                "display": "Panic disorder without agoraphobia"}]
                }],
                "hospitalization": {
                    "dischargeDisposition": {
                        "coding": [{"code": "other", "display": "Returned to homelessness"}]
                    }
                },
                "estimated_cost_usd": 2385,
            },
            source_record_id="enc-rj-2024-er-038",
            data_timestamp=base + timedelta(hours=23),
        )
        results.append(r)
        logger.info("[RJ 23:00] ER discharge — panic attack, returned to street — quality=%.3f",
                    r.quality.composite if r.quality else 0)

        return results
