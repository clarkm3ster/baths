# BATHS Game Engine

**The unified game engine for DOMES + SPHERES**

Cosm × Chron = Flourishing

---

## What Is This?

A production pipeline game engine that teaches people to be **Producers** by building:

1. **DOMES** — Anti-scale depth. Build a dome around one person using the entire US government. Score: **Cosm** (weakest dimension principle).

2. **SPHERES** — Activate public spaces in cities. Score: **Chron** (m² × time, evolving to significance density).

Both games mirror the film/TV production pipeline:
- Development
- Pre-Production
- Production  
- Post-Production
- Distribution

The engine orchestrates the 17 existing BATHS backend APIs as production tools.

---

## Architecture

```
baths-engine/
├── backend/              # Game engine API (port 9000)
│   ├── models.py         # Player, Production, Portfolio, Scoring
│   ├── pipeline.py       # Production pipeline director
│   ├── main.py           # FastAPI server
│   └── run.py            # Run script
├── frontend/             # Game UI (port 5300)
│   ├── src/
│   │   ├── App.jsx       # Main app
│   │   └── components/
│   │       ├── GameSelector.jsx
│   │       ├── ProductionPipeline.jsx
│   │       └── Portfolio.jsx
│   └── vite.config.js
└── DESIGN.md             # Full design document
```

**Dependencies:**
- 17 existing BATHS APIs (domes-*, spheres-*)
- `api-registry.json` for service discovery

---

## Setup

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

---

## Run

### Start the Game Engine Backend

```bash
cd backend
python run.py
```

Backend will run on **http://localhost:9000**

### Start the Game Frontend

```bash
cd frontend
npm run dev
```

Frontend will run on **http://localhost:5300**

---

## How to Play

1. **Open the game:** http://localhost:5300

2. **Choose a game:**
   - **DOMES** — Enter a person's name
   - **SPHERES** — Enter a parcel ID

3. **Navigate the production pipeline:**
   - Click "Advance Stage" to move through Development → Distribution
   - The engine calls the appropriate backend APIs at each stage
   - Watch your Cosm/Chron scores grow

4. **Build your portfolio:**
   - Complete productions
   - Generate IP and innovations
   - Change industries
   - Track your **Flourishing** (Cosm × Chron)

---

## API Endpoints

### Players
- `POST /api/players?name=...` — Create player
- `GET /api/players/{player_id}` — Get player state
- `GET /api/players` — List all players

### Productions
- `POST /api/productions/start` — Start new production
- `GET /api/productions/{production_id}` — Get production state
- `POST /api/productions/{production_id}/advance` — Advance to next stage

### Portfolio
- `GET /api/players/{player_id}/portfolio` — Get player portfolio

### Game Info
- `GET /api/games` — List games and scoring dimensions
- `GET /api/health` — Health check

---

## Production Pipeline

### DOMES Pipeline

| Stage | APIs Called | Output |
|-------|-------------|--------|
| Development | domes-profile-research, domes-data-research, domes-legal | Research data |
| Pre-Production | domes-architect, domes-datamap, domes-flourishing | Dome design |
| Production | domes-contracts, domes-profiles | Built dome |
| Post-Production | domes-brain, domes-lab | Verified + innovations |
| Distribution | domes-viz | Narrative + Cosm score |

### SPHERES Pipeline

| Stage | APIs Called | Output |
|-------|-------------|--------|
| Development | spheres-assets, spheres-legal | Parcel + permits |
| Pre-Production | spheres-studio | Design + cost + timeline |
| Production | spheres-legal, spheres-studio | Built sphere |
| Post-Production | spheres-viz, spheres-lab | Episodes + innovations |
| Distribution | spheres-brain | Metrics + Chron score |

---

## Scoring

### COSM (DOMES)
- **Legal** — CFR provisions matched
- **Data** — Systems connected, consent pathways
- **Fiscal** — Cost model accuracy
- **Coordination** — Contracts executed
- **Flourishing** — Philosophy/finance/culture/vitality balance
- **Narrative** — Story coherence, IP generated

**Total Cosm = min(all dimensions)** — Weakest link principle

### CHRON (SPHERES)
- **Unlock** — Square meters activated
- **Access** — Public access hours
- **Permanence** — Duration multiplier
- **Catalyst** — Ripple effects
- **Policy** — Policy changes unlocked

**Total Chron = (m² × time) × significance**

---

## Roadmap

### Phase 1: Core Engine ✅
- Player state models
- Production pipeline director
- Scoring calculators
- Game frontend

### Phase 2: Backend Integration (Next)
- Wire engine to 17 existing APIs
- Real scoring from API responses
- IP/innovation extraction logic

### Phase 3: Advanced Features
- Multi-player support
- Leaderboards
- IP marketplace
- Innovation sharing
- Policy impact visualization

### Phase 4: Evolution
- Cosm evolution (insurance obsolescence)
- Chron evolution (significance density)
- Cross-game mechanics (Cosm × Chron synergies)

---

## Philosophy

**Production mindset over scale mindset.**

DOMES is anti-scale by design — depth over breadth. One person, infinite resources.

SPHERES starts with scale (m² everywhere) but evolves to significance density (brief moments in small spaces matter more).

Together, they teach the equation:

**Cosm × Chron = Flourishing**

---

Built by Mike @ BATHS with Molty 🏛️
