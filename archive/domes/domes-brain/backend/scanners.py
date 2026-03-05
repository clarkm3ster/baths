"""
Scanner implementations for the DOMES Discovery Engine.

Each scanner is a class with an ``async scan()`` method that returns a list of
Discovery items.  When DEMO_MODE is True the scanners return realistic
simulated data; when False they attempt real API calls with a graceful
fallback to demo output.
"""

from __future__ import annotations

import hashlib
import logging
import random
import time
from datetime import datetime, timedelta
from typing import Optional

import httpx

from discovery_models import (
    Discovery,
    DiscoveryStatus,
    ImpactLevel,
    ScanResult,
    SourceType,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Global demo-mode toggle.  Set to False to attempt real API calls.
# ---------------------------------------------------------------------------
DEMO_MODE = True

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _deterministic_score(seed: str, low: int = 30, high: int = 95) -> int:
    """Derive a repeatable-ish relevance score from a string seed."""
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    return low + (h % (high - low + 1))


def _random_date(days_back: int = 30) -> datetime:
    """Return a datetime within the last *days_back* days."""
    offset = random.randint(0, days_back * 24 * 60)
    return datetime.utcnow() - timedelta(minutes=offset)


def _pick_impact(score: int) -> ImpactLevel:
    if score >= 85:
        return ImpactLevel.critical
    if score >= 70:
        return ImpactLevel.high
    if score >= 50:
        return ImpactLevel.medium
    return ImpactLevel.low


# ===================================================================
# 1. Federal Register Scanner
# ===================================================================

class FederalRegisterScanner:
    """
    Scans the Federal Register API (api.federalregister.gov) for documents
    related to human-services programs: Medicaid, SNAP, TANF, housing
    vouchers, child welfare, workforce development, criminal justice reentry.
    """

    SOURCE_NAME = "Federal Register"
    BASE_URL = "https://api.federalregister.gov/v1"
    KEYWORDS = [
        "Medicaid", "SNAP", "TANF", "housing vouchers",
        "child welfare", "workforce development",
        "criminal justice reentry", "social services block grant",
    ]

    # -- demo data --------------------------------------------------------

    _DEMO_ITEMS = [
        {
            "title": "Proposed Rule: Medicaid Managed Care Quality Rating System",
            "summary": "CMS proposes a mandatory quality rating system for Medicaid managed care plans to improve transparency and enrollee choice. States would be required to publish plan-level quality scores across standardized domains including access, care coordination, and health outcomes.",
            "url": "https://www.federalregister.gov/documents/2026/02/05/2026-02311/medicaid-managed-care-quality-rating",
            "tags": ["medicaid", "managed-care", "quality", "cms"],
            "metadata": {"document_type": "Proposed Rule", "agency": "CMS", "docket_id": "CMS-2026-0041"},
        },
        {
            "title": "Final Rule: SNAP Employment and Training Program Modernization",
            "summary": "USDA finalizes updates to SNAP E&T programs, expanding allowable training activities to include digital literacy, remote-work readiness, and micro-credentialing. Increases federal reimbursement rate for state-administered programs from 50% to 65%.",
            "url": "https://www.federalregister.gov/documents/2026/01/28/2026-01788/snap-employment-training-modernization",
            "tags": ["snap", "employment", "workforce", "usda"],
            "metadata": {"document_type": "Final Rule", "agency": "USDA-FNS", "docket_id": "FNS-2025-0093"},
        },
        {
            "title": "Notice: TANF Data Collection and Reporting Requirements Update",
            "summary": "ACF announces revised reporting requirements for TANF programs, mandating cross-system data sharing metrics and outcome tracking across employment, housing stability, and child well-being domains beginning FY2027.",
            "url": "https://www.federalregister.gov/documents/2026/02/10/2026-02490/tanf-data-reporting-update",
            "tags": ["tanf", "data-reporting", "acf", "outcomes"],
            "metadata": {"document_type": "Notice", "agency": "ACF", "docket_id": "ACF-2026-0012"},
        },
        {
            "title": "Proposed Rule: Housing Choice Voucher Mobility Demonstration Expansion",
            "summary": "HUD proposes expanding the Housing Choice Voucher mobility demonstration to 25 additional metropolitan areas, with enhanced portability provisions and landlord incentive payments to increase voucher utilization in opportunity neighborhoods.",
            "url": "https://www.federalregister.gov/documents/2026/01/15/2026-00934/hcv-mobility-demonstration-expansion",
            "tags": ["housing", "vouchers", "hud", "mobility"],
            "metadata": {"document_type": "Proposed Rule", "agency": "HUD", "docket_id": "HUD-2026-0008"},
        },
        {
            "title": "Final Rule: Child Welfare Information Gateway Interoperability Standards",
            "summary": "ACF finalizes mandatory interoperability standards for state child welfare information systems (CCWIS), requiring real-time data exchange capabilities with Medicaid, education, and housing systems by 2028.",
            "url": "https://www.federalregister.gov/documents/2026/02/01/2026-02100/ccwis-interoperability-standards",
            "tags": ["child-welfare", "ccwis", "interoperability", "acf"],
            "metadata": {"document_type": "Final Rule", "agency": "ACF", "docket_id": "ACF-2025-0088"},
        },
        {
            "title": "Notice: Workforce Innovation and Opportunity Act Performance Indicators Revision",
            "summary": "DOL publishes revised primary indicators of performance under WIOA, adding measures for credential attainment within 1 year, employer satisfaction, and cross-program coordination effectiveness.",
            "url": "https://www.federalregister.gov/documents/2026/01/20/2026-01205/wioa-performance-indicators-revision",
            "tags": ["workforce", "wioa", "performance", "dol"],
            "metadata": {"document_type": "Notice", "agency": "DOL-ETA", "docket_id": "ETA-2026-0003"},
        },
    ]

    async def scan(self, days_back: int = 7) -> list[Discovery]:
        if not DEMO_MODE:
            try:
                return await self._real_scan(days_back)
            except Exception as exc:
                logger.warning("Federal Register real scan failed, falling back to demo: %s", exc)

        return self._demo_scan()

    async def _real_scan(self, days_back: int) -> list[Discovery]:
        start_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        items: list[Discovery] = []

        async with httpx.AsyncClient(timeout=30) as client:
            for kw in self.KEYWORDS:
                resp = await client.get(
                    f"{self.BASE_URL}/documents.json",
                    params={
                        "conditions[term]": kw,
                        "conditions[publication_date][gte]": start_date,
                        "per_page": 5,
                        "order": "newest",
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                for doc in data.get("results", []):
                    score = self._score_document(doc, kw)
                    items.append(Discovery(
                        source_type=SourceType.federal_register,
                        title=doc.get("title", "Untitled"),
                        summary=doc.get("abstract", doc.get("title", "")),
                        url=doc.get("html_url", ""),
                        relevance_score=score,
                        impact_level=_pick_impact(score),
                        tags=[kw.lower().replace(" ", "-")],
                        metadata_json={
                            "document_type": doc.get("type", ""),
                            "agency": ", ".join(a.get("name", "") for a in doc.get("agencies", [])),
                            "publication_date": doc.get("publication_date", ""),
                        },
                    ))
        return items

    def _score_document(self, doc: dict, keyword: str) -> int:
        text = f"{doc.get('title', '')} {doc.get('abstract', '')}".lower()
        count = sum(text.count(k.lower()) for k in self.KEYWORDS)
        base = min(40 + count * 8, 98)
        # Boost for rules vs notices
        if doc.get("type") in ("Rule", "Proposed Rule"):
            base = min(base + 10, 99)
        return base

    def _demo_scan(self) -> list[Discovery]:
        items: list[Discovery] = []
        for entry in self._DEMO_ITEMS:
            score = _deterministic_score(entry["url"])
            items.append(Discovery(
                source_type=SourceType.federal_register,
                title=entry["title"],
                summary=entry["summary"],
                url=entry["url"],
                relevance_score=score,
                impact_level=_pick_impact(score),
                discovered_at=_random_date(14),
                tags=entry["tags"],
                metadata_json=entry["metadata"],
            ))
        return items


# ===================================================================
# 2. eCFR Scanner
# ===================================================================

class ECFRScanner:
    """
    Scans the eCFR API for regulatory text changes in:
    - Title 20 (Employees' Benefits)
    - Title 24 (Housing and Urban Development)
    - Title 34 (Education)
    - Title 42 (Public Health and Welfare)
    - Title 45 (Public Welfare)
    """

    SOURCE_NAME = "eCFR"
    BASE_URL = "https://www.ecfr.gov/api"
    TITLES = {
        20: "Employees' Benefits",
        24: "Housing and Urban Development",
        34: "Education",
        42: "Public Health and Welfare",
        45: "Public Welfare",
    }

    _DEMO_ITEMS = [
        {
            "title": "42 CFR Part 438 -- Managed Care: Grievance and Appeal System Amendments",
            "summary": "Updated regulatory text refines the grievance and appeal system requirements for Medicaid managed care organizations, including shortened timelines for expedited reviews and new requirements for plain-language notices to enrollees.",
            "url": "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-438/subpart-F",
            "tags": ["medicaid", "managed-care", "grievance", "42-cfr"],
            "metadata": {"cfr_title": 42, "cfr_part": 438, "subpart": "F", "change_type": "amendment"},
        },
        {
            "title": "45 CFR Part 205 -- General Administrative Requirements: Data Exchange Standards",
            "summary": "New regulatory language establishes minimum data exchange standards for state agencies administering TANF, SNAP, and Medicaid programs, requiring adoption of FHIR-based interoperability protocols by January 2028.",
            "url": "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-205",
            "tags": ["data-exchange", "interoperability", "fhir", "45-cfr"],
            "metadata": {"cfr_title": 45, "cfr_part": 205, "subpart": "A", "change_type": "new_section"},
        },
        {
            "title": "24 CFR Part 982 -- Section 8 Tenant-Based Assistance: Payment Standards Update",
            "summary": "Revised payment standard calculations for the Housing Choice Voucher program incorporating Small Area Fair Market Rents (SAFMRs) as the default methodology for metropolitan statistical areas with high rent variation.",
            "url": "https://www.ecfr.gov/current/title-24/subtitle-B/chapter-IX/part-982/subpart-K",
            "tags": ["housing", "section-8", "safmr", "24-cfr"],
            "metadata": {"cfr_title": 24, "cfr_part": 982, "subpart": "K", "change_type": "amendment"},
        },
        {
            "title": "20 CFR Part 416 -- Supplemental Security Income: Resource Exclusion Modernization",
            "summary": "SSA amends resource exclusion rules for SSI, increasing the general resource limit from $2,000 to $10,000 for individuals and from $3,000 to $20,000 for couples, effective October 2026.",
            "url": "https://www.ecfr.gov/current/title-20/chapter-III/part-416/subpart-L",
            "tags": ["ssi", "resources", "ssa", "20-cfr"],
            "metadata": {"cfr_title": 20, "cfr_part": 416, "subpart": "L", "change_type": "amendment"},
        },
        {
            "title": "34 CFR Part 361 -- State Vocational Rehabilitation Programs: Coordinated Service Delivery",
            "summary": "New provisions require state VR agencies to establish formal coordination agreements with TANF agencies, workforce boards, and community mental health centers, with defined referral protocols and shared outcome metrics.",
            "url": "https://www.ecfr.gov/current/title-34/subtitle-B/chapter-III/part-361/subpart-B",
            "tags": ["vocational-rehab", "coordination", "education", "34-cfr"],
            "metadata": {"cfr_title": 34, "cfr_part": 361, "subpart": "B", "change_type": "new_section"},
        },
    ]

    async def scan(self, days_back: int = 14) -> list[Discovery]:
        if not DEMO_MODE:
            try:
                return await self._real_scan(days_back)
            except Exception as exc:
                logger.warning("eCFR real scan failed, falling back to demo: %s", exc)

        return self._demo_scan()

    async def _real_scan(self, days_back: int) -> list[Discovery]:
        start_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        items: list[Discovery] = []

        async with httpx.AsyncClient(timeout=30) as client:
            for title_num, title_name in self.TITLES.items():
                resp = await client.get(
                    f"{self.BASE_URL}/versioner/v1/versions/title-{title_num}.json",
                    params={"on_or_after": start_date},
                )
                resp.raise_for_status()
                data = resp.json()
                for version in data.get("content_versions", [])[:3]:
                    part = version.get("part", "")
                    score = _deterministic_score(f"{title_num}-{part}")
                    items.append(Discovery(
                        source_type=SourceType.ecfr,
                        title=f"{title_num} CFR Part {part} -- {title_name}: Amendment",
                        summary=f"Regulatory text change detected in Title {title_num}, Part {part} ({title_name}). Amendment effective {version.get('date', 'unknown')}.",
                        url=f"https://www.ecfr.gov/current/title-{title_num}/part-{part}",
                        relevance_score=score,
                        impact_level=_pick_impact(score),
                        tags=[f"{title_num}-cfr", title_name.lower().replace(" ", "-")],
                        metadata_json={
                            "cfr_title": title_num,
                            "cfr_part": part,
                            "change_type": "amendment",
                        },
                    ))
        return items

    def _demo_scan(self) -> list[Discovery]:
        items: list[Discovery] = []
        for entry in self._DEMO_ITEMS:
            score = _deterministic_score(entry["url"])
            items.append(Discovery(
                source_type=SourceType.ecfr,
                title=entry["title"],
                summary=entry["summary"],
                url=entry["url"],
                relevance_score=score,
                impact_level=_pick_impact(score),
                discovered_at=_random_date(14),
                tags=entry["tags"],
                metadata_json=entry["metadata"],
            ))
        return items


# ===================================================================
# 3. State Legislation Scanner
# ===================================================================

class StateLegislationScanner:
    """
    Monitors state legislation for key states (PA, NJ, NY, CA, TX, FL)
    using a LegiScan-compatible API structure.
    """

    SOURCE_NAME = "State Legislation Tracker"
    BASE_URL = "https://api.legiscan.com"
    STATES = ["PA", "NJ", "NY", "CA", "TX", "FL"]
    TOPICS = [
        "human services coordination",
        "social determinants of health",
        "system integration",
        "benefits cliff",
        "cross-agency data sharing",
        "reentry services",
    ]

    _DEMO_ITEMS = [
        {
            "title": "PA HB 1247 -- Human Services Integration and Data Sharing Act",
            "summary": "Creates a state-level Human Services Integration Office within the Governor's Office to coordinate data sharing among DHS, DOH, DOC, and PDE. Mandates a unified client identifier system and real-time eligibility verification across programs.",
            "url": "https://legiscan.com/PA/bill/HB1247/2025",
            "tags": ["pennsylvania", "data-sharing", "integration", "legislation"],
            "metadata": {"state": "PA", "bill_id": "HB1247", "session": "2025-2026", "status": "In Committee", "sponsor": "Rep. Martinez"},
        },
        {
            "title": "NJ S 3891 -- Benefits Cliff Mitigation and Transition Support Act",
            "summary": "Establishes graduated benefit reduction schedules for SNAP, TANF, and childcare subsidies in New Jersey to prevent sudden loss of benefits as household income rises. Creates a 24-month transition period with declining subsidies.",
            "url": "https://legiscan.com/NJ/bill/S3891/2025",
            "tags": ["new-jersey", "benefits-cliff", "tanf", "snap", "legislation"],
            "metadata": {"state": "NJ", "bill_id": "S3891", "session": "2025-2026", "status": "Second Reading", "sponsor": "Sen. Williams"},
        },
        {
            "title": "NY A 8834 -- Cross-Agency Reentry Coordination Act",
            "summary": "Requires DOCCS, DOH, OTDA, and HCR to establish a coordinated reentry planning process beginning 90 days before release, including housing placement, Medicaid enrollment, employment services, and behavioral health linkages.",
            "url": "https://legiscan.com/NY/bill/A8834/2025",
            "tags": ["new-york", "reentry", "coordination", "criminal-justice", "legislation"],
            "metadata": {"state": "NY", "bill_id": "A8834", "session": "2025-2026", "status": "Passed Assembly", "sponsor": "Asm. Jackson"},
        },
        {
            "title": "CA AB 2156 -- Social Determinants of Health Screening and Referral Act",
            "summary": "Mandates SDOH screening in all Medi-Cal managed care encounters and requires MCOs to maintain closed-loop referral systems with community-based organizations. Allocates $45M annually for CBO capacity building.",
            "url": "https://legiscan.com/CA/bill/AB2156/2025",
            "tags": ["california", "sdoh", "medicaid", "referral", "legislation"],
            "metadata": {"state": "CA", "bill_id": "AB2156", "session": "2025-2026", "status": "In Committee", "sponsor": "Asm. Chen"},
        },
        {
            "title": "TX HB 4420 -- Whole Family Services Coordination Pilot Program",
            "summary": "Authorizes a 3-year pilot in 5 Texas counties for a whole-family case management model, co-locating TANF, SNAP, WIC, childcare, and workforce services in community hubs with shared case plans and outcomes tracking.",
            "url": "https://legiscan.com/TX/bill/HB4420/2025",
            "tags": ["texas", "whole-family", "pilot", "coordination", "legislation"],
            "metadata": {"state": "TX", "bill_id": "HB4420", "session": "2025-2026", "status": "Enrolled", "sponsor": "Rep. Davis"},
        },
        {
            "title": "FL SB 1088 -- Integrated Eligibility System Modernization Act",
            "summary": "Appropriates $120M over 4 years to replace Florida's legacy eligibility systems with a cloud-based integrated platform supporting real-time eligibility determination across SNAP, TANF, Medicaid, and childcare assistance.",
            "url": "https://legiscan.com/FL/bill/SB1088/2025",
            "tags": ["florida", "eligibility", "modernization", "technology", "legislation"],
            "metadata": {"state": "FL", "bill_id": "SB1088", "session": "2025-2026", "status": "In Committee", "sponsor": "Sen. Thompson"},
        },
        {
            "title": "PA SB 782 -- Child Welfare and Behavioral Health System Alignment Act",
            "summary": "Requires DHS to align child welfare service plans with behavioral health treatment plans for children in out-of-home placements. Establishes joint training requirements for caseworkers and clinicians.",
            "url": "https://legiscan.com/PA/bill/SB782/2025",
            "tags": ["pennsylvania", "child-welfare", "behavioral-health", "alignment", "legislation"],
            "metadata": {"state": "PA", "bill_id": "SB782", "session": "2025-2026", "status": "Third Reading", "sponsor": "Sen. Brooks"},
        },
    ]

    async def scan(self) -> list[Discovery]:
        if not DEMO_MODE:
            try:
                return await self._real_scan()
            except Exception as exc:
                logger.warning("State legislation real scan failed, falling back to demo: %s", exc)

        return self._demo_scan()

    async def _real_scan(self) -> list[Discovery]:
        items: list[Discovery] = []
        async with httpx.AsyncClient(timeout=30) as client:
            for state in self.STATES:
                for topic in self.TOPICS[:2]:  # limit to avoid rate-limits
                    resp = await client.get(
                        self.BASE_URL,
                        params={
                            "op": "getSearch",
                            "state": state,
                            "query": topic,
                            "key": "DEMO",  # would need a real key
                        },
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    for bill in data.get("searchresult", {}).values():
                        if not isinstance(bill, dict):
                            continue
                        title = bill.get("title", "")
                        score = _deterministic_score(f"{state}-{bill.get('bill_id', '')}")
                        items.append(Discovery(
                            source_type=SourceType.state_legislation,
                            title=f"{state} {bill.get('bill_number', '')} -- {title}",
                            summary=title,
                            url=bill.get("url", ""),
                            relevance_score=score,
                            impact_level=_pick_impact(score),
                            tags=[state.lower(), "legislation"],
                            metadata_json={"state": state, "bill_id": bill.get("bill_id")},
                        ))
        return items

    def _demo_scan(self) -> list[Discovery]:
        items: list[Discovery] = []
        for entry in self._DEMO_ITEMS:
            score = _deterministic_score(entry["url"])
            items.append(Discovery(
                source_type=SourceType.state_legislation,
                title=entry["title"],
                summary=entry["summary"],
                url=entry["url"],
                relevance_score=score,
                impact_level=_pick_impact(score),
                discovered_at=_random_date(10),
                tags=entry["tags"],
                metadata_json=entry["metadata"],
            ))
        return items


# ===================================================================
# 4. Academic Scanner
# ===================================================================

class AcademicScanner:
    """
    Searches Semantic Scholar for recent academic research related to
    super-utilizer populations, care coordination, social determinants,
    and cross-system integration.
    """

    SOURCE_NAME = "Semantic Scholar"
    BASE_URL = "https://api.semanticscholar.org/graph/v1"
    QUERIES = [
        "super-utilizer high-cost high-need populations",
        "care coordination cross-system integration",
        "social determinants of health data systems",
        "wraparound services multi-system youth",
        "benefits cliff income volatility public assistance",
        "criminal justice reentry social services coordination",
    ]

    _DEMO_ITEMS = [
        {
            "title": "Cross-System Data Integration for Identifying Super-Utilizers: A Multi-State Analysis",
            "summary": "Analyzes linked administrative data from Medicaid, homeless services, criminal justice, and behavioral health systems across 8 states. Finds that 4.2% of individuals account for 38% of total public expenditure. Identifies predictive factors for cross-system super-utilization and proposes a risk stratification framework.",
            "url": "https://api.semanticscholar.org/paper/a1b2c3d4e5f6",
            "tags": ["super-utilizer", "data-integration", "risk-stratification", "multi-state"],
            "metadata": {"authors": ["Chen, L.", "Patel, R.", "Williams, K."], "year": 2026, "venue": "Health Affairs", "citation_count": 12},
        },
        {
            "title": "The Benefits Cliff in Practice: Longitudinal Analysis of Income Volatility Among TANF Leavers",
            "summary": "Tracks 15,000 TANF recipients over 5 years after exit, documenting income trajectories and benefit loss patterns. Finds that 62% experience a net income decline within 18 months of TANF exit due to simultaneous loss of SNAP, childcare, and Medicaid benefits. Proposes graduated phase-out model.",
            "url": "https://api.semanticscholar.org/paper/b2c3d4e5f6g7",
            "tags": ["benefits-cliff", "tanf", "income-volatility", "longitudinal"],
            "metadata": {"authors": ["Rodriguez, M.", "Kim, S."], "year": 2025, "venue": "Journal of Policy Analysis and Management", "citation_count": 28},
        },
        {
            "title": "Wraparound Services for Justice-Involved Youth: A Randomized Controlled Trial",
            "summary": "RCT of 800 justice-involved youth assigned to either wraparound coordination (including education, behavioral health, family support, and housing) or standard probation. Wraparound group showed 43% reduction in recidivism, 67% improvement in school attendance, and 55% reduction in emergency department visits at 24-month follow-up.",
            "url": "https://api.semanticscholar.org/paper/c3d4e5f6g7h8",
            "tags": ["wraparound", "juvenile-justice", "rct", "recidivism"],
            "metadata": {"authors": ["Thompson, A.", "Garcia, J.", "Lee, H.", "Brown, D."], "year": 2026, "venue": "JAMA Pediatrics", "citation_count": 7},
        },
        {
            "title": "Machine Learning Approaches to Predicting Housing Instability Using Cross-Agency Administrative Data",
            "summary": "Develops ML models using features from 6 administrative data systems (HMIS, Medicaid, TANF, SNAP, criminal justice, child welfare) to predict housing instability 6 months in advance. Gradient boosted model achieves AUC of 0.84. Key predictive features include ER visit frequency, benefit gap duration, and prior homelessness episodes.",
            "url": "https://api.semanticscholar.org/paper/d4e5f6g7h8i9",
            "tags": ["machine-learning", "housing", "prediction", "administrative-data"],
            "metadata": {"authors": ["Wang, X.", "Johnson, T."], "year": 2025, "venue": "Social Science & Medicine", "citation_count": 19},
        },
        {
            "title": "Interoperability Standards for Human Services: A Systematic Review of FHIR Implementation in Social Care",
            "summary": "Systematic review of 34 studies examining FHIR implementation for social care data exchange. Identifies key barriers including vocabulary gaps for social determinants, consent management complexity, and workforce digital literacy. Proposes an extension framework for human services interoperability.",
            "url": "https://api.semanticscholar.org/paper/e5f6g7h8i9j0",
            "tags": ["interoperability", "fhir", "social-care", "systematic-review"],
            "metadata": {"authors": ["Park, S.", "O'Brien, C.", "Nguyen, T."], "year": 2026, "venue": "JAMIA", "citation_count": 5},
        },
    ]

    async def scan(self) -> list[Discovery]:
        if not DEMO_MODE:
            try:
                return await self._real_scan()
            except Exception as exc:
                logger.warning("Academic real scan failed, falling back to demo: %s", exc)

        return self._demo_scan()

    async def _real_scan(self) -> list[Discovery]:
        items: list[Discovery] = []
        year = datetime.utcnow().year
        async with httpx.AsyncClient(timeout=30) as client:
            for query in self.QUERIES:
                resp = await client.get(
                    f"{self.BASE_URL}/paper/search",
                    params={
                        "query": query,
                        "year": f"{year - 1}-{year}",
                        "limit": 3,
                        "fields": "title,abstract,url,year,authors,citationCount,venue",
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                for paper in data.get("data", []):
                    abstract = paper.get("abstract") or paper.get("title", "")
                    score = self._score_paper(paper)
                    items.append(Discovery(
                        source_type=SourceType.academic,
                        title=paper.get("title", "Untitled Paper"),
                        summary=abstract[:500],
                        url=paper.get("url", f"https://api.semanticscholar.org/paper/{paper.get('paperId', '')}"),
                        relevance_score=score,
                        impact_level=_pick_impact(score),
                        tags=["academic", query.split()[0].lower()],
                        metadata_json={
                            "authors": [a.get("name", "") for a in paper.get("authors", [])[:5]],
                            "year": paper.get("year"),
                            "venue": paper.get("venue", ""),
                            "citation_count": paper.get("citationCount", 0),
                        },
                    ))
        return items

    def _score_paper(self, paper: dict) -> int:
        text = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
        priority_terms = ["super-utilizer", "cross-system", "integration", "coordination", "social determinants"]
        hits = sum(1 for t in priority_terms if t in text)
        citations = paper.get("citationCount", 0)
        base = 35 + hits * 10 + min(citations, 20)
        return min(base, 98)

    def _demo_scan(self) -> list[Discovery]:
        items: list[Discovery] = []
        for entry in self._DEMO_ITEMS:
            score = _deterministic_score(entry["url"])
            items.append(Discovery(
                source_type=SourceType.academic,
                title=entry["title"],
                summary=entry["summary"],
                url=entry["url"],
                relevance_score=score,
                impact_level=_pick_impact(score),
                discovered_at=_random_date(30),
                tags=entry["tags"],
                metadata_json=entry["metadata"],
            ))
        return items


# ===================================================================
# 5. News Scanner
# ===================================================================

class NewsScanner:
    """
    Monitors news for policy changes, system failures, benefits cliff events,
    and human services technology developments.
    """

    SOURCE_NAME = "News Monitor"
    BASE_URL = "https://newsapi.org/v2"
    SEARCH_TERMS = [
        "government coordination failure social services",
        "benefits cliff poverty trap",
        "human services technology modernization",
        "child welfare system failure",
        "Medicaid unwinding coverage loss",
        "homeless services data integration",
    ]

    _DEMO_ITEMS = [
        {
            "title": "GAO Report Finds Critical Gaps in Federal-State Data Sharing for Public Benefits",
            "summary": "A new Government Accountability Office report reveals that fragmented data systems between federal and state agencies result in an estimated $14.2 billion annually in improper payments, delayed benefits, and duplicated administrative costs across SNAP, Medicaid, and TANF programs.",
            "url": "https://www.govexec.com/technology/2026/02/gao-federal-state-data-sharing-gaps/412847/",
            "tags": ["gao", "data-sharing", "improper-payments", "federal-state"],
            "metadata": {"source": "Government Executive", "published_at": "2026-02-08T14:30:00Z", "category": "policy"},
        },
        {
            "title": "Philadelphia Launches Unified Case Management Pilot for Multi-System Families",
            "summary": "The City of Philadelphia announced a $8.5 million pilot program to create a unified case management platform for families involved in three or more public service systems. The pilot will integrate child welfare, behavioral health, housing, and workforce data for 2,000 families over 2 years.",
            "url": "https://www.inquirer.com/news/philadelphia-unified-case-management-pilot-2026.html",
            "tags": ["philadelphia", "case-management", "integration", "pilot"],
            "metadata": {"source": "Philadelphia Inquirer", "published_at": "2026-02-03T09:15:00Z", "category": "local"},
        },
        {
            "title": "Study: 3.2 Million Children Lost Medicaid Coverage Due to Renewal Processing Failures",
            "summary": "New analysis from Georgetown University's Center for Children and Families finds that 3.2 million children lost Medicaid coverage during the unwinding period not because they were ineligible but due to administrative processing failures, returned mail, and system errors.",
            "url": "https://www.healthaffairs.org/content/forefront/medicaid-unwinding-children-coverage-losses",
            "tags": ["medicaid", "unwinding", "children", "coverage-loss"],
            "metadata": {"source": "Health Affairs", "published_at": "2026-01-28T11:00:00Z", "category": "health-policy"},
        },
        {
            "title": "California Allocates $200M for Statewide Social Determinants Data Infrastructure",
            "summary": "Governor signs budget allocation of $200 million over 3 years to build CalSDOH, a statewide social determinants of health data infrastructure connecting health plans, hospitals, community organizations, and public agencies. System will support closed-loop referrals and population-level analytics.",
            "url": "https://www.governing.com/health/california-200m-social-determinants-data-infrastructure",
            "tags": ["california", "sdoh", "infrastructure", "investment"],
            "metadata": {"source": "Governing", "published_at": "2026-02-01T16:45:00Z", "category": "state-policy"},
        },
        {
            "title": "Bipartisan Bill Would Require Federal Agencies to Share Benefits Eligibility Data",
            "summary": "Senators Collins (R-ME) and Hassan (D-NH) introduce the Benefits Coordination Improvement Act, requiring HHS, USDA, HUD, DOL, and SSA to establish automated data sharing for eligibility verification. Bill includes $50M for a shared API infrastructure.",
            "url": "https://www.nextgov.com/policy/2026/02/bipartisan-bill-benefits-eligibility-data-sharing/412901/",
            "tags": ["federal", "bipartisan", "data-sharing", "eligibility", "legislation"],
            "metadata": {"source": "Nextgov", "published_at": "2026-02-06T10:30:00Z", "category": "federal-policy"},
        },
        {
            "title": "Texas County Sees 40% Drop in Recidivism After Implementing Cross-Agency Reentry Program",
            "summary": "Harris County, Texas reports a 40% reduction in 2-year recidivism rates after implementing a cross-agency reentry coordination program connecting the sheriff's office, workforce board, housing authority, and community health centers through a shared data platform and unified case management.",
            "url": "https://www.governing.com/public-safety/harris-county-reentry-program-recidivism-reduction",
            "tags": ["texas", "reentry", "recidivism", "cross-agency", "success-story"],
            "metadata": {"source": "Governing", "published_at": "2026-01-22T13:00:00Z", "category": "criminal-justice"},
        },
    ]

    async def scan(self) -> list[Discovery]:
        if not DEMO_MODE:
            try:
                return await self._real_scan()
            except Exception as exc:
                logger.warning("News real scan failed, falling back to demo: %s", exc)

        return self._demo_scan()

    async def _real_scan(self) -> list[Discovery]:
        items: list[Discovery] = []
        async with httpx.AsyncClient(timeout=30) as client:
            for term in self.SEARCH_TERMS:
                resp = await client.get(
                    f"{self.BASE_URL}/everything",
                    params={
                        "q": term,
                        "language": "en",
                        "sortBy": "publishedAt",
                        "pageSize": 3,
                        "apiKey": "DEMO",  # would need a real key
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                for article in data.get("articles", []):
                    title = article.get("title", "")
                    desc = article.get("description", "")
                    score = _deterministic_score(article.get("url", title))
                    items.append(Discovery(
                        source_type=SourceType.news,
                        title=title,
                        summary=desc[:500] if desc else title,
                        url=article.get("url", ""),
                        relevance_score=score,
                        impact_level=_pick_impact(score),
                        tags=["news", term.split()[0].lower()],
                        metadata_json={
                            "source": article.get("source", {}).get("name", ""),
                            "published_at": article.get("publishedAt", ""),
                            "category": "news",
                        },
                    ))
        return items

    def _demo_scan(self) -> list[Discovery]:
        items: list[Discovery] = []
        for entry in self._DEMO_ITEMS:
            score = _deterministic_score(entry["url"])
            items.append(Discovery(
                source_type=SourceType.news,
                title=entry["title"],
                summary=entry["summary"],
                url=entry["url"],
                relevance_score=score,
                impact_level=_pick_impact(score),
                discovered_at=_random_date(7),
                tags=entry["tags"],
                metadata_json=entry["metadata"],
            ))
        return items


# ===================================================================
# 6. Gap Analyzer
# ===================================================================

class GapAnalyzer:
    """
    Analyses coverage across all DOMES applications.  Pings each service
    for its data scope, identifies domains or jurisdictions not covered,
    and flags stale data.
    """

    SOURCE_NAME = "DOMES Gap Analyzer"

    # Known DOMES services and their expected endpoints
    SERVICES = {
        "domes-legal-research": {"url": "http://localhost:8000", "domain": "Legal Rights"},
        "spheres-assets": {"url": "http://localhost:8000", "domain": "Public Assets"},
        "domes-data-research": {"url": "http://localhost:8001", "domain": "Government Data Systems"},
        "domes-profile-research": {"url": "http://localhost:8002", "domain": "Composite Profiles"},
        "domes-contracts": {"url": "http://localhost:8003", "domain": "Agreements"},
        "domes-architect": {"url": "http://localhost:8004", "domain": "Coordination Architecture"},
    }

    _DEMO_ITEMS = [
        {
            "title": "Coverage Gap: No Housing Authority Data Integration for NJ, NY",
            "summary": "The DOMES ecosystem currently integrates housing authority data only for Philadelphia (PHA). Housing authorities in Camden (NJ), Newark (NJ), and New York City (NYCHA) are not covered. This represents a significant gap for cross-jurisdictional housing analysis affecting an estimated 520,000 voucher holders.",
            "url": "internal://gap-analysis/housing-authority-coverage",
            "tags": ["gap", "housing", "jurisdiction", "nj", "ny"],
            "metadata": {"gap_type": "jurisdiction", "domain": "Housing", "affected_population_est": 520000, "priority": "high"},
        },
        {
            "title": "Stale Data: Criminal Justice Reentry Programs Database Last Updated 47 Days Ago",
            "summary": "The criminal justice reentry programs dataset in domes-data-research has not been refreshed in 47 days (threshold: 30 days). This may affect profile completeness for justice-involved individuals and accuracy of available reentry services information.",
            "url": "internal://gap-analysis/stale-data/criminal-justice-reentry",
            "tags": ["stale-data", "criminal-justice", "reentry", "data-quality"],
            "metadata": {"gap_type": "stale_data", "domain": "Justice", "days_since_update": 47, "threshold_days": 30, "service": "domes-data-research"},
        },
        {
            "title": "Coverage Gap: No Workforce Development Board Data for Rural Counties",
            "summary": "Workforce development board data is limited to urban/suburban counties. 23 rural counties in Pennsylvania have no representation in the workforce data constellation, affecting service coordination for approximately 180,000 residents in poverty.",
            "url": "internal://gap-analysis/workforce-rural-counties",
            "tags": ["gap", "workforce", "rural", "pennsylvania"],
            "metadata": {"gap_type": "coverage", "domain": "Employment", "missing_counties": 23, "state": "PA", "affected_population_est": 180000},
        },
        {
            "title": "Integration Gap: Child Welfare and Education Data Not Cross-Referenced",
            "summary": "Profile builder does not currently cross-reference child welfare involvement with educational outcomes data. This prevents identification of educational disruption patterns among children in foster care, a critical factor in long-term outcome planning.",
            "url": "internal://gap-analysis/child-welfare-education-linkage",
            "tags": ["gap", "child-welfare", "education", "integration"],
            "metadata": {"gap_type": "integration", "domains": ["Child Welfare", "Education"], "service": "domes-profile-research"},
        },
        {
            "title": "Coverage Gap: Behavioral Health Provider Directory Incomplete for Medicaid Providers",
            "summary": "The behavioral health provider directory in domes-data-research covers only 34% of Medicaid-enrolled behavioral health providers in the Philadelphia region. Missing providers include 67% of substance use disorder treatment facilities and 45% of community mental health centers.",
            "url": "internal://gap-analysis/behavioral-health-providers",
            "tags": ["gap", "behavioral-health", "medicaid", "providers", "directory"],
            "metadata": {"gap_type": "coverage", "domain": "Health", "coverage_pct": 34, "missing_sud_pct": 67, "missing_cmhc_pct": 45},
        },
    ]

    async def scan(self) -> list[Discovery]:
        if not DEMO_MODE:
            try:
                return await self._real_scan()
            except Exception as exc:
                logger.warning("Gap analysis real scan failed, falling back to demo: %s", exc)

        return self._demo_scan()

    async def _real_scan(self) -> list[Discovery]:
        """Ping each DOMES service and check for availability / staleness."""
        items: list[Discovery] = []
        async with httpx.AsyncClient(timeout=10) as client:
            for svc_name, svc_info in self.SERVICES.items():
                try:
                    resp = await client.get(f"{svc_info['url']}/api/health")
                    if resp.status_code != 200:
                        raise httpx.HTTPStatusError("unhealthy", request=resp.request, response=resp)
                except Exception:
                    score = 75
                    items.append(Discovery(
                        source_type=SourceType.gap_analysis,
                        title=f"Service Unreachable: {svc_name}",
                        summary=f"The {svc_name} service ({svc_info['domain']}) at {svc_info['url']} did not respond to health check. This may indicate downtime or misconfiguration.",
                        url=f"internal://gap-analysis/service-health/{svc_name}",
                        relevance_score=score,
                        impact_level=_pick_impact(score),
                        tags=["gap", "service-health", svc_name],
                        metadata_json={"gap_type": "service_health", "service": svc_name, "domain": svc_info["domain"]},
                    ))

        # Always add the demo items for comprehensive coverage analysis
        items.extend(self._demo_scan())
        return items

    def _demo_scan(self) -> list[Discovery]:
        items: list[Discovery] = []
        for entry in self._DEMO_ITEMS:
            score = _deterministic_score(entry["url"])
            items.append(Discovery(
                source_type=SourceType.gap_analysis,
                title=entry["title"],
                summary=entry["summary"],
                url=entry["url"],
                relevance_score=score,
                impact_level=_pick_impact(score),
                discovered_at=_random_date(3),
                tags=entry["tags"],
                metadata_json=entry["metadata"],
            ))
        return items


# ===================================================================
# Scanner Registry
# ===================================================================

SCANNER_REGISTRY: dict[str, object] = {
    "federal_register": FederalRegisterScanner(),
    "ecfr": ECFRScanner(),
    "state_legislation": StateLegislationScanner(),
    "academic": AcademicScanner(),
    "news": NewsScanner(),
    "gap_analysis": GapAnalyzer(),
}


async def run_scanner(source_type: Optional[str] = None) -> list[ScanResult]:
    """
    Run one or all scanners.  Returns a list of ScanResult summaries.
    The actual Discovery items are returned separately by each scanner.
    """
    scanners_to_run = (
        {source_type: SCANNER_REGISTRY[source_type]}
        if source_type and source_type in SCANNER_REGISTRY
        else SCANNER_REGISTRY
    )

    results: list[ScanResult] = []
    for stype, scanner in scanners_to_run.items():
        t0 = time.monotonic()
        try:
            discoveries = await scanner.scan()
            duration_ms = int((time.monotonic() - t0) * 1000)
            results.append(ScanResult(
                source_name=stype,
                items_found=len(discoveries),
                new_items=len(discoveries),  # caller will de-dup before persisting
                scan_duration_ms=duration_ms,
            ))
        except Exception as exc:
            logger.exception("Scanner %s failed: %s", stype, exc)
            duration_ms = int((time.monotonic() - t0) * 1000)
            results.append(ScanResult(
                source_name=stype,
                items_found=0,
                new_items=0,
                scan_duration_ms=duration_ms,
            ))
    return results


async def run_scanner_and_collect(source_type: Optional[str] = None) -> tuple[list[Discovery], list[ScanResult]]:
    """
    Run scanners and return both the raw Discovery items and the ScanResult
    summaries.  Used by the API endpoint to persist results.
    """
    scanners_to_run = (
        {source_type: SCANNER_REGISTRY[source_type]}
        if source_type and source_type in SCANNER_REGISTRY
        else SCANNER_REGISTRY
    )

    all_discoveries: list[Discovery] = []
    results: list[ScanResult] = []

    for stype, scanner in scanners_to_run.items():
        t0 = time.monotonic()
        try:
            discoveries = await scanner.scan()
            duration_ms = int((time.monotonic() - t0) * 1000)
            all_discoveries.extend(discoveries)
            results.append(ScanResult(
                source_name=stype,
                items_found=len(discoveries),
                new_items=len(discoveries),
                scan_duration_ms=duration_ms,
            ))
        except Exception as exc:
            logger.exception("Scanner %s failed: %s", stype, exc)
            duration_ms = int((time.monotonic() - t0) * 1000)
            results.append(ScanResult(
                source_name=stype,
                items_found=0,
                new_items=0,
                scan_duration_ms=duration_ms,
            ))

    return all_discoveries, results
