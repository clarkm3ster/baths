"""
DOMES v2 — Schemas Package

Exports all Pydantic request/response schemas used in the DOMES v2 API.

Usage:
    from domes.schemas import PersonCreate, PersonRead, DomeRead, ConsentCreate
"""
from domes.schemas.consent import (
    ConsentAuditEntryRead,
    ConsentBase,
    ConsentCreate,
    ConsentRead,
    ConsentUpdate,
)
from domes.schemas.dome import (
    DomeAssembleRequest,
    DomeCostAnalysis,
    DomeRead,
    DomeSummary,
    DomainScoreDetail,
    RecommendationItem,
    RiskScoreDetail,
)
from domes.schemas.flourishing import (
    FlourishingProfile,
    FlourishingScoreCreate,
    FlourishingScoreRead,
    FlourishingTrend,
)
from domes.schemas.fragment import (
    FragmentCreate,
    FragmentRead,
    FragmentSummary,
)
from domes.schemas.observation import (
    ObservationCreate,
    ObservationRead,
    ObservationSummary,
    ObservationUpdate,
)
from domes.schemas.person import (
    PersonBase,
    PersonCreate,
    PersonRead,
    PersonSummary,
    PersonUpdate,
)

__all__ = [
    # Consent
    "ConsentAuditEntryRead",
    "ConsentBase",
    "ConsentCreate",
    "ConsentRead",
    "ConsentUpdate",
    # Dome
    "DomeAssembleRequest",
    "DomeCostAnalysis",
    "DomeRead",
    "DomeSummary",
    "DomainScoreDetail",
    "RecommendationItem",
    "RiskScoreDetail",
    # Flourishing
    "FlourishingProfile",
    "FlourishingScoreCreate",
    "FlourishingScoreRead",
    "FlourishingTrend",
    # Fragment
    "FragmentCreate",
    "FragmentRead",
    "FragmentSummary",
    # Observation
    "ObservationCreate",
    "ObservationRead",
    "ObservationSummary",
    "ObservationUpdate",
    # Person
    "PersonBase",
    "PersonCreate",
    "PersonRead",
    "PersonSummary",
    "PersonUpdate",
]
