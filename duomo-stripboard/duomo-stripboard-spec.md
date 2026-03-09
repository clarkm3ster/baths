# DUOMO Production Stripboard — Architecture Spec

## Concept Mapping: Film Production → Person Production

| Film Scheduling         | DUOMO Equivalent                              |
|------------------------|-----------------------------------------------|
| Production             | A Person's DUOMO (their whole-person profile) |
| Script                 | Circumstances + Narrative                     |
| Scene                  | A Life Domain (health, justice, housing, etc.) |
| Scene Strip            | A System Intervention (Medicaid, DOC, etc.)   |
| Cast Member            | Government System / Agency                    |
| Department             | Domain Category (health, justice, housing...)  |
| Day Out of Days (DOOD) | Timeline of system engagements over 12 months |
| Call Sheet             | Today's coordination actions for this person  |
| Budget                 | Fragmented cost vs Coordinated cost           |
| Strip Color            | Domain color + severity/priority              |
| Board                  | The full stripboard view of all interventions |
| Breakdown              | Per-domain drill-down of provisions/gaps/bridges |

## Design Direction

- **Dark theme**: #0a0a0f background, #c9a84c gold, #f5f0e8 ivory
- **Aesthetic**: "A24 meets Movie Magic Scheduling" — cinematic but functional
- **Layout**: Full-viewport dashboard (no body scroll). Sidebar + header + main.
- **Color accents per domain**: Health=#1A6B3C, Justice=#8B1A1A, Housing=#1A3D8B, Income=#6B5A1A
- **Typography**: System UI for body, monospace for data/IDs, Georgia serif for headings

## Views (sidebar navigation)

### 1. BOARD (Stripboard) — Default view
Horizontal scrolling kanban. Each column = one domain. Each strip = one system.
Strips show: system label, annual cost, coordination savings %, severity tags.
Color-coded by domain. Ghost strips for gaps (dashed borders).
Top: profile selector dropdown. Split-screen option to compare fragmented vs coordinated.

### 2. BREAKDOWN
Scene-level detail. Select a domain → see all systems, provisions, gaps, bridges.
Collapsible tree structure. Each provision has type badge, relevance note.
Gaps highlighted in red. Bridges in green. Cost breakdown chart per domain.

### 3. SCHEDULE (Day Out of Days)
12-month calendar grid. Rows = systems, Columns = months.
Cells show engagement type: ● active, ◐ partial, ○ pending, ✕ gap.
Color intensity = cost intensity. Hover shows detail popover.
Auto-generated from profile circumstances.

### 4. CALL SHEET
Today's view for one profile. Priority-sorted list of actions.
Each action: system, contact, what's needed, deadline, status.
Printable format. Like StudioBinder's call sheet but for civic coordination.

### 5. BUDGET
Full cost engine visualization. Two-panel: fragmented (left) vs coordinated (right).
Stacked bar charts per domain. Total savings KPI cards at top.
5-year projection line chart. ROI waterfall chart.
Bond pricing section (from finance module).

### 6. SLATE (Apollo Slate)
The existing stripboard.js config for DUOMO — "The First 10 Connectomes"
Already built. Import stripboard.js and render the config.

## Data: 5 Productions (Canonical Profiles)

Profiles from seed.py, fully extracted:

### Marcus Thompson (DUOMO-001)
- Age 34, Kensington Philadelphia
- Circumstances: recently_released, substance_use, on_medicaid, homeless, on_probation, on_snap, unemployed
- Systems (10): doc, medicaid, bha, hmis, probation, snap, unemployment, mco, pdmp, shelter
- Domains: health ($45,500), justice ($20,000), housing ($20,000), income ($1,900)
- Total: $87,400 fragmented → $34,200 coordinated = $53,200 savings
- 5yr: $266,000 | Lifetime: $1,085,280

### Sarah Chen (DUOMO-002)
- Age 28, Center City Philadelphia
- Circumstances: has_housing_instability, has_mental_illness, is_on_medicaid, is_on_snap, is_unemployed, has_dv_history, is_in_shelter
- Systems (7): medicaid, bha, hmis, snap, unemployment, court_cms, shelter
- Domains: health, justice, housing, income
- Total: $72,200 → $29,100 = $43,100 savings

### James Williams (DUOMO-003)
- Age 52, West Philadelphia
- Circumstances: has_chronic_health, has_disability, is_on_medicaid, is_on_ssdi, is_frequent_er, has_substance_use, is_on_probation
- Systems (7): medicaid, mco, hie, er_frequent, ssdi, bha, probation
- Total: $94,700 → $52,300 = $41,800 savings (est)

### Maria Rodriguez (DUOMO-004)
- Age 16, North Philadelphia
- Circumstances: is_in_foster_care, has_child_in_foster, is_juvenile_justice, has_mental_illness, is_on_medicaid
- Systems (5): sacwis, foster_care, juvenile_court, bha, medicaid
- Total: $68,500 → $31,200 = $37,300 savings (est)

### Robert Jackson (DUOMO-005)
- Age 45, Downtown Philadelphia (no fixed address)
- Circumstances: is_homeless, has_chronic_health, has_substance_use, has_mental_illness, is_on_medicaid, is_frequent_er, is_on_snap, has_disability
- Systems (8): hmis, shelter, medicaid, bha, mco, er_frequent, snap, ssa
- Total: $109,300 → $47,100 = $62,200 savings (est)

## System Benchmarks (from profile_engine.py)

Full system cost data embedded in data layer. 24 systems across 6 domains.
Each has: id, domain, label, annual_cost, coord_savings_pct.

## File Structure

```
duomo-stripboard/
├── index.html        (shell: sidebar + header + main + CSS + router)
├── data.js           (all profile/system/domain/provision data)
├── board.js          (stripboard kanban view)
├── breakdown.js      (domain/provision drill-down)
├── schedule.js       (DOOD calendar)
├── callsheet.js      (daily actions view)
├── budget.js         (cost engine dashboard)
├── slate.js          (Apollo Slate integration)
└── stripboard.js     (shared engine, copied from baths-suite)
```
