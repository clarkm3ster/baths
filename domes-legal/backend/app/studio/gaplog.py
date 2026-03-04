"""
Dome Studio -- Gap Intake and Triage

Implements gap management for Dome productions:
  - intake and severity scoring
  - triage into urgency buckets
  - backlog view generation
  - OS engineering ticket conversion
  - production gap summaries

All inputs are plain dicts to avoid circular imports with schemas.py.
"""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SEVERITY_WEIGHTS: dict[str, float] = {
    "blocking": 1.0,
    "high":     0.7,
    "medium":   0.4,
    "low":      0.1,
}

AREA_IMPORTANCE: dict[str, float] = {
    "validation":  0.9,
    "connectors":  0.8,
    "ledger":      0.7,
    "consent":     0.9,
    "identity":    0.8,
    "simulation":  0.7,
    "rendering":   0.6,
    "audio":       0.5,
    "ui":          0.5,
    "pipeline":    0.6,
    "data":        0.7,
    "api":         0.6,
    "auth":        0.8,
    "storage":     0.5,
    "analytics":   0.4,
    "export":      0.4,
    "testing":     0.6,
    "docs":        0.3,
}

# All known OS areas (used for coverage scoring)
ALL_OS_AREAS = set(AREA_IMPORTANCE.keys())

# Triage severity -> bucket mapping
_TRIAGE_BUCKETS: dict[str, str] = {
    "blocking": "immediate",
    "high":     "next_sprint",
    "medium":   "backlog",
    "low":      "backlog",
}


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class BacklogGroup(BaseModel):
    """A single grouping in the backlog view."""
    key: str
    count: int = 0
    gap_ids: list[Any] = Field(default_factory=list)


class BacklogView(BaseModel):
    """Structured backlog view with multiple groupings."""
    by_severity: list[BacklogGroup] = Field(default_factory=list)
    by_area: list[BacklogGroup] = Field(default_factory=list)
    by_owner_module: list[BacklogGroup] = Field(default_factory=list)
    total: int = 0


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_gap_priority(gap: dict[str, Any]) -> float:
    """Score a gap from 0.0 to 1.0 by combining severity and area importance.

    Formula:  (severity_weight * 0.6) + (area_importance * 0.4)

    Severity gets the dominant weight while area importance boosts gaps in
    critical OS subsystems.

    Args:
        gap: Dict with at least severity and area keys.

    Returns:
        Float in [0, 1] -- higher means more urgent.
    """
    severity = (gap.get("severity") or "medium").lower().strip()
    area = (gap.get("area") or "").lower().strip()

    sev_score = SEVERITY_WEIGHTS.get(severity, 0.4)
    area_score = AREA_IMPORTANCE.get(area, 0.5)  # default mid-range

    return round(sev_score * 0.6 + area_score * 0.4, 4)


# ---------------------------------------------------------------------------
# Triage
# ---------------------------------------------------------------------------

