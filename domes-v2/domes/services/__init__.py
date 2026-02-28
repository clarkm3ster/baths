"""
DOMES v2 — Services Package

This package contains all service-layer modules for the DOMES v2 system.
Each service encapsulates domain logic for a major subsystem:

    prediction   — Risk scoring, intervention ranking, causal modeling
    flourishing  — 12-domain flourishing scores, tradition views, cost-of-suffering
    fragment     — Data ingestion, normalization, quality metrics
    cosm         — Composite Outcome Scoring Model (COSM) computation
    compute      — Compute budget tracking (3×10²¹ FLOPS / 5-year budget)
    api          — Unified FastAPI gateway — the public front door

Import pattern
--------------
Most application code should import from this package directly::

    from domes.services import ComputeBudgetTracker, COMPUTE_BUDGET

For the FastAPI application object::

    from domes.services.api import app

For individual service classes (once implemented)::

    from domes.services.compute import ComputeBudgetTracker, ServiceName
    from domes.services.prediction import PredictionService
    from domes.services.flourishing import FlourishingService
    from domes.services.fragment import FragmentService
    from domes.services.cosm import CosmService

Parallel build note
-------------------
prediction.py, flourishing.py, fragment.py, and cosm.py are being built in
parallel. Until they are available, those imports use try/except guards so
the package can be imported cleanly by the API gateway and compute tracker.
"""
from __future__ import annotations

# Compute service is always available (no DB dependency for budget tracking)
from domes.services.compute import (
    ComputeBudgetTracker,
    ComputeAllocation,
    InformationGainCurve,
    ServiceName,
    COMPUTE_BUDGET,
    TOTAL_FLOPS,
    TOTAL_BUDGET_USD_LOW,
    TOTAL_BUDGET_USD_HIGH,
    BUDGET_YEARS,
    SUSTAINED_FLOPS_PER_SECOND,
    COST_PER_FLOP,
)

# Services built in parallel — graceful degradation until available
try:
    from domes.services.prediction import PredictionService  # type: ignore[import]
except ImportError:
    PredictionService = None  # type: ignore[assignment,misc]

try:
    from domes.services.flourishing import FlourishingService  # type: ignore[import]
except ImportError:
    FlourishingService = None  # type: ignore[assignment,misc]

try:
    from domes.services.fragment import FragmentService  # type: ignore[import]
    from domes.services.fragment import FragmentEngine  # type: ignore[import]
except ImportError:
    FragmentService = None  # type: ignore[assignment,misc]
    FragmentEngine = None   # type: ignore[assignment,misc]

try:
    from domes.services.cosm import CosmService  # type: ignore[import]
    from domes.services.cosm import CosmEngine  # type: ignore[import]
except ImportError:
    CosmService = None  # type: ignore[assignment,misc]
    CosmEngine = None   # type: ignore[assignment,misc]

# Legacy imports from parallel agent's prediction.py — guarded
try:
    from domes.services.prediction import (  # type: ignore[import]
        CrisisPredictionEngine,
        RiskDashboard,
        RiskPrediction,
        InterventionScore,
        InterventionOption,
        CausalSignal,
        CausalPathway,
        CrisisType,
        InterventionType,
        SignalStrength,
        CrisisHorizon,
    )
except ImportError:
    CrisisPredictionEngine = None  # type: ignore[assignment,misc]
    RiskDashboard = None           # type: ignore[assignment,misc]
    RiskPrediction = None          # type: ignore[assignment,misc]
    InterventionScore = None       # type: ignore[assignment,misc]
    InterventionOption = None      # type: ignore[assignment,misc]
    CausalSignal = None            # type: ignore[assignment,misc]
    CausalPathway = None           # type: ignore[assignment,misc]
    CrisisType = None              # type: ignore[assignment,misc]
    InterventionType = None        # type: ignore[assignment,misc]
    SignalStrength = None          # type: ignore[assignment,misc]
    CrisisHorizon = None           # type: ignore[assignment,misc]


__all__ = [
    # Compute (always available)
    "ComputeBudgetTracker",
    "ComputeAllocation",
    "InformationGainCurve",
    "ServiceName",
    "COMPUTE_BUDGET",
    # Constants
    "TOTAL_FLOPS",
    "TOTAL_BUDGET_USD_LOW",
    "TOTAL_BUDGET_USD_HIGH",
    "BUDGET_YEARS",
    "SUSTAINED_FLOPS_PER_SECOND",
    "COST_PER_FLOP",
    # Services (available after parallel build completes)
    "PredictionService",
    "FlourishingService",
    "FragmentService",
    "FragmentEngine",
    "CosmService",
    "CosmEngine",
    # Legacy / parallel agent symbols
    "CrisisPredictionEngine",
    "RiskDashboard",
    "RiskPrediction",
    "InterventionScore",
    "InterventionOption",
    "CausalSignal",
    "CausalPathway",
    "CrisisType",
    "InterventionType",
    "SignalStrength",
    "CrisisHorizon",
]
