from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import System, Connection, Gap, Bridge

router = APIRouter(prefix="/api", tags=["person-map"])


class PersonMapRequest(BaseModel):
    circumstances: list[str]


@router.post("/person-map")
def get_person_map(request: PersonMapRequest, db: Session = Depends(get_db)):
    """Generate a person-specific data map based on their circumstances.

    Given a list of circumstances (e.g., ["medicaid", "incarcerated", "substance_use"]),
    returns all systems that would hold data about this person, all connections
    between those systems, all gaps between those systems, and all bridges
    that could close those gaps.
    """
    circumstances = set(request.circumstances)

    # Find all systems whose applies_when overlaps with person's circumstances
    all_systems = db.query(System).all()
    matching_systems = []
    matching_ids = set()

    for system in all_systems:
        system_applies = set(system.applies_when)
        if system_applies & circumstances:
            matching_systems.append(system)
            matching_ids.add(system.id)

    # Find connections between matching systems
    all_connections = db.query(Connection).all()
    matching_connections = []
    connected_pairs = set()

    for conn in all_connections:
        if conn.source_id in matching_ids and conn.target_id in matching_ids:
            matching_connections.append(conn)
            connected_pairs.add((conn.source_id, conn.target_id))
            if conn.direction == "bidirectional":
                connected_pairs.add((conn.target_id, conn.source_id))

    # Find gaps between matching systems
    all_gaps = db.query(Gap).all()
    matching_gaps = []
    matching_gap_ids = set()

    for gap in all_gaps:
        if gap.system_a_id in matching_ids and gap.system_b_id in matching_ids:
            # Also check if gap applies_when overlaps with circumstances
            gap_applies = set(gap.applies_when)
            if gap_applies & circumstances:
                matching_gaps.append(gap)
                matching_gap_ids.add(gap.id)

    # Find bridges for matching gaps
    matching_bridges = []
    if matching_gap_ids:
        matching_bridges = (
            db.query(Bridge)
            .filter(Bridge.gap_id.in_(matching_gap_ids))
            .order_by(Bridge.priority_score.desc())
            .all()
        )

    # Calculate summary
    n_systems = len(matching_systems)
    n_connected = len(matching_connections)

    # Count total possible pairs and disconnected pairs
    total_possible_pairs = 0
    disconnected_pairs = 0
    for i, sys_a in enumerate(matching_systems):
        for j, sys_b in enumerate(matching_systems):
            if i < j:
                total_possible_pairs += 1
                if (sys_a.id, sys_b.id) not in connected_pairs and (sys_b.id, sys_a.id) not in connected_pairs:
                    disconnected_pairs += 1

    consent_closable_count = sum(1 for g in matching_gaps if g.consent_closable)

    return {
        "systems": [s.to_dict() for s in matching_systems],
        "connections": [c.to_dict() for c in matching_connections],
        "gaps": [g.to_dict() for g in matching_gaps],
        "bridges": [b.to_dict() for b in matching_bridges],
        "summary": {
            "total_systems": n_systems,
            "connected_pairs": n_connected,
            "disconnected_pairs": disconnected_pairs,
            "gaps_count": len(matching_gaps),
            "consent_closable_count": consent_closable_count,
            "total_bridge_cost": _estimate_total_cost(matching_bridges),
        },
    }




@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get summary statistics for the entire data map."""
    total_systems = db.query(System).count()
    total_connections = db.query(Connection).count()
    total_gaps = db.query(Gap).count()
    total_bridges = db.query(Bridge).count()

    gaps = db.query(Gap).all()
    by_severity: dict[str, int] = {}
    by_barrier_type: dict[str, int] = {}
    consent_closable_count = 0

    for gap in gaps:
        by_severity[gap.severity] = by_severity.get(gap.severity, 0) + 1
        by_barrier_type[gap.barrier_type] = by_barrier_type.get(gap.barrier_type, 0) + 1
        if gap.consent_closable:
            consent_closable_count += 1

    bridges = db.query(Bridge).all()
    avg_priority = 0.0
    if bridges:
        avg_priority = round(sum(b.priority_score for b in bridges) / len(bridges), 2)

    return {
        "total_systems": total_systems,
        "total_connections": total_connections,
        "total_gaps": total_gaps,
        "total_bridges": total_bridges,
        "by_severity": by_severity,
        "by_barrier_type": by_barrier_type,
        "consent_closable_count": consent_closable_count,
        "avg_priority": avg_priority,
    }


def _estimate_total_cost(bridges: list) -> str:
    """Estimate total cost range from bridge cost strings."""
    if not bridges:
        return "$0"

    total_low = 0
    total_high = 0

    for bridge in bridges:
        cost = bridge.estimated_cost
        # Parse cost strings like "$50K", "$1-3M", "$200K-500K"
        cost = cost.replace("$", "").replace(",", "")
        parts = cost.split("-")

        try:
            low = _parse_cost_value(parts[0].strip())
            high = _parse_cost_value(parts[-1].strip()) if len(parts) > 1 else low
            total_low += low
            total_high += high
        except (ValueError, IndexError):
            continue

    if total_low == total_high:
        return f"${_format_cost(total_low)}"
    return f"${_format_cost(total_low)}-${_format_cost(total_high)}"


def _parse_cost_value(s: str) -> int:
    """Parse a cost value like '50K' or '3M' into an integer."""
    s = s.strip().upper()
    if s.endswith("M"):
        return int(float(s[:-1]) * 1_000_000)
    elif s.endswith("K"):
        return int(float(s[:-1]) * 1_000)
    else:
        return int(float(s))


def _format_cost(value: int) -> str:
    """Format integer cost back to human-readable string."""
    if value >= 1_000_000:
        m = value / 1_000_000
        return f"{m:.1f}M" if m != int(m) else f"{int(m)}M"
    elif value >= 1_000:
        k = value / 1_000
        return f"{k:.0f}K" if k != int(k) else f"{int(k)}K"
    else:
        return str(value)
