#!/usr/bin/env python3
"""Kill and restart the viz backends. They now read MARBLE_API_KEY from .env files."""
import subprocess, os, signal, time

# Kill existing processes on ports 8005 and 8008
for line in subprocess.check_output(["ps", "aux"]).decode().splitlines():
    if "uvicorn main:app" in line and ("port 8005" in line or "port 8008" in line):
        pid = int(line.split()[1])
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"Killed PID {pid}")
        except ProcessLookupError:
            pass

time.sleep(2)

os.chdir("/workspaces/baths/domes-viz/backend")
subprocess.Popen(
    ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"],
    stdout=open("/tmp/be-8005.log", "w"),
    stderr=subprocess.STDOUT,
    start_new_session=True,
)
print("domes-viz started on 8005")

os.chdir("/workspaces/baths/spheres-viz/backend")
subprocess.Popen(
    ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008"],
    stdout=open("/tmp/be-8008.log", "w"),
    stderr=subprocess.STDOUT,
    start_new_session=True,
)
print("spheres-viz started on 8008")
print("Done.")
