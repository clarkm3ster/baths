"""Governance & Digital Rights layer for Dome Studio.

Implements two sub-systems:

PredictionAppeal
    When the Dome classifies someone into a trajectory or triggers an alert,
    the person can formally challenge it.  Tracks filing, review, resolution,
    and aggregate statistics (including overturn rate).

DataDominion
    A person owns their digital twin with enforceable rights: export,
    deletion, benefit-sharing, access-log review, and correction.  Tracks
    requests through fulfillment and computes benefit-share amounts.
"""
from __future__ import annotations

import math
from datetime import datetime
from typing import Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════════
# PredictionAppeal
# ═══════════════════════════════════════════════════════════════════

class AppealRequest(BaseModel):
    """Formal challenge to a Dome prediction or classification."""
    appeal_id: str = Field(default_factory=lambda: str(uuid4()))
    person_id: str
    prediction_type: Literal["trajectory", "alert", "classification"]
    prediction_id: str
    grounds: str
    evidence: list[str] = Field(default_factory=list)
    status: Literal[
        "submitted", "under_review", "upheld", "overturned", "withdrawn"
    ] = "submitted"
    filed_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    resolved_at: Optional[str] = None
    resolution_notes: Optional[str] = None


def file_appeal(
    person_id: str,
    prediction_type: Literal["trajectory", "alert", "classification"],
    prediction_id: str,
    grounds: str,
    evidence: list[str] | None = None,
) -> AppealRequest:
    """File a new appeal against a Dome prediction.

    Args:
        person_id: Identifier of the person challenging the prediction.
        prediction_type: Category of prediction being challenged.
        prediction_id: Unique ID of the specific prediction.
        grounds: Free-text explanation of why the prediction is contested.
        evidence: Optional list of evidence references (URIs, doc IDs, etc.).

    Returns:
        A newly created AppealRequest in *submitted* status.
    """
    if not grounds.strip():
        raise ValueError("Appeal grounds cannot be empty")

    return AppealRequest(
        person_id=person_id,
        prediction_type=prediction_type,
        prediction_id=prediction_id,
        grounds=grounds.strip(),
        evidence=evidence or [],
    )


def review_appeal(
    appeal: AppealRequest,
    decision: Literal["upheld", "overturned", "withdrawn"],
    resolution_notes: str = "",
) -> AppealRequest:
    """Resolve a pending appeal.

    Args:
        appeal: The appeal to resolve.
        decision: Outcome -- upheld (prediction stands), overturned
            (prediction invalidated), or withdrawn (person withdrew).
        resolution_notes: Reviewer commentary on the decision.

    Returns:
        Updated AppealRequest with resolved status and timestamp.

    Raises:
        ValueError: If the appeal is not in a reviewable state.
    """
    if appeal.status not in ("submitted", "under_review"):
        raise ValueError(
            f"Cannot review appeal in status '{appeal.status}'; "
            f"must be 'submitted' or 'under_review'"
        )

    return appeal.model_copy(update={
        "status": decision,
        "resolved_at": datetime.utcnow().isoformat(),
        "resolution_notes": resolution_notes or None,
    })


def get_appeal_stats(appeals: list[AppealRequest]) -> dict:
    """Compute aggregate appeal statistics.

    Args:
        appeals: Full list of AppealRequest objects to summarise.

    Returns:
        Dict with:
          - total: int
          - by_status: dict[str, int]
          - by_prediction_type: dict[str, int]
          - overturn_rate: float (0-1) -- fraction of resolved appeals
            that were overturned.  NaN-safe: returns 0.0 when no appeals
            have been resolved.
    """
    by_status: dict[str, int] = {}
    by_prediction_type: dict[str, int] = {}

    for a in appeals:
        by_status[a.status] = by_status.get(a.status, 0) + 1
        by_prediction_type[a.prediction_type] = (
            by_prediction_type.get(a.prediction_type, 0) + 1
        )

    resolved_statuses = {"upheld", "overturned"}
    resolved = sum(by_status.get(s, 0) for s in resolved_statuses)
    overturned = by_status.get("overturned", 0)
    overturn_rate = (overturned / resolved) if resolved > 0 else 0.0

    return {
        "total": len(appeals),
        "by_status": dict(sorted(by_status.items())),
        "by_prediction_type": dict(sorted(by_prediction_type.items())),
        "overturn_rate": round(overturn_rate, 4),
    }


