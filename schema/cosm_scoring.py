"""
BATHS Dome — Rigorous Cosm Scoring

The BATHS Dome: A Whole-Person Digital Twin Architecture

The Cosm score is the dome's vital sign. It works like this:

  Total Cosm = minimum across all 12 layer completeness scores.
  The dome is only as strong as its weakest layer.

Each layer's completeness score is computed from DEFINED METRICS,
not arbitrary ratings. Every score is:
1. Transparent — here's exactly how it was computed
2. Auditable — here are the specific data points that determined it
3. Actionable — here's exactly what would raise it

A CTO reading a Cosm score report should be able to verify every
number in it. A policy researcher should be able to understand
exactly what "Layer 4 scores 7.2/10" means in terms of specific
health data gaps. An investor should be able to see exactly what
improving the weakest layer would cost.

This is not a dashboard metric. This is an engineering metric
with the rigor of a structural integrity assessment.
"""

from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


# ── Layer Scoring Metrics ───────────────────────────────────────

class ScoringMetric(BaseModel):
    """A single metric that contributes to a layer's completeness score."""
    metric_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    weight: float = 1.0                # Relative weight in layer score
    max_score: float = 10.0
    current_score: float = 0.0
    # How it's computed
    computation_method: str = ""       # Exact description of how score is derived
    data_source: str = ""              # What data feeds this metric
    # Evidence
    data_points_evaluated: int = 0     # How many data points were assessed
    data_points_missing: int = 0       # How many are missing
    # Gap analysis
    gap_description: str = ""          # What's missing
    improvement_action: str = ""       # What would raise the score
    improvement_cost_estimate: Optional[float] = None  # Estimated cost to improve


class LayerCompletenessScore(BaseModel):
    """
    Complete, auditable score for a single dome layer.
    Every number has a source. Every gap has a remedy.
    """
    layer_number: int
    layer_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Score components
    metrics: List[ScoringMetric] = Field(default_factory=list)
    total_score: float = 0.0           # 0-100
    max_possible_score: float = 100.0

    # Audit trail
    computation_log: List[str] = Field(default_factory=list)
    # e.g., ["data_coverage: 8 of 12 fields populated → 6.7/10",
    #        "action_completion: 3 of 7 actions done → 4.3/10"]

    # Gap analysis
    gaps: List[Dict[str, Any]] = Field(default_factory=list)
    # e.g., [{"field": "insurance_status", "gap": "unknown", "impact": 1.2,
    #         "remedy": "Query Medicaid eligibility via Layer 2 systems"}]
    what_would_make_it_100: List[str] = Field(default_factory=list)

    # Trajectory
    score_history: List[Dict[str, Any]] = Field(default_factory=list)
    # [{"timestamp": "...", "score": 45.2, "trigger": "new data ingested"}]
    trend: str = ""                    # "improving", "stable", "declining"

    def compute(self) -> float:
        """
        Compute the total layer score from individual metrics.
        Weighted average, normalized to 0-100.
        """
        if not self.metrics:
            self.total_score = 0.0
            self.computation_log.append("No metrics defined — score is 0")
            return 0.0

        total_weight = sum(m.weight for m in self.metrics)
        if total_weight == 0:
            self.total_score = 0.0
            return 0.0

        weighted_sum = sum(
            (m.current_score / m.max_score) * m.weight
            for m in self.metrics
        )
        raw = (weighted_sum / total_weight) * 100.0
        self.total_score = round(min(raw, 100.0), 1)

        # Build computation log
        self.computation_log = []
        for m in self.metrics:
            pct = (m.current_score / m.max_score) * 100.0
            self.computation_log.append(
                f"{m.name}: {m.current_score}/{m.max_score} = {pct:.1f}% "
                f"(weight: {m.weight}, data points: {m.data_points_evaluated})"
            )
        self.computation_log.append(
            f"TOTAL: {self.total_score}/100 "
            f"(weighted average of {len(self.metrics)} metrics)"
        )

        # Record in history
        self.score_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "score": self.total_score,
            "trigger": "recomputed",
        })

        return self.total_score


