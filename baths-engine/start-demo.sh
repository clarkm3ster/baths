#!/bin/bash
# BATHS Game Engine - Start Demo

set -e

echo "🏛️  Starting BATHS Game Engine Demo..."
echo ""

# Kill any existing services
pkill -f "uvicorn.*900[0-9]" 2>/dev/null || true
pkill -f "vite.*5300" 2>/dev/null || true
sleep 1

# Start game engine backend
echo "Starting game engine backend (port 9000)..."
cd /root/clawd/baths/baths-engine/backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 9000 > /tmp/baths-engine.log 2>&1 &

sleep 2

# Start frontend
echo "Starting game frontend (port 5300)..."
cd /root/clawd/baths/baths-engine/frontend
npm run dev -- --host 0.0.0.0 > /tmp/baths-frontend.log 2>&1 &

sleep 3

echo ""
echo "✅ BATHS Game Engine is running!"
echo ""
echo "   🎮 Frontend: http://localhost:5300"
echo "   🔧 Backend:  http://localhost:9000/api/health"
echo ""
echo "Note: Backend APIs are mocked for now (real integration pending)"
echo ""