# ═══════════════════════════════════════════════════════════════════
# DataDominion
# ═══════════════════════════════════════════════════════════════════

# Benefit-sharing defaults
_DEFAULT_PERSON_SHARE = 0.15          # 15 % of attributed revenue
_MINIMUM_SHARE_USD = 25.00            # floor payment

VALID_RIGHT_TYPES = (
    "export", "deletion", "benefit_sharing", "access_log", "correction",
)


class DataRights(BaseModel):
    """A single data-rights request from a person."""
    right_id: str = Field(default_factory=lambda: str(uuid4()))
    person_id: str
    right_type: Literal[
        "export", "deletion", "benefit_sharing", "access_log", "correction"
    ]
    requested_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
    fulfilled_at: Optional[str] = None
    status: Literal["requested", "in_progress", "fulfilled", "denied"] = "requested"
    details: Optional[str] = None


def request_data_right(
    person_id: str,
    right_type: Literal[
        "export", "deletion", "benefit_sharing", "access_log", "correction"
    ],
    details: str = "",
) -> DataRights:
    """Submit a data-rights request on behalf of a person.

    Args:
        person_id: The person exercising their right.
        right_type: Which right is being exercised.
        details: Optional additional context for the request.

    Returns:
        A new DataRights request in *requested* status.
    """
    return DataRights(
        person_id=person_id,
        right_type=right_type,
        details=details or None,
    )


def fulfill_data_right(
    right: DataRights,
    notes: str = "",
) -> DataRights:
    """Mark a data-rights request as fulfilled.

    Args:
        right: The DataRights request to fulfill.
        notes: Optional notes on how the right was satisfied.

    Returns:
        Updated DataRights with *fulfilled* status and timestamp.

    Raises:
        ValueError: If the request is already fulfilled or denied.
    """
    if right.status in ("fulfilled", "denied"):
        raise ValueError(
            f"Cannot fulfill right in status '{right.status}'"
        )

    details = right.details or ""
    if notes:
        details = f"{details}\n--- fulfillment ---\n{notes}".strip()

    return right.model_copy(update={
        "status": "fulfilled",
        "fulfilled_at": datetime.utcnow().isoformat(),
        "details": details,
    })


def calculate_benefit_share(
    person_id: str,
    production_revenue: float,
    share_rate: float = _DEFAULT_PERSON_SHARE,
    minimum_payment: float = _MINIMUM_SHARE_USD,
) -> dict:
    """Calculate a person's benefit share from production revenue.

    The person receives the larger of (revenue * share_rate) and the
    guaranteed minimum payment.  If production_revenue is zero or
    negative, the person still receives the minimum.

    Args:
        person_id: Identifier of the data subject.
        production_revenue: Total revenue attributed to this person's data.
        share_rate: Fraction of revenue owed (default 15 %).
        minimum_payment: Floor payment in USD.

    Returns:
        Dict with person_id, person_share, calculation_basis
        explaining the computation.
    """
    raw_share = production_revenue * share_rate
    person_share = max(raw_share, minimum_payment)

    if raw_share >= minimum_payment:
        basis = (
            f"{share_rate * 100:.1f}% of ${production_revenue:,.2f} revenue"
        )
    else:
        basis = (
            f"Minimum guarantee ${minimum_payment:,.2f} "
            f"(raw share ${raw_share:,.2f} was below floor)"
        )

    return {
        "person_id": person_id,
        "person_share": round(person_share, 2),
        "calculation_basis": basis,
    }
