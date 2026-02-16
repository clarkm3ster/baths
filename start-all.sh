#!/bin/bash
# BATHS - Start All 18 Apps
set -e

echo "=== BATHS - Starting All 18 Apps ==="
echo ""

# Function to start a backend
start_backend() {
    local name=$1
    local dir=$2
    local module=$3
    local port=$4
    echo "  Starting $name backend on port $port..."
    cd /workspaces/baths/$dir
    nohup python3 -m uvicorn $module --host 0.0.0.0 --port $port > /tmp/${name}-backend.log 2>&1 &
    cd /workspaces/baths
}

# Function to start a frontend
start_frontend() {
    local name=$1
    local dir=$2
    local port=$3
    echo "  Starting $name frontend on port $port..."
    cd /workspaces/baths/$dir
    nohup npx vite --host 0.0.0.0 --port $port > /tmp/${name}-frontend.log 2>&1 &
    cd /workspaces/baths
}

echo "--- DOMES Backends ---"
start_backend "domes-legal-research" "backend" "app.main:app" 8000
start_backend "domes-data-research" "domes-data-research/backend" "app.main:app" 8001
start_backend "domes-profile-research" "domes-profile-research/backend" "app.main:app" 8002
start_backend "domes-legal" "domes-legal/backend" "app.main:app" 8003
start_backend "domes-profiles" "domes-profiles/backend" "app.main:app" 8004
start_backend "domes-viz" "domes-viz/backend" "main:app" 8005
start_backend "domes-brain" "domes-brain/backend" "main:app" 8006
start_backend "domes-lab" "domes-lab/backend" "main:app" 8007
start_backend "domes-datamap" "domes-datamap/backend" "app.main:app" 8013
start_backend "domes-contracts" "domes-contracts/backend" "app.main:app" 8014
start_backend "domes-architect" "domes-architect/backend" "app.main:app" 8015
start_backend "domes-flourishing" "domes-flourishing/backend" "main:app" 8016

echo ""
echo "--- SPHERES Backends ---"
start_backend "spheres-assets" "spheres-assets/backend" "app.main:app" 8017
start_backend "spheres-legal" "spheres-legal/backend" "main:app" 8018
start_backend "spheres-studio" "spheres-studio/backend" "main:app" 8019
start_backend "spheres-viz" "spheres-viz/backend" "main:app" 8008
start_backend "spheres-brain" "spheres-brain/backend" "main:app" 8009
start_backend "spheres-lab" "spheres-lab/backend" "main:app" 8010

echo ""
echo "Waiting 5 seconds for backends to start..."
sleep 5

echo ""
echo "=== All backends started. Check /tmp/*-backend.log for details ==="
echo ""
echo "To start frontends, run: bash /workspaces/baths/start-frontends.sh"
