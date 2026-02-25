"""
BATHS Gravitational Schema — Integration Bridge

Everything is one architecture:
  - The games are schema editors
  - The portfolio sites are schema readers
  - The talent agent is a schema matchmaker
  - The AI agents are schema fillers
  - The creative teams are schema designers
  - The world model is the schema renderer

This module bridges the gravitational schema to every existing app.
"""

from datetime import datetime
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
import json
import uuid

from schema.core import (
    GameType, ProductionStage, IPDomain,
    LayerInterface, IngestInterface, ProcessInterface,
    StateInterface, ActInterface, ExportInterface,
    DataSource, DataModality, IngestMode,
    Deliverable, LayerScore, SchemaMetadata,
    TemporalState, TemporalEntry,
)
from schema.dome import (
    DomeSchema, DomeSubject, DomeLegalLayer,
    DomeSystemsLayer, DomeFiscalLayer, DomeBond,
    DOME_LAYER_DEFINITIONS,
)
from schema.sphere import (
    SphereSchema, SphereSubject, SphereParcelLayer,
    SphereEconomicLayer, ChronBond,
    SPHERE_LAYER_DEFINITIONS,
)
from schema.world_model import (
    WorldModelFormat, DomeWorldModel, SphereWorldModel,
    LayerVisualization, Color, Vector3,
)
from schema.creative import CreativeCanvas


# ── Conversion: Production JSON → Gravitational Schema ──────────

def production_json_to_dome_schema(production_data: Dict[str, Any]) -> DomeSchema:
    """Convert existing production JSON (from talent-agent) to a DomeSchema.

    This bridges the current production data format into the gravitational architecture.
    The production's stage_log deliverables map to layer interfaces.
    """
    project = production_data.get("project", {})
    character = project.get("character", {})

    # Build subject
    subject = DomeSubject(
        name=character.get("name", ""),
        source=character.get("source", ""),
        source_citation=character.get("source_citation", ""),
        situation=character.get("situation", ""),
        full_landscape=character.get("full_landscape", ""),
        production_challenge=character.get("production_challenge", ""),
        key_systems=character.get("key_systems", []),
        flourishing_dimensions=character.get("flourishing_dimensions", []),
    )

    # Create schema
    dome = DomeSchema(
        metadata=SchemaMetadata(
            schema_type=GameType.DOMES,
            title=project.get("title", ""),
            project_id=project.get("project_id", ""),
            status="completed" if production_data.get("status") == "completed" else "active",
        ),
        subject=subject,
    )

    # Map stage_log deliverables to layers
    stage_log = project.get("stage_log", [])
    _map_deliverables_to_dome_layers(dome, stage_log)

    # Score each layer based on mapped content
    _score_dome_layers(dome)

    return dome


def _map_deliverables_to_dome_layers(dome: DomeSchema, stage_log: List[Dict]) -> None:
    """Map production deliverables to their appropriate dome layers."""
    # Capability → layer mapping
    capability_to_layer = {
        "legal_navigation": 1,   # Legal
        "data_systems": 2,       # Systems (also feeds Fiscal)
        "narrative": 12,         # Flourishing (narrative is integrative)
        "flourishing_design": 12, # Flourishing
    }

    # IP domain → layer mapping
    domain_to_layer = {
        "policy": 1,
        "technology": 2,
        "financial_product": 3,
        "healthcare": 4,
        "housing": 5,
        "entertainment": 11,     # Creativity
        "research": 9,
        "architectural": 12,
        "performance": 11,
        "culinary": 11,
    }

    for stage_entry in stage_log:
        stage = stage_entry.get("stage", "")
        deliverables = stage_entry.get("deliverables", [])
        ip_generated = stage_entry.get("ip_generated", [])

        for deliv in deliverables:
            cap = deliv.get("capability", "")
            ip_domain = deliv.get("ip_domain", "")

            # Determine target layer
            layer_num = capability_to_layer.get(cap)
            if not layer_num:
                layer_num = domain_to_layer.get(ip_domain, 12)

            layer = dome.get_layer(layer_num)

            # Add as deliverable to the layer's export interface
            export_deliv = Deliverable(
                title=deliv.get("title", ""),
                description=deliv.get("description", ""),
                format=deliv.get("ip_domain", ""),
                ip_domain=IPDomain(ip_domain) if ip_domain in IPDomain.__members__.values() else None,
                data={
                    "stage": stage,
                    "capability": cap,
                    "is_unlikely": deliv.get("is_unlikely", False),
                    "work_referenced": deliv.get("work_referenced", []),
                },
                practitioner_id=deliv.get("talent_id"),
                practitioner_name=deliv.get("talent_name"),
                practice=deliv.get("practice"),
            )
            layer.interfaces.export.deliverables.append(export_deliv)

            # Add data source to ingest
            source = DataSource(
                name=f"{deliv.get('talent_name', 'Unknown')} - {stage}",
                modality=DataModality.UNSTRUCTURED,
                mode=IngestMode.MANUAL_ENTRY,
            )
            layer.interfaces.ingest.sources.append(source)
            layer.interfaces.ingest.total_records += 1


