"""
Upstream API clients for DOMES services.

Calls domes-legal (port 8003), domes-datamap (port 8003),
and domes-profile-research (port 8002) with graceful fallbacks.
"""

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

LEGAL_BASE = "http://localhost:8003"
DATAMAP_BASE = "http://localhost:8003"
PROFILE_RESEARCH_BASE = "http://localhost:8002"

TIMEOUT = httpx.Timeout(10.0, connect=5.0)

# ---------------------------------------------------------------------------
# Circumstance-to-domain mapping (used to query provisions by domain)
# ---------------------------------------------------------------------------

CIRCUMSTANCE_DOMAINS: dict[str, str] = {
    "is_homeless": "housing",
    "has_housing_instability": "housing",
    "is_section_8": "housing",
    "is_in_shelter": "housing",
    "has_substance_use": "health",
    "has_mental_illness": "health",
    "has_chronic_health": "health",
    "is_frequent_er": "health",
    "is_on_medicaid": "health",
    "is_va_healthcare": "health",
    "is_dual_eligible": "health",
    "has_disability": "health",
    "is_incarcerated": "justice",
    "is_recently_released": "justice",
    "is_on_probation": "justice",
    "is_on_parole": "justice",
    "is_juvenile_justice": "justice",
    "has_dv_history": "justice",
    "is_on_tanf": "income",
    "is_on_snap": "income",
    "is_on_ssi": "income",
    "is_on_ssdi": "income",
    "is_unemployed": "income",
    "is_in_foster_care": "child_welfare",
    "has_child_in_foster": "child_welfare",
    "is_aging_out_foster": "child_welfare",
    "has_iep": "education",
    "is_in_special_ed": "education",
    "has_truancy": "education",
    "is_school_age": "education",
}


# ---------------------------------------------------------------------------
# Helper to convert circumstance flags to flat list
# ---------------------------------------------------------------------------

def circumstances_to_list(circumstances: dict) -> list[str]:
    """Convert {"is_homeless": true, ...} to ["homeless", ...]."""
    result = []
    for key, value in circumstances.items():
        if value:
            # Strip common prefixes: is_, has_, on_
            clean = key
            for prefix in ("is_", "has_", "is_on_", "is_in_"):
                if clean.startswith(prefix):
                    clean = clean[len(prefix):]
                    break
            result.append(clean)
    return result


def circumstances_to_domains(circumstances: dict) -> list[str]:
    """Return unique domains relevant to given circumstances."""
    domains = set()
    for key, value in circumstances.items():
        if value and key in CIRCUMSTANCE_DOMAINS:
            domains.add(CIRCUMSTANCE_DOMAINS[key])
    return sorted(domains)


# ===========================================================================
# domes-legal (port 8003)
# ===========================================================================

async def fetch_provisions(
    domain: str | None = None,
    provision_type: str | None = None,
    search: str | None = None,
) -> list[dict]:
    """GET /api/provisions with optional filters."""
    params: dict[str, Any] = {}
    if domain:
        params["domain"] = domain
    if provision_type:
        params["provision_type"] = provision_type
    if search:
        params["search"] = search
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.get(f"{LEGAL_BASE}/api/provisions", params=params)
            resp.raise_for_status()
            data = resp.json()
            # Handle both list and dict-with-items response shapes
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and "items" in data:
                return data["items"]
            return data if isinstance(data, list) else []
    except Exception as exc:
        logger.warning("domes-legal /api/provisions failed: %s", exc)
        return []


async def fetch_provision(provision_id: str) -> dict | None:
    """GET /api/provisions/{id}."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.get(f"{LEGAL_BASE}/api/provisions/{provision_id}")
            resp.raise_for_status()
            return resp.json()
    except Exception as exc:
        logger.warning("domes-legal /api/provisions/%s failed: %s", provision_id, exc)
        return None


async def fetch_provisions_for_profile(circumstances: dict) -> dict[str, list[dict]]:
    """
    Query provisions for each domain relevant to a person's circumstances.
    Returns {domain: [provisions...]}.
    """
    domains = circumstances_to_domains(circumstances)
    result: dict[str, list[dict]] = {}
    for domain in domains:
        provisions = await fetch_provisions(domain=domain)
        if provisions:
            result[domain] = provisions
    return result


# ===========================================================================
# domes-datamap (port 8003)
# ===========================================================================

async def fetch_person_map(circumstances_list: list[str]) -> dict:
    """POST /api/person-map with circumstance list."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{DATAMAP_BASE}/api/person-map",
                json={"circumstances": circumstances_list},
            )
            resp.raise_for_status()
            return resp.json()
    except Exception as exc:
        logger.warning("domes-datamap /api/person-map failed: %s", exc)
        return {"systems": [], "connections": [], "gaps": [], "bridges": []}


async def fetch_consent_pathways(circumstances_list: list[str]) -> list[dict]:
    """POST /api/bridges/consent-pathway."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{DATAMAP_BASE}/api/bridges/consent-pathway",
                json={"circumstances": circumstances_list},
            )
            resp.raise_for_status()
            data = resp.json()
            return data if isinstance(data, list) else data.get("pathways", [])
    except Exception as exc:
        logger.warning("domes-datamap /api/bridges/consent-pathway failed: %s", exc)
        return []


async def fetch_bridge_priorities(limit: int = 10) -> list[dict]:
    """GET /api/bridges/priority."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.get(
                f"{DATAMAP_BASE}/api/bridges/priority",
                params={"limit": limit},
            )
            resp.raise_for_status()
            data = resp.json()
            return data if isinstance(data, list) else data.get("bridges", [])
    except Exception as exc:
        logger.warning("domes-datamap /api/bridges/priority failed: %s", exc)
        return []


async def fetch_quick_wins(circumstances: list[str] | None = None) -> list[dict]:
    """GET /api/bridges/quick-wins."""
    params: dict[str, Any] = {}
    if circumstances:
        params["circumstances"] = ",".join(circumstances)
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.get(
                f"{DATAMAP_BASE}/api/bridges/quick-wins",
                params=params,
            )
            resp.raise_for_status()
            data = resp.json()
            return data if isinstance(data, list) else data.get("wins", [])
    except Exception as exc:
        logger.warning("domes-datamap /api/bridges/quick-wins failed: %s", exc)
        return []


# ===========================================================================
# domes-profile-research (port 8002)
# ===========================================================================

async def fetch_composite_profile(circumstances_dict: dict) -> dict:
    """POST /api/profiles/generate."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(
                f"{PROFILE_RESEARCH_BASE}/api/profiles/generate",
                json=circumstances_dict,
            )
            resp.raise_for_status()
            return resp.json()
    except Exception as exc:
        logger.warning("domes-profile-research /api/profiles/generate failed: %s", exc)
        return {}


async def fetch_systems() -> list[dict]:
    """GET /api/systems."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.get(f"{PROFILE_RESEARCH_BASE}/api/systems")
            resp.raise_for_status()
            data = resp.json()
            return data if isinstance(data, list) else data.get("systems", [])
    except Exception as exc:
        logger.warning("domes-profile-research /api/systems failed: %s", exc)
        return []


async def fetch_costs() -> dict:
    """GET /api/costs."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.get(f"{PROFILE_RESEARCH_BASE}/api/costs")
            resp.raise_for_status()
            return resp.json()
    except Exception as exc:
        logger.warning("domes-profile-research /api/costs failed: %s", exc)
        return {}
