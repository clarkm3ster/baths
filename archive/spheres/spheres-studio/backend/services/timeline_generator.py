"""
SPHERES Studio — Timeline Generation Engine

Produces a fully-phased project timeline from a design specification and a
target activation date.  All date arithmetic uses the Python standard library
``datetime`` module (no third-party date libs required).

Phases
------
1. PERMITS          60-120 days before activation
2. PROCUREMENT      30-60 days before
3. SITE_PREP        7-14 days before
4. SETUP            1-3 days before
5. ACTIVATION       the event / installation period
6. TEARDOWN         starts day after activation ends
7. PERMANENCE_HANDOFF  starts after teardown
"""

from __future__ import annotations

import uuid
from datetime import date, timedelta
from typing import Optional

from models.timeline import (
    ActivationType,
    AssignedTeam,
    ConflictLevel,
    ConflictReport,
    DesignElement,
    DesignInput,
    Phase,
    PhillyEvent,
    Season,
    TaskStatus,
    Timeline,
    TimelineTask,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _uid() -> str:
    return uuid.uuid4().hex[:12]


def _season(d: date) -> Season:
    month = d.month
    if month in (3, 4, 5):
        return Season.SPRING
    if month in (6, 7, 8):
        return Season.SUMMER
    if month in (9, 10, 11):
        return Season.FALL
    return Season.WINTER


def _is_outdoor_friendly(d: date) -> bool:
    """Philadelphia outdoor events are best April-October."""
    return 4 <= d.month <= 10


def _is_planting_season(d: date) -> bool:
    """Garden planting in Philly: March-May or September-October."""
    return d.month in (3, 4, 5, 9, 10)


def _is_construction_hostile(d: date) -> bool:
    """Avoid construction December-February in Philadelphia."""
    return d.month in (12, 1, 2)


def _activation_duration(activation_type: ActivationType, explicit_days: int) -> int:
    """Resolve the activation length in days."""
    mapping = {
        ActivationType.SINGLE_DAY: 1,
        ActivationType.WEEKEND: 2,
        ActivationType.WEEK: 7,
        ActivationType.MONTH: 30,
        ActivationType.ONGOING: 90,
    }
    if explicit_days > 1:
        return explicit_days
    return mapping.get(activation_type, 1)


# ---------------------------------------------------------------------------
# Known Philadelphia events (static calendar — would be an API in production)
# ---------------------------------------------------------------------------

_PHILLY_EVENTS: list[dict] = [
    {
        "name": "Mummers Parade",
        "month": 1, "day": 1,
        "location": "Broad Street",
        "conflict_level": ConflictLevel.HIGH,
        "description": "Annual New Year's Day parade along Broad Street",
        "impact_notes": "Major road closures on Broad Street, heavy crowds downtown",
    },
    {
        "name": "Philadelphia Flower Show",
        "month": 3, "day": 1,
        "duration_days": 10,
        "location": "Pennsylvania Convention Center / South Philadelphia",
        "conflict_level": ConflictLevel.MEDIUM,
        "description": "World's largest indoor flower show",
        "impact_notes": "Increased traffic near Convention Center, hotel availability reduced",
    },
    {
        "name": "Penn Relays",
        "month": 4, "day": 24,
        "duration_days": 3,
        "location": "Franklin Field, University of Pennsylvania",
        "conflict_level": ConflictLevel.MEDIUM,
        "description": "Oldest and largest track relay meet in the US",
        "impact_notes": "Heavy traffic in University City, increased transit usage",
    },
    {
        "name": "Broad Street Run",
        "month": 5, "day": 4,
        "location": "Broad Street",
        "conflict_level": ConflictLevel.HIGH,
        "description": "10-mile run down Broad Street",
        "impact_notes": "Complete closure of Broad Street, major transit disruptions",
    },
    {
        "name": "Odunde Festival",
        "month": 6, "day": 8,
        "location": "23rd Street and South Street",
        "conflict_level": ConflictLevel.MEDIUM,
        "description": "Largest African American street festival in the US",
        "impact_notes": "Street closures around 23rd & South, heavy pedestrian traffic",
    },
    {
        "name": "Wawa Welcome America / July 4th",
        "month": 7, "day": 4,
        "duration_days": 4,
        "location": "Benjamin Franklin Parkway / citywide",
        "conflict_level": ConflictLevel.CRITICAL,
        "description": "Multi-day Independence Day celebration and concert",
        "impact_notes": "Parkway closed, massive crowds, all parks heavily used, "
                        "fireworks staging, security perimeters",
    },
    {
        "name": "Made in America Festival",
        "month": 9, "day": 1,
        "duration_days": 2,
        "location": "Benjamin Franklin Parkway",
        "conflict_level": ConflictLevel.CRITICAL,
        "description": "Major music festival on the Parkway",
        "impact_notes": "Parkway fully closed for a week (setup/teardown), "
                        "significant noise, massive crowds",
    },
    {
        "name": "Philadelphia Marathon",
        "month": 11, "day": 23,
        "duration_days": 2,
        "location": "City-wide route",
        "conflict_level": ConflictLevel.HIGH,
        "description": "Full marathon and half marathon through the city",
        "impact_notes": "Extensive road closures along the Schuylkill, MLK Drive, "
                        "Center City, and Manayunk",
    },
    {
        "name": "Thanksgiving Day Parade",
        "month": 11, "day": 28,
        "location": "Center City / Benjamin Franklin Parkway",
        "conflict_level": ConflictLevel.HIGH,
        "description": "Annual Thanksgiving parade",
        "impact_notes": "Parkway and Market Street closures, heavy foot traffic",
    },
    {
        "name": "Dilworth Park Winterfest / Christmas Village",
        "month": 11, "day": 22,
        "duration_days": 45,
        "location": "Dilworth Park / LOVE Park / City Hall",
        "conflict_level": ConflictLevel.LOW,
        "description": "Holiday markets and ice skating",
        "impact_notes": "Reduced available park space at City Hall, moderate crowds",
    },
]


def _resolve_philly_events(year: int) -> list[PhillyEvent]:
    """Materialise the static calendar entries for a given year."""
    events: list[PhillyEvent] = []
    for ev in _PHILLY_EVENTS:
        try:
            start = date(year, ev["month"], ev["day"])
        except ValueError:
            # handle e.g. Feb 29 in non-leap years
            continue
        dur = ev.get("duration_days", 1)
        end = start + timedelta(days=max(dur - 1, 0))
        events.append(PhillyEvent(
            name=ev["name"],
            date=start,
            end_date=end,
            location=ev["location"],
            conflict_level=ev["conflict_level"],
            description=ev.get("description", ""),
            impact_notes=ev.get("impact_notes", ""),
        ))
    return events


# ---------------------------------------------------------------------------
# Timeline Generator
# ---------------------------------------------------------------------------

class TimelineGenerator:
    """Builds a complete phased timeline from a design specification."""

    def generate_timeline(
        self,
        design: DesignInput,
        target_activation_date: date,
        duration_days: int = 1,
    ) -> Timeline:
        activation_len = _activation_duration(design.activation_type, duration_days)
        activation_end = target_activation_date + timedelta(days=max(activation_len - 1, 0))

        # Collect metadata from elements
        all_permits: list[str] = []
        has_permanent = False
        has_construction = False
        has_vendors = False
        has_gardens = False
        max_lead_time = 0
        total_setup_hours = 0.0
        total_teardown_hours = 0.0

        for el in design.elements:
            all_permits.extend(el.permit_requirements)
            if el.is_permanent:
                has_permanent = True
            if el.requires_construction:
                has_construction = True
            if el.requires_vendors:
                has_vendors = True
            if el.element_type in ("garden",):
                has_gardens = True
            if el.lead_time_days > max_lead_time:
                max_lead_time = el.lead_time_days
            total_setup_hours += el.setup_hours
            total_teardown_hours += el.teardown_hours

        unique_permits = sorted(set(all_permits))

        # Season / weather analysis
        season_warnings: list[str] = []
        weather_buffer = 0

        if not _is_outdoor_friendly(target_activation_date):
            season_warnings.append(
                f"Target date {target_activation_date} is outside the ideal "
                f"outdoor season (April-October) for Philadelphia."
            )
            weather_buffer += 7

        if has_gardens and not _is_planting_season(target_activation_date):
            season_warnings.append(
                "Design includes garden elements but target date is outside "
                "planting season (March-May, September-October)."
            )
            weather_buffer += 5

        # Check construction window
        prep_start_est = target_activation_date - timedelta(days=14)
        if has_construction and _is_construction_hostile(prep_start_est):
            season_warnings.append(
                "Site preparation falls in December-February — construction "
                "delays likely. Consider moving to spring."
            )
            weather_buffer += 10

        if _season(target_activation_date) == Season.WINTER:
            weather_buffer += 5

        # -----------------------------------------------------------------
        # Build tasks per phase
        # -----------------------------------------------------------------
        tasks: list[TimelineTask] = []

        # ---- Phase 1: PERMITS ----
        permit_task_ids: list[str] = []
        if unique_permits:
            # Stagger: park_use first, then event, then everything else
            priority_order = ["park_use", "event"]
            ordered = [p for p in priority_order if p in unique_permits]
            ordered += [p for p in unique_permits if p not in priority_order]

            permit_start = target_activation_date - timedelta(
                days=120 + weather_buffer
            )
            previous_id: Optional[str] = None
            stagger_offset = 0

            for idx, permit_name in enumerate(ordered):
                tid = _uid()
                app_start = permit_start + timedelta(days=stagger_offset)
                app_duration = 3  # days to prepare application
                app_end = app_start + timedelta(days=app_duration - 1)

                tasks.append(TimelineTask(
                    id=tid,
                    name=f"Apply for {permit_name.replace('_', ' ')} permit",
                    phase=Phase.PERMITS,
                    start_date=app_start,
                    end_date=app_end,
                    duration_days=app_duration,
                    dependencies=[previous_id] if previous_id else [],
                    assigned_team=AssignedTeam.PERMITS_TEAM,
                    notes=f"Permit type: {permit_name}",
                ))

                review_id = _uid()
                review_start = app_end + timedelta(days=1)
                review_duration = 21  # 3-week review period
                review_end = review_start + timedelta(days=review_duration - 1)

                tasks.append(TimelineTask(
                    id=review_id,
                    name=f"{permit_name.replace('_', ' ').title()} permit review period",
                    phase=Phase.PERMITS,
                    start_date=review_start,
                    end_date=review_end,
                    duration_days=review_duration,
                    dependencies=[tid],
                    assigned_team=AssignedTeam.PERMITS_TEAM,
                    notes="Awaiting city review",
                ))

                approval_id = _uid()
                approval_date = review_end + timedelta(days=1)

                tasks.append(TimelineTask(
                    id=approval_id,
                    name=f"{permit_name.replace('_', ' ').title()} permit approval",
                    phase=Phase.PERMITS,
                    start_date=approval_date,
                    end_date=approval_date,
                    duration_days=1,
                    dependencies=[review_id],
                    assigned_team=AssignedTeam.PERMITS_TEAM,
                    milestone=True,
                    notes="Expected approval date — follow up if delayed",
                ))

                permit_task_ids.append(approval_id)
                previous_id = tid
                stagger_offset += 5  # stagger each permit by 5 days

            # Insurance procurement
            insurance_id = _uid()
            insurance_start = permit_start + timedelta(days=10)
            insurance_duration = 14

            tasks.append(TimelineTask(
                id=insurance_id,
                name="Procure event insurance",
                phase=Phase.PERMITS,
                start_date=insurance_start,
                end_date=insurance_start + timedelta(days=insurance_duration - 1),
                duration_days=insurance_duration,
                dependencies=[],
                assigned_team=AssignedTeam.PERMITS_TEAM,
                notes="General liability and event cancellation coverage",
            ))
            permit_task_ids.append(insurance_id)

        # ---- Phase 2: PROCUREMENT ----
        procurement_task_ids: list[str] = []
        procurement_start = target_activation_date - timedelta(
            days=60 + weather_buffer
        )

        if has_permanent:
            tid = _uid()
            dur = max(max_lead_time, 21)
            tasks.append(TimelineTask(
                id=tid,
                name="Order materials for permanent elements",
                phase=Phase.PROCUREMENT,
                start_date=procurement_start,
                end_date=procurement_start + timedelta(days=dur - 1),
                duration_days=dur,
                dependencies=permit_task_ids[:1] if permit_task_ids else [],
                assigned_team=AssignedTeam.PROCUREMENT,
                notes="Longer lead time for permanent installations",
            ))
            procurement_task_ids.append(tid)

        # Equipment rental reservations
        equip_id = _uid()
        equip_start = procurement_start + timedelta(days=5)
        equip_dur = 7
        tasks.append(TimelineTask(
            id=equip_id,
            name="Reserve equipment rentals",
            phase=Phase.PROCUREMENT,
            start_date=equip_start,
            end_date=equip_start + timedelta(days=equip_dur - 1),
            duration_days=equip_dur,
            dependencies=permit_task_ids[:1] if permit_task_ids else [],
            assigned_team=AssignedTeam.PROCUREMENT,
            notes="Tents, tables, chairs, generators, AV equipment",
        ))
        procurement_task_ids.append(equip_id)

        if has_vendors:
            vendor_id = _uid()
            vendor_start = procurement_start + timedelta(days=3)
            vendor_dur = 14
            tasks.append(TimelineTask(
                id=vendor_id,
                name="Vendor coordination and contracts",
                phase=Phase.PROCUREMENT,
                start_date=vendor_start,
                end_date=vendor_start + timedelta(days=vendor_dur - 1),
                duration_days=vendor_dur,
                dependencies=[],
                assigned_team=AssignedTeam.PROCUREMENT,
                notes="Food, market, and service vendor agreements",
            ))
            procurement_task_ids.append(vendor_id)

        if has_construction:
            contractor_id = _uid()
            contractor_start = procurement_start + timedelta(days=7)
            contractor_dur = 10
            tasks.append(TimelineTask(
                id=contractor_id,
                name="Book contractors",
                phase=Phase.PROCUREMENT,
                start_date=contractor_start,
                end_date=contractor_start + timedelta(days=contractor_dur - 1),
                duration_days=contractor_dur,
                dependencies=permit_task_ids[:1] if permit_task_ids else [],
                assigned_team=AssignedTeam.PROCUREMENT,
                notes="Construction crew scheduling and contracts",
            ))
            procurement_task_ids.append(contractor_id)

        # Procurement complete milestone
        proc_complete_id = _uid()
        latest_proc_end = max(
            (t.end_date for t in tasks if t.phase == Phase.PROCUREMENT),
            default=procurement_start + timedelta(days=14),
        )
        tasks.append(TimelineTask(
            id=proc_complete_id,
            name="Procurement complete",
            phase=Phase.PROCUREMENT,
            start_date=latest_proc_end + timedelta(days=1),
            end_date=latest_proc_end + timedelta(days=1),
            duration_days=1,
            dependencies=procurement_task_ids,
            assigned_team=AssignedTeam.PROCUREMENT,
            milestone=True,
        ))
        procurement_task_ids.append(proc_complete_id)

        # ---- Phase 3: SITE PREP ----
        site_prep_task_ids: list[str] = []
        site_prep_start = target_activation_date - timedelta(
            days=14 + weather_buffer
        )

        survey_id = _uid()
        tasks.append(TimelineTask(
            id=survey_id,
            name="Site survey and marking",
            phase=Phase.SITE_PREP,
            start_date=site_prep_start,
            end_date=site_prep_start + timedelta(days=1),
            duration_days=2,
            dependencies=[proc_complete_id],
            assigned_team=AssignedTeam.CONSTRUCTION,
        ))
        site_prep_task_ids.append(survey_id)

        if has_permanent or has_gardens:
            ground_id = _uid()
            ground_start = site_prep_start + timedelta(days=2)
            ground_dur = 5
            tasks.append(TimelineTask(
                id=ground_id,
                name="Ground preparation",
                phase=Phase.SITE_PREP,
                start_date=ground_start,
                end_date=ground_start + timedelta(days=ground_dur - 1),
                duration_days=ground_dur,
                dependencies=[survey_id],
                assigned_team=AssignedTeam.CONSTRUCTION,
                notes="Grading, soil prep, drainage for permanent/garden elements",
            ))
            site_prep_task_ids.append(ground_id)

        infra_id = _uid()
        infra_start = site_prep_start + timedelta(days=3)
        infra_dur = 4
        tasks.append(TimelineTask(
            id=infra_id,
            name="Infrastructure installation",
            phase=Phase.SITE_PREP,
            start_date=infra_start,
            end_date=infra_start + timedelta(days=infra_dur - 1),
            duration_days=infra_dur,
            dependencies=[survey_id],
            assigned_team=AssignedTeam.CONSTRUCTION,
            notes="Power drops, water hookups, temporary utilities",
        ))
        site_prep_task_ids.append(infra_id)

        pathway_id = _uid()
        pathway_start = site_prep_start + timedelta(days=5)
        pathway_dur = 3
        tasks.append(TimelineTask(
            id=pathway_id,
            name="Pathway and fencing installation",
            phase=Phase.SITE_PREP,
            start_date=pathway_start,
            end_date=pathway_start + timedelta(days=pathway_dur - 1),
            duration_days=pathway_dur,
            dependencies=[survey_id],
            assigned_team=AssignedTeam.CONSTRUCTION,
            notes="Pedestrian routes, perimeter fencing, ADA access",
        ))
        site_prep_task_ids.append(pathway_id)

        site_ready_id = _uid()
        latest_prep_end = max(
            (t.end_date for t in tasks if t.phase == Phase.SITE_PREP),
            default=site_prep_start + timedelta(days=7),
        )
        tasks.append(TimelineTask(
            id=site_ready_id,
            name="Site ready",
            phase=Phase.SITE_PREP,
            start_date=latest_prep_end + timedelta(days=1),
            end_date=latest_prep_end + timedelta(days=1),
            duration_days=1,
            dependencies=site_prep_task_ids,
            assigned_team=AssignedTeam.CONSTRUCTION,
            milestone=True,
        ))

        # ---- Phase 4: SETUP ----
        setup_task_ids: list[str] = []
        setup_days = max(1, min(3, int(total_setup_hours / 8) + 1))
        setup_start = target_activation_date - timedelta(days=setup_days)

        if has_construction:
            stage_id = _uid()
            stage_dur = max(1, setup_days - 1)
            tasks.append(TimelineTask(
                id=stage_id,
                name="Stage and structure assembly",
                phase=Phase.SETUP,
                start_date=setup_start,
                end_date=setup_start + timedelta(days=stage_dur - 1),
                duration_days=stage_dur,
                dependencies=[site_ready_id],
                assigned_team=AssignedTeam.CONSTRUCTION,
            ))
            setup_task_ids.append(stage_id)

        equip_place_id = _uid()
        equip_place_start = setup_start + timedelta(days=0 if not has_construction else 1)
        tasks.append(TimelineTask(
            id=equip_place_id,
            name="Equipment placement",
            phase=Phase.SETUP,
            start_date=equip_place_start,
            end_date=equip_place_start,
            duration_days=1,
            dependencies=[site_ready_id] + (setup_task_ids[:1] if setup_task_ids else []),
            assigned_team=AssignedTeam.OPERATIONS,
        ))
        setup_task_ids.append(equip_place_id)

        # Art installation
        art_elements = [e for e in design.elements if e.element_type == "art_installation"]
        if art_elements:
            art_id = _uid()
            tasks.append(TimelineTask(
                id=art_id,
                name="Art installation",
                phase=Phase.SETUP,
                start_date=equip_place_start,
                end_date=equip_place_start + timedelta(days=1),
                duration_days=2,
                dependencies=[site_ready_id],
                assigned_team=AssignedTeam.OPERATIONS,
                notes=f"{len(art_elements)} art piece(s) to install",
            ))
            setup_task_ids.append(art_id)

        if has_vendors:
            vendor_setup_id = _uid()
            vendor_setup_start = target_activation_date - timedelta(days=1)
            tasks.append(TimelineTask(
                id=vendor_setup_id,
                name="Vendor setup",
                phase=Phase.SETUP,
                start_date=vendor_setup_start,
                end_date=vendor_setup_start,
                duration_days=1,
                dependencies=[equip_place_id],
                assigned_team=AssignedTeam.OPERATIONS,
            ))
            setup_task_ids.append(vendor_setup_id)

        safety_id = _uid()
        safety_date = target_activation_date - timedelta(days=1)
        tasks.append(TimelineTask(
            id=safety_id,
            name="Safety inspection",
            phase=Phase.SETUP,
            start_date=safety_date,
            end_date=safety_date,
            duration_days=1,
            dependencies=setup_task_ids.copy(),
            assigned_team=AssignedTeam.OPERATIONS,
            milestone=True,
            notes="Fire marshal, ADA compliance, structural sign-off",
        ))
        setup_task_ids.append(safety_id)

        # Sound / lighting check
        sound_elements = [
            e for e in design.elements
            if e.element_type in ("sound", "lighting", "stage")
        ]
        if sound_elements:
            sl_id = _uid()
            tasks.append(TimelineTask(
                id=sl_id,
                name="Sound and lighting check",
                phase=Phase.SETUP,
                start_date=safety_date,
                end_date=safety_date,
                duration_days=1,
                dependencies=[equip_place_id],
                assigned_team=AssignedTeam.OPERATIONS,
                notes="Full AV run-through and level-set",
            ))
            setup_task_ids.append(sl_id)

        # ---- Phase 5: ACTIVATION ----
        activation_task_ids: list[str] = []

        opening_id = _uid()
        tasks.append(TimelineTask(
            id=opening_id,
            name="Opening",
            phase=Phase.ACTIVATION,
            start_date=target_activation_date,
            end_date=target_activation_date,
            duration_days=1,
            dependencies=[safety_id],
            assigned_team=AssignedTeam.OPERATIONS,
            milestone=True,
            notes="Grand opening / ribbon cutting",
        ))
        activation_task_ids.append(opening_id)

        if activation_len > 1:
            ops_id = _uid()
            ops_start = target_activation_date + timedelta(days=1)
            ops_end = activation_end
            tasks.append(TimelineTask(
                id=ops_id,
                name="Daily operations",
                phase=Phase.ACTIVATION,
                start_date=ops_start,
                end_date=ops_end,
                duration_days=(ops_end - ops_start).days + 1,
                dependencies=[opening_id],
                assigned_team=AssignedTeam.OPERATIONS,
                notes="Staff scheduling, crowd management, logistics",
            ))
            activation_task_ids.append(ops_id)

            prog_id = _uid()
            tasks.append(TimelineTask(
                id=prog_id,
                name="Programming schedule",
                phase=Phase.ACTIVATION,
                start_date=target_activation_date,
                end_date=activation_end,
                duration_days=activation_len,
                dependencies=[opening_id],
                assigned_team=AssignedTeam.COMMUNITY,
                notes="Performances, workshops, community events",
            ))
            activation_task_ids.append(prog_id)

            maint_id = _uid()
            tasks.append(TimelineTask(
                id=maint_id,
                name="Maintenance",
                phase=Phase.ACTIVATION,
                start_date=target_activation_date,
                end_date=activation_end,
                duration_days=activation_len,
                dependencies=[opening_id],
                assigned_team=AssignedTeam.OPERATIONS,
                notes="Daily cleaning, repairs, restocking",
            ))
            activation_task_ids.append(maint_id)

        # ---- Phase 6: TEARDOWN ----
        teardown_task_ids: list[str] = []
        teardown_start = activation_end + timedelta(days=1)
        teardown_days = max(1, int(total_teardown_hours / 8) + 1)

        remove_id = _uid()
        tasks.append(TimelineTask(
            id=remove_id,
            name="Remove temporary elements",
            phase=Phase.TEARDOWN,
            start_date=teardown_start,
            end_date=teardown_start + timedelta(days=teardown_days - 1),
            duration_days=teardown_days,
            dependencies=[activation_task_ids[-1]] if activation_task_ids else [],
            assigned_team=AssignedTeam.CONSTRUCTION,
        ))
        teardown_task_ids.append(remove_id)

        return_id = _uid()
        return_start = teardown_start + timedelta(days=1)
        tasks.append(TimelineTask(
            id=return_id,
            name="Equipment return",
            phase=Phase.TEARDOWN,
            start_date=return_start,
            end_date=return_start + timedelta(days=1),
            duration_days=2,
            dependencies=[remove_id],
            assigned_team=AssignedTeam.PROCUREMENT,
            notes="Return all rental equipment, verify condition",
        ))
        teardown_task_ids.append(return_id)

        if has_vendors:
            vendor_dep_id = _uid()
            tasks.append(TimelineTask(
                id=vendor_dep_id,
                name="Vendor departure",
                phase=Phase.TEARDOWN,
                start_date=teardown_start,
                end_date=teardown_start,
                duration_days=1,
                dependencies=[activation_task_ids[-1]] if activation_task_ids else [],
                assigned_team=AssignedTeam.OPERATIONS,
                notes="Vendor pack-up, final settlement, key return",
            ))
            teardown_task_ids.append(vendor_dep_id)

        cleaning_id = _uid()
        cleaning_start = teardown_start + timedelta(days=teardown_days)
        tasks.append(TimelineTask(
            id=cleaning_id,
            name="Site cleaning and restoration",
            phase=Phase.TEARDOWN,
            start_date=cleaning_start,
            end_date=cleaning_start + timedelta(days=1),
            duration_days=2,
            dependencies=teardown_task_ids.copy(),
            assigned_team=AssignedTeam.OPERATIONS,
            notes="Return site to original condition (or better)",
        ))
        teardown_task_ids.append(cleaning_id)

        # ---- Phase 7: PERMANENCE HANDOFF ----
        permanence_task_ids: list[str] = []
        if has_permanent:
            handoff_start = cleaning_start + timedelta(days=2)

            inspect_id = _uid()
            tasks.append(TimelineTask(
                id=inspect_id,
                name="Permanent element inspection",
                phase=Phase.PERMANENCE_HANDOFF,
                start_date=handoff_start,
                end_date=handoff_start + timedelta(days=1),
                duration_days=2,
                dependencies=[cleaning_id],
                assigned_team=AssignedTeam.CONSTRUCTION,
                notes="Structural, safety, and quality assessment",
            ))
            permanence_task_ids.append(inspect_id)

            doc_id = _uid()
            doc_start = handoff_start + timedelta(days=2)
            tasks.append(TimelineTask(
                id=doc_id,
                name="Documentation",
                phase=Phase.PERMANENCE_HANDOFF,
                start_date=doc_start,
                end_date=doc_start + timedelta(days=2),
                duration_days=3,
                dependencies=[inspect_id],
                assigned_team=AssignedTeam.OPERATIONS,
                notes="As-built drawings, material specs, warranty info",
            ))
            permanence_task_ids.append(doc_id)

            ceremony_id = _uid()
            ceremony_date = doc_start + timedelta(days=3)
            tasks.append(TimelineTask(
                id=ceremony_id,
                name="Community handoff ceremony",
                phase=Phase.PERMANENCE_HANDOFF,
                start_date=ceremony_date,
                end_date=ceremony_date,
                duration_days=1,
                dependencies=[doc_id],
                assigned_team=AssignedTeam.COMMUNITY,
                milestone=True,
                notes="Public ceremony transferring stewardship to community",
            ))
            permanence_task_ids.append(ceremony_id)

            maint_plan_id = _uid()
            maint_plan_start = ceremony_date + timedelta(days=1)
            tasks.append(TimelineTask(
                id=maint_plan_id,
                name="Maintenance plan delivery",
                phase=Phase.PERMANENCE_HANDOFF,
                start_date=maint_plan_start,
                end_date=maint_plan_start + timedelta(days=1),
                duration_days=2,
                dependencies=[ceremony_id],
                assigned_team=AssignedTeam.COMMUNITY,
                notes="Seasonal care guide, vendor contacts, budget estimates",
            ))
            permanence_task_ids.append(maint_plan_id)

            report_id = _uid()
            report_start = maint_plan_start + timedelta(days=2)
            tasks.append(TimelineTask(
                id=report_id,
                name="Final reporting",
                phase=Phase.PERMANENCE_HANDOFF,
                start_date=report_start,
                end_date=report_start + timedelta(days=2),
                duration_days=3,
                dependencies=[maint_plan_id],
                assigned_team=AssignedTeam.OPERATIONS,
                milestone=True,
                notes="Budget reconciliation, impact metrics, lessons learned",
            ))
            permanence_task_ids.append(report_id)

        # -----------------------------------------------------------------
        # Compute total duration
        # -----------------------------------------------------------------
        all_dates = [t.start_date for t in tasks] + [t.end_date for t in tasks]
        earliest = min(all_dates) if all_dates else target_activation_date
        latest = max(all_dates) if all_dates else activation_end
        total_duration = (latest - earliest).days + 1

        return Timeline(
            design_id=design.id,
            name=f"Timeline: {design.name}",
            tasks=tasks,
            target_activation_date=target_activation_date,
            activation_end_date=activation_end,
            total_duration_days=total_duration,
            weather_buffer_days=weather_buffer,
            season_warnings=season_warnings,
        )

    # ------------------------------------------------------------------
    # Conflict checking
    # ------------------------------------------------------------------

    def check_conflicts(
        self,
        start_date: date,
        end_date: date,
        location: str = "Philadelphia, PA",
    ) -> ConflictReport:
        """Check for Philadelphia city event conflicts in a date range."""
        conflicts: list[PhillyEvent] = []
        years = set()
        d = start_date
        while d <= end_date:
            years.add(d.year)
            d += timedelta(days=365)
        years.add(end_date.year)

        for year in sorted(years):
            for ev in _resolve_philly_events(year):
                ev_end = ev.end_date or ev.date
                # Ranges overlap?
                if ev.date <= end_date and ev_end >= start_date:
                    conflicts.append(ev)

        has_critical = any(
            c.conflict_level == ConflictLevel.CRITICAL for c in conflicts
        )
        has_high = any(
            c.conflict_level == ConflictLevel.HIGH for c in conflicts
        )

        if has_critical:
            recommendation = (
                "CRITICAL conflicts detected. Strongly recommend choosing "
                "different dates to avoid major city events that will compete "
                "for space, attention, and city resources."
            )
        elif has_high:
            recommendation = (
                "High-impact city events overlap with your date range. "
                "Consider adjusting dates or planning for road closures, "
                "increased traffic, and reduced parking."
            )
        elif conflicts:
            recommendation = (
                "Minor city events overlap with your dates. Plan accordingly "
                "but no major conflicts expected."
            )
        else:
            recommendation = "No known city event conflicts in this date range."

        return ConflictReport(
            checked_range_start=start_date,
            checked_range_end=end_date,
            conflicts=conflicts,
            total_conflicts=len(conflicts),
            has_critical=has_critical,
            recommendation=recommendation,
        )
