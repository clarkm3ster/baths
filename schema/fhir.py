"""
BATHS Dome — FHIR R4 Health Layer Scaffolding

The BATHS Dome: A Whole-Person Digital Twin Architecture
Layer 4 (Health) speaks FHIR R4.

This module scaffolds real FHIR R4 resource types as the ingestion format
for the dome health layer. These are not full FHIR implementations — they
are typed Pydantic models that mirror FHIR resource structures closely
enough that:
1. A healthcare informaticist would recognize them immediately
2. Real FHIR data can be ingested without transformation
3. Cross-layer queries can reference health data with type safety
4. Export produces valid FHIR-compatible JSON

Standard coding systems used:
- SNOMED CT (http://snomed.info/sct) — clinical terms
- ICD-10-CM (http://hl7.org/fhir/sid/icd-10-cm) — diagnoses
- LOINC (http://loinc.org) — observations/lab results
- RxNorm (http://www.nlm.nih.gov/research/umls/rxnorm) — medications
- CPT (http://www.ama-assn.org/go/cpt) — procedures
- NPI (http://hl7.org/fhir/sid/us-npi) — provider identification

Reference: HL7 FHIR R4 (http://hl7.org/fhir/R4/)
"""

from datetime import datetime, date
from typing import Optional, Dict, List, Any, Literal
from pydantic import BaseModel, Field
from enum import Enum
import uuid


# ── FHIR Primitives ─────────────────────────────────────────────

class CodingSystem(str, Enum):
    """Standard FHIR coding system URIs."""
    SNOMED = "http://snomed.info/sct"
    ICD10 = "http://hl7.org/fhir/sid/icd-10-cm"
    LOINC = "http://loinc.org"
    RXNORM = "http://www.nlm.nih.gov/research/umls/rxnorm"
    CPT = "http://www.ama-assn.org/go/cpt"
    NPI = "http://hl7.org/fhir/sid/us-npi"
    CVX = "http://hl7.org/fhir/sid/cvx"
    FHIR_CONDITION_CLINICAL = "http://terminology.hl7.org/CodeSystem/condition-clinical"
    FHIR_CONDITION_VERIFICATION = "http://terminology.hl7.org/CodeSystem/condition-ver-status"
    FHIR_COVERAGE_TYPE = "http://terminology.hl7.org/CodeSystem/v3-ActCode"
    FHIR_OBSERVATION_CATEGORY = "http://terminology.hl7.org/CodeSystem/observation-category"


class Coding(BaseModel):
    """FHIR Coding — a reference to a code in a code system.
    See: http://hl7.org/fhir/R4/datatypes.html#Coding"""
    system: str                    # URI of the code system
    code: str                      # Code value
    display: Optional[str] = None  # Human-readable display text


class CodeableConcept(BaseModel):
    """FHIR CodeableConcept — a concept with one or more codings.
    See: http://hl7.org/fhir/R4/datatypes.html#CodeableConcept"""
    coding: List[Coding] = Field(default_factory=list)
    text: Optional[str] = None     # Plain text representation


class Period(BaseModel):
    """FHIR Period — a time range.
    See: http://hl7.org/fhir/R4/datatypes.html#Period"""
    start: Optional[datetime] = None
    end: Optional[datetime] = None


class Reference(BaseModel):
    """FHIR Reference — a reference to another resource.
    See: http://hl7.org/fhir/R4/references.html"""
    reference: Optional[str] = None   # Relative reference (e.g., "Patient/123")
    type: Optional[str] = None        # Resource type
    display: Optional[str] = None     # Human-readable description


class Quantity(BaseModel):
    """FHIR Quantity — a measured amount.
    See: http://hl7.org/fhir/R4/datatypes.html#Quantity"""
    value: Optional[float] = None
    unit: Optional[str] = None
    system: Optional[str] = None      # UCUM system for units
    code: Optional[str] = None        # UCUM code


class HumanName(BaseModel):
    """FHIR HumanName.
    See: http://hl7.org/fhir/R4/datatypes.html#HumanName"""
    use: Optional[str] = None         # usual, official, temp, nickname, anonymous, old, maiden
    family: Optional[str] = None
    given: List[str] = Field(default_factory=list)
    prefix: List[str] = Field(default_factory=list)
    suffix: List[str] = Field(default_factory=list)
    text: Optional[str] = None


