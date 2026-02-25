"""
BATHS Gravitational Schema Architecture

The person (DOME) and the place (SPHERE) are gravitational centers.
Every advancing AI capability is captured as a layer interface.
Every layer has five interfaces: Ingest, Process, State, Act, Export.
Every layer has an AI capability map.
Every layer exports world-model-ready structured data.
Every layer has a time dimension — the schema is alive.

The games are schema editors.
The portfolio sites are schema readers.
The talent agent is a schema matchmaker.
The AI agents are schema fillers.
The creative teams are schema designers.
The world model is the schema renderer.
Everything is one architecture.
"""

from schema.core import (
    LayerInterface,
    IngestInterface,
    ProcessInterface,
    StateInterface,
    ActInterface,
    ExportInterface,
    AICapability,
    AICapabilityMap,
    TemporalEntry,
    TemporalState,
    WorldModelExport,
    CreativeInput,
    CreativeInputType,
    IPAttribution,
    LayerDefinition,
    LayerScore,
    SchemaMetadata,
)

from schema.dome import (
    DomeSchema,
    DomeLayer,
    DomeLegalLayer,
    DomeSystemsLayer,
    DomeFiscalLayer,
    DomeHealthLayer,
    DomeHousingLayer,
    DomeEconomicLayer,
    DomeEducationLayer,
    DomeCommunityLayer,
    DomeEnvironmentLayer,
    DomeAutonomyLayer,
    DomeCreativityLayer,
    DomeFlourishingLayer,
    DOME_LAYER_DEFINITIONS,
)

from schema.sphere import (
    SphereSchema,
    SphereLayer,
    SphereParcelLayer,
    SphereInfrastructureLayer,
    SphereEnvironmentalLayer,
    SphereEconomicLayer,
    SphereSocialLayer,
    SphereTemporalLayer,
    SphereActivationLayer,
    SpherePermanenceLayer,
    SpherePolicyLayer,
    SphereCatalystLayer,
    SPHERE_LAYER_DEFINITIONS,
)

from schema.scaling import (
    PatternLibrary,
    SchemaPattern,
    DraftGenerator,
    CrossSchemaLearning,
)

from schema.world_model import (
    WorldModelFormat,
    DomeWorldModel,
    SphereWorldModel,
    LayerVisualization,
    TemporalVisualization,
)

from schema.creative import (
    CreativeCanvas,
    ArchitecturalInput,
    SonicInput,
    MaterialInput,
    NarrativeInput,
    MovementInput,
    VisualInput,
    CulinaryInput,
    PhilosophicalInput,
    ExperienceInput,
)

from schema.bridge import (
    production_json_to_dome_schema,
    production_json_to_sphere_schema,
    dome_schema_to_world_model,
    sphere_schema_to_world_model,
    schema_to_match_request,
    schema_to_json,
    dome_from_json,
    sphere_from_json,
)