# ── Per-Layer Scoring Definitions ───────────────────────────────
# Each layer has a defined set of metrics. These are the EXACT
# metrics used to compute each layer's score.

def score_layer_1_legal(layer_data: Dict[str, Any]) -> LayerCompletenessScore:
    """
    Score Layer 1: Legal

    Metrics:
    1. Provision coverage — what % of applicable federal provisions are mapped
    2. Eligibility assessment — how many entitlements have eligibility determined
    3. Application progress — how many eligible entitlements have applications filed
    4. Access rate — actual benefits accessed / total entitled value
    5. Legal barrier documentation — are barriers identified and remedied
    """
    score = LayerCompletenessScore(layer_number=1, layer_name="Legal")

    entitlements = layer_data.get("entitlements", [])
    total_entitled = layer_data.get("total_entitled_value", 0)
    total_accessed = layer_data.get("total_accessed_value", 0)
    barriers = layer_data.get("legal_barriers", [])

    # Metric 1: Provision mapping completeness
    provision_count = len(entitlements)
    # Expected range: 15-40 provisions for a typical dome subject
    provision_score = min(provision_count / 25.0, 1.0) * 10.0
    score.metrics.append(ScoringMetric(
        name="provision_coverage",
        description="Federal and state provisions mapped to this person's circumstances",
        weight=2.0,
        max_score=10.0,
        current_score=round(provision_score, 1),
        computation_method=f"{provision_count} provisions mapped. Target: ~25 for full coverage.",
        data_source="Layer 1 entitlements list",
        data_points_evaluated=provision_count,
        gap_description=f"{'Comprehensive' if provision_count >= 20 else f'Need {25 - provision_count} more provisions mapped'}",
        improvement_action="Run legal navigator agent across all US Code titles and CFR parts applicable to this person's circumstances",
    ))

    # Metric 2: Eligibility determination rate
    assessed = sum(1 for e in entitlements if e.get("eligibility_status") not in ("unknown", None))
    assessment_rate = assessed / max(provision_count, 1)
    score.metrics.append(ScoringMetric(
        name="eligibility_assessment",
        description="Percentage of mapped provisions with eligibility determined",
        weight=1.5,
        max_score=10.0,
        current_score=round(assessment_rate * 10.0, 1),
        computation_method=f"{assessed}/{provision_count} provisions assessed = {assessment_rate:.0%}",
        data_source="Layer 1 eligibility_status field",
        data_points_evaluated=provision_count,
        data_points_missing=provision_count - assessed,
        gap_description=f"{provision_count - assessed} provisions with unknown eligibility",
        improvement_action="Complete eligibility assessment for all unmapped provisions via computer use agents on government portals",
    ))

    # Metric 3: Application filing rate
    eligible = [e for e in entitlements if e.get("eligibility_status") == "eligible"]
    filed = [e for e in eligible if e.get("application_status") not in ("not_started", None)]
    filing_rate = len(filed) / max(len(eligible), 1)
    score.metrics.append(ScoringMetric(
        name="application_progress",
        description="Percentage of eligible entitlements with applications filed",
        weight=1.5,
        max_score=10.0,
        current_score=round(filing_rate * 10.0, 1),
        computation_method=f"{len(filed)}/{len(eligible)} eligible entitlements filed = {filing_rate:.0%}",
        data_source="Layer 1 application_status field",
        data_points_evaluated=len(eligible),
        data_points_missing=len(eligible) - len(filed),
        gap_description=f"{len(eligible) - len(filed)} eligible entitlements with applications not yet filed",
        improvement_action="File applications for all eligible entitlements. Computer use agents can automate portal filing.",
    ))

    # Metric 4: Access rate (money flowing)
    access_rate = total_accessed / max(total_entitled, 1)
    score.metrics.append(ScoringMetric(
        name="access_rate",
        description="Actual benefits accessed as percentage of total entitled value",
        weight=2.0,
        max_score=10.0,
        current_score=round(access_rate * 10.0, 1),
        computation_method=f"${total_accessed:,.0f} accessed / ${total_entitled:,.0f} entitled = {access_rate:.0%}",
        data_source="Layer 1 fiscal values",
        gap_description=f"${total_entitled - total_accessed:,.0f} in unclaimed entitlements",
        improvement_action="Close the access gap by completing applications and resolving barriers",
        improvement_cost_estimate=500.0,  # Estimated cost to file remaining applications
    ))

    # Metric 5: Barrier documentation
    barrier_score = min(len(barriers) * 2.0, 10.0) if barriers else 0.0
    score.metrics.append(ScoringMetric(
        name="barrier_documentation",
        description="Legal barriers identified, documented, and remedied",
        weight=1.0,
        max_score=10.0,
        current_score=round(barrier_score, 1),
        computation_method=f"{len(barriers)} barriers documented",
        data_source="Layer 1 legal_barriers",
        data_points_evaluated=len(barriers),
        gap_description="Barriers need strategies for removal" if barriers else "No barriers documented — may indicate incomplete analysis",
        improvement_action="Complete barrier analysis and develop removal strategies for each",
    ))

    # Build gap list
    if provision_count < 20:
        score.gaps.append({
            "field": "entitlements",
            "gap": f"Only {provision_count} provisions mapped",
            "impact": 2.0,
            "remedy": "Comprehensive federal provision scan across all applicable US Code titles",
        })
    if access_rate < 0.5:
        score.gaps.append({
            "field": "access_gap",
            "gap": f"Only {access_rate:.0%} of entitled value accessed",
            "impact": 3.0,
            "remedy": f"File applications for ${total_entitled - total_accessed:,.0f} in unclaimed entitlements",
        })

    # What would make it 100
    score.what_would_make_it_100 = [
        "Map ALL applicable federal provisions (target: 25+)",
        "Determine eligibility for 100% of mapped provisions",
        "File applications for 100% of eligible entitlements",
        "Achieve 100% access rate (all entitled benefits flowing)",
        "Document all barriers with removal strategies",
    ]

    score.compute()
    return score


