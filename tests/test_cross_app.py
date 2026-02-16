"""Cross-app integration tests."""
import requests

def test_domes_brain_services():
    r = requests.get("http://localhost:8006/api/services", timeout=5)
    assert r.status_code == 200

def test_spheres_brain_services():
    r = requests.get("http://localhost:8009/api/services", timeout=5)
    assert r.status_code == 200