class Address(BaseModel):
    """FHIR Address.
    See: http://hl7.org/fhir/R4/datatypes.html#Address"""
    use: Optional[str] = None         # home, work, temp, old, billing
    type: Optional[str] = None        # postal, physical, both
    line: List[str] = Field(default_factory=list)
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None


class ContactPoint(BaseModel):
    """FHIR ContactPoint.
    See: http://hl7.org/fhir/R4/datatypes.html#ContactPoint"""
    system: Optional[str] = None      # phone, fax, email, pager, url, sms, other
    value: Optional[str] = None
    use: Optional[str] = None         # home, work, temp, old, mobile


class Identifier(BaseModel):
    """FHIR Identifier.
    See: http://hl7.org/fhir/R4/datatypes.html#Identifier"""
    system: Optional[str] = None      # URI of the identifier system
    value: Optional[str] = None       # The identifier value
    use: Optional[str] = None         # usual, official, temp, secondary, old
    type: Optional[CodeableConcept] = None


class Annotation(BaseModel):
    """FHIR Annotation — a text note with attribution.
    See: http://hl7.org/fhir/R4/datatypes.html#Annotation"""
    text: str
    time: Optional[datetime] = None
    authorString: Optional[str] = None


# ── FHIR Resources ──────────────────────────────────────────────

class FHIRResource(BaseModel):
    """Base for all FHIR resources in the dome."""
    resourceType: str
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    meta: Dict[str, Any] = Field(default_factory=lambda: {
        "profile": [],
        "lastUpdated": datetime.utcnow().isoformat(),
    })
    # Dome-specific extension: link to dome layer
    _dome_layer: int = 4
    _dome_timestamp: datetime = Field(default_factory=datetime.utcnow)


class FHIRPatient(FHIRResource):
    """FHIR Patient — the dome subject's demographic and administrative data.
    See: http://hl7.org/fhir/R4/patient.html

    This is the gravitational center of the dome's health layer.
    Every other health resource references this Patient.
    """
    resourceType: str = "Patient"
    identifier: List[Identifier] = Field(default_factory=list)
    name: List[HumanName] = Field(default_factory=list)
    gender: Optional[str] = None      # male, female, other, unknown
    birthDate: Optional[str] = None   # YYYY-MM-DD
    address: List[Address] = Field(default_factory=list)
    telecom: List[ContactPoint] = Field(default_factory=list)
    maritalStatus: Optional[CodeableConcept] = None
    communication: List[Dict[str, Any]] = Field(default_factory=list)
    # Extensions
    race: Optional[CodeableConcept] = None        # US Core Race
    ethnicity: Optional[CodeableConcept] = None   # US Core Ethnicity
    birthSex: Optional[str] = None                # US Core Birth Sex


class FHIRCondition(FHIRResource):
    """FHIR Condition — a clinical condition, problem, or diagnosis.
    See: http://hl7.org/fhir/R4/condition.html

    Coded with ICD-10-CM or SNOMED CT.
    Clinical status tracks active/recurrence/remission/resolved.
    Verification status tracks confirmed/unconfirmed/differential.
    """
    resourceType: str = "Condition"
    clinicalStatus: Optional[CodeableConcept] = None
    verificationStatus: Optional[CodeableConcept] = None
    category: List[CodeableConcept] = Field(default_factory=list)
    severity: Optional[CodeableConcept] = None
    code: Optional[CodeableConcept] = None         # ICD-10 or SNOMED code
    subject: Optional[Reference] = None            # Reference to Patient
    onsetDateTime: Optional[str] = None
    abatementDateTime: Optional[str] = None
    recordedDate: Optional[str] = None
    note: List[Annotation] = Field(default_factory=list)
    # Dome extensions
    barriers_to_treatment: List[str] = Field(default_factory=list)
    cross_layer_impacts: List[Dict[str, Any]] = Field(default_factory=list)
    # e.g., [{"layer": 5, "impact": "Asthma exacerbated by housing mold"}]