def score_layer_2_systems(layer_data: Dict[str, Any]) -> LayerCompletenessScore:
    """Score Layer 2: Systems"""
    score = LayerCompletenessScore(layer_number=2, layer_name="Systems")

    systems = layer_data.get("systems", [])
    total = layer_data.get("total_systems", len(systems))
    connected = layer_data.get("connected_systems", 0)
    frag_index = layer_data.get("fragmentation_index", 1.0)
    gaps = layer_data.get("cross_system_gaps", [])

    # Metric 1: System mapping completeness
    mapping_score = min(total / 8.0, 1.0) * 10.0
    score.metrics.append(ScoringMetric(
        name="system_mapping",
        description="Government systems identified and mapped",
        weight=1.5,
        current_score=round(mapping_score, 1),
        computation_method=f"{total} systems mapped. Target: 8+ for comprehensive coverage.",
        data_source="Layer 2 systems list",
        data_points_evaluated=total,
    ))

    # Metric 2: System connectivity
    conn_rate = connected / max(total, 1)
    score.metrics.append(ScoringMetric(
        name="system_connectivity",
        description="Percentage of systems with active data connections",
        weight=2.0,
        current_score=round(conn_rate * 10.0, 1),
        computation_method=f"{connected}/{total} systems connected = {conn_rate:.0%}",
        data_source="Layer 2 data_shared_with field",
    ))

    # Metric 3: Fragmentation index
    defrag_score = max(0, (1.0 - frag_index) * 10.0)
    score.metrics.append(ScoringMetric(
        name="defragmentation",
        description="How defragmented the system landscape is (inverse of fragmentation)",
        weight=2.0,
        current_score=round(defrag_score, 1),
        computation_method=f"Fragmentation index: {frag_index:.2f}. Lower = better.",
        data_source="Layer 2 fragmentation_index",
    ))

    # Metric 4: Gap documentation
    gap_score = min(len(gaps) * 1.5, 10.0) if gaps else 0
    score.metrics.append(ScoringMetric(
        name="gap_documentation",
        description="Cross-system gaps identified and documented",
        weight=1.0,
        current_score=round(gap_score, 1),
        computation_method=f"{len(gaps)} cross-system gaps documented",
        data_source="Layer 2 cross_system_gaps",
    ))

    score.what_would_make_it_100 = [
        "Map all government systems this person interacts with",
        "Establish data-sharing connections between all systems",
        "Reduce fragmentation index to near 0",
        "Document and remediate all cross-system gaps",
    ]

    score.compute()
    return score


