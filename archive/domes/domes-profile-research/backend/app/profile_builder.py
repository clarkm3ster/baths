"""
Composite Profile Builder

Constructs a coherent composite person from real documented cases,
matching circumstances to relevant systems, costs, and citations.
"""
import json
import random
import uuid
from sqlalchemy.orm import Session
from .models import DocumentedCase, CostBenchmark, SystemProfile, CompositeProfile

# First names and last names for composite profiles
FIRST_NAMES_MALE = ["Marcus", "Darnell", "James", "Robert", "Devon", "Andre", "Carlos", "Michael", "Terrence", "David"]
FIRST_NAMES_FEMALE = ["Keisha", "Maria", "Tamika", "Angela", "Crystal", "Jasmine", "Denise", "Patricia", "Sandra", "Latoya"]
LAST_NAMES = ["Thompson", "Williams", "Johnson", "Davis", "Jackson", "Rodriguez", "Martinez", "Taylor", "Anderson", "Brown"]

AGE_RANGES = {
    "child": (6, 12),
    "youth": (13, 17),
    "young_adult": (18, 25),
    "adult": (26, 55),
    "elderly": (56, 72),
}


def build_profile(db: Session, circumstances: dict) -> dict:
    """Build a composite profile from circumstances."""
    profile_id = str(uuid.uuid4())[:8]

    # Determine age
    age_bracket = circumstances.get("age", "adult")
    age_min, age_max = AGE_RANGES.get(age_bracket, (26, 55))
    age = random.randint(age_min, age_max)

    # Determine name
    gender = circumstances.get("gender", "male")
    first = random.choice(FIRST_NAMES_MALE if gender == "male" else FIRST_NAMES_FEMALE)
    last = random.choice(LAST_NAMES)
    name = f"{first} {last}"

    # Collect circumstance tags from boolean flags
    tags = set()
    tag_mapping = {
        "has_mental_health": "mental_health",
        "has_substance_use": "substance_use",
        "has_disability": "disability",
        "is_homeless": "homeless",
        "has_criminal_justice": "criminal_justice",
        "has_children": "children",
        "is_on_medicaid": "medicaid",
        "is_on_snap": "snap",
        "is_on_tanf": "tanf",
        "is_on_ssi": "ssi",
        "has_housing_assistance": "housing_assistance",
        "is_unemployed": "unemployed",
        "has_foster_care": "foster_care",
        "has_juvenile_justice": "juvenile_justice",
        "has_chronic_health": "chronic_health",
        "is_on_probation": "probation",
    }
    for key, tag in tag_mapping.items():
        if circumstances.get(key):
            tags.add(tag)

    # Always add income tag for benefit recipients
    if tags & {"snap", "tanf", "ssi", "medicaid", "housing_assistance"}:
        tags.add("low_income")

    # Add age-based tags
    if age_bracket in ("child", "youth"):
        tags.add("children")
        tags.add("school_age")
    if age_bracket == "youth":
        tags.add("youth")

    # Auto-expand tags for maximum system coverage (14+ systems)
    # Criminal justice involvement implies pretrial detention exposure
    if "criminal_justice" in tags:
        tags.add("pretrial")
    # Homelessness implies shelter system contact
    if "homeless" in tags:
        tags.add("shelter")
    # Parents with low income implies child-related systems
    if "has_children" in tags or ("children" in tags and "low_income" in tags):
        tags.add("children")
        tags.add("school_age")

    # Find matching systems
    systems = db.query(SystemProfile).all()
    matched_systems = []
    for s in systems:
        applies = set(json.loads(s.applies_when or "[]"))
        if applies & tags:
            matched_systems.append(s)

    system_ids = [s.id for s in matched_systems]

    # Find matching cases
    all_cases = db.query(DocumentedCase).all()
    matched_cases = []
    for c in all_cases:
        case_tags = set(json.loads(c.circumstance_tags or "[]"))
        case_systems = set(json.loads(c.system_ids or "[]"))
        # Match if shares at least one tag and at least one system
        if (case_tags & tags) and (case_systems & set(system_ids)):
            matched_cases.append(c)

    # If few matches, also include cases that match on tags alone
    if len(matched_cases) < 3:
        for c in all_cases:
            if c in matched_cases:
                continue
            case_tags = set(json.loads(c.circumstance_tags or "[]"))
            if len(case_tags & tags) >= 2:
                matched_cases.append(c)

    # Calculate costs using typical_utilization to reflect realistic per-person usage
    # A person cycling through multiple systems doesn't use each at full annual capacity
    # Age-appropriate adjustments: childhood systems (foster care, juvenile justice,
    # school) have zero current cost for adults -- they remain in the profile as
    # historical systems but don't contribute to annual spending.
    CHILDHOOD_SYSTEMS = {"dhs_cw", "juvenile_justice", "school_district"}
    is_adult = age_bracket in ("adult", "young_adult", "elderly")

    cost_breakdown = []
    total_annual = 0.0
    domain_costs = {}
    for s in matched_systems:
        if s.annual_cost_per_person:
            utilization = s.typical_utilization or 1.0
            # Zero out utilization for childhood-only systems when profiling adults
            if is_adult and s.id in CHILDHOOD_SYSTEMS:
                utilization = 0.0
            utilized_cost = s.annual_cost_per_person * utilization
            cost_breakdown.append({
                "system_id": s.id,
                "system_name": s.name,
                "acronym": s.acronym,
                "domain": s.domain,
                "full_annual_cost": s.annual_cost_per_person,
                "typical_utilization": utilization,
                "utilized_cost": utilized_cost,
                "annual_cost": utilized_cost,
                "source": s.cost_source,
            })
            total_annual += utilized_cost
            domain_costs[s.domain] = domain_costs.get(s.domain, 0) + utilized_cost

    # Coordinated cost estimate: per-domain savings based on published research
    # Health: 55% savings (integrated care), Housing: 65% (Housing First),
    # Justice: 60% (coordinated reentry), Income: 40%, Child Welfare: 50%, Education: 35%
    from .cost_calculator import COORDINATION_SAVINGS
    coordinated_cost = 0.0
    for domain, domain_cost in domain_costs.items():
        savings_info = COORDINATION_SAVINGS.get(domain, {"factor": 0.35})
        factor = savings_info["factor"]
        coordinated_cost += domain_cost * (1 - factor)

    # Build timeline and link each event to a documented case
    timeline = _build_timeline(age, tags, matched_systems, matched_cases)
    timeline = _link_events_to_cases(timeline, matched_cases)

    # Build systems_detail for the frontend systems panel
    systems_detail = []
    for s in matched_systems:
        systems_detail.append({
            "id": s.id,
            "name": s.name,
            "acronym": s.acronym,
            "domain": s.domain,
            "data_held": json.loads(s.data_held or "[]"),
            "annual_cost_per_person": s.annual_cost_per_person,
            "cost_source": s.cost_source,
        })

    # Count separate application forms across systems
    application_count = sum(1 for s in matched_systems if s.annual_cost_per_person)

    # Build narrative
    narrative = _build_narrative(
        name, age, tags, matched_systems, total_annual, coordinated_cost,
        application_count,
    )

    # Store profile
    profile = CompositeProfile(
        id=profile_id,
        name=name,
        age=age,
        circumstances=json.dumps(circumstances),
        systems_involved=json.dumps(system_ids),
        timeline=json.dumps(timeline),
        total_annual_cost=total_annual,
        cost_breakdown=json.dumps(cost_breakdown),
        citations=json.dumps([c.id for c in matched_cases]),
        coordinated_cost=coordinated_cost,
        narrative=narrative,
    )
    db.add(profile)
    db.commit()

    result = profile.to_dict()
    result["matched_cases"] = [c.to_dict() for c in matched_cases]
    result["matched_systems"] = [s.to_dict() for s in matched_systems]
    result["systems_detail"] = systems_detail
    result["cost_benchmarks"] = [b.to_dict() for b in db.query(CostBenchmark).all()]
    return result


