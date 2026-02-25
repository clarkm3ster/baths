"""
BATHS Gravitational Schema — Creative Team Canvas

Layers 10-12 (DOMES) and 7-10 (SPHERES) are where the creative team works.
Each creative input is:
  - Attributed to the practitioner
  - Categorized by IP domain
  - Scored for layer completeness
  - Exportable as a deliverable
  - Renderable in the world model

Creative inputs span every discipline:
  Architectural, Sonic, Material, Narrative, Movement,
  Visual, Culinary, Philosophical, Experience design
"""

from datetime import datetime
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
import uuid

from schema.core import (
    CreativeInput,
    CreativeInputType,
    IPAttribution,
    IPDomain,
    Deliverable,
)


# ── Discipline-Specific Creative Inputs ──────────────────────────

class ArchitecturalInput(CreativeInput):
    """3D models, spatial designs, renderings"""
    input_type: CreativeInputType = CreativeInputType.ARCHITECTURAL
    mesh_format: str = ""                 # glTF, OBJ, FBX, USD
    mesh_url: Optional[str] = None
    dimensions: Dict[str, float] = Field(default_factory=dict)  # width, height, depth
    materials_list: List[str] = Field(default_factory=list)
    structural_requirements: str = ""
    accessibility_features: List[str] = Field(default_factory=list)
    environmental_integration: str = ""


class SonicInput(CreativeInput):
    """Compositions, soundscapes, acoustic specifications"""
    input_type: CreativeInputType = CreativeInputType.SONIC
    audio_format: str = ""                 # WAV, FLAC, MP3
    audio_url: Optional[str] = None
    duration_seconds: float = 0.0
    spatial_audio: bool = False            # Ambisonics, Dolby Atmos
    acoustic_specifications: Dict[str, Any] = Field(default_factory=dict)
    frequency_range: Dict[str, float] = Field(default_factory=dict)
    intended_emotional_response: str = ""


class MaterialInput(CreativeInput):
    """Textile specifications, material palettes, physical prototypes"""
    input_type: CreativeInputType = CreativeInputType.MATERIAL
    material_type: str = ""                # textile, ceramic, metal, wood, composite
    specifications: Dict[str, Any] = Field(default_factory=dict)
    color_palette: List[Dict[str, Any]] = Field(default_factory=list)
    sustainability_rating: Optional[str] = None
    sourcing: str = ""
    prototype_documented: bool = False
    prototype_images: List[str] = Field(default_factory=list)


class NarrativeInput(CreativeInput):
    """Scripts, treatments, story arcs, series bibles"""
    input_type: CreativeInputType = CreativeInputType.NARRATIVE
    narrative_format: str = ""             # script, treatment, story_arc, series_bible, poem
    word_count: int = 0
    characters: List[str] = Field(default_factory=list)
    themes: List[str] = Field(default_factory=list)
    structure: str = ""                    # three_act, episodic, nonlinear, cyclical
    medium: str = ""                       # film, theater, podcast, installation, book


class MovementInput(CreativeInput):
    """Choreographic notation, movement patterns, accessibility pathways"""
    input_type: CreativeInputType = CreativeInputType.MOVEMENT
    notation_system: str = ""              # Laban, Benesh, custom
    duration_minutes: float = 0.0
    performers_required: int = 0
    space_requirements: Dict[str, Any] = Field(default_factory=dict)
    accessibility_pathways: List[str] = Field(default_factory=list)
    body_requirements: str = ""


class VisualInput(CreativeInput):
    """Graphic systems, data visualizations as art, exhibition designs"""
    input_type: CreativeInputType = CreativeInputType.VISUAL
    visual_format: str = ""                # poster, installation, projection, interactive, mural
    dimensions_cm: Dict[str, float] = Field(default_factory=dict)
    color_system: str = ""
    data_source_layers: List[int] = Field(default_factory=list)  # Which schema layers feed this viz
    interactive: bool = False
    display_requirements: Dict[str, Any] = Field(default_factory=dict)