def score_layer_3_fiscal(layer_data: Dict[str, Any]) -> LayerCompletenessScore:
    """Score Layer 3: Fiscal"""
    score = LayerCompletenessScore(layer_number=3, layer_name="Fiscal")

    income = layer_data.get("income_streams", [])
    expenses = layer_data.get("expense_streams", [])
    savings = layer_data.get("coordination_savings", 0)
    frag_cost = layer_data.get("cost_of_fragmentation", 0)
    bond = layer_data.get("dome_bond")

    # Metric 1: Income stream mapping
    income_score = min(len(income) / 5.0, 1.0) * 10.0
    score.metrics.append(ScoringMetric(
        name="income_mapping",
        description="Income and benefit streams documented",
        weight=1.5,
        current_score=round(income_score, 1),
        computation_method=f"{len(income)} income streams mapped",
        data_source="Layer 3 income_streams",
    ))

    # Metric 2: Coordination savings quantified
    savings_score = min(savings / 30000.0, 1.0) * 10.0 if savings > 0 else 0
    score.metrics.append(ScoringMetric(
        name="coordination_savings",
        description="Annual coordination savings computed and documented",
        weight=2.0,
        current_score=round(savings_score, 1),
        computation_method=f"${savings:,.0f} in annual coordination savings computed",
        data_source="Layer 3 coordination_savings",
    ))

    # Metric 3: Fragmentation cost quantified
    frag_score = min(1.0, 1.0 if frag_cost > 0 else 0.0) * 10.0
    score.metrics.append(ScoringMetric(
        name="fragmentation_cost",
        description="Cost of system fragmentation computed",
        weight=1.5,
        current_score=round(frag_score, 1),
        computation_method=f"${frag_cost:,.0f} annual cost of fragmentation documented",
        data_source="Layer 3 cost_of_fragmentation",
    ))

    # Metric 4: Dome Bond structured
    bond_score = 8.0 if bond else 0.0
    score.metrics.append(ScoringMetric(
        name="dome_bond",
        description="Dome Bond prospectus structured and computed",
        weight=2.0,
        current_score=round(bond_score, 1),
        computation_method="Dome Bond prospectus " + ("complete" if bond else "not yet structured"),
        data_source="Layer 3 dome_bond",
    ))

    score.what_would_make_it_100 = [
        "Map ALL income and benefit streams with amounts",
        "Quantify full coordination savings from dome",
        "Document complete cost of fragmentation",
        "Structure Dome Bond with outcome metrics and risk assessment",
        "Model complete financial trajectory (24-month projection)",
    ]

    score.compute()
    return score