def triage_gaps(
    gaps: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Split gaps into urgency buckets.

    Returns:
        Dict with keys immediate (blocking), next_sprint (high),
        and backlog (medium + low). Each value is a list of gap dicts
        sorted by descending priority score.
    """
    buckets: dict[str, list[dict[str, Any]]] = {
        "immediate":   [],
        "next_sprint": [],
        "backlog":     [],
    }

    for gap in gaps:
        severity = (gap.get("severity") or "medium").lower().strip()
        bucket_key = _TRIAGE_BUCKETS.get(severity, "backlog")
        buckets[bucket_key].append(gap)

    # Sort each bucket by priority score descending
    for key in buckets:
        buckets[key].sort(key=lambda g: score_gap_priority(g), reverse=True)

    return buckets


# ---------------------------------------------------------------------------
# Backlog view
# ---------------------------------------------------------------------------

def _group_by_field(
    gaps: list[dict[str, Any]],
    field: str,
    default: str = "unknown",
) -> list[BacklogGroup]:
    """Group gaps by a dict field and return sorted BacklogGroup list."""
    groups: dict[str, list[Any]] = {}
    for gap in gaps:
        key = (gap.get(field) or default).lower().strip()
        if key == "":
            key = default
        groups.setdefault(key, []).append(gap.get("id", gap.get("gap_id")))

    return sorted(
        [
            BacklogGroup(key=k, count=len(ids), gap_ids=ids)
            for k, ids in groups.items()
        ],
        key=lambda g: g.count,
        reverse=True,
    )


def generate_backlog_view(gaps: list[dict[str, Any]]) -> BacklogView:
    """Build a structured backlog view grouped by severity, area, and owner_module.

    Args:
        gaps: List of gap dicts.

    Returns:
        BacklogView with three grouping dimensions and a total count.
    """
    return BacklogView(
        by_severity=_group_by_field(gaps, "severity", default="medium"),
        by_area=_group_by_field(gaps, "area", default="unknown"),
        by_owner_module=_group_by_field(gaps, "owner_module", default="unassigned"),
        total=len(gaps),
    )


# ---------------------------------------------------------------------------
# OS ticket conversion
# ---------------------------------------------------------------------------

_SEVERITY_TO_TICKET_PRIORITY: dict[str, str] = {
    "blocking": "P0",
    "high":     "P1",
    "medium":   "P2",
    "low":      "P3",
}


def gap_to_os_ticket(gap: dict[str, Any]) -> dict[str, Any]:
    """Convert a gap item to an OS engineering ticket format.

    Returns a dict with keys: title, description, module, priority, labels.
    """
    severity = (gap.get("severity") or "medium").lower().strip()
    area = (gap.get("area") or "unknown").strip()
    module = (gap.get("owner_module") or gap.get("module") or "unassigned").strip()
    title = gap.get("title") or gap.get("summary") or f"Gap in {area}"
    description = gap.get("description") or gap.get("detail") or ""
    gap_id = gap.get("id") or gap.get("gap_id")

    labels: list[str] = [
        f"area:{area}",
        f"severity:{severity}",
        "source:dome-gap-log",
    ]
    if gap.get("production_id"):
        labels.append(f"production:{gap['production_id']}")

    return {
        "title": f"[GAP] {title}",
        "description": (
            f"{description}" + "\n\n---\n"
            + f"Gap ID: {gap_id}\n"
            + f"Area: {area}\n"
            + f"Severity: {severity}\n"
            + f"Priority Score: {score_gap_priority(gap)}"
        ).strip(),
        "module": module,
        "priority": _SEVERITY_TO_TICKET_PRIORITY.get(severity, "P2"),
        "labels": labels,
    }


# ---------------------------------------------------------------------------
# Production gap summary
# ---------------------------------------------------------------------------

def production_gap_summary(gaps: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute summary statistics for a production gap log.

    Returns a dict with:
      - total: int
      - by_severity: dict[str, int]
      - by_area: dict[str, int]
      - by_status: dict[str, int]
      - coverage_score: float (0-1) -- what fraction of known OS areas
        have at least one gap logged (i.e. have been tested / examined).
    """
    by_severity: dict[str, int] = {}
    by_area: dict[str, int] = {}
    by_status: dict[str, int] = {}
    areas_seen: set[str] = set()

    for gap in gaps:
        sev = (gap.get("severity") or "medium").lower().strip()
        area = (gap.get("area") or "unknown").lower().strip()
        status = (gap.get("status") or "new").lower().strip()

        by_severity[sev] = by_severity.get(sev, 0) + 1
        by_area[area] = by_area.get(area, 0) + 1
        by_status[status] = by_status.get(status, 0) + 1

        if area in ALL_OS_AREAS:
            areas_seen.add(area)

    coverage = round(len(areas_seen) / len(ALL_OS_AREAS), 4) if ALL_OS_AREAS else 0.0

    return {
        "total": len(gaps),
        "by_severity": dict(sorted(by_severity.items())),
        "by_area": dict(sorted(by_area.items())),
        "by_status": dict(sorted(by_status.items())),
        "coverage_score": coverage,
    }