def _score_dome_layers(dome: DomeSchema) -> None:
    """Score each dome layer based on content."""
    for i, layer in enumerate(dome.all_layers(), 1):
        deliverable_count = len(layer.interfaces.export.deliverables)
        source_count = len(layer.interfaces.ingest.sources)

        # Simple completeness based on content presence
        completeness = min(deliverable_count * 15.0, 100.0)
        quality = min(deliverable_count * 12.0, 100.0)
        coverage = sum([
            25 if source_count > 0 else 0,          # Ingest active
            25 if deliverable_count > 0 else 0,      # Export active
            25 if layer.interfaces.state.current else 0,  # State populated
            25 if layer.interfaces.act.actions else 0,     # Actions available
        ])

        layer.score = LayerScore(
            layer_number=i,
            layer_name=layer.layer_name,
            completeness=completeness,
            quality=quality,
            coverage=coverage,
        )

    # Update metadata total score
    dome.metadata.total_score = dome.total_score()
    dome.metadata.layer_scores = [l.score for l in dome.all_layers()]


def production_json_to_sphere_schema(production_data: Dict[str, Any]) -> SphereSchema:
    """Convert existing production JSON to a SphereSchema."""
    project = production_data.get("project", {})
    parcel = project.get("parcel", project.get("character", {}))

    subject = SphereSubject(
        address=parcel.get("address", ""),
        neighborhood=parcel.get("neighborhood", ""),
        city=parcel.get("city", ""),
        lot_size_sqft=parcel.get("lot_size_sqft", 0.0),
        history=parcel.get("history", ""),
        opportunity=parcel.get("opportunity", ""),
        community_context=parcel.get("community_context", ""),
        constraints=parcel.get("constraints", []),
    )

    sphere = SphereSchema(
        metadata=SchemaMetadata(
            schema_type=GameType.SPHERES,
            title=project.get("title", ""),
            project_id=project.get("project_id", ""),
            status="completed" if production_data.get("status") == "completed" else "active",
        ),
        subject=subject,
    )

    stage_log = project.get("stage_log", [])
    _map_deliverables_to_sphere_layers(sphere, stage_log)
    _score_sphere_layers(sphere)

    return sphere


def _map_deliverables_to_sphere_layers(sphere: SphereSchema, stage_log: List[Dict]) -> None:
    """Map production deliverables to sphere layers."""
    capability_to_layer = {
        "spatial_legal": 1,      # Parcel
        "economics": 4,          # Economic
        "activation_design": 7,  # Activation
        "narrative": 7,          # Activation (narrative drives experience)
    }

    domain_to_layer = {
        "policy": 9,
        "real_estate": 1,
        "urban_design": 2,
        "architectural": 8,      # Permanence
        "environmental": 3,
        "entertainment": 7,
        "technology": 2,
        "financial_product": 4,
    }

    for stage_entry in stage_log:
        stage = stage_entry.get("stage", "")
        deliverables = stage_entry.get("deliverables", [])

        for deliv in deliverables:
            cap = deliv.get("capability", "")
            ip_domain = deliv.get("ip_domain", "")

            layer_num = capability_to_layer.get(cap)
            if not layer_num:
                layer_num = domain_to_layer.get(ip_domain, 7)

            layer = sphere.get_layer(layer_num)

            export_deliv = Deliverable(
                title=deliv.get("title", ""),
                description=deliv.get("description", ""),
                format=deliv.get("ip_domain", ""),
                data={
                    "stage": stage,
                    "capability": cap,
                    "is_unlikely": deliv.get("is_unlikely", False),
                    "work_referenced": deliv.get("work_referenced", []),
                },
                practitioner_id=deliv.get("talent_id"),
                practitioner_name=deliv.get("talent_name"),
                practice=deliv.get("practice"),
            )
            layer.interfaces.export.deliverables.append(export_deliv)
            layer.interfaces.ingest.total_records += 1


