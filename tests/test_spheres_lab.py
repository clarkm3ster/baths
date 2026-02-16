"""Tests for spheres-lab API."""
import requests

BASE = "http://localhost:8010"

def test_health():
    r = requests.get(f"{BASE}/api/health", timeout=5)
    assert r.status_code == 200

def test_teammates():
    r = requests.get(f"{BASE}/api/teammates", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert len(data["data"]) == 12

def test_innovations():
    r = requests.get(f"{BASE}/api/innovations", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert len(data["data"]) == 66

def test_domain_filter():
    r = requests.get(f"{BASE}/api/innovations", params={"domain": "space-economics"}, timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert len(data["data"]) == 6

def test_stats():
    r = requests.get(f"{BASE}/api/stats", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert data["data"]["totals"]["teammates"] == 12
