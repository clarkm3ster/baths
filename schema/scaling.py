"""
BATHS Gravitational Schema — Scaling Architecture

One dome is art. 100 domes is a dataset. 10,000 domes is infrastructure.

AI agents that fill layers 1-9 learn patterns across completed domes.
"Every dome for someone aging out of foster care has this gap in Layer 5.
Here's the fix from Dome 47."

Draft domes can be auto-generated for new people using patterns from completed domes.
Human creative teams then design layers 10-12 and refine everything.
Same for spheres.
"""

from datetime import datetime
from typing import Optional, Dict, List, Any, Literal
from pydantic import BaseModel, Field
import uuid

from schema.core import GameType, LayerScore


# ── Schema Pattern ──────────────────────────────────────────────

class LayerGap(BaseModel):
    """A gap found in a specific layer — and the fix that worked"""
    gap_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    layer_number: int
    layer_name: str
    gap_description: str                   # What's missing or weak
    population_tag: str                    # e.g. "aging_out_foster_care", "serial_eviction"
    frequency: float = 0.0                 # How often this gap appears (0-1)
    fix_description: str = ""              # What fixed it
    fix_source_schema_id: Optional[str] = None  # Which dome/sphere had the fix
    fix_effectiveness: float = 0.0         # 0-100


class LayerPattern(BaseModel):
    """A pattern found in a specific layer across multiple schemas"""
    pattern_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    layer_number: int
    layer_name: str
    pattern_type: str                      # "common_gap", "best_practice", "correlation", "sequence"
    description: str
    schemas_observed: int = 0              # How many schemas show this pattern
    population_tags: List[str] = Field(default_factory=list)
    confidence: float = 0.0                # 0-1
    data: Dict[str, Any] = Field(default_factory=dict)


class CrossLayerPattern(BaseModel):
    """A pattern that spans multiple layers"""
    pattern_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    layers_involved: List[int] = Field(default_factory=list)
    description: str
    correlation_type: str                  # "causal", "correlated", "sequential"
    strength: float = 0.0                  # 0-1
    population_tags: List[str] = Field(default_factory=list)
    intervention_point: Optional[int] = None  # Which layer to intervene in
    intervention_description: str = ""


class SchemaPattern(BaseModel):
    """A complete pattern extracted from multiple schemas"""
    pattern_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    schema_type: GameType
    name: str
    description: str
    population_tags: List[str] = Field(default_factory=list)  # Who this applies to
    geography_tags: List[str] = Field(default_factory=list)   # Where this applies
    layer_patterns: List[LayerPattern] = Field(default_factory=list)
    cross_layer_patterns: List[CrossLayerPattern] = Field(default_factory=list)
    gaps: List[LayerGap] = Field(default_factory=list)
    schemas_analyzed: int = 0
    confidence: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ── Pattern Library ──────────────────────────────────────────────

class PatternLibrary(BaseModel):
    """The collective intelligence of all completed schemas.

    This is what makes 10,000 domes infrastructure, not just 10,000 art pieces.
    """
    library_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    # Dome patterns
    dome_patterns: List[SchemaPattern] = Field(default_factory=list)
    dome_gaps: List[LayerGap] = Field(default_factory=list)
    total_domes_analyzed: int = 0

    # Sphere patterns
    sphere_patterns: List[SchemaPattern] = Field(default_factory=list)
    sphere_gaps: List[LayerGap] = Field(default_factory=list)
    total_spheres_analyzed: int = 0

    # Population-specific insights
    population_insights: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict)
    # e.g. {"aging_out_foster_care": [{"layer": 5, "gap": "...", "fix": "..."}]}

    # Geography-specific insights
    geography_insights: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict)

    last_updated: datetime = Field(default_factory=datetime.utcnow)

    def get_patterns_for_population(self, tag: str) -> List[SchemaPattern]:
        """Get all patterns relevant to a population tag"""
        return [p for p in self.dome_patterns if tag in p.population_tags]

    def get_gaps_for_layer(self, layer_number: int, schema_type: GameType) -> List[LayerGap]:
        """Get known gaps for a specific layer"""
        gaps = self.dome_gaps if schema_type == GameType.DOMES else self.sphere_gaps
        return [g for g in gaps if g.layer_number == layer_number]


# ── Draft Generator ─────────────────────────────────────────────

class DraftLayerSeed(BaseModel):
    """Seed data for auto-generating a layer from patterns"""
    layer_number: int
    layer_name: str
    source_patterns: List[str] = Field(default_factory=list)  # Pattern IDs used
    pre_filled_data: Dict[str, Any] = Field(default_factory=dict)
    predicted_gaps: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    requires_human_review: bool = True


class DraftSchema(BaseModel):
    """An auto-generated draft schema from pattern library.

    Layers 1-9 (dome) / 1-6 (sphere) are pre-filled from patterns.
    Human creative teams still design the upper layers.
    Everything is marked as draft and requires review.
    """
    draft_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    schema_type: GameType
    title: str
    population_tags: List[str] = Field(default_factory=list)
    geography_tags: List[str] = Field(default_factory=list)
    layer_seeds: List[DraftLayerSeed] = Field(default_factory=list)
    patterns_used: List[str] = Field(default_factory=list)  # Pattern IDs
    overall_confidence: float = 0.0
    predicted_weak_layers: List[int] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    reviewed: bool = False
    reviewer_notes: str = ""