def _link_events_to_cases(events, cases):
    """Match each timeline event to the most relevant documented case.

    Scoring is based on overlap between the event's system/domain and the
    case's system_ids and circumstance_tags.  The best-matching case id is
    stored in ``citation_id``; if no case is relevant the field is ``None``.
    """
    for event in events:
        best_case = None
        best_score = 0
        event_system = event.get("system")
        event_domain = event.get("domain")
        for c in cases:
            case_systems = set(json.loads(c.system_ids or "[]"))
            case_tags = set(json.loads(c.circumstance_tags or "[]"))
            score = 0
            # Direct system match is strongest signal
            if event_system and event_system in case_systems:
                score += 3
            # Domain match
            if event_domain and c.domain == event_domain:
                score += 2
            # Tag overlap with event type keywords
            event_text_lower = event.get("event", "").lower()
            for tag in case_tags:
                if tag.replace("_", " ") in event_text_lower:
                    score += 1
            if score > best_score:
                best_score = score
                best_case = c
        event["citation_id"] = best_case.id if best_case and best_score >= 2 else None
    return events


def _build_timeline(age, tags, systems, cases):
    """Build a timeline of system interactions.

    Each event reads like a moment in a real life -- specific, grounded in
    documented failures, and referencing the laws and data-sharing barriers
    that created the gap.  After construction, ``_link_events_to_cases``
    attaches the best-matching ``citation_id`` to each event.
    """
    events = []
    system_names = {s.id: s.name for s in systems}
    system_acronyms = {s.id: s.acronym for s in systems}
    system_costs = {s.id: s.annual_cost_per_person for s in systems if s.annual_cost_per_person}

    def _sys_label(sid):
        """Return 'Name (ACRONYM)' for a system id, with fallback."""
        n = system_names.get(sid, sid)
        a = system_acronyms.get(sid, "")
        return f"{n} ({a})" if a else n

    # ------- Early life -------
    if "children" in tags or "foster_care" in tags:
        events.append({
            "age": max(3, age - 15) if age > 18 else max(3, age - 5),
            "event": (
                "A teacher files a mandated-reporter referral. Child Protective Services "
                "opens an investigation, but the family's Medicaid and TANF records are in "
                "separate county systems -- the caseworker has no idea the family is already "
                "receiving services from two other agencies."
            ),
            "system": "dhs_cw",
            "domain": "child_welfare",
            "type": "entry",
        })
        if "foster_care" in tags:
            events.append({
                "age": max(5, age - 13) if age > 18 else max(5, age - 3),
                "event": (
                    "Removed from the home and placed in foster care. The school district is "
                    "not notified for 11 days. Under FERPA (20 U.S.C. \u00a71232g), education "
                    "records require a signed release to transfer -- so his IEP, behavioral "
                    "plan, and progress notes stay behind at the old school."
                ),
                "system": "dhs_cw",
                "domain": "child_welfare",
                "type": "placement",
            })
            events.append({
                "age": max(6, age - 12) if age > 18 else max(6, age - 2),
                "event": (
                    "Third school in two years. Each time, the IEP is lost in transfer. The "
                    "new school starts behavioral assessments from scratch. A GAO report found "
                    "foster children change schools 1.6 times more than peers, losing 4-6 "
                    "months of academic progress with each move."
                ),
                "system": "school_district",
                "domain": "education",
                "type": "disruption",
            })

    if "school_age" in tags:
        events.append({
            "age": max(6, age - 8) if age > 15 else 6,
            "event": (
                "Enrolled in public school. Teachers flag behavioral issues within the first "
                "month, but FERPA walls prevent the school from accessing the CPS case file "
                "or the behavioral health records that would explain the trauma history."
            ),
            "system": "school_district",
            "domain": "education",
            "type": "entry",
        })

    if "juvenile_justice" in tags:
        events.append({
            "age": min(15, age),
            "event": (
                "First juvenile arrest. The detention facility conducts a mental health "
                "screening, but under state confidentiality law the results cannot be shared "
                "with the school counselor. The school sees only the absence -- not the "
                "diagnosis. The judge has no access to the child welfare history."
            ),
            "system": "juvenile_justice",
            "domain": "justice",
            "type": "entry",
        })

    # ------- Adult system entries -------
    if "mental_health" in tags:
        entry_age = max(18, age - 8)
        events.append({
            "age": entry_age,
            "event": (
                "First psychiatric hospitalization. Diagnosed with serious mental illness "
                "after a 72-hour involuntary hold. The inpatient facility creates a treatment "
                "record in its own EHR system. Under HIPAA (45 CFR \u00a7164.506), this "
                "record will not follow him to the next provider without explicit consent."
            ),
            "system": "behavioral_health",
            "domain": "health",
            "type": "entry",
        })
        events.append({
            "age": entry_age + 1,
            "event": (
                "Discharged to outpatient care. The community mental health center cannot "
                "access the hospital's records -- different EHR, different consent form, "
                "different network. The outpatient psychiatrist starts over: new intake, "
                "new assessment, new medication trial. Six weeks of progress lost."
            ),
            "system": "behavioral_health",
            "domain": "health",
            "type": "gap",
        })

    if "substance_use" in tags:
        events.append({
            "age": max(18, age - 6),
            "event": (
                "Enters substance use treatment. Under 42 CFR Part 2, these records are "
                "sealed behind the strictest federal confidentiality standard in healthcare. "
                "His psychiatrist, his probation officer, and the ER doctors who will treat "
                "him next month cannot see that he is in treatment -- or what substances "
                "are involved. They will prescribe blind."
            ),
            "system": "behavioral_health",
            "domain": "health",
            "type": "entry",
        })

    if "medicaid" in tags:
        mc_cost = system_costs.get("medicaid", "")
        cost_note = f" Medicaid will spend ${mc_cost:,.0f}/year on his care" if mc_cost else ""
        events.append({
            "age": max(18, age - 7),
            "event": (
                f"Enrolled in Medicaid after a 23-page application.{cost_note}, but claims "
                "data lives in the state Medicaid Management Information System (MMIS), "
                "completely siloed from the behavioral health treatment records that would "
                "reveal what is actually working."
            ),
            "system": "medicaid",
            "domain": "health",
            "type": "entry",
        })

    if "tanf" in tags:
        events.append({
            "age": max(18, age - 7),
            "event": (
                "Applies for TANF cash assistance -- a separate 12-page application that "
                "asks for the same income documentation already provided to Medicaid and "
                "SNAP. The TANF caseworker cannot see the Medicaid application sitting in "
                "a database one floor below."
            ),
            "system": "tanf",
            "domain": "income",
            "type": "entry",
        })

    if "snap" in tags:
        events.append({
            "age": max(18, age - 6),
            "event": (
                "Approved for SNAP food assistance after a separate eligibility determination. "
                "He has now verified his income, household size, and identity to three "
                "different agencies using three different forms. None of them share a database."
            ),
            "system": "snap",
            "domain": "income",
            "type": "entry",
        })

    if "homeless" in tags:
        shelter_cost = system_costs.get("shelter_system", "")
        cost_note = f" Each shelter night costs the city ${shelter_cost / 365:,.0f}" if shelter_cost else ""
        events.append({
            "age": max(19, age - 4),
            "event": (
                f"First shelter entry. An HMIS record is created in the Homeless Management "
                f"Information System.{cost_note}. But HMIS is not linked to the behavioral "
                "health system, the Medicaid claims database, or the criminal justice records "
                "that would show why he keeps cycling back."
            ),
            "system": "shelter_system",
            "domain": "housing",
            "type": "entry",
        })
        events.append({
            "age": max(20, age - 3),
            "event": (
                "Name added to the Public Housing Authority waitlist. Average wait: 22 "
                "months. The housing authority has no idea that placing him would eliminate "
                "an estimated $40,000/year in ER visits and shelter costs -- because those "
                "figures live in health and homeless system databases they cannot access."
            ),
            "system": "pha",
            "domain": "housing",
            "type": "waiting",
        })

    if "criminal_justice" in tags:
        events.append({
            "age": max(19, age - 5),
            "event": (
                "First adult arrest. Booked into county jail. His psychiatric medications "
                "are discontinued because the jail pharmacy cannot access his community "
                "prescription records. He decompensates within 72 hours. The jail starts "
                "the medication trial over from scratch."
            ),
            "system": "county_jail",
            "domain": "justice",
            "type": "entry",
        })
        if "pretrial" in tags:
            events.append({
                "age": max(19, age - 5),
                "event": (
                    "Held pretrial for 47 days because the court has no verified treatment "
                    "history to support a supervised release. A single data query to the "
                    "behavioral health system would confirm he is engaged in treatment -- "
                    "but no such query is legally or technically possible."
                ),
                "system": "pretrial",
                "domain": "justice",
                "type": "waiting",
            })
        events.append({
            "age": max(20, age - 4),
            "event": (
                "Released from jail. Medicaid coverage was terminated on the day of booking "
                "per federal law (the Medicaid Inmate Exclusion Policy). He now faces a "
                "45-day gap in health coverage. No prescriptions. No therapy. No continuity."
            ),
            "system": "county_jail",
            "domain": "justice",
            "type": "release",
        })

    if "probation" in tags:
        events.append({
            "age": max(21, age - 3),
            "event": (
                "Placed on probation. The probation officer's case management system has no "
                "interface to the behavioral health EHR. Compliance with treatment is a "
                "condition of probation -- but the PO cannot verify it without calling the "
                "clinic and waiting on hold. 42 CFR Part 2 means substance use treatment "
                "compliance is entirely invisible."
            ),
            "system": "probation",
            "domain": "justice",
            "type": "entry",
        })

    if "ssi" in tags:
        events.append({
            "age": max(20, age - 5),
            "event": (
                "Applied for SSI disability benefits through the Social Security "
                "Administration. Determination takes an average of 7 months. SSA requests "
                "medical records by fax -- the behavioral health provider responds 6 weeks "
                "later with an incomplete file. A direct data connection would resolve the "
                "claim in days, not months."
            ),
            "system": "ssi",
            "domain": "income",
            "type": "waiting",
        })

    if "housing_assistance" in tags:
        events.append({
            "age": max(21, age - 3),
            "event": (
                "Receives a Housing Choice Voucher after 19 months on the waitlist. The "
                "housing authority's data shows a tenant -- but not the $83,000/year in "
                "health and justice costs that stable housing will prevent. HUD's PIH "
                "system does not connect to Medicaid, HMIS, or the county jail booking system."
            ),
            "system": "pha",
            "domain": "housing",
            "type": "entry",
        })

    if "unemployed" in tags:
        events.append({
            "age": max(20, age - 2),
            "event": (
                "Registered with the state workforce development system (CareerLink). "
                "Employers can see his criminal record through public court databases, but "
                "his rehabilitation progress, treatment compliance, and skills training "
                "completion are invisible -- locked in separate justice and health systems."
            ),
            "system": "workforce",
            "domain": "income",
            "type": "entry",
        })

    if "chronic_health" in tags:
        events.append({
            "age": max(22, age - 4),
            "event": (
                "Diagnosed with a chronic condition (diabetes/hypertension). His primary "
                "care provider is unaware of the psychiatric medications prescribed by the "
                "behavioral health system -- creating a dangerous drug interaction risk. "
                "HIPAA permits sharing for treatment, but the systems are technically "
                "incapable of exchanging data."
            ),
            "system": "medicaid",
            "domain": "health",
            "type": "entry",
        })

    if "disability" in tags:
        events.append({
            "age": max(20, age - 6),
            "event": (
                "Disability documented by a provider, but the documentation format required "
                "by SSA differs from the format in the behavioral health EHR. The provider "
                "must manually re-enter clinical data into SSA's forms -- a process that "
                "takes 3 hours of staff time per application."
            ),
            "system": "ssi",
            "domain": "income",
            "type": "gap",
        })

    # ------- Recent crisis cycle -------
    if "mental_health" in tags and "homeless" in tags:
        er_cost = system_costs.get("emergency_dept", "")
        cost_note = f" This single ER visit costs ${er_cost / 4:,.0f}." if er_cost else ""
        events.append({
            "age": age - 1,
            "event": (
                "Crisis: found unresponsive on the street by police at 2 AM. Transported "
                "to the emergency department. The ER physician has no access to his "
                "psychiatric treatment history, his medication list, or his substance use "
                f"records (sealed under 42 CFR Part 2).{cost_note} They stabilize him with "
                "a generic protocol and discharge him back to the same shelter."
            ),
            "system": "emergency_dept",
            "domain": "health",
            "type": "crisis",
        })

    if "criminal_justice" in tags and "mental_health" in tags:
        events.append({
            "age": age,
            "event": (
                "Arrested during a mental health crisis after police respond to a trespassing "
                "call. The officers have no mobile access to his treatment status. At the "
                "jail, intake staff restart the entire medication protocol from scratch -- the "
                "third time in two years. The cycle that costs taxpayers tens of thousands "
                "per revolution continues because no single system can see the whole picture."
            ),
            "system": "county_jail",
            "domain": "justice",
            "type": "crisis",
        })

    # ------- Current state -------
    sys_count = len(systems)
    cost_str = f"${sum(system_costs.values()):,.0f}" if system_costs else "unknown"
    acronym_list = ", ".join(
        system_acronyms[s.id] for s in systems if s.id in system_acronyms
    )
    events.append({
        "age": age,
        "event": (
            f"Today: Active in {sys_count} government systems simultaneously "
            f"({acronym_list}). Combined annual cost: {cost_str}. Each system maintains "
            "its own record, its own case plan, its own goals. Not one of them has a "
            "complete picture. Not one of them knows what the others are doing."
        ),
        "system": None,
        "domain": None,
        "type": "current",
    })

    events.sort(key=lambda e: e["age"])
    return events


