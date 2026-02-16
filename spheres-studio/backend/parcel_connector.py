import httpx
import os

ASSETS_BASE = os.environ.get("SPHERES_ASSETS_URL", "http://localhost:8000")

async def fetch_parcels(neighborhood: str = None, limit: int = 20):
    """Fetch parcels from spheres-assets API."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            params = {"limit": limit}
            if neighborhood:
                params["neighborhood"] = neighborhood
            resp = await client.get(f"{ASSETS_BASE}/api/parcels", params=params)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("data", data)
    except Exception:
        pass
    return []

async def fetch_parcel(parcel_id: str):
    """Fetch a single parcel by ID."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{ASSETS_BASE}/api/parcels/{parcel_id}")
            if resp.status_code == 200:
                data = resp.json()
                return data.get("data", data)
    except Exception:
        pass
    return None