class DraftGenerator(BaseModel):
    """Generates draft schemas from the pattern library.

    "Give me a draft dome for a single mother facing eviction in Milwaukee."
    The generator pulls patterns from every completed dome with similar tags,
    pre-fills layers 1-9, and marks where the creative team needs to design.
    """
    generator_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    pattern_library: PatternLibrary = Field(default_factory=PatternLibrary)

    def generate_dome_draft(
        self,
        population_tags: List[str],
        geography_tags: List[str],
        subject_name: str = "",
    ) -> DraftSchema:
        """Generate a draft dome from patterns.

        In production this would query the pattern library, find matching patterns,
        and pre-fill each AI-fillable layer (1-9). Layers 10-12 are left empty
        for human creative teams.
        """
        matching_patterns = []
        for tag in population_tags:
            matching_patterns.extend(
                self.pattern_library.get_patterns_for_population(tag)
            )

        layer_seeds = []
        for layer_num in range(1, 13):
            is_human = layer_num >= 10
            layer_names = {
                1: "Legal", 2: "Systems", 3: "Fiscal", 4: "Health",
                5: "Housing", 6: "Economic", 7: "Education", 8: "Community",
                9: "Environment", 10: "Autonomy", 11: "Creativity", 12: "Flourishing",
            }
            seed = DraftLayerSeed(
                layer_number=layer_num,
                layer_name=layer_names[layer_num],
                source_patterns=[p.pattern_id for p in matching_patterns
                                 if any(lp.layer_number == layer_num
                                       for lp in p.layer_patterns)],
                predicted_gaps=[
                    g.gap_description
                    for g in self.pattern_library.get_gaps_for_layer(
                        layer_num, GameType.DOMES
                    )
                    if any(t in g.population_tag for t in population_tags)
                ],
                confidence=0.0 if is_human else min(
                    len(matching_patterns) / 10.0, 1.0
                ),
                requires_human_review=True,
            )
            layer_seeds.append(seed)

        predicted_weak = [
            s.layer_number for s in layer_seeds
            if s.predicted_gaps and not s.requires_human_review
        ]

        return DraftSchema(
            schema_type=GameType.DOMES,
            title=f"Draft Dome: {subject_name}" if subject_name else "Draft Dome",
            population_tags=population_tags,
            geography_tags=geography_tags,
            layer_seeds=layer_seeds,
            patterns_used=[p.pattern_id for p in matching_patterns],
            overall_confidence=sum(s.confidence for s in layer_seeds) / len(layer_seeds),
            predicted_weak_layers=predicted_weak,
        )

    def generate_sphere_draft(
        self,
        geography_tags: List[str],
        address: str = "",
    ) -> DraftSchema:
        """Generate a draft sphere from patterns.

        Pre-fills AI layers (1-6). Leaves creative layers (7-10) for human teams.
        """
        layer_seeds = []
        for layer_num in range(1, 11):
            is_human = layer_num >= 7
            layer_names = {
                1: "Parcel", 2: "Infrastructure", 3: "Environmental",
                4: "Economic", 5: "Social", 6: "Temporal",
                7: "Activation", 8: "Permanence", 9: "Policy", 10: "Catalyst",
            }
            seed = DraftLayerSeed(
                layer_number=layer_num,
                layer_name=layer_names[layer_num],
                confidence=0.0 if is_human else min(
                    len(geography_tags) / 5.0, 1.0
                ),
                requires_human_review=True,
            )
            layer_seeds.append(seed)

        return DraftSchema(
            schema_type=GameType.SPHERES,
            title=f"Draft Sphere: {address}" if address else "Draft Sphere",
            geography_tags=geography_tags,
            layer_seeds=layer_seeds,
            overall_confidence=sum(s.confidence for s in layer_seeds) / len(layer_seeds),
        )


# ── Cross-Schema Learning ──────────────────────────────────────

class ResearchHypothesis(BaseModel):
    """A hypothesis generated by research agents from cross-schema analysis"""
    hypothesis_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    hypothesis: str
    evidence: List[str] = Field(default_factory=list)
    schemas_supporting: int = 0
    schemas_contradicting: int = 0
    layers_involved: List[int] = Field(default_factory=list)
    schema_type: GameType
    population_tags: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    status: Literal["proposed", "testing", "validated", "rejected"] = "proposed"


class CrossSchemaLearning(BaseModel):
    """The intelligence layer that learns across all schemas.

    Powers the Lab apps (domes-lab, spheres-lab).
    Research agents continuously scan literature, map findings to active schemas,
    and generate novel hypotheses.
    """
    learning_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    pattern_library: PatternLibrary = Field(default_factory=PatternLibrary)
    hypotheses: List[ResearchHypothesis] = Field(default_factory=list)

    # Literature scanning
    literature_sources: List[str] = Field(default_factory=list)
    papers_scanned: int = 0
    last_scan: Optional[datetime] = None

    # Active research questions
    research_questions: List[str] = Field(default_factory=list)

    # Findings mapped to schema layers
    layer_findings: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict)
    # e.g. {"dome_layer_4_health": [{"finding": "...", "source": "...", "implication": "..."}]}

    def add_hypothesis(self, hypothesis: str, schema_type: GameType,
                       layers: List[int], evidence: List[str]) -> ResearchHypothesis:
        """Add a new research hypothesis from cross-schema analysis"""
        h = ResearchHypothesis(
            hypothesis=hypothesis,
            evidence=evidence,
            layers_involved=layers,
            schema_type=schema_type,
        )
        self.hypotheses.append(h)
        return h
