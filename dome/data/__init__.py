"""
DOME Reference Data Package
============================

Static reference data for THE DOME fiscal-cascade simulation engine.

Modules:
    programs            -- 63 government programs with eligibility, spending, and cascade links
    cascades            -- 6 cascade-type definitions with probabilistic link parameters
    interventions       -- 12+ evidence-based interventions that can break cascade links
    unit_costs          -- Published per-unit costs for services and placements
    population_baselines -- Population-level fiscal and demographic baselines
    fiscal_trajectories -- 5 lifetime fiscal trajectory archetypes
"""

from dome.data.programs import PROGRAMS
from dome.data.cascades import CASCADE_DEFINITIONS
from dome.data.interventions import INTERVENTION_DEFINITIONS
from dome.data.unit_costs import UNIT_COSTS
from dome.data.population_baselines import POPULATION_BASELINES
from dome.data.fiscal_trajectories import FISCAL_TRAJECTORIES

__all__ = [
    "PROGRAMS",
    "CASCADE_DEFINITIONS",
    "INTERVENTION_DEFINITIONS",
    "UNIT_COSTS",
    "POPULATION_BASELINES",
    "FISCAL_TRAJECTORIES",
]