class FHIRObservation(FHIRResource):
    """FHIR Observation — measurements and assessments.
    See: http://hl7.org/fhir/R4/observation.html

    Covers vital signs, lab results, social assessments, screening scores.
    Coded with LOINC.
    """
    resourceType: str = "Observation"
    status: str = "final"              # registered, preliminary, final, amended
    category: List[CodeableConcept] = Field(default_factory=list)
    code: Optional[CodeableConcept] = None  # LOINC code
    subject: Optional[Reference] = None
    effectiveDateTime: Optional[str] = None
    valueQuantity: Optional[Quantity] = None
    valueCodeableConcept: Optional[CodeableConcept] = None
    valueString: Optional[str] = None
    interpretation: List[CodeableConcept] = Field(default_factory=list)
    referenceRange: List[Dict[str, Any]] = Field(default_factory=list)
    note: List[Annotation] = Field(default_factory=list)
    # Dome extensions
    sdoh_domain: Optional[str] = None  # PRAPARE/AHC-HRSN domain if social assessment


class FHIRCoverage(FHIRResource):
    """FHIR Coverage — insurance and benefit plan information.
    See: http://hl7.org/fhir/R4/coverage.html

    Tracks Medicaid, CHIP, employer insurance, marketplace plans.
    Links to Layer 1 (legal entitlements) and Layer 3 (fiscal).
    """
    resourceType: str = "Coverage"
    status: str = "active"             # active, cancelled, draft, entered-in-error
    type: Optional[CodeableConcept] = None  # Type of coverage
    subscriber: Optional[Reference] = None
    beneficiary: Optional[Reference] = None
    period: Optional[Period] = None
    payor: List[Reference] = Field(default_factory=list)
    class_: List[Dict[str, Any]] = Field(default_factory=list, alias="class")
    # Dome extensions
    program_name: Optional[str] = None          # e.g., "Medicaid", "CHIP", "ACA Marketplace"
    layer_1_entitlement_id: Optional[str] = None  # Cross-reference to legal layer
    layer_3_fiscal_stream_id: Optional[str] = None  # Cross-reference to fiscal layer
    coverage_gaps: List[str] = Field(default_factory=list)

    class Config:
        populate_by_name = True


class FHIRMedicationRequest(FHIRResource):
    """FHIR MedicationRequest — a prescription or medication order.
    See: http://hl7.org/fhir/R4/medicationrequest.html

    Coded with RxNorm.
    """
    resourceType: str = "MedicationRequest"
    status: str = "active"             # active, on-hold, cancelled, completed, stopped, draft
    intent: str = "order"              # proposal, plan, order, original-order, reflex-order
    medicationCodeableConcept: Optional[CodeableConcept] = None  # RxNorm code
    subject: Optional[Reference] = None
    authoredOn: Optional[str] = None
    requester: Optional[Reference] = None
    dosageInstruction: List[Dict[str, Any]] = Field(default_factory=list)
    note: List[Annotation] = Field(default_factory=list)
    # Dome extensions
    affordability_barrier: bool = False
    access_barrier: bool = False
    adherence_status: Optional[str] = None  # full, partial, non-adherent, unknown
    drug_interactions_flagged: List[str] = Field(default_factory=list)


class FHIRCarePlan(FHIRResource):
    """FHIR CarePlan — a plan for patient care.
    See: http://hl7.org/fhir/R4/careplan.html

    In the dome context, this represents the cross-layer care coordination plan.
    """
    resourceType: str = "CarePlan"
    status: str = "active"
    intent: str = "plan"
    title: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[Reference] = None
    period: Optional[Period] = None
    category: List[CodeableConcept] = Field(default_factory=list)
    activity: List[Dict[str, Any]] = Field(default_factory=list)
    goal: List[Reference] = Field(default_factory=list)
    note: List[Annotation] = Field(default_factory=list)
    # Dome extensions
    cross_layer_goals: List[Dict[str, Any]] = Field(default_factory=list)
    # e.g., [{"layer": 5, "goal": "Stable housing within 90 days",
    #          "health_impact": "Reduced ER visits for asthma"}]
    coordination_complexity: Optional[float] = None  # 0-100


