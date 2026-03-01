"""Scenario model re-export for THE DOME.

This module re-exports ``ScenarioBudget`` from ``budget_output`` for
convenience, so that consumers can import it as::

    from dome.models.scenario import ScenarioBudget
"""

from dome.models.budget_output import ScenarioBudget

__all__ = ["ScenarioBudget"]
