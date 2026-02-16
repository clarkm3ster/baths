# BATHS Health Report

Generated: 2026-02-16

## Summary

- **Total apps audited**: 17 (11 DOMES + 6 SPHERES)
- **Note**: `domes-legal-research` does not exist as a separate app directory. It is referenced conceptually in `domes-legal` and `domes-brain` but has no standalone codebase. The actual DOMES count is 11, not 12.
- **TypeScript errors found and fixed**: 1
- **Missing files created**: 1 (requirements.txt for domes-legal)
- **Backend port conflicts**: 5 groups (noted but not fixed -- may be by design for non-simultaneous use)
- **Frontend port conflicts**: 4 groups (noted but not fixed)

---

## domes-data-research
- Backend: 8001 -- OK -- FastAPI app with app/ package structure; run.py; SQLAlchemy+SQLite
- Frontend: 5174 -- OK -- Vite+React; proxy to localhost:8001
- Issues found: None
- Issues fixed: None
- Remaining issues: None

---

## domes-profile-research
- Backend: 8002 -- OK -- FastAPI app with app/ package structure; run.py; SQLAlchemy+SQLite
- Frontend: 5173 (default) -- OK -- Vite+React; proxy to localhost:8002
- Issues found: None
- Issues fixed: None
- Remaining issues: None

---

## domes-legal
- Backend: 8003 -- OK -- FastAPI with app/ package structure; run.py; SQLAlchemy+SQLite
- Frontend: 5177 -- OK -- Vite+React; proxy to localhost:8003; uses components/App.tsx pattern
- Issues found:
  - Missing requirements.txt
  - Port 8003 shared with domes-datamap and domes-contracts
- Issues fixed:
  - Created requirements.txt (fastapi, uvicorn, sqlalchemy, pydantic)
- Remaining issues:
  - Backend port 8003 conflicts with domes-datamap and domes-contracts (will fail if run simultaneously)

---

## domes-datamap
- Backend: 8003 -- OK -- FastAPI with app/ package structure; run.py; SQLAlchemy+SQLite
- Frontend: 5173 (default) -- OK -- Vite+React; proxy to localhost:8003; uses components/App.tsx pattern
- Issues found:
  - Port 8003 shared with domes-legal and domes-contracts
- Issues fixed: None
- Remaining issues:
  - Backend port 8003 conflicts with domes-legal and domes-contracts

---

## domes-profiles
- Backend: 8004 -- OK -- FastAPI with app/ package structure; run.py with lifespan; SQLAlchemy+SQLite; httpx dependency
- Frontend: 5178 -- OK -- Vite+React; proxy to localhost:8004; uses components/App.tsx pattern
- Issues found:
  - Port 8004 shared with domes-architect
  - Frontend port 5178 shared with domes-architect
- Issues fixed: None
- Remaining issues:
  - Backend port 8004 and frontend port 5178 conflict with domes-architect

---

## domes-contracts
- Backend: 8003 -- OK -- FastAPI with app/ package structure; run.py; SQLAlchemy+SQLite
- Frontend: 5177 -- OK -- Vite+React; proxy to localhost:8003; also proxies /datamap-api to localhost:8001
- Issues found:
  - Port 8003 shared with domes-legal and domes-datamap
  - Frontend port 5177 shared with domes-legal
- Issues fixed: None
- Remaining issues:
  - Backend port 8003 conflicts with domes-legal and domes-datamap
  - Frontend port 5177 conflicts with domes-legal

---

## domes-architect
- Backend: 8004 -- OK -- FastAPI with app/ package structure; run.py; SQLAlchemy+SQLite
- Frontend: 5178 -- OK (after fix) -- Vite+React; proxy to localhost:8004
- Issues found:
  - TypeScript error: RiskDashboard.tsx had garbage text "export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1" prepended to line 1
  - Port 8004 shared with domes-profiles
  - Frontend port 5178 shared with domes-profiles
- Issues fixed:
  - Removed corrupted prefix from src/components/RiskDashboard.tsx (TS compilation now passes)
- Remaining issues:
  - Backend port 8004 conflicts with domes-profiles
  - Frontend port 5178 conflicts with domes-profiles

---

## domes-viz
- Backend: 8005 (implied) -- OK -- FastAPI with flat structure; main.py + narrative.py; no run.py; no explicit port
- Frontend: 5179 -- OK -- Vite+React; proxy to localhost:8005; uses three.js
- Issues found:
  - No run.py and no `if __name__` block -- backend must be started manually with `uvicorn main:app --port 8005`
  - Port 8005 shared with domes-flourishing
- Issues fixed: None
- Remaining issues:
  - No convenient run entry point (no run.py, no __main__ block)
  - Backend port 8005 conflicts with domes-flourishing

---

## domes-brain
- Backend: 8006 -- OK -- FastAPI flat structure; main.py with lifespan, health monitoring, discovery scanner, scheduler; SQLAlchemy+SQLite; httpx; apscheduler
- Frontend: 5180 -- OK -- Vite+React; proxy to localhost:8006
- Issues found:
  - Frontend port 5180 shared with spheres-legal
- Issues fixed: None
- Remaining issues:
  - Frontend port 5180 conflicts with spheres-legal

---

## domes-lab
- Backend: 8007 -- OK -- FastAPI flat structure; main.py with lifespan; SQLAlchemy+SQLite; 12 teammate generators; httpx
- Frontend: 5181 -- OK -- Vite+React; proxy to localhost:8007
- Issues found:
  - Backend port 8007 shared with spheres-studio
- Issues fixed: None
- Remaining issues:
  - Backend port 8007 conflicts with spheres-studio

---