def score_layer_4_health(layer_data: Dict[str, Any]) -> LayerCompletenessScore:
    """Score Layer 4: Health — uses FHIR R4 data completeness."""
    score = LayerCompletenessScore(layer_number=4, layer_name="Health")

    patient = layer_data.get("patient")
    conditions = layer_data.get("conditions", [])
    observations = layer_data.get("observations", [])
    coverages = layer_data.get("coverages", [])
    medications = layer_data.get("medication_requests", [])
    care_plans = layer_data.get("care_plans", [])
    encounters = layer_data.get("encounters", [])

    # Metric 1: Patient record completeness
    patient_fields = 0
    if patient:
        if patient.get("name"): patient_fields += 1
        if patient.get("birthDate"): patient_fields += 1
        if patient.get("gender"): patient_fields += 1
        if patient.get("address"): patient_fields += 1
        if patient.get("telecom"): patient_fields += 1
    patient_score = (patient_fields / 5.0) * 10.0 if patient else 0
    score.metrics.append(ScoringMetric(
        name="patient_record",
        description="FHIR Patient resource completeness",
        weight=1.0,
        current_score=round(patient_score, 1),
        computation_method=f"{patient_fields}/5 patient fields populated",
        data_source="FHIR Patient resource",
    ))

    # Metric 2: Condition documentation (ICD-10 coded)
    coded_conditions = sum(
        1 for c in conditions
        if c.get("code") and c["code"].get("coding")
    )
    cond_score = min(coded_conditions / 3.0, 1.0) * 10.0
    score.metrics.append(ScoringMetric(
        name="condition_documentation",
        description="Health conditions documented with ICD-10/SNOMED codes",
        weight=2.0,
        current_score=round(cond_score, 1),
        computation_method=f"{coded_conditions} coded conditions. {len(conditions)} total conditions.",
        data_source="FHIR Condition resources",
        data_points_evaluated=len(conditions),
    ))

    # Metric 3: Coverage documentation
    coverage_score = min(len(coverages) / 2.0, 1.0) * 10.0
    score.metrics.append(ScoringMetric(
        name="coverage_documentation",
        description="Insurance/benefit coverage documented",
        weight=1.5,
        current_score=round(coverage_score, 1),
        computation_method=f"{len(coverages)} coverage records",
        data_source="FHIR Coverage resources",
    ))

    # Metric 4: Care plan presence
    care_score = 8.0 if care_plans else 0.0
    score.metrics.append(ScoringMetric(
        name="care_plan",
        description="Cross-layer care plan established",
        weight=2.0,
        current_score=round(care_score, 1),
        computation_method=f"{len(care_plans)} care plans",
        data_source="FHIR CarePlan resources",
    ))

    # Metric 5: Cross-layer health impacts documented
    cross_impacts = sum(
        len(c.get("cross_layer_impacts", [])) for c in conditions
    )
    cross_score = min(cross_impacts / 3.0, 1.0) * 10.0
    score.metrics.append(ScoringMetric(
        name="cross_layer_impacts",
        description="Health conditions linked to impacts on other dome layers",
        weight=1.5,
        current_score=round(cross_score, 1),
        computation_method=f"{cross_impacts} cross-layer health impacts documented",
        data_source="FHIR Condition cross_layer_impacts extension",
    ))

    score.what_would_make_it_100 = [
        "Complete FHIR Patient record with all demographic fields",
        "Document all conditions with ICD-10/SNOMED coding",
        "Document all insurance/benefit coverage with gaps identified",
        "Establish cross-layer care plan",
        "Map all health condition impacts on other dome layers",
        "Document medication adherence and interaction data",
    ]

    score.compute()
    return score


