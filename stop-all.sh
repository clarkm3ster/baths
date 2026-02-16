#!/bin/bash
# BATHS - Stop All Apps
echo "=== Stopping all BATHS apps ==="
# Kill all uvicorn processes
pkill -f "uvicorn" 2>/dev/null && echo "  Stopped all backends" || echo "  No backends running"
# Kill all vite processes
pkill -f "vite" 2>/dev/null && echo "  Stopped all frontends" || echo "  No frontends running"
echo "=== All stopped ==="
