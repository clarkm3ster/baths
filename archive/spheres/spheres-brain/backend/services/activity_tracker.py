"""
Activity Tracker for SPHERES Brain.

Maintains an in-memory log of events that flow across the entire SPHERES
ecosystem.  On startup the tracker seeds itself with 30+ realistic events
spanning the past seven days so the API never returns an empty feed.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta

from models.services import ActivityEvent, ActivationMetrics


def _now() -> datetime:
    return datetime.utcnow()


def _ago(days: float = 0, hours: float = 0, minutes: float = 0) -> datetime:
    return _now() - timedelta(days=days, hours=hours, minutes=minutes)


# ---------------------------------------------------------------------------
# Seeded events — realistic Philadelphia activity over the last 7 days
# ---------------------------------------------------------------------------

def _seed_events() -> list[ActivityEvent]:
    """Return 35 realistic events spanning all four SPHERES apps."""
    return [
        # ── Day 0 (today) ──────────────────────────────────────────────
        ActivityEvent(
            event_id="evt-001",
            timestamp=_ago(hours=1),
            source_app="spheres-studio",
            event_type="design_created",
            description=(
                "New design created in Studio: Kensington Community Garden "
                "— 24 raised beds with ADA-accessible pathways"
            ),
            parcel_id="88-2-0347-00",
        ),
        ActivityEvent(
            event_id="evt-002",
            timestamp=_ago(hours=2),
            source_app="spheres-viz",
            event_type="episode_viewed",
            description="Episode 4 (Germantown) 3D world viewed 847 times today",
        ),
        ActivityEvent(
            event_id="evt-003",
            timestamp=_ago(hours=3),
            source_app="spheres-assets",
            event_type="parcel_updated",
            description=(
                "Vacancy status updated: 1800 N Broad St now marked "
                "'Vacant 7+ years' after field inspection"
            ),
            parcel_id="43-2-0200-00",
        ),
        ActivityEvent(
            event_id="evt-004",
            timestamp=_ago(hours=4),
            source_app="spheres-legal",
            event_type="permit_submitted",
            description=(
                "Permit application submitted via Legal for parcel "
                "88-2-0347-00 — L&I Vacant Lot Clean-Up Permit"
            ),
            parcel_id="88-2-0347-00",
        ),
        ActivityEvent(
            event_id="evt-005",
            timestamp=_ago(hours=5),
            source_app="spheres-studio",
            event_type="design_voted",
            description=(
                "Strawberry Mansion Pocket Park design received 12 new "
                "community votes (now 4.5 stars, 87 total votes)"
            ),
            parcel_id="32-1-1120-00",
        ),

        # ── Day 1 ─────────────────────────────────────────────────────
        ActivityEvent(
            event_id="evt-006",
            timestamp=_ago(days=1, hours=2),
            source_app="spheres-legal",
            event_type="contract_generated",
            description=(
                "Community Land Use Agreement generated for "
                "Germantown Ave parcel — Germantown Community Dev Corp"
            ),
            parcel_id="22-3-0890-00",
        ),
        ActivityEvent(
            event_id="evt-007",
            timestamp=_ago(days=1, hours=5),
            source_app="spheres-viz",
            event_type="episode_published",
            description=(
                "Episode 5 (North Broad — The Corridor of Possibility) "
                "published with 3 new 3D worlds"
            ),
        ),
        ActivityEvent(
            event_id="evt-008",
            timestamp=_ago(days=1, hours=8),
            source_app="spheres-assets",
            event_type="new_parcel_discovered",
            description=(
                "New vacant parcel discovered: 2741 N Broad St, "
                "4,200 sq ft, RSA-5, city-owned"
            ),
            parcel_id="43-2-0200-00",
        ),
        ActivityEvent(
            event_id="evt-009",
            timestamp=_ago(days=1, hours=10),
            source_app="spheres-studio",
            event_type="cost_estimate_completed",
            description=(
                "Cost estimate completed for Point Breeze Mural & "
                "Performance Wall: $6,800 total"
            ),
            parcel_id="36-4-0056-00",
        ),

        # ── Day 2 ─────────────────────────────────────────────────────
        ActivityEvent(
            event_id="evt-010",
            timestamp=_ago(days=2, hours=1),
            source_app="spheres-legal",
            event_type="permit_approved",
            description=(
                "L&I approved Vacant Lot Clean-Up Permit for 2510 N 29th St, "
                "Strawberry Mansion — 21-day fast-track"
            ),
            parcel_id="32-1-1120-00",
        ),
        ActivityEvent(
            event_id="evt-011",
            timestamp=_ago(days=2, hours=4),
            source_app="spheres-viz",
            event_type="scroll_engagement",
            description=(
                "Kensington episode scroll completion rate hit 72% "
                "this week — up from 58% last week"
            ),
        ),
        ActivityEvent(
            event_id="evt-012",
            timestamp=_ago(days=2, hours=7),
            source_app="spheres-assets",
            event_type="ownership_change",
            description=(
                "Ownership transfer detected: 5401 Germantown Ave "
                "transferred from private estate to Germantown CDC"
            ),
            parcel_id="22-3-0890-00",
        ),
        ActivityEvent(
            event_id="evt-013",
            timestamp=_ago(days=2, hours=9),
            source_app="spheres-studio",
            event_type="design_created",
            description=(
                "New design created: North Broad Rain Garden & Bio-Swale "
                "by Dr. Lena Park — green infrastructure focus"
            ),
            parcel_id="43-2-0200-00",
        ),

        # ── Day 3 ─────────────────────────────────────────────────────
        ActivityEvent(
            event_id="evt-014",
            timestamp=_ago(days=3, hours=2),
            source_app="spheres-legal",
            event_type="policy_alert",
            description=(
                "Policy alert: City Council Bill 240132 passed — "
                "Streamlined Vacant Lot Activation Permits now available"
            ),
        ),
        ActivityEvent(
            event_id="evt-015",
            timestamp=_ago(days=3, hours=5),
            source_app="spheres-assets",
            event_type="batch_update",
            description=(
                "Batch parcel update: 147 parcels refreshed from OPA "
                "data feed — 3 new vacancies identified in Kensington"
            ),
        ),
        ActivityEvent(
            event_id="evt-016",
            timestamp=_ago(days=3, hours=8),
            source_app="spheres-viz",
            event_type="episode_viewed",
            description=(
                "Episode 2 (Strawberry Mansion) crossed 5,000 total "
                "views — highest engagement in SPHERES history"
            ),
        ),
        ActivityEvent(
            event_id="evt-017",
            timestamp=_ago(days=3, hours=11),
            source_app="spheres-studio",
            event_type="timeline_generated",
            description=(
                "Implementation timeline generated for Kensington "
                "Community Garden: 45 days from permit to planting"
            ),
            parcel_id="88-2-0347-00",
        ),

        # ── Day 4 ─────────────────────────────────────────────────────
        ActivityEvent(
            event_id="evt-018",
            timestamp=_ago(days=4, hours=1),
            source_app="spheres-legal",
            event_type="contract_generated",
            description=(
                "Volunteer Liability Waiver generated for Strawberry "
                "Mansion community clean-up event (March 2026)"
            ),
            parcel_id="32-1-1120-00",
        ),
        ActivityEvent(
            event_id="evt-019",
            timestamp=_ago(days=4, hours=4),
            source_app="spheres-assets",
            event_type="assessment_updated",
            description=(
                "Assessed value updated: 1523 S 22nd St (Point Breeze) "
                "from $38,000 to $42,000 per latest OPA cycle"
            ),
            parcel_id="36-4-0056-00",
        ),
        ActivityEvent(
            event_id="evt-020",
            timestamp=_ago(days=4, hours=7),
            source_app="spheres-viz",
            event_type="world_asset_uploaded",
            description=(
                "New 3D world asset uploaded for Episode 3 (Point Breeze): "
                "community garden before/after visualization"
            ),
        ),
        ActivityEvent(
            event_id="evt-021",
            timestamp=_ago(days=4, hours=10),
            source_app="spheres-studio",
            event_type="design_voted",
            description=(
                "Germantown Micro-Market Pavilion design received "
                "23 votes in 24 hours — trending"
            ),
            parcel_id="22-3-0890-00",
        ),

        # ── Day 5 ─────────────────────────────────────────────────────
        ActivityEvent(
            event_id="evt-022",
            timestamp=_ago(days=5, hours=2),
            source_app="spheres-legal",
            event_type="permit_submitted",
            description=(
                "Zoning Use Registration Permit submitted for "
                "5401 Germantown Ave — community market use"
            ),
            parcel_id="22-3-0890-00",
        ),
        ActivityEvent(
            event_id="evt-023",
            timestamp=_ago(days=5, hours=5),
            source_app="spheres-assets",
            event_type="new_parcel_discovered",
            description=(
                "Double lot identified: 1823-1825 S 58th St, Kingsessing "
                "— 5,600 sq ft, community interest confirmed"
            ),
        ),
        ActivityEvent(
            event_id="evt-024",
            timestamp=_ago(days=5, hours=8),
            source_app="spheres-viz",
            event_type="episode_viewed",
            description=(
                "Episode 1 (Kensington) featured in Philadelphia Citizen "
                "article — 340 new visitors in 6 hours"
            ),
        ),
        ActivityEvent(
            event_id="evt-025",
            timestamp=_ago(days=5, hours=11),
            source_app="spheres-studio",
            event_type="design_created",
            description=(
                "New design: Point Breeze Pocket Park & Reading Nook "
                "by Darius Johnson — Little Free Library concept"
            ),
            parcel_id="36-4-0056-00",
        ),

        # ── Day 6 ─────────────────────────────────────────────────────
        ActivityEvent(
            event_id="evt-026",
            timestamp=_ago(days=6, hours=1),
            source_app="spheres-legal",
            event_type="contract_signed",
            description=(
                "Philadelphia Land Bank Garden License signed for "
                "2510 N 29th St — 3-year renewable term"
            ),
            parcel_id="32-1-1120-00",
        ),
        ActivityEvent(
            event_id="evt-027",
            timestamp=_ago(days=6, hours=3),
            source_app="spheres-assets",
            event_type="parcel_updated",
            description=(
                "Field survey completed: 2847 Kensington Ave — "
                "lot cleared, no structures, ready for activation"
            ),
            parcel_id="88-2-0347-00",
        ),
        ActivityEvent(
            event_id="evt-028",
            timestamp=_ago(days=6, hours=6),
            source_app="spheres-viz",
            event_type="scroll_engagement",
            description=(
                "Total SPHERES Viz engagement this week: 4,231 unique "
                "visitors, 12,847 scroll interactions"
            ),
        ),
        ActivityEvent(
            event_id="evt-029",
            timestamp=_ago(days=6, hours=9),
            source_app="spheres-studio",
            event_type="cost_estimate_completed",
            description=(
                "Cost estimate for Strawberry Mansion Community Garden "
                "revised down to $7,200 after PHS material donation"
            ),
            parcel_id="32-1-1120-00",
        ),

        # ── Day 7 ─────────────────────────────────────────────────────
        ActivityEvent(
            event_id="evt-030",
            timestamp=_ago(days=7, hours=2),
            source_app="spheres-legal",
            event_type="policy_alert",
            description=(
                "Zoning Code Amendment: CMX-1 Outdoor Community Use "
                "now by-right — no ZBA hearing required"
            ),
        ),
        ActivityEvent(
            event_id="evt-031",
            timestamp=_ago(days=7, hours=4),
            source_app="spheres-assets",
            event_type="new_parcel_discovered",
            description=(
                "Corner lot at 3rd & Girard (Fishtown) cleared Phase II "
                "ESA — 2,800 sq ft, CMX-2, high foot traffic"
            ),
        ),
        ActivityEvent(
            event_id="evt-032",
            timestamp=_ago(days=7, hours=6),
            source_app="spheres-viz",
            event_type="episode_published",
            description=(
                "Episode 4 (Germantown — Layered Time) launched with "
                "interactive timeline spanning 300 years of history"
            ),
        ),
        ActivityEvent(
            event_id="evt-033",
            timestamp=_ago(days=7, hours=9),
            source_app="spheres-studio",
            event_type="activation_started",
            description=(
                "Activation started: soil prep and bed construction "
                "begun at 1800 N Broad St community garden site"
            ),
            parcel_id="43-2-0200-00",
        ),
        ActivityEvent(
            event_id="evt-034",
            timestamp=_ago(days=7, hours=11),
            source_app="spheres-legal",
            event_type="permit_approved",
            description=(
                "Streets Dept Sidewalk Occupancy Permit approved for "
                "Germantown Ave micro-market — valid through Dec 2026"
            ),
            parcel_id="22-3-0890-00",
        ),
        ActivityEvent(
            event_id="evt-035",
            timestamp=_ago(days=7, hours=14),
            source_app="spheres-assets",
            event_type="batch_update",
            description=(
                "Weekly Land Bank inventory sync complete: 12 new "
                "parcels added, 4 dispositions recorded"
            ),
        ),
    ]


# ---------------------------------------------------------------------------
# Tracker
# ---------------------------------------------------------------------------

class ActivityTracker:
    """
    In-memory event store for cross-app activity.

    On construction the tracker seeds itself with realistic historical
    events so the API is never empty.  New events can be added at runtime.
    """

    def __init__(self) -> None:
        self._events: list[ActivityEvent] = _seed_events()

    # -- read -----------------------------------------------------------------

    def get_recent(self, limit: int = 50) -> list[ActivityEvent]:
        """Return the *limit* most recent events, newest first."""
        sorted_events = sorted(
            self._events, key=lambda e: e.timestamp, reverse=True
        )
        return sorted_events[:limit]

    def get_by_app(self, app_name: str) -> list[ActivityEvent]:
        """Return all events from a specific SPHERES app, newest first."""
        filtered = [e for e in self._events if e.source_app == app_name]
        return sorted(filtered, key=lambda e: e.timestamp, reverse=True)

    def get_by_parcel(self, parcel_id: str) -> list[ActivityEvent]:
        """Return all events related to a specific parcel."""
        filtered = [e for e in self._events if e.parcel_id == parcel_id]
        return sorted(filtered, key=lambda e: e.timestamp, reverse=True)

    # -- write ----------------------------------------------------------------

    def record(self, event: ActivityEvent) -> ActivityEvent:
        """Add an event to the store. Auto-assigns an ID if missing."""
        if not event.event_id:
            event.event_id = f"evt-{uuid.uuid4().hex[:8]}"
        self._events.append(event)
        return event

    # -- metrics --------------------------------------------------------------

    def get_metrics(self) -> ActivationMetrics:
        """
        Compute aggregate activation metrics from the event stream.

        In production these numbers would come from the downstream services;
        here we derive plausible totals from the seeded events plus some
        hardcoded baseline figures.
        """
        designs_created = sum(
            1 for e in self._events if e.event_type == "design_created"
        )
        permits_pulled = sum(
            1 for e in self._events if e.event_type in (
                "permit_submitted", "permit_approved",
            )
        )
        activations_completed = sum(
            1 for e in self._events if e.event_type == "activation_started"
        )

        unique_parcels = {
            e.parcel_id for e in self._events if e.parcel_id
        }

        return ActivationMetrics(
            total_designs=42 + designs_created,
            permits_pulled=18 + permits_pulled,
            activations_completed=12 + activations_completed,
            activations_in_progress=7,
            permanent_value_installed=284_500.0,
            revenue_generated=67_200.0,
            active_parcels=len(unique_parcels) + 23,
            community_participants=1_847,
            period="all-time",
        )

    # -- internals ------------------------------------------------------------

    @property
    def total_events(self) -> int:
        return len(self._events)