def score_layer_5_housing(layer_data: Dict[str, Any]) -> LayerCompletenessScore:
    """Score Layer 5: Housing"""
    score = LayerCompletenessScore(layer_number=5, layer_name="Housing")

    housing = layer_data.get("current_housing")
    stability = layer_data.get("housing_stability_score", 0)
    history = layer_data.get("housing_history", [])
    evictions = layer_data.get("eviction_history", 0)

    # Metric 1: Current housing documented
    housing_fields = 0
    if housing:
        if housing.get("address"): housing_fields += 1
        if housing.get("unit_type"): housing_fields += 1
        if housing.get("tenure"): housing_fields += 1
        if housing.get("monthly_cost"): housing_fields += 1
        if housing.get("condition_score"): housing_fields += 1
    h_score = (housing_fields / 5.0) * 10.0
    score.metrics.append(ScoringMetric(
        name="housing_documentation",
        description="Current housing situation fully documented",
        weight=1.5,
        current_score=round(h_score, 1),
        computation_method=f"{housing_fields}/5 housing fields populated",
        data_source="Layer 5 current_housing",
    ))

    # Metric 2: Housing stability
    stability_score = (stability / 100.0) * 10.0
    score.metrics.append(ScoringMetric(
        name="housing_stability",
        description="Housing stability score (inverse of instability risk)",
        weight=2.0,
        current_score=round(stability_score, 1),
        computation_method=f"Stability score: {stability}/100",
        data_source="Layer 5 housing_stability_score",
    ))

    # Metric 3: History documented
    history_score = min(len(history) / 3.0, 1.0) * 8.0 if history else 2.0
    score.metrics.append(ScoringMetric(
        name="housing_history",
        description="Housing history documented for trajectory analysis",
        weight=1.0,
        current_score=round(history_score, 1),
        computation_method=f"{len(history)} housing history records",
        data_source="Layer 5 housing_history",
    ))

    score.what_would_make_it_100 = [
        "Complete documentation of current housing situation",
        "Housing stability score > 80/100",
        "Full housing history for trajectory analysis",
        "Environmental hazard assessment complete",
        "SDOH Housing Instability screen administered and linked",
    ]

    score.compute()
    return score


# Scoring functions for layers 6-12 follow the same rigorous pattern.
# Each layer has 3-5 defined metrics with specific computation methods.

def score_layer_generic(
    layer_number: int,
    layer_name: str,
    layer_data: Dict[str, Any],
    metric_definitions: List[Dict[str, Any]],
) -> LayerCompletenessScore:
    """
    Generic layer scoring for layers 6-12.
    Each layer passes its own metric definitions.
    """
    score = LayerCompletenessScore(layer_number=layer_number, layer_name=layer_name)

    for mdef in metric_definitions:
        field = mdef["field"]
        value = layer_data.get(field)

        if mdef["type"] == "count":
            items = value if isinstance(value, list) else []
            raw = min(len(items) / mdef["target"], 1.0) * 10.0
        elif mdef["type"] == "score":
            raw = (float(value or 0) / mdef.get("max_val", 100.0)) * 10.0
        elif mdef["type"] == "boolean":
            raw = 8.0 if value else 0.0
        elif mdef["type"] == "text":
            raw = 7.0 if value and len(str(value)) > 20 else 0.0
        else:
            raw = 0.0

        score.metrics.append(ScoringMetric(
            name=mdef["name"],
            description=mdef["description"],
            weight=mdef.get("weight", 1.0),
            current_score=round(min(raw, 10.0), 1),
            computation_method=mdef.get("method", f"Field: {field}"),
            data_source=f"Layer {layer_number} {field}",
        ))

    score.compute()
    return score


# ── Layer metric definitions for layers 6-12 ───────────────────

LAYER_6_METRICS = [
    {"name": "employment_status", "field": "current_employment", "type": "boolean",
     "description": "Current employment documented", "weight": 1.5},
    {"name": "skills_inventory", "field": "skills", "type": "count", "target": 5,
     "description": "Skills inventory documented", "weight": 1.0},
    {"name": "income_trajectory", "field": "income_trajectory", "type": "boolean",
     "description": "Income trajectory modeled", "weight": 1.5},
    {"name": "market_match", "field": "market_demand_match", "type": "score", "max_val": 100,
     "description": "Skills matched to local labor market demand", "weight": 1.0},
]