def _score_sphere_layers(sphere: SphereSchema) -> None:
    """Score each sphere layer."""
    for i, layer in enumerate(sphere.all_layers(), 1):
        deliverable_count = len(layer.interfaces.export.deliverables)
        completeness = min(deliverable_count * 15.0, 100.0)

        layer.score = LayerScore(
            layer_number=i,
            layer_name=layer.layer_name,
            completeness=completeness,
            quality=min(deliverable_count * 12.0, 100.0),
            coverage=min(deliverable_count * 20.0, 100.0),
        )

    sphere.metadata.total_score = sphere.total_score()
    sphere.metadata.layer_scores = [l.score for l in sphere.all_layers()]


# ── World Model Generation ─────────────────────────────────────

# Color palette for dome layers (inner to outer)
DOME_LAYER_COLORS = {
    1: Color(r=0.2, g=0.4, b=0.8, hex="#3366CC"),     # Legal — blue
    2: Color(r=0.3, g=0.5, b=0.7, hex="#4D80B3"),     # Systems — steel blue
    3: Color(r=0.1, g=0.6, b=0.3, hex="#1A993D"),     # Fiscal — green
    4: Color(r=0.8, g=0.2, b=0.2, hex="#CC3333"),     # Health — red
    5: Color(r=0.6, g=0.4, b=0.2, hex="#996633"),     # Housing — brown
    6: Color(r=0.9, g=0.6, b=0.1, hex="#E6991A"),     # Economic — amber
    7: Color(r=0.5, g=0.3, b=0.7, hex="#804DB3"),     # Education — purple
    8: Color(r=0.2, g=0.7, b=0.6, hex="#33B399"),     # Community — teal
    9: Color(r=0.3, g=0.7, b=0.3, hex="#4DB34D"),     # Environment — green
    10: Color(r=0.9, g=0.4, b=0.6, hex="#E66699"),    # Autonomy — pink
    11: Color(r=0.8, g=0.5, b=0.9, hex="#CC80E6"),    # Creativity — lavender
    12: Color(r=1.0, g=0.8, b=0.2, hex="#FFCC33"),    # Flourishing — gold
}

SPHERE_LAYER_COLORS = {
    1: Color(r=0.4, g=0.3, b=0.2, hex="#664D33"),     # Parcel — earth
    2: Color(r=0.5, g=0.5, b=0.5, hex="#808080"),     # Infrastructure — gray
    3: Color(r=0.2, g=0.6, b=0.2, hex="#339933"),     # Environmental — green
    4: Color(r=0.1, g=0.5, b=0.3, hex="#1A804D"),     # Economic — dark green
    5: Color(r=0.7, g=0.4, b=0.2, hex="#B36633"),     # Social — warm brown
    6: Color(r=0.5, g=0.3, b=0.6, hex="#804D99"),     # Temporal — purple
    7: Color(r=1.0, g=0.5, b=0.0, hex="#FF8000"),     # Activation — orange
    8: Color(r=0.6, g=0.6, b=0.4, hex="#999966"),     # Permanence — olive
    9: Color(r=0.2, g=0.4, b=0.8, hex="#3366CC"),     # Policy — blue
    10: Color(r=0.9, g=0.3, b=0.3, hex="#E64D4D"),    # Catalyst — red
}


def dome_schema_to_world_model(dome: DomeSchema) -> DomeWorldModel:
    """Generate a world model from a completed dome schema."""
    layers_viz = []
    for i in range(1, 13):
        layer = dome.get_layer(i)
        color = DOME_LAYER_COLORS.get(i, Color())

        viz = LayerVisualization(
            layer_number=i,
            layer_name=layer.layer_name,
            geometry_type="sphere_shell",
            radius_inner=10.0 + (i - 1) * 8.0,
            radius_outer=10.0 + i * 8.0,
            opacity=0.3 + (layer.score.completeness / 100.0) * 0.5,
            color=color,
            completeness=layer.score.completeness,
            density=layer.score.completeness / 100.0,
            data_points=[
                {"type": "deliverable", "title": d.title}
                for d in layer.interfaces.export.deliverables[:10]
            ],
        )
        layers_viz.append(viz)

    weakest = dome.weakest_layer()

    fmt = WorldModelFormat(
        schema_type=GameType.DOMES,
        schema_id=dome.metadata.schema_id,
        title=dome.metadata.title,
        scene_type="dome",
        layers=layers_viz,
    )

    return DomeWorldModel(
        schema_id=dome.metadata.schema_id,
        subject_name=dome.subject.name,
        format=fmt,
        weakest_layer=weakest.layer_number,
        total_cosm=dome.metadata.total_score,
    )


