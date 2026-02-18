# 🏛️ BATHS Game Engine - Demo Guide

## What You Built

A unified game engine for **DOMES** and **SPHERES** that teaches people to be Producers by navigating real production pipelines.

**Cosm × Chron = Flourishing**

---

## How to Run

```bash
cd /root/clawd/baths/baths-engine
./start-demo.sh
```

Then open: **http://localhost:5300**

---

## Game Flow

### 1. Game Selector Screen
- Two game cards: **DOMES** and **SPHERES**
- Each shows:
  - Description
  - Currency (Cosm or Chron)
  - Scoring dimensions
- Click a card to select
- Enter subject (person name or parcel ID)
- Click "Start Production"

### 2. Production Pipeline Screen
- Visual pipeline showing 5 stages:
  1. **Development** - Research & planning
  2. **Pre-Production** - Design & architecture
  3. **Production** - Build & execute
  4. **Post-Production** - Verify & innovate
  5. **Distribution** - Score & package
- Progress bar (0-100%)
- "Advance Stage" button
- Real-time stage data display (JSON)

### 3. Portfolio Screen
- **Total Cosm** (DOMES score)
  - Legal, Data, Fiscal, Coordination, Flourishing, Narrative
  - Minimum dimension = Total Cosm (weakest link)
- **Total Chron** (SPHERES score)
  - Unlock (m²), Access (hrs), Permanence, Catalyst, Policy
  - Formula: (m² × time) × significance
- **Flourishing** = Cosm × Chron
- Completed productions list
- IP created
- Innovations generated
- Industries changed

---

## What's Working

✅ Game engine backend (port 9000)  
✅ Frontend UI (port 5300)  
✅ Player creation & management  
✅ Production state tracking  
✅ Pipeline stage orchestration  
✅ Scoring system (Cosm + Chron)  
✅ Portfolio tracking  
✅ Real API integration hooks  

---

## What's Next

To get the full experience with real data:

1. Start all 17 backend APIs
2. Each API needs dependencies installed
3. Update `api-registry.json` ports if needed
4. Game engine will call real APIs instead of mocks

The infrastructure is built. The APIs just need to be running.

---

## Architecture

```
User Browser
    ↓
Frontend (React + Vite, port 5300)
    ↓
Game Engine Backend (FastAPI, port 9000)
    ↓
Pipeline Director
    ↓
17 BATHS APIs (domes-*, spheres-*)
    ↓
Real scoring, innovations, IP generation
```

---

## Files

- `backend/main.py` - Game engine API
- `backend/models.py` - Data models (Player, Production, Scoring)
- `backend/pipeline.py` - Production pipeline director
- `frontend/src/App.jsx` - Main game UI
- `frontend/src/components/` - Game selector, pipeline, portfolio
- `start-demo.sh` - One-command startup

---

Built by Mike @ BATHS with Molty 🏛️