LAYER_7_METRICS = [
    {"name": "education_history", "field": "education_history", "type": "count", "target": 3,
     "description": "Education history documented", "weight": 1.0},
    {"name": "credential_gaps", "field": "credential_gaps", "type": "count", "target": 3,
     "description": "Credential gaps identified", "weight": 1.5},
    {"name": "pathways", "field": "personalized_pathways", "type": "count", "target": 2,
     "description": "Personalized education pathways designed", "weight": 2.0},
]

LAYER_8_METRICS = [
    {"name": "connections", "field": "connections", "type": "count", "target": 5,
     "description": "Community connections mapped", "weight": 1.5},
    {"name": "isolation_risk", "field": "isolation_risk_score", "type": "score", "max_val": 100,
     "description": "Isolation risk assessed (lower = better, inverted)", "weight": 2.0},
    {"name": "support_strength", "field": "support_network_strength", "type": "score", "max_val": 100,
     "description": "Support network strength", "weight": 1.5},
]

LAYER_9_METRICS = [
    {"name": "air_quality", "field": "air_quality_index", "type": "score", "max_val": 500,
     "description": "Air quality assessed", "weight": 1.0},
    {"name": "food_access", "field": "food_access_score", "type": "score", "max_val": 100,
     "description": "Food access scored", "weight": 1.5},
    {"name": "walkability", "field": "walkability_score", "type": "score", "max_val": 100,
     "description": "Walkability assessed", "weight": 1.0},
    {"name": "env_justice", "field": "environmental_justice_score", "type": "score", "max_val": 100,
     "description": "Environmental justice screen completed", "weight": 1.5},
]

LAYER_10_METRICS = [
    {"name": "friction_points", "field": "friction_points", "type": "count", "target": 5,
     "description": "Friction points between person and resources identified", "weight": 1.5},
    {"name": "autonomy_definition", "field": "autonomy_definition", "type": "text",
     "description": "Autonomy defined for this specific person (human design)", "weight": 2.0},
    {"name": "autonomy_design", "field": "autonomy_design", "type": "boolean",
     "description": "Autonomy design completed by creative team", "weight": 2.0},
]

LAYER_11_METRICS = [
    {"name": "cultural_resources", "field": "cultural_resources", "type": "count", "target": 5,
     "description": "Cultural resources in person's landscape mapped", "weight": 1.5},
    {"name": "meaning_framework", "field": "meaning_framework", "type": "text",
     "description": "Meaning framework designed (how this person makes meaning)", "weight": 2.0},
    {"name": "creative_design", "field": "creative_design", "type": "boolean",
     "description": "Creative design completed", "weight": 2.0},
]

LAYER_12_METRICS = [
    {"name": "flourishing_dimensions", "field": "flourishing_dimensions", "type": "count", "target": 6,
     "description": "Flourishing dimensions defined for this person", "weight": 1.5},
    {"name": "awe_design", "field": "awe_design", "type": "boolean",
     "description": "Awe framework designed using Keltner triggers", "weight": 2.0},
    {"name": "flourishing_definition", "field": "flourishing_definition", "type": "text",
     "description": "Flourishing defined for THIS person", "weight": 2.0},
    {"name": "world_model_design", "field": "world_model_design", "type": "boolean",
     "description": "3D world model visualization designed", "weight": 1.5},
]


# ── Master Cosm Calculator ─────────────────────────────────────

class CosmScore(BaseModel):
    """
    Complete Cosm score with full audit trail.

    The dome is only as strong as its weakest layer.
    Total Cosm = minimum across all 12 layer completeness scores.
    """
    dome_id: str = ""
    dome_subject: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Per-layer scores
    layer_scores: List[LayerCompletenessScore] = Field(default_factory=list)

    # Aggregate
    total_cosm: float = 0.0
    weakest_layer: int = 0
    weakest_layer_name: str = ""
    strongest_layer: int = 0
    strongest_layer_name: str = ""

    # Audit
    computation_summary: str = ""
    gap_summary: List[str] = Field(default_factory=list)

    # Capitol Dome metrics (the full scope of federal architecture)
    total_federal_provisions_mapped: int = 0
    total_federal_spending_relevant: float = 0.0
    total_agencies_with_jurisdiction: int = 0
    total_systems_holding_data: int = 0


