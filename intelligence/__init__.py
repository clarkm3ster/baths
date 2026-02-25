"""
BATHS Intelligence System

The brain that gets smarter with every dome and sphere.

Components:
- memory: Cross-project learning (domes learn from domes, spheres from spheres)
- world_model: Accumulated understanding of people (domes) and places (spheres)
- frontier: Frontier AI research tracker mapped to BATHS capabilities
- researcher: The ongoing frontier AI researcher agent
- agent_network: Multi-agent coordination architecture
- models: Data structures for the intelligence system
"""

from intelligence.models import (
    Learning,
    LearningType,
    ProjectMemory,
    PersonKnowledge,
    PlaceKnowledge,
    FrontierCapability,
    ResearchFrontier,
    ResearchMaturity,
    WorldModelDomain,
    IntelligenceMetrics,
    AgentCapabilityProfile,
    AgentTask,
)
from intelligence.memory import ProjectMemoryStore
from intelligence.world_model import PersonWorldModel, PlaceWorldModel
from intelligence.frontier import FrontierTracker
from intelligence.researcher import FrontierResearcher
from intelligence.agent_network import AgentOrchestrator

__all__ = [
    # Core store
    "ProjectMemoryStore",
    # World models
    "PersonWorldModel",
    "PlaceWorldModel",
    # Frontier
    "FrontierTracker",
    "FrontierResearcher",
    # Agent network
    "AgentOrchestrator",
    # Data models
    "Learning",
    "LearningType",
    "ProjectMemory",
    "PersonKnowledge",
    "PlaceKnowledge",
    "FrontierCapability",
    "ResearchFrontier",
    "ResearchMaturity",
    "WorldModelDomain",
    "IntelligenceMetrics",
    "AgentCapabilityProfile",
    "AgentTask",
]