class FHIREncounter(FHIRResource):
    """FHIR Encounter — an interaction with the healthcare system.
    See: http://hl7.org/fhir/R4/encounter.html

    Tracks ER visits, clinic appointments, telehealth, inpatient stays.
    """
    resourceType: str = "Encounter"
    status: str = "finished"
    class_: Optional[Coding] = Field(default=None, alias="class")
    type: List[CodeableConcept] = Field(default_factory=list)
    subject: Optional[Reference] = None
    period: Optional[Period] = None
    reasonCode: List[CodeableConcept] = Field(default_factory=list)
    hospitalization: Optional[Dict[str, Any]] = None
    # Dome extensions
    avoidable: bool = False            # Was this avoidable with coordination?
    coordination_failure: Optional[str] = None  # Which system failure caused this?
    layer_2_system_gap: Optional[str] = None    # Cross-ref to systems layer

    class Config:
        populate_by_name = True


# ── FHIR Bundle ─────────────────────────────────────────────────

class FHIRBundleEntry(BaseModel):
    """An entry in a FHIR Bundle."""
    fullUrl: Optional[str] = None
    resource: Dict[str, Any] = Field(default_factory=dict)


class FHIRBundle(BaseModel):
    """FHIR Bundle — a collection of resources.
    See: http://hl7.org/fhir/R4/bundle.html

    Used to export the complete health layer as a FHIR-compatible document.
    """
    resourceType: str = "Bundle"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str = "collection"           # collection, document, message, transaction
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    total: int = 0
    entry: List[FHIRBundleEntry] = Field(default_factory=list)
    # Dome header
    _dome_schema_id: Optional[str] = None
    _dome_subject_name: Optional[str] = None


# ── Health Layer Integration ────────────────────────────────────

class HealthLayerFHIR(BaseModel):
    """
    The BATHS Dome: A Whole-Person Digital Twin Architecture
    Layer 4 Health Data — FHIR R4 Format

    All health data in the dome is stored as FHIR resources.
    This provides:
    1. Standard interoperability with any EHR/HIE
    2. Type-safe cross-layer queries (health → housing, health → legal)
    3. Temporal tracking of all health events
    4. Export as valid FHIR Bundle
    """
    # The patient resource (one per dome)
    patient: Optional[FHIRPatient] = None

    # Active conditions (ICD-10 / SNOMED coded)
    conditions: List[FHIRCondition] = Field(default_factory=list)

    # Observations: vitals, labs, screenings, social assessments
    observations: List[FHIRObservation] = Field(default_factory=list)

    # Coverage: insurance, benefits, entitlements
    coverages: List[FHIRCoverage] = Field(default_factory=list)

    # Medications
    medication_requests: List[FHIRMedicationRequest] = Field(default_factory=list)

    # Care plans (including cross-layer coordination plans)
    care_plans: List[FHIRCarePlan] = Field(default_factory=list)

    # Encounters: ER visits, clinic, inpatient
    encounters: List[FHIREncounter] = Field(default_factory=list)

    # Aggregate metrics
    total_conditions: int = 0
    total_medications: int = 0
    total_encounters_last_year: int = 0
    avoidable_encounters: int = 0      # Encounters caused by coordination failure
    coverage_gap_count: int = 0
    drug_interaction_count: int = 0

    def to_fhir_bundle(self) -> FHIRBundle:
        """Export the complete health layer as a FHIR Bundle."""
        entries = []
        if self.patient:
            entries.append(FHIRBundleEntry(
                fullUrl=f"urn:uuid:{self.patient.id}",
                resource=self.patient.model_dump(),
            ))
        for condition in self.conditions:
            entries.append(FHIRBundleEntry(
                fullUrl=f"urn:uuid:{condition.id}",
                resource=condition.model_dump(),
            ))
        for obs in self.observations:
            entries.append(FHIRBundleEntry(
                fullUrl=f"urn:uuid:{obs.id}",
                resource=obs.model_dump(),
            ))
        for cov in self.coverages:
            entries.append(FHIRBundleEntry(
                fullUrl=f"urn:uuid:{cov.id}",
                resource=cov.model_dump(by_alias=True),
            ))
        for med in self.medication_requests:
            entries.append(FHIRBundleEntry(
                fullUrl=f"urn:uuid:{med.id}",
                resource=med.model_dump(),
            ))
        for cp in self.care_plans:
            entries.append(FHIRBundleEntry(
                fullUrl=f"urn:uuid:{cp.id}",
                resource=cp.model_dump(),
            ))
        for enc in self.encounters:
            entries.append(FHIRBundleEntry(
                fullUrl=f"urn:uuid:{enc.id}",
                resource=enc.model_dump(by_alias=True),
            ))

        return FHIRBundle(
            total=len(entries),
            entry=entries,
        )

    def compute_metrics(self) -> Dict[str, Any]:
        """Compute aggregate health metrics for scoring."""
        self.total_conditions = len(self.conditions)
        self.total_medications = len(self.medication_requests)
        self.coverage_gap_count = sum(
            len(c.coverage_gaps) for c in self.coverages
        )
        self.drug_interaction_count = sum(
            len(m.drug_interactions_flagged) for m in self.medication_requests
        )
        self.avoidable_encounters = sum(
            1 for e in self.encounters if e.avoidable
        )

        # Conditions by clinical status
        active = sum(1 for c in self.conditions
                     if c.clinicalStatus and
                     any(cd.code == "active" for cd in c.clinicalStatus.coding))
        resolved = sum(1 for c in self.conditions
                       if c.clinicalStatus and
                       any(cd.code == "resolved" for cd in c.clinicalStatus.coding))

        # Cross-layer impact count
        cross_layer_impacts = sum(
            len(c.cross_layer_impacts) for c in self.conditions
        )

        return {
            "total_conditions": self.total_conditions,
            "active_conditions": active,
            "resolved_conditions": resolved,
            "total_medications": self.total_medications,
            "drug_interactions": self.drug_interaction_count,
            "coverage_gaps": self.coverage_gap_count,
            "avoidable_encounters": self.avoidable_encounters,
            "cross_layer_health_impacts": cross_layer_impacts,
            "has_primary_care": any(
                cp.title and "primary" in cp.title.lower()
                for cp in self.care_plans
            ),
            "has_mental_health_plan": any(
                cp.title and "mental" in cp.title.lower()
                for cp in self.care_plans
            ),
            "adherence_issues": sum(
                1 for m in self.medication_requests
                if m.adherence_status in ("partial", "non-adherent")
            ),
        }