class CulinaryInput(CreativeInput):
    """Nutrition models, menu designs, food access plans"""
    input_type: CreativeInputType = CreativeInputType.CULINARY
    menu_items: List[Dict[str, Any]] = Field(default_factory=list)
    nutritional_model: Dict[str, Any] = Field(default_factory=dict)
    food_access_plan: str = ""
    local_sourcing: List[str] = Field(default_factory=list)
    cultural_significance: str = ""
    dietary_accommodations: List[str] = Field(default_factory=list)


class PhilosophicalInput(CreativeInput):
    """Frameworks for what flourishing means HERE"""
    input_type: CreativeInputType = CreativeInputType.PHILOSOPHICAL
    framework_name: str = ""
    core_principles: List[str] = Field(default_factory=list)
    informed_by: List[str] = Field(default_factory=list)  # Philosophical traditions, lived experience
    applied_to_layers: List[int] = Field(default_factory=list)
    measurable_outcomes: List[str] = Field(default_factory=list)


class ExperienceInput(CreativeInput):
    """Awe triggers, emotional journeys, transformation arcs"""
    input_type: CreativeInputType = CreativeInputType.EXPERIENCE
    awe_triggers: List[str] = Field(default_factory=list)
    emotional_journey: List[Dict[str, Any]] = Field(default_factory=list)  # Sequence of emotional states
    transformation_arc: str = ""
    measurement_methods: List[str] = Field(default_factory=list)  # How to measure awe/transformation
    research_basis: List[str] = Field(default_factory=list)        # Environmental psychology sources
    duration_minutes: float = 0.0
    participant_capacity: Optional[int] = None


# ── Creative Canvas ─────────────────────────────────────────────

class CreativeCanvas(BaseModel):
    """The creative team's workspace for a schema.

    This is where practitioners add their work to the human-designed layers.
    Every input is attributed, categorized, scored, and renderable.
    """
    canvas_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    schema_id: str
    schema_type: str                       # "domes" or "spheres"

    # All creative inputs organized by type
    architectural: List[ArchitecturalInput] = Field(default_factory=list)
    sonic: List[SonicInput] = Field(default_factory=list)
    material: List[MaterialInput] = Field(default_factory=list)
    narrative: List[NarrativeInput] = Field(default_factory=list)
    movement: List[MovementInput] = Field(default_factory=list)
    visual: List[VisualInput] = Field(default_factory=list)
    culinary: List[CulinaryInput] = Field(default_factory=list)
    philosophical: List[PhilosophicalInput] = Field(default_factory=list)
    experience: List[ExperienceInput] = Field(default_factory=list)

    # IP tracking
    total_ip_items: int = 0
    ip_by_domain: Dict[str, int] = Field(default_factory=dict)
    ip_by_practitioner: Dict[str, int] = Field(default_factory=dict)

    # Layer completeness from creative inputs
    layer_completeness: Dict[int, float] = Field(default_factory=dict)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def all_inputs(self) -> List[CreativeInput]:
        """All creative inputs across all types"""
        return (
            self.architectural + self.sonic + self.material +
            self.narrative + self.movement + self.visual +
            self.culinary + self.philosophical + self.experience
        )

    def inputs_for_layer(self, layer_number: int) -> List[CreativeInput]:
        """All creative inputs targeting a specific layer"""
        return [i for i in self.all_inputs() if i.layer_number == layer_number]

    def inputs_by_practitioner(self, practitioner_id: str) -> List[CreativeInput]:
        """All creative inputs from a specific practitioner"""
        return [
            i for i in self.all_inputs()
            if i.attribution and i.attribution.practitioner_id == practitioner_id
        ]

    def to_deliverables(self) -> List[Deliverable]:
        """Convert all creative inputs to exportable deliverables"""
        deliverables = []
        for inp in self.all_inputs():
            d = Deliverable(
                title=inp.title,
                description=inp.description,
                format=inp.input_type.value,
                ip_domain=inp.attribution.ip_domain if inp.attribution else None,
                data=inp.content,
                world_model_ready=inp.world_model_renderable,
                created_at=inp.created_at,
                practitioner_id=inp.attribution.practitioner_id if inp.attribution else None,
                practitioner_name=inp.attribution.practitioner_name if inp.attribution else None,
                practice=inp.attribution.practice if inp.attribution else None,
            )
            deliverables.append(d)
        return deliverables
