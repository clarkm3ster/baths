"""THE DOME -- Pydantic v2 data models.

This package exports every model in THE DOME's data layer so that
consumers can import any model directly from ``dome.models``::

    from dome.models import Person, IdentitySpine, DynamicState

The models are organised into the following sub-modules:

* **identity** -- AddressEntry, CrossSystemIds, IdentitySpine
* **static_profile** -- StaticProfile
* **dynamic_state** -- BioState, MentalState, EconState, HousingState,
  FamilyState, JusticeState, EducationState, EligibilitySnapshot,
  EnrollmentSnapshot, ProgramState, DynamicState
* **dome_metrics** -- DomeMetrics
* **fiscal_event** -- FiscalEvent
* **budget_key** -- BudgetHorizon, PersonBudgetKey
* **budget_output** -- PayerBreakdown, PayerView, ProgramSpend,
  DomainBudget, MechanismBudget, CatastrophicEventRisk, RiskProfile,
  ScenarioBudget, HorizonBudget, WholePersonBudget
* **trajectory** -- FiscalTrajectoryTag
* **cascade** -- CascadeLink, CascadeDefinition, CascadeAlert
* **intervention** -- InterventionDefinition, InterventionPlan
* **scenario** -- (re-exports ScenarioBudget)
* **settlement_matrix** -- PayerSettlementRow, PayerTransfer, SettlementMatrix
* **person** -- Person
"""

# identity
from dome.models.identity import (
    AddressEntry,
    CrossSystemIds,
    IdentitySpine,
)

# static_profile
from dome.models.static_profile import StaticProfile

# dynamic_state
from dome.models.dynamic_state import (
    BioState,
    DynamicState,
    EconState,
    EducationState,
    EligibilitySnapshot,
    EnrollmentSnapshot,
    FamilyState,
    HousingState,
    JusticeState,
    MentalState,
    ProgramState,
)

# dome_metrics
from dome.models.dome_metrics import DomeMetrics

# fiscal_event
from dome.models.fiscal_event import FiscalEvent

# budget_key
from dome.models.budget_key import BudgetHorizon, PersonBudgetKey

# budget_output
from dome.models.budget_output import (
    CatastrophicEventRisk,
    DomainBudget,
    HorizonBudget,
    MechanismBudget,
    PayerBreakdown,
    PayerView,
    ProgramSpend,
    RiskProfile,
    ScenarioBudget,
    WholePersonBudget,
)

# trajectory
from dome.models.trajectory import FiscalTrajectoryTag

# cascade
from dome.models.cascade import CascadeAlert, CascadeDefinition, CascadeLink

# intervention
from dome.models.intervention import InterventionDefinition, InterventionPlan

# settlement_matrix
from dome.models.settlement_matrix import (
    PayerSettlementRow,
    PayerTransfer,
    SettlementMatrix,
)

# person (top-level aggregate)
from dome.models.person import Person

__all__ = [
    # identity
    "AddressEntry",
    "CrossSystemIds",
    "IdentitySpine",
    # static_profile
    "StaticProfile",
    # dynamic_state
    "BioState",
    "MentalState",
    "EconState",
    "HousingState",
    "FamilyState",
    "JusticeState",
    "EducationState",
    "EligibilitySnapshot",
    "EnrollmentSnapshot",
    "ProgramState",
    "DynamicState",
    # dome_metrics
    "DomeMetrics",
    # fiscal_event
    "FiscalEvent",
    # budget_key
    "BudgetHorizon",
    "PersonBudgetKey",
    # budget_output
    "PayerBreakdown",
    "PayerView",
    "ProgramSpend",
    "DomainBudget",
    "MechanismBudget",
    "CatastrophicEventRisk",
    "RiskProfile",
    "ScenarioBudget",
    "HorizonBudget",
    "WholePersonBudget",
    # trajectory
    "FiscalTrajectoryTag",
    # cascade
    "CascadeLink",
    "CascadeDefinition",
    "CascadeAlert",
    # intervention
    "InterventionDefinition",
    "InterventionPlan",
    # settlement_matrix
    "PayerSettlementRow",
    "PayerTransfer",
    "SettlementMatrix",
    # person
    "Person",
]