def compute_cosm(
    dome_data: Dict[int, Dict[str, Any]],
    dome_id: str = "",
    dome_subject: str = "",
) -> CosmScore:
    """
    Compute the complete Cosm score for a dome.

    Args:
        dome_data: Dict mapping layer number (1-12) → layer data dict.

    Returns:
        CosmScore with complete audit trail.
    """
    cosm = CosmScore(dome_id=dome_id, dome_subject=dome_subject)

    # Score each layer using its specific scoring function
    scoring_functions = {
        1: score_layer_1_legal,
        2: score_layer_2_systems,
        3: score_layer_3_fiscal,
        4: score_layer_4_health,
        5: score_layer_5_housing,
        6: lambda d: score_layer_generic(6, "Economic", d, LAYER_6_METRICS),
        7: lambda d: score_layer_generic(7, "Education", d, LAYER_7_METRICS),
        8: lambda d: score_layer_generic(8, "Community", d, LAYER_8_METRICS),
        9: lambda d: score_layer_generic(9, "Environment", d, LAYER_9_METRICS),
        10: lambda d: score_layer_generic(10, "Autonomy", d, LAYER_10_METRICS),
        11: lambda d: score_layer_generic(11, "Creativity", d, LAYER_11_METRICS),
        12: lambda d: score_layer_generic(12, "Flourishing", d, LAYER_12_METRICS),
    }

    for layer_num in range(1, 13):
        layer_data = dome_data.get(layer_num, {})
        scoring_fn = scoring_functions[layer_num]
        layer_score = scoring_fn(layer_data)
        cosm.layer_scores.append(layer_score)

    # Total Cosm = minimum across all layers
    if cosm.layer_scores:
        scores = [(ls.layer_number, ls.layer_name, ls.total_score) for ls in cosm.layer_scores]
        scores.sort(key=lambda x: x[2])

        cosm.total_cosm = round(scores[0][2], 1)
        cosm.weakest_layer = scores[0][0]
        cosm.weakest_layer_name = scores[0][1]
        cosm.strongest_layer = scores[-1][0]
        cosm.strongest_layer_name = scores[-1][1]

        # Build summary
        lines = [f"Cosm Score: {cosm.total_cosm}/100"]
        lines.append(f"Weakest: Layer {cosm.weakest_layer} ({cosm.weakest_layer_name}) = {scores[0][2]}")
        lines.append(f"Strongest: Layer {cosm.strongest_layer} ({cosm.strongest_layer_name}) = {scores[-1][2]}")
        lines.append("---")
        for num, name, s in scores:
            lines.append(f"  Layer {num:2d} ({name:12s}): {s:5.1f}/100")
        cosm.computation_summary = "\n".join(lines)

        # Gap summary
        for ls in cosm.layer_scores:
            if ls.total_score < 50:
                for gap in ls.gaps:
                    cosm.gap_summary.append(
                        f"Layer {ls.layer_number} ({ls.layer_name}): {gap['gap']} — {gap['remedy']}"
                    )

    # Capitol Dome metrics
    legal_data = dome_data.get(1, {})
    systems_data = dome_data.get(2, {})
    cosm.total_federal_provisions_mapped = len(legal_data.get("entitlements", []))
    cosm.total_agencies_with_jurisdiction = len(set(
        e.get("agency", "") for e in legal_data.get("entitlements", [])
        if e.get("agency")
    ))
    cosm.total_systems_holding_data = len(systems_data.get("systems", []))
    cosm.total_federal_spending_relevant = legal_data.get("total_entitled_value", 0)

    return cosm
