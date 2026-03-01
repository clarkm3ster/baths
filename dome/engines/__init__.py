"""THE DOME computational engines.

This package contains the core engines that power THE DOME:

- :class:`BudgetEngine` -- the Skeleton Key.  Computes Whole-Person Budgets.
- :class:`TrajectoryClassifier` -- classifies lifetime fiscal trajectories.
- :class:`WrongPocketAnalyzer` -- analyzes cross-payer wrong-pocket dynamics.
- :class:`CascadeDetector` -- real-time cascade detection (Step 5).
- :class:`InterventionRecommender` -- optimal intervention selection (Step 6).
- :class:`BenefitsCliffCalculator` -- benefits cliff calculator (Step 7).
- :class:`LifeSimulator` -- Monte Carlo whole-life simulator (Step 11).
"""

from dome.engines.budget_engine import BudgetEngine
from dome.engines.trajectory_classifier import TrajectoryClassifier
from dome.engines.wrong_pocket_analyzer import WrongPocketAnalyzer
from dome.engines.cascade_detector import CascadeDetector
from dome.engines.intervention_recommender import InterventionRecommender
from dome.engines.benefits_cliff import BenefitsCliffCalculator
from dome.engines.simulator import LifeSimulator

__all__ = [
    "BudgetEngine",
    "TrajectoryClassifier",
    "WrongPocketAnalyzer",
    "CascadeDetector",
    "InterventionRecommender",
    "BenefitsCliffCalculator",
    "LifeSimulator",
]