# ── Helper: Create common FHIR codes ────────────────────────────

def icd10(code: str, display: str) -> CodeableConcept:
    """Create an ICD-10-CM coded concept."""
    return CodeableConcept(
        coding=[Coding(system=CodingSystem.ICD10.value, code=code, display=display)],
        text=display,
    )


def snomed(code: str, display: str) -> CodeableConcept:
    """Create a SNOMED CT coded concept."""
    return CodeableConcept(
        coding=[Coding(system=CodingSystem.SNOMED.value, code=code, display=display)],
        text=display,
    )


def loinc(code: str, display: str) -> CodeableConcept:
    """Create a LOINC coded concept."""
    return CodeableConcept(
        coding=[Coding(system=CodingSystem.LOINC.value, code=code, display=display)],
        text=display,
    )


def rxnorm(code: str, display: str) -> CodeableConcept:
    """Create an RxNorm coded concept."""
    return CodeableConcept(
        coding=[Coding(system=CodingSystem.RXNORM.value, code=code, display=display)],
        text=display,
    )


def condition_clinical_status(status: str) -> CodeableConcept:
    """Create a condition clinical status (active, recurrence, relapse, inactive, remission, resolved)."""
    return CodeableConcept(
        coding=[Coding(
            system=CodingSystem.FHIR_CONDITION_CLINICAL.value,
            code=status,
            display=status.title(),
        )],
    )


def condition_verification_status(status: str) -> CodeableConcept:
    """Create a condition verification status (unconfirmed, provisional, differential, confirmed, refuted)."""
    return CodeableConcept(
        coding=[Coding(
            system=CodingSystem.FHIR_CONDITION_VERIFICATION.value,
            code=status,
            display=status.title(),
        )],
    )


def patient_reference(patient_id: str, display: Optional[str] = None) -> Reference:
    """Create a reference to a Patient resource."""
    return Reference(
        reference=f"Patient/{patient_id}",
        type="Patient",
        display=display,
    )
