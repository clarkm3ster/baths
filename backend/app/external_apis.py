import httpx

ECFR_BASE = "https://www.ecfr.gov/api/versioner/v1"
FEDERAL_REGISTER_BASE = "https://www.federalregister.gov/api/v1"


async def fetch_ecfr_regulation(title: int, part: int, section: str | None = None) -> dict:
    """Fetch a regulation from the eCFR API by title, part, and optional section.

    Example: fetch_ecfr_regulation(42, 438) for Medicaid managed care at 42 CFR Part 438.
    """
    url = f"{ECFR_BASE}/full/{title}/part-{part}.json"
    if section:
        url = f"{ECFR_BASE}/full/{title}/section-{section}.json"

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()


async def search_ecfr(query: str, title: int | None = None) -> dict:
    """Search eCFR for regulations matching a query string."""
    params = {"query": query}
    if title:
        params["title"] = str(title)

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(f"{ECFR_BASE}/search", params=params)
        resp.raise_for_status()
        return resp.json()


async def fetch_federal_register_documents(
    search_term: str,
    doc_type: str = "RULE",
    per_page: int = 20,
) -> dict:
    """Fetch documents from the Federal Register API.

    doc_type: RULE, PRORULE, NOTICE, PRESDOCU
    """
    params = {
        "conditions[term]": search_term,
        "conditions[type][]": doc_type,
        "per_page": per_page,
        "order": "relevance",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(f"{FEDERAL_REGISTER_BASE}/documents.json", params=params)
        resp.raise_for_status()
        return resp.json()


async def fetch_federal_register_document(document_number: str) -> dict:
    """Fetch a specific Federal Register document by its document number."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(f"{FEDERAL_REGISTER_BASE}/documents/{document_number}.json")
        resp.raise_for_status()
        return resp.json()
