"""
BATHS Gravitational Schema — World Model

When world model APIs (Google Genie, DeepMind, or equivalent) become available:
- A complete DOME renders as a navigable 3D environment representing one person's life
- A complete SPHERE renders as a navigable simulation of the place

For now: Three.js/Cesium for basic 3D visualization.
The data format is the same regardless of renderer.
"""

from datetime import datetime
from typing import Optional, Dict, List, Any, Literal
from pydantic import BaseModel, Field
import uuid

from schema.core import GameType


# ── Spatial Primitives ───────────────────────────────────────────

class Vector3(BaseModel):
    """3D position/direction"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


class BoundingBox(BaseModel):
    """Axis-aligned bounding box"""
    min: Vector3 = Field(default_factory=Vector3)
    max: Vector3 = Field(default_factory=Vector3)


class GeoCoordinate(BaseModel):
    """Geographic coordinate for Cesium/globe rendering"""
    latitude: float
    longitude: float
    altitude: float = 0.0


class Color(BaseModel):
    """Color with optional opacity"""
    r: float = 1.0
    g: float = 1.0
    b: float = 1.0
    a: float = 1.0
    hex: Optional[str] = None


# ── Layer Visualization ─────────────────────────────────────────

class LayerVisualization(BaseModel):
    """How a single layer renders in the world model"""
    layer_number: int
    layer_name: str
    # Geometry
    geometry_type: str = "sphere_shell"    # sphere_shell, terrain, volume, particles, mesh
    radius_inner: float = 0.0             # For shell geometry
    radius_outer: float = 0.0
    opacity: float = 0.8
    color: Color = Field(default_factory=Color)
    # Completeness drives visual density
    completeness: float = 0.0              # 0-100, from layer score
    density: float = 0.0                   # Visual density derived from completeness
    # Data points rendered as objects within the layer
    data_points: List[Dict[str, Any]] = Field(default_factory=list)
    # Connections to other layers (rendered as edges/bridges)
    connections: List[Dict[str, Any]] = Field(default_factory=list)
    # Annotations
    labels: List[Dict[str, Any]] = Field(default_factory=list)
    # Human-designed creative content (layers 10-12 dome, 7-10 sphere)
    creative_meshes: List[Dict[str, Any]] = Field(default_factory=list)  # 3D model references
    creative_textures: List[str] = Field(default_factory=list)           # Texture paths
    creative_audio: List[str] = Field(default_factory=list)              # Audio asset paths


class TemporalKeyframe(BaseModel):
    """A keyframe in the temporal visualization"""
    timestamp: datetime
    label: str
    layer_states: Dict[int, float] = Field(default_factory=dict)  # Layer num → completeness
    total_score: float = 0.0
    event: Optional[str] = None
    camera_position: Optional[Vector3] = None


class TemporalVisualization(BaseModel):
    """How the time dimension renders"""
    keyframes: List[TemporalKeyframe] = Field(default_factory=list)
    playback_speed: float = 1.0
    loop: bool = False
    timeline_start: Optional[datetime] = None
    timeline_end: Optional[datetime] = None


# ── World Model Format ──────────────────────────────────────────

class WorldModelFormat(BaseModel):
    """Universal world model format — same structure for any renderer.

    Three.js reads this today.
    Cesium reads this for geospatial context.
    Genie/DeepMind reads this tomorrow.
    The format doesn't change — the renderer does.
    """
    format_version: str = "1.0"
    schema_type: GameType
    schema_id: str
    title: str

    # Scene setup
    scene_type: Literal["dome", "sphere"] = "dome"
    center: Vector3 = Field(default_factory=Vector3)
    geo_center: Optional[GeoCoordinate] = None  # For geospatial rendering
    bounds: BoundingBox = Field(default_factory=BoundingBox)
    ambient_color: Color = Field(default_factory=Color)

    # Layers as concentric visualization elements
    layers: List[LayerVisualization] = Field(default_factory=list)

    # Temporal
    temporal: TemporalVisualization = Field(default_factory=TemporalVisualization)

    # Metadata for renderer
    renderer_hints: Dict[str, Any] = Field(default_factory=dict)
    # e.g. { "threejs": { "camera_distance": 50 }, "cesium": { "terrain": true } }

    # Interaction points — where the user can click/explore
    interaction_points: List[Dict[str, Any]] = Field(default_factory=list)

    # Narrative overlays — text/audio that plays during exploration
    narrative_overlays: List[Dict[str, Any]] = Field(default_factory=list)


# ── Dome World Model ────────────────────────────────────────────

class DomeWorldModel(BaseModel):
    """World model for a DOME — a navigable 3D environment representing one person's life.

    12 concentric layers, each with varying opacity/density based on completeness.
    The weakest layer is visually thinnest. The person is at the center.
    Creative layers (10-12) have artistic 3D content designed by the team.
    """
    schema_id: str
    subject_name: str
    format: WorldModelFormat = Field(default_factory=lambda: WorldModelFormat(
        schema_type=GameType.DOMES, schema_id="", title="", scene_type="dome"
    ))

    # Dome-specific rendering
    dome_radius: float = 100.0             # Base radius for the dome shell
    layer_spacing: float = 8.0             # Spacing between concentric layers
    weakest_layer: Optional[int] = None    # Highlighted visually
    total_cosm: float = 0.0

    # Subject representation at center
    subject_avatar: Dict[str, Any] = Field(default_factory=dict)

    # Life trajectory path — a curve through time
    trajectory_path: List[Vector3] = Field(default_factory=list)


# ── Sphere World Model ──────────────────────────────────────────

class SphereWorldModel(BaseModel):
    """World model for a SPHERE — a navigable simulation of a place.

    Before, during, and after activation. Geospatially anchored.
    10 layers rendered as concentric spheres around the parcel.
    Creative layers (7-10) have artistic 3D content designed by the team.
    """
    schema_id: str
    address: str
    format: WorldModelFormat = Field(default_factory=lambda: WorldModelFormat(
        schema_type=GameType.SPHERES, schema_id="", title="", scene_type="sphere"
    ))

    # Sphere-specific rendering
    parcel_outline: List[GeoCoordinate] = Field(default_factory=list)
    sphere_radius: float = 50.0
    layer_spacing: float = 5.0
    weakest_layer: Optional[int] = None
    total_chron: float = 0.0

    # Temporal states of the place
    state_before: Dict[str, Any] = Field(default_factory=dict)     # Pre-activation
    state_during: Dict[str, Any] = Field(default_factory=dict)     # During activation
    state_after: Dict[str, Any] = Field(default_factory=dict)      # Post-activation

    # Catalyst visualization — lines connecting to adjacent activations
    catalyst_connections: List[Dict[str, Any]] = Field(default_factory=list)
