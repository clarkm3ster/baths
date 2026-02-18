# BATHS Game Engine - Design Document

## Mission

Build a unified game engine that runs **DOMES** and **SPHERES** — two games teaching people to be Producers by navigating real production pipelines.

**Cosm × Chron = Flourishing** — the civilization equation.

---

## Game 1: DOMES

**Premise:** Build a dome around one person using the entire resources of the US government (the Capitol Dome). Completely anti-scale. Depth over breadth.

**Player role:** Producer navigating the production pipeline

**Production stages:**
1. **Development** — Research the subject, identify legal/data/fiscal needs
2. **Pre-Production** — Design the dome architecture, map all systems
3. **Production** — Execute contracts, build the dome
4. **Post-Production** — Verify completeness, stress-test weakest dimension
5. **Distribution** — Package innovations, IP, story, measure industry impact

**Score: COSM** (minimum of all dimensions — dome is only as strong as its thinnest point)
- **Legal Cosm** — CFR provisions matched, compliance gaps closed
- **Data Cosm** — Systems connected, consent pathways built, data bridges complete
- **Fiscal Cosm** — Cost model accuracy, funding secured
- **Coordination Cosm** — Contracts executed, agencies coordinated
- **Flourishing Cosm** — Philosophy/finance/culture/vitality dimensions balanced
- **Narrative Cosm** — Story coherence, IP generated

**Portfolio output:**
- IP created
- Innovations uncovered (from domes-lab)
- Film/TV story packages
- Industries fundamentally changed (insurance, finance, healthcare, gov contracting)

---

## Game 2: SPHERES

**Premise:** Activate public spaces in cities. Score is square meters unlocked × time. As cities activate everywhere, the scarce resource becomes significance density.

**Player role:** Producer with a portfolio of projects

**Production stages:**
1. **Development** — Identify parcels, research legal/permits
2. **Pre-Production** — Design the activation, model cost/timeline
3. **Production** — Execute permits, build the sphere
4. **Post-Production** — Document the activation, capture episodes
5. **Distribution** — Measure Chron, package story, assess policy impact

**Score: CHRON** (square meters × time, evolving toward significance density)
- **Unlock Chron** — Parcels unlocked, square meters activated
- **Access Chron** — Public access hours, foot traffic
- **Permanence Chron** — Duration of activation (temporary → permanent)
- **Catalyst Chron** — Ripple effects, other spaces activated
- **Policy Chron** — Zoning changes, policy unlocked

**Portfolio output:**
- Parcels activated
- Episodes documented (spheres-viz)
- Innovations generated (spheres-lab)
- Policy changes catalyzed

---

## Game Engine Components

### 1. Player State
```python
{
  "player_id": "uuid",
  "current_game": "domes" | "spheres",
  "active_production": {
    "production_id": "uuid",
    "subject": "...",  # (DOMES) or "parcel_id" (SPHERES)
    "stage": "development" | "pre-production" | "production" | "post-production" | "distribution",
    "progress": 0-100
  },
  "portfolio": {
    "domes_completed": [...],
    "spheres_completed": [...],
    "total_cosm": {...},  # dimension breakdown
    "total_chron": {...},  # dimension breakdown
    "ip_created": [...],
    "innovations": [...],
    "industries_changed": [...]
  }
}
```

### 2. Production Pipeline Director

Orchestrates the player through the five stages, calling the appropriate APIs at each step:

**DOMES Pipeline:**
- Development: domes-profile-research, domes-data-research, domes-legal
- Pre-Production: domes-architect, domes-datamap, domes-flourishing
- Production: domes-contracts, domes-profiles
- Post-Production: domes-brain (verification), domes-lab (innovations)
- Distribution: domes-viz (story), portfolio tracker

**SPHERES Pipeline:**
- Development: spheres-assets, spheres-legal
- Pre-Production: spheres-studio (design + cost)
- Production: spheres-legal (permits), spheres-studio (build)
- Post-Production: spheres-viz (episodes), spheres-lab (innovations)
- Distribution: spheres-brain (metrics), portfolio tracker

### 3. Scoring System

**COSM Calculator:**
- Queries all DOMES APIs for dimension scores
- Takes **minimum** dimension (weakest link principle)
- Updates player portfolio

**CHRON Calculator:**
- Queries spheres-assets (square meters)
- Queries spheres-studio (timeline)
- Multiplies: m² × hours
- Eventually evolves to significance density

### 4. Game Frontend

Dual-game interface:
- Game selector (DOMES / SPHERES)
- Production stage tracker (visual pipeline)
- Real-time dimension scores
- Portfolio dashboard
- API tool palette (call any backend service)

---

## Technical Stack

- **Backend:** FastAPI + SQLite (player state, productions, portfolio)
- **Frontend:** Vite + React + react-router-dom
- **Port:** Backend 9000, Frontend 5300 (avoid conflicts)
- **API Orchestration:** HTTP client calls to existing 17 APIs

---

## Implementation Plan

### Phase 1: Core Engine
- [x] Design document
- [ ] Backend: Player state models + API
- [ ] Backend: Production pipeline director
- [ ] Backend: Scoring calculators (Cosm + Chron)
- [ ] Backend: Portfolio tracker

### Phase 2: Game Frontend
- [ ] Frontend: Game selector
- [ ] Frontend: Production stage UI
- [ ] Frontend: Dimension scoreboard
- [ ] Frontend: Portfolio dashboard
- [ ] Frontend: API tool palette

### Phase 3: Integration
- [ ] Wire frontend to engine backend
- [ ] Wire engine backend to 17 existing APIs
- [ ] Test DOMES production run end-to-end
- [ ] Test SPHERES production run end-to-end

### Phase 4: Evolution
- [ ] Multi-player support
- [ ] Leaderboards
- [ ] IP marketplace
- [ ] Innovation sharing
- [ ] Policy impact visualization

---

## API Registry Integration

The engine will consume `api-registry.json` to discover and call the 17 backends dynamically.

Example call flow:
```python
# Player enters Development stage for DOMES
→ Engine calls domes-profile-research API
→ Engine calls domes-data-research API
→ Engine calls domes-legal API
→ Engine synthesizes results
→ Player proceeds to Pre-Production
```

---

**Next:** Build the backend game engine (player state, pipeline director, scoring).
