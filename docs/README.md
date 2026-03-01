# THE DOME — Whole-Person Operating System

**A comprehensive Python application implementing prevention-based service delivery
to replace fragmented government programs with bespoke, person-centered coordination.**

## Core Concept

Today, government services are delivered through 63+ siloed programs across federal,
state, and local agencies. A single person experiencing homelessness might touch
Medicaid, SNAP, emergency shelter, county jail, the emergency room, and disability
services — each administered by a different agency with no shared view of the whole
person.

THE DOME creates that shared view through:

1. **Identity Resolution** — Link records across 30+ systems into a single person profile
2. **Fiscal Ledger** — Every dollar spent on (or by) a person, from every payer
3. **137-Metric Assessment** — 9 layers of biometric, clinical, economic, social, and other metrics
4. **The Skeleton Key** — A single computation that produces a WholePersonBudget showing all costs by payer, domain, and mechanism
5. **Cascade Detection** — Real-time detection of multi-domain deterioration chains
6. **Intervention Optimization** — Evidence-based selection of interventions with ROI projections
7. **Wrong-Pocket Resolution** — Settlement matrices showing who should pay whom for prevention
8. **Monte Carlo Simulation** — Path A (no intervention) vs Path B (DOME active) projections

## Quick Start

### Using Docker

```bash
docker compose up -d
```

This starts PostgreSQL and the DOME API on port 8000.

### Local Development

```bash
# Install dependencies
pip install -e ".[dev]"

# Run with SQLite (no PostgreSQL needed)
export DOME_DATABASE_URL="sqlite+aiosqlite:///dome.db"
uvicorn dome.main:app --reload

# Run tests
pytest
```

### API Documentation

Once running, visit:
- Interactive docs: http://localhost:8000/docs
- OpenAPI spec: http://localhost:8000/openapi.json

## Computing a Skeleton Key Budget

### Example: Maria (Trajectory 3 — Moderate Net Cost)

```bash
# 1. Create the person
curl -X POST http://localhost:8000/api/v1/persons/ \
  -H "Content-Type: application/json" \
  -d '{
    "person_uid": "dome-maria-034",
    "name_hash": "a1b2c3d4e5f6maria",
    "dob": "1992-03-15",
    "sex_at_birth": "female",
    "employment_status": "gig",
    "current_annual_income": 24000,
    "housing_status": "cost_burdened",
    "household_size": 3,
    "dependents_ages": [6, 4],
    "chronic_conditions": ["pre_diabetes", "hypertension_stage1"],
    "highest_credential": "some_college"
  }'

# 2. Add fiscal events
curl -X POST http://localhost:8000/api/v1/persons/dome-maria-034/fiscal-events \
  -H "Content-Type: application/json" \
  -d '[
    {"event_date": "2025-03-10", "payer_level": "federal", "payer_entity": "CMS-Medicaid",
     "program_or_fund": "Medicaid", "domain": "healthcare", "mechanism": "service_utilization",
     "service_category": "outpatient_visit", "amount_paid": 1400}
  ]'

# 3. Compute the Skeleton Key budget
curl -X POST http://localhost:8000/api/v1/persons/dome-maria-034/budget \
  -H "Content-Type: application/json" \
  -d '{"monte_carlo_iterations": 1000, "include_scenarios": true}'

# 4. Get trajectory classification
curl http://localhost:8000/api/v1/persons/dome-maria-034/trajectory

# 5. Detect cascades
curl -X POST http://localhost:8000/api/v1/persons/dome-maria-034/detect-cascades \
  -H "Content-Type: application/json" \
  -d '{"lookback_months": 12, "min_confidence": 0.3}'

# 6. Run Path A vs Path B simulation
curl -X POST http://localhost:8000/api/v1/persons/dome-maria-034/simulate \
  -H "Content-Type: application/json" \
  -d '{"iterations": 1000, "projection_years": 46}'
```

### Three Example Persons

| Person | Age | Trajectory | Path A Lifetime | DOME Cost | Path B | Net Savings |
|--------|-----|-----------|----------------|-----------|--------|-------------|
| Maria  | 34  | Moderate Net Cost | $868K | $197K | $188K | $483K |
| James  | 42  | High Net Cost | $1.8M | $350K | $280K | $1.17M |
| Sarah  | 28  | Net Contributor | $120K govt cost | $120K | — | 3:1 ROI |

See `tests/fixtures/` for complete JSON profiles of each person.

## Architecture

```
dome/
├── models/          # 35+ Pydantic models (identity, state, budget, cascade, etc.)
├── engines/         # Core computational engines
│   ├── budget_engine.py          # THE SKELETON KEY
│   ├── cascade_detector.py       # 6 cascade types
│   ├── simulator.py              # Monte Carlo whole-life simulation
│   ├── wrong_pocket_analyzer.py  # Cross-payer settlement matrix
│   ├── benefits_cliff.py         # Benefits cliff calculator
│   └── ...
├── api/             # FastAPI routers (persons, budgets, cascades, etc.)
├── data/            # Reference data (63 programs, 6 cascades, 12 interventions)
├── validation/      # Holdout validation, fairness checks, bias audit
├── schemas/         # API request/response schemas
└── db/              # SQLAlchemy async ORM
```

## Key Numbers

- **$20,600** — Federal spend per person per year (FY2025 baseline)
- **$524,625** — Average lifetime taxes paid
- **$316,600** — Average lifetime healthcare spending
- **54%** — Share of Medicaid spending by top 5% of utilizers
- **$35,000–$45,000** — Annual cost of chronic homelessness in reactive services
- **$35,000–$60,000** — Annual cost per incarcerated person
- **6** — Number of cascade types (multi-domain deterioration chains)
- **5** — Fiscal trajectory tiers (net contributor → catastrophic net cost)

## Testing

```bash
pytest                           # Run all tests
pytest tests/test_models/        # Model validation tests
pytest tests/test_engines/       # Engine unit tests
pytest tests/test_api/           # API integration tests
pytest tests/test_validation/    # Fairness + accuracy tests
```

## Documentation

- [SPECIFICATION.md](SPECIFICATION.md) — Full DOME system specification
- [SCHEMA.md](SCHEMA.md) — Complete data model documentation
- [API.md](API.md) — API endpoint reference
- [SKELETON_KEY.md](SKELETON_KEY.md) — The Skeleton Key concept in depth
