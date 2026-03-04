# CLAUDE.md — DOMES Platform

## What This Is
DOMES is one half of BATHS, a civic production company. DOMES points the Hubble
telescope at a **person**. SPHERES (a separate platform, separate repo) points it
at a **place**. This repo is DOMES only.

DOMES creates whole-person digital twins — the most comprehensive longitudinal
representation of a single human life ever attempted. The founding proof case is
Robert Jackson: 47 ER visits/year, $112K annual cost, touching 63 fragmented
government programs that never talk to each other.

## Core Philosophy
**Cosm x Chron = Flourishing**
- Cosm = 12 domains of a person's life (the breadth)
- Chron = the 5-year temporal arc (the depth)
- Multiply them → the full picture no single agency has ever seen

## The 12 BATHS Domains
1. Housing — stability, type, transitions, risk of loss
2. Health — physical, mental, behavioral, substance use, ER utilization
3. Income & Employment — wages, benefits, barriers
4. Education & Skills — literacy, credentials, digital fluency
5. Legal & Justice — involvement, reentry, warrants, child welfare
6. Social & Family — support network, isolation, caregiving
7. Food & Nutrition — security, access, quality
8. Transportation — access, reliability, cost burden
9. Financial — debt, credit, banking status, predatory exposure
10. Civic & Identity — documentation, voting, community participation
11. Digital & Connectivity — internet, devices, digital skills
12. Safety & Environment — neighborhood conditions, exposure, climate risk

## Non-Negotiable Architectural Boundary
- DOMES MUST NOT contain SPHERES code: no spaces, no BELOW, no venues, no
  environmental telemetry for places, no booking, no Season/Episodes, no
  material innovation catalog, no SPHERE/OS.
- If you encounter SPHERES files → move to /archive/spheres/ or delete.
- DOMES is PII/sensitive-data oriented. Default to strict permissions,
  auditability, and least-privilege.

## Key Architecture Components

### Settlement Matrix (shared engine, also used by SPHERES)
Solves the "trillion wrong-pocket problem." When housing Robert Jackson saves
$112K/year in ER costs:
- Who pays for the housing? (HUD, local authority)
- Who saves? (Medicaid, hospital, police/EMS)
- Who should reimburse whom? (the settlement)
Core types: CostEvent, PayerEntity, SavingsAttribution, SettlementProposal

### Person Model (Event-Sourced)
Every person is an event stream, not a static record.
Events: IntakeAssessed, InterventionStarted, CrisisOccurred, MilestoneReached,
DomainScoreChanged
Current state = projection of all past events
Enables: counterfactual simulation ("what if intervention X happened 6mo earlier?")

### Show-Runner Framework
Each person's 5-year arc = producing a show:
- Director (lead coordinator), Talent Team (multi-disciplinary specialists)
- Production Bible (intervention plan as living document)
- Episodes (intake → stabilization → growth → independence → contribution)
- IP Generation (learnings refine Dome OS)

### Self-Sovereign Portal
The person MUST own their twin. Non-negotiable ethical architecture:
- View everything known about them
- Correct inaccuracies
- Control data sharing consent per domain, per agency
- See who accessed their data and why
- Opt out with full data export

### Biological & Insurance Layers
- Biological: RCT-ready health tracking, biomarker trends, ER utilization curves
- Insurance/Risk: actuarial modeling, risk score trajectories, premium impact
- Financial: cross-payer cost tracking, benefits utilization, ROI per intervention

## Tech Stack
- Frontend: Next.js 14+ App Router / TypeScript
- Styling: Tailwind CSS + shadcn/ui + lucide-react
- Animation: Framer Motion (spring-based, cinematic)
- Charts: Recharts for radar + timelines, D3 for Sankey diagrams
- API: Next.js route handlers (mock now, real DB later)
- Contracts: Zod schemas in /src/lib/contracts/
- Database (future): Isolated Supabase project for PII protection

## Design Language
- Dark theme: deep navy/charcoal (#0a0f1a), NOT pure black
- Accent: warm amber/gold (#f59e0b) — human warmth against institutional precision
- Font: Inter — clean, medical-grade readability
- Feeling: "What it looks like when civilization decides to truly see one person"
- Motion: slow, deliberate reveals. Spring easing. Nothing flashy.
- Hero visual: 12-domain radar chart — it should feel like looking through the telescope
- Loading: skeleton screens, never spinners

## Seed Characters

### Robert Jackson — "The Permanent Crisis"
47 ER visits/year, $112K annual cost, unhoused, severe mental health + substance use
Touches 63 programs, none coordinated. THE thesis case.
Domain scores: Housing:8, Health:12, Income:15, Education:22, Legal:18, Social:11,
Food:25, Transportation:20, Financial:5, Civic:10, Digital:14, Safety:16

### Maria Santos — "The Invisible Juggler"
Working mother, 3 kids, housing-unstable. Uses 12+ programs, falls through every gap.
$47K/yr fragmented spending with declining outcomes.

### David Park — "The Reentry Spiral"
Recently incarcerated, rebuilding. Employment/housing/health barriers at every transition.

## Target File Structure
```
domes/
├── src/
│   ├── app/                    # Next.js app router
│   │   ├── page.tsx            # Landing
│   │   ├── dashboard/          # Main dashboard
│   │   ├── person/[id]/        # Person deep view
│   │   ├── settlement/         # Settlement Matrix explorer
│   │   └── portal/             # Self-sovereign portal
│   ├── components/
│   │   ├── ui/                 # shadcn/ui primitives
│   │   ├── radar-chart/        # 12-domain visualization
│   │   ├── timeline/           # 5-year arc
│   │   ├── settlement-flow/    # Sankey diagram
│   │   └── show-runner/        # Production bible UI
│   ├── lib/
│   │   ├── contracts/          # Zod schemas
│   │   ├── settlement/         # Pure functions + tests
│   │   └── demo-data/          # Seed JSON
│   └── archive/spheres/        # Removed SPHERES files
├── CLAUDE.md
└── package.json
```

## Priority Build Order
P0: Person model + 12-domain radar + Robert Jackson seed data
P0: Settlement Matrix API + Sankey visualization
P1: 5-year timeline with event stream
P1: Show-runner dashboard (director view, talent, intervention plan)
P2: Self-sovereign portal (consent/access)
P2: Counterfactual simulator
P3: Biological layer (ER curves, biomarkers)
P3: Insurance/risk actuarial projections

## Existing Backend Assets (from BATHS monorepo)
The following Python/FastAPI backends contain DOMES logic and seed data:
- backend/ — core legal matching engine (214 provisions, 5 profiles)
- domes-brain/ — central API gateway + service discovery
- domes-data-research/ — data gap analysis
- domes-profile-research/ — profile building + cost calculation
- domes-legal/ — legal provisions DB + Studio (10 OS layers, 57 endpoints)
- domes-profiles/ — profile engine + benchmarks (Marcus, Sarah, James, Maria, Robert)
- domes-contracts/ — smart contracts + compliance
- domes-datamap/ — data bridge engine (31 government systems)
- domes-architect/ — enterprise architecture modeling
- domes-flourishing/ — philosophy + finance + culture + vitality
- domes-lab/ — innovation generation + AI teammates
- domes-viz/ — 3D marble worlds visualization