## domes-flourishing
- Backend: 8005 -- OK -- FastAPI flat structure; main.py with all routes inline; pydantic models; no database (pure data)
- Frontend: 5173 (default) -- OK -- Vite+React; proxy to localhost:8005
- Issues found:
  - Port 8005 shared with domes-viz
- Issues fixed: None
- Remaining issues:
  - Backend port 8005 conflicts with domes-viz

---

## domes-legal-research
- **DOES NOT EXIST** as a separate app directory
- Referenced conceptually in domes-legal/backend/app/main.py and domes-brain/backend/scanners.py
- May have been planned but never built, or is an alias for domes-data-research
- Issues found: App directory missing entirely
- Issues fixed: N/A
- Remaining issues: N/A (not a bug if it was never intended to be a separate app)

---

## spheres-assets
- Backend: 8000 -- OK -- FastAPI with app/ package structure; run.py; SQLAlchemy+SQLite; httpx for data ingestion
- Frontend: 5173 (default) -- OK -- Vite+React; proxy to localhost:8000
- Issues found: None
- Issues fixed: None
- Remaining issues: None

---

## spheres-legal
- Backend: 8006 -- OK -- FastAPI flat structure; main.py with all routes inline; permits.py + contracts.py + policy.py modules; no database (pure data)
- Frontend: 5180 -- OK -- Vite+React+react-router-dom; proxy to localhost:8006
- Issues found:
  - Backend port 8006 conflicts with domes-brain
  - Frontend port 5180 conflicts with domes-brain
- Issues fixed: None
- Remaining issues:
  - Backend port 8006 conflicts with domes-brain
  - Frontend port 5180 conflicts with domes-brain

---

## spheres-studio
- Backend: 8007 -- OK -- FastAPI flat structure with models/, routes/, services/ subpackages; lifespan; no database (in-memory data)
- Frontend: 5190 -- OK -- Vite+React+react-router-dom; proxy to localhost:8007
- Issues found:
  - Backend port 8007 conflicts with domes-lab
- Issues fixed: None
- Remaining issues:
  - Backend port 8007 conflicts with domes-lab

---

## spheres-viz
- Backend: 8008 -- OK -- FastAPI flat structure with models/ and routes/ subpackages; episode data
- Frontend: 5200 -- OK -- Vite+React; proxy to localhost:8008; three.js for 3D worlds
- Issues found: None
- Issues fixed: None
- Remaining issues: None

---

## spheres-brain
- Backend: 8009 -- OK -- FastAPI flat structure with models/, routes/, services/ subpackages; lifespan; httpx for service health probes
- Frontend: 5210 -- OK -- Vite+React; proxy to localhost:8009
- Issues found: None
- Issues fixed: None
- Remaining issues: None

---

## spheres-lab
- Backend: 8010 -- OK -- FastAPI flat structure; main.py with lifespan; SQLAlchemy+SQLite; 11 innovation domain modules in innovations/ package; routes.py, models.py, teammates.py at root level
- Frontend: 5220 -- OK -- Vite+React; proxy to localhost:8010; lucide-react icons
- Issues found:
  - Empty models/, routes/, services/ subdirectories (vestigial -- unused)
- Issues fixed: None
- Remaining issues:
  - Empty subdirectories could be cleaned up (cosmetic only)

---

## Port Conflict Summary

### Backend Port Conflicts (will fail if run simultaneously)
| Port | Apps |
|------|------|
| 8003 | domes-legal, domes-datamap, domes-contracts |
| 8004 | domes-profiles, domes-architect |
| 8005 | domes-viz, domes-flourishing |
| 8006 | domes-brain, spheres-legal |
| 8007 | domes-lab, spheres-studio |

### Frontend Port Conflicts
| Port | Apps |
|------|------|
| 5173 | domes-profile-research, domes-datamap, domes-flourishing, spheres-assets (all use Vite default) |
| 5177 | domes-legal, domes-contracts |
| 5178 | domes-profiles, domes-architect |
| 5180 | domes-brain, spheres-legal |

---

## Issues Fixed

1. **domes-architect/frontend/src/components/RiskDashboard.tsx** -- Removed corrupted text `export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` prepended to line 1, which caused TypeScript compilation failure (TS1128, TS1351)
2. **domes-legal/backend/requirements.txt** -- Created missing file with required dependencies: fastapi, uvicorn, sqlalchemy, pydantic

---

## All TypeScript Compilation Results

| App | Result |
|-----|--------|
| domes-data-research | PASS |
| domes-profile-research | PASS |
| domes-legal | PASS |
| domes-datamap | PASS |
| domes-profiles | PASS |
| domes-contracts | PASS |
| domes-architect | PASS (after fix) |
| domes-viz | PASS |
| domes-brain | PASS |
| domes-lab | PASS |
| domes-flourishing | PASS |
| spheres-assets | PASS |
| spheres-legal | PASS |
| spheres-studio | PASS |
| spheres-viz | PASS |
| spheres-brain | PASS |
| spheres-lab | PASS |

---

## All Python Syntax Check Results

| App | File | Result |
|-----|------|--------|
| domes-data-research | app/main.py | PASS |
| domes-profile-research | app/main.py | PASS |
| domes-legal | app/main.py | PASS |
| domes-datamap | app/main.py | PASS |
| domes-profiles | app/main.py | PASS |
| domes-contracts | app/main.py | PASS |
| domes-architect | app/main.py | PASS |
| domes-viz | main.py | PASS |
| domes-brain | main.py | PASS |
| domes-lab | main.py | PASS |
| domes-flourishing | main.py | PASS |
| spheres-assets | app/main.py | PASS |
| spheres-legal | main.py | PASS |
| spheres-studio | main.py | PASS |
| spheres-viz | main.py | PASS |
| spheres-brain | main.py | PASS |
| spheres-lab | main.py | PASS |
