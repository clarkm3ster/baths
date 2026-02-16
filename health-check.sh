#!/bin/bash
# BATHS - Health Check All Apps
echo "=== BATHS Health Check ==="
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

check_backend() {
    local name=$1
    local port=$2
    local url="http://localhost:${port}/api/health"
    local response=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 $url 2>/dev/null)
    if [ "$response" = "200" ]; then
        echo -e "  ${GREEN}[OK]${NC}  $name backend (port $port)"
    elif [ "$response" = "000" ]; then
        echo -e "  ${RED}[DOWN]${NC} $name backend (port $port)"
    else
        echo -e "  ${YELLOW}[${response}]${NC} $name backend (port $port)"
    fi
}

echo "--- DOMES Backends ---"
check_backend "domes-legal-research" 8000
check_backend "domes-data-research" 8001
check_backend "domes-profile-research" 8002
check_backend "domes-legal" 8003
check_backend "domes-profiles" 8004
check_backend "domes-viz" 8005
check_backend "domes-brain" 8006
check_backend "domes-lab" 8007
check_backend "domes-datamap" 8013
check_backend "domes-contracts" 8014
check_backend "domes-architect" 8015
check_backend "domes-flourishing" 8016

echo ""
echo "--- SPHERES Backends ---"
check_backend "spheres-assets" 8017
check_backend "spheres-legal" 8018
check_backend "spheres-studio" 8019
check_backend "spheres-viz" 8008
check_backend "spheres-brain" 8009
check_backend "spheres-lab" 8010

echo ""
echo "=== Health check complete ==="
