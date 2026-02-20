# BATHS Game Engine

## Overview
A unified game engine for DOMES + SPHERES that teaches people to be Producers.
Built by Mike @ BATHS with Molty.

**Cosm x Chron = Flourishing**

## Project Architecture

### Games
- **DOMES**: Build a dome around one person using the entire US government. Scored by Cosm (weakest dimension = total).
- **SPHERES**: Activate public spaces in cities. Scored by Chron (m2 x time).

### Structure
- `baths-engine/frontend/` - React + Vite frontend (port 5000)
- `baths-engine/backend/` - FastAPI Python backend (port 9000)
- `domes-*` - DOMES domain modules (profile-research, data-research, legal, architect, datamap, flourishing, contracts, profiles, brain, lab, viz)
- `spheres-*` - SPHERES domain modules (assets, legal, studio, viz, lab, brain)
- `baths-dashboard/` - Dashboard module

### Demo Mode
The pipeline runs in demo/fallback mode. When backend APIs aren't available, it uses built-in demo data. Set `BATHS_DEMO_MODE=false` to disable demo fallback.

### Production Pipeline
5 stages: Development > Pre-Production > Production > Post-Production > Distribution

## Recent Changes
- 2026-02-20: Configured for Replit environment (port 5000, allowedHosts)
- 2026-02-20: Added demo mode with mock data fallback to pipeline
- 2026-02-20: Fixed SPHERES Chron scoring data flow (metrics in post_production)

## User Preferences
- User goes by Mike
- Built with Molty (previous AI assistant)