def sphere_schema_to_world_model(sphere: SphereSchema) -> SphereWorldModel:
    """Generate a world model from a completed sphere schema."""
    layers_viz = []
    for i in range(1, 11):
        layer = sphere.get_layer(i)
        color = SPHERE_LAYER_COLORS.get(i, Color())

        viz = LayerVisualization(
            layer_number=i,
            layer_name=layer.layer_name,
            geometry_type="sphere_shell",
            radius_inner=5.0 + (i - 1) * 5.0,
            radius_outer=5.0 + i * 5.0,
            opacity=0.3 + (layer.score.completeness / 100.0) * 0.5,
            color=color,
            completeness=layer.score.completeness,
            density=layer.score.completeness / 100.0,
        )
        layers_viz.append(viz)

    weakest = sphere.weakest_layer()

    fmt = WorldModelFormat(
        schema_type=GameType.SPHERES,
        schema_id=sphere.metadata.schema_id,
        title=sphere.metadata.title,
        scene_type="sphere",
        layers=layers_viz,
    )

    coords = sphere.subject.coordinates
    geo_coords = None
    if coords:
        from schema.world_model import GeoCoordinate
        geo_coords = [GeoCoordinate(
            latitude=coords.get("lat", 0),
            longitude=coords.get("lng", 0),
        )]

    return SphereWorldModel(
        schema_id=sphere.metadata.schema_id,
        address=sphere.subject.address,
        format=fmt,
        weakest_layer=weakest.layer_number,
        total_chron=sphere.metadata.total_score,
        parcel_outline=geo_coords or [],
    )


# ── Talent Agent Integration ───────────────────────────────────

class SchemaMatchRequest(BaseModel):
    """Request for talent agent to match a team to a schema"""
    schema_id: str
    schema_type: GameType
    target_layers: List[int] = Field(default_factory=list)  # Which layers need work
    capability_gaps: List[str] = Field(default_factory=list)  # What's missing
    creative_disciplines_needed: List[str] = Field(default_factory=list)


class SchemaMatchResult(BaseModel):
    """Talent agent's recommended team for a schema"""
    schema_id: str
    recommended_talent: List[Dict[str, Any]] = Field(default_factory=list)
    layer_assignments: Dict[int, List[str]] = Field(default_factory=dict)  # Layer → talent IDs
    coverage_score: float = 0.0
    creative_coverage: Dict[str, bool] = Field(default_factory=dict)


def schema_to_match_request(
    schema: Any,  # DomeSchema or SphereSchema
) -> SchemaMatchRequest:
    """Analyze a schema and generate a match request for the talent agent.

    Identifies which layers are weak and what capabilities are needed.
    """
    layers = schema.all_layers()
    weak_layers = [l for l in layers if l.score.completeness < 50.0]
    human_layers = schema.human_design_layers()

    target_layers = [l.layer_number for l in weak_layers]
    capability_gaps = []
    creative_needs = []

    # Check AI-fillable layers for gaps
    for layer in schema.ai_fillable_layers():
        if layer.score.completeness < 50:
            # Find the layer definition to know what capabilities are needed
            defs = DOME_LAYER_DEFINITIONS if schema.metadata.schema_type == GameType.DOMES else SPHERE_LAYER_DEFINITIONS
            layer_def = next((d for d in defs if d.layer_number == layer.layer_number), None)
            if layer_def:
                for cap in layer_def.ai_capability_map.capabilities:
                    capability_gaps.append(cap.name)

    # Check human-designed layers
    for layer in human_layers:
        if layer.score.completeness < 50:
            creative_needs.append(layer.layer_name)

    return SchemaMatchRequest(
        schema_id=schema.metadata.schema_id,
        schema_type=schema.metadata.schema_type,
        target_layers=target_layers,
        capability_gaps=capability_gaps,
        creative_disciplines_needed=creative_needs,
    )


# ── Schema Export/Import ────────────────────────────────────────

def schema_to_json(schema: Any) -> str:
    """Export a schema (Dome or Sphere) to JSON."""
    return schema.model_dump_json(indent=2)


def dome_from_json(json_str: str) -> DomeSchema:
    """Import a DomeSchema from JSON."""
    return DomeSchema.model_validate_json(json_str)


def sphere_from_json(json_str: str) -> SphereSchema:
    """Import a SphereSchema from JSON."""
    return SphereSchema.model_validate_json(json_str)
