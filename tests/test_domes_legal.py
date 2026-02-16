"""Tests for domes-legal API."""
import requests

BASE = "http://localhost:8003"

def test_health():
    r = requests.get(f"{BASE}/api/health", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"

def test_provisions_list():
    r = requests.get(f"{BASE}/api/provisions", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert "data" in data or isinstance(data, list)

def test_provision_search():
    r = requests.get(f"{BASE}/api/search", params={"q": "medicaid"}, timeout=5)
    assert r.status_code == 200