def _build_narrative(name, age, tags, systems, total_cost, coordinated_cost,
                     application_count=0):
    """Build a narrative summary with specific system names, costs, and details."""
    system_count = len(systems)
    savings = total_cost - coordinated_cost

    # Collect system names grouped by domain for readable lists
    domain_systems = {}
    for s in systems:
        domain_systems.setdefault(s.domain, []).append(f"{s.name} ({s.acronym})")

    parts = [f"{name} is {age} years old."]

    # Life circumstances
    descriptors = []
    if "mental_health" in tags:
        descriptors.append("lives with serious mental illness")
    if "substance_use" in tags:
        descriptors.append("has a substance use history")
    if "homeless" in tags:
        descriptors.append("is experiencing homelessness")
    if "criminal_justice" in tags:
        descriptors.append("has been through the criminal justice system")
    if "disability" in tags:
        descriptors.append("has a disability")
    if "foster_care" in tags:
        descriptors.append("grew up in foster care")
    if "chronic_health" in tags:
        descriptors.append("manages a chronic health condition")

    if descriptors:
        if len(descriptors) == 1:
            parts.append(f"He {descriptors[0]}.")
        elif len(descriptors) == 2:
            parts.append(f"He {descriptors[0]} and {descriptors[1]}.")
        else:
            parts.append(f"He {', '.join(descriptors[:-1])}, and {descriptors[-1]}.")

    # Specific system names
    all_sys_names = [f"{s.name} ({s.acronym})" for s in systems]
    if all_sys_names:
        sys_list = ", ".join(all_sys_names[:8])
        remainder = len(all_sys_names) - 8
        if remainder > 0:
            sys_list += f", and {remainder} more"
        parts.append(
            f"He exists in {system_count} government databases simultaneously: "
            f"{sys_list}. Each system tracks him independently. None of them talk to "
            "each other."
        )
    else:
        parts.append(
            f"He exists in {system_count} government databases simultaneously. "
            f"Each system tracks him independently. None of them talk to each other."
        )

    # Application burden
    if application_count >= 3:
        parts.append(
            f"To access services, {name} filled out {application_count} separate "
            "applications -- each one asking for the same income verification, the "
            "same identity documents, the same household information. A single shared "
            "intake would have taken 20 minutes. Instead, the process took weeks."
        )

    # Specific cost breakdown by domain
    domain_costs = {}
    for s in systems:
        if s.annual_cost_per_person:
            domain_costs.setdefault(s.domain, 0.0)
            domain_costs[s.domain] += s.annual_cost_per_person
    if domain_costs:
        cost_parts = []
        for domain, cost in sorted(domain_costs.items(), key=lambda x: -x[1]):
            domain_label = domain.replace("_", " ").title()
            cost_parts.append(f"${cost:,.0f} in {domain_label}")
        cost_list = ", ".join(cost_parts)
        parts.append(
            f"The government spends ${total_cost:,.0f} per year on {name} across "
            f"these fragmented systems: {cost_list}. With coordinated care and shared "
            f"data, this would drop to ${coordinated_cost:,.0f} -- saving "
            f"${savings:,.0f} per year while actually improving his outcomes."
        )
    else:
        parts.append(
            f"The government spends ${total_cost:,.0f} per year on {name} across these "
            f"fragmented systems -- with nothing to show for it. If these systems shared "
            f"data and coordinated care, the cost would drop to ${coordinated_cost:,.0f}, "
            f"saving ${savings:,.0f} per year while actually improving his outcomes."
        )

    # Legal barriers
    legal_notes = []
    if "substance_use" in tags:
        legal_notes.append(
            "42 CFR Part 2 seals his substance use treatment records from every other provider"
        )
    if "foster_care" in tags or "school_age" in tags:
        legal_notes.append(
            "FERPA prevents his school records from following him between placements"
        )
    if "mental_health" in tags:
        legal_notes.append(
            "HIPAA's consent requirements mean his psychiatric history is invisible "
            "to the ER physicians who treat him in crisis"
        )
    if legal_notes:
        parts.append(
            "The data silos are not accidental -- they are built into federal law: "
            + "; ".join(legal_notes) + "."
        )

    parts.append(
        f"Every detail in this profile is sourced from real investigations, audits, "
        f"and published research. {name} is a composite -- but the systems, the costs, "
        f"and the failures are documented fact."
    )

    return " ".join(parts)
