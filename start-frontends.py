#!/usr/bin/env python3
"""Start all 19 BATHS frontends."""
import subprocess, os, time

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

print("=== Starting 19 frontends ===")
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
    time.sleep(0.5)

print("\nAll frontends launched. Waiting 30s for Vite to compile...")
time.sleep(30)

# Make key ports public
print("\n=== Making ports public ===")
all_ports = [f[2] for f in FRONTENDS]
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

print("\nDone!")
