#!/usr/bin/env python3
"""Start all 18 BATHS backends and 19 frontends using subprocess.Popen."""
import subprocess, os, time, sys

BACKENDS = [
    ("domes-legal-research", "backend", "app.main:app", 8000),
    ("domes-data-research", "domes-data-research/backend", "app.main:app", 8001),
    ("domes-profile-research", "domes-profile-research/backend", "app.main:app", 8002),
    ("domes-legal", "domes-legal/backend", "app.main:app", 8003),
    ("domes-profiles", "domes-profiles/backend", "app.main:app", 8004),
    ("domes-viz", "domes-viz/backend", "main:app", 8005),
    ("domes-brain", "domes-brain/backend", "main:app", 8006),
    ("domes-lab", "domes-lab/backend", "main:app", 8007),
    ("domes-datamap", "domes-datamap/backend", "app.main:app", 8013),
    ("domes-contracts", "domes-contracts/backend", "app.main:app", 8014),
    ("domes-architect", "domes-architect/backend", "app.main:app", 8015),
    ("domes-flourishing", "domes-flourishing/backend", "main:app", 8016),
    ("spheres-assets", "spheres-assets/backend", "app.main:app", 8017),
    ("spheres-legal", "spheres-legal/backend", "main:app", 8018),
    ("spheres-studio", "spheres-studio/backend", "main:app", 8019),
    ("spheres-viz", "spheres-viz/backend", "main:app", 8008),
    ("spheres-brain", "spheres-brain/backend", "main:app", 8009),
    ("spheres-lab", "spheres-lab/backend", "main:app", 8010),
]

FRONTENDS = [
    ("dashboard", "baths-dashboard", 5173),
    ("domes-data-research", "domes-data-research/frontend", 5174),
    ("domes-profile-research", "domes-profile-research/frontend", 5175),
    ("domes-datamap", "domes-datamap/frontend", 5176),
    ("domes-legal", "domes-legal/frontend", 5177),
    ("domes-profiles", "domes-profiles/frontend", 5178),
    ("domes-viz", "domes-viz/frontend", 5179),
    ("domes-legal-research", "frontend", 5180),
    ("domes-lab", "domes-lab/frontend", 5181),
    ("domes-contracts", "domes-contracts/frontend", 5182),
    ("domes-architect", "domes-architect/frontend", 5183),
    ("domes-flourishing", "domes-flourishing/frontend", 5184),
    ("spheres-assets", "spheres-assets/frontend", 5185),
    ("spheres-legal", "spheres-legal/frontend", 5186),
    ("domes-brain", "domes-brain/frontend", 5188),
    ("spheres-studio", "spheres-studio/frontend", 5190),
    ("spheres-viz", "spheres-viz/frontend", 5200),
    ("spheres-brain", "spheres-brain/frontend", 5210),
    ("spheres-lab", "spheres-lab/frontend", 5220),
]

BASE = "/workspaces/baths"

print("=== Starting 18 backends ===")
for name, directory, module, port in BACKENDS:
    cwd = os.path.join(BASE, directory)
    log = f"/tmp/be-{port}.log"
    subprocess.Popen(
        ["python3", "-m", "uvicorn", module, "--host", "0.0.0.0", "--port", str(port)],
        cwd=cwd,
        stdout=open(log, "w"),
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    print(f"  {name} -> port {port}")

print("\nWaiting 5s for backends...")
time.sleep(5)

print("\n=== Starting 19 frontends ===")
for name, directory, port in FRONTENDS:
    cwd = os.path.join(BASE, directory)
    log = f"/tmp/fe-{port}.log"
    subprocess.Popen(
        ["npx", "vite", "--host", "0.0.0.0", "--port", str(port)],
        cwd=cwd,
        stdout=open(log, "w"),
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    print(f"  {name} -> port {port}")
    time.sleep(0.5)  # stagger to avoid resource contention

print("\nAll processes launched. Waiting 30s for Vite to compile...")
time.sleep(30)

# Make ports public
print("\n=== Making ports public ===")
all_ports = [b[3] for b in BACKENDS] + [f[2] for f in FRONTENDS]
port_args = ",".join(f"{p}:public" for p in all_ports)
try:
    result = subprocess.run(
        ["gh", "codespace", "ports", "visibility", port_args,
         "--codespace", "congenial-train-q7x9wqpw65qq3xpq7"],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        print("  All ports set to public")
    else:
        print(f"  Warning: {result.stderr.strip()}")
except Exception as e:
    print(f"  Port visibility error: {e}")

print("\nDone! Dashboard: https://congenial-train-q7x9wqpw65qq3xpq7-5173.app.github.dev")
