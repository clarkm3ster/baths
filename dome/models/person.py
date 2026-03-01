"""Person model for THE DOME.

The ``Person`` model is the top-level aggregation of every data structure
in THE DOME's data model.  It composes the identity spine, static profile,
dynamic state, DOME metrics, fiscal history, budget key, optional budget
output, and optional fiscal trajectory tag into a single unified record
that represents everything the system knows about one human being.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from dome.models.budget_key import PersonBudgetKey
from dome.models.budget_output import WholePersonBudget
from dome.models.dome_metrics import DomeMetrics
from dome.models.dynamic_state import DynamicState
from dome.models.fiscal_event import FiscalEvent
from dome.models.identity import IdentitySpine
from dome.models.static_profile import StaticProfile
from dome.models.trajectory import FiscalTrajectoryTag


class Person(BaseModel):
    """Top-level record representing a single person in THE DOME.

    This model composes every major sub-model into one document.  It is
    designed to be the canonical serialisation format for person-level data
    flowing between DOME engines, APIs, and storage layers.

    Key design choices:

    * ``whole_person_budget`` and ``fiscal_trajectory_tag`` are optional
      because they are computed asynchronously by downstream engines and
      may not yet exist for a newly ingested person.
    * ``fiscal_history`` is a list of ``FiscalEvent`` instances ordered
      chronologically; consumers should not assume the list is sorted.
    """

    person_uid: str = Field(
        ..., description="Globally unique person identifier."
    )
    identity_spine: IdentitySpine = Field(
        ..., description="Master cross-system identity record."
    )
    static_profile: StaticProfile = Field(
        ..., description="Time-invariant personal attributes."
    )
    dynamic_state: DynamicState = Field(
        ..., description="Most recent mutable state snapshot."
    )
    dome_metrics: DomeMetrics = Field(
        default_factory=DomeMetrics,
        description="Nine-layer DOME metrics snapshot.",
    )
    fiscal_history: list[FiscalEvent] = Field(
        default_factory=list,
        description="Chronological list of fiscal events for this person.",
    )
    whole_person_budget_key: PersonBudgetKey = Field(
        ...,
        description="Input key for the Whole-Person Budget engine.",
    )
    whole_person_budget: WholePersonBudget | None = Field(
        default=None,
        description=(
            "Output of the Whole-Person Budget engine.  None if not yet "
            "computed."
        ),
    )
    fiscal_trajectory_tag: FiscalTrajectoryTag | None = Field(
        default=None,
        description=(
            "Lifetime fiscal trajectory classification.  None if not yet "
            "computed."
        ),
    )
