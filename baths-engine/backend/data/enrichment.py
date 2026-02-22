"""
Enrichment Engine — Cross-references data across all engines to discover patterns.

This is what makes the data get SMARTER over time. Each enrichment run:
  1. Cross-references legal provisions with cost data
  2. Maps provisions to government systems they affect
  3. Identifies regulatory conflicts between systems
  4. Calculates coordination opportunity scores
  5. Detects cost anomalies and fragmentation hotspots
  6. Builds a knowledge graph of connections

Every discovery is stored as an enrichment record. The games surface these
insights — they're what make a DOMES player feel the real weight of
fragmentation and a SPHERES player see the real opportunity in a parcel.
"""

import json
import logging
import re
from .store import DataStore, get_store

logger = logging.getLogger("baths.enrichment")


class EnrichmentEngine:
    """Cross-references all data engines to produce insights."""

    def __init__(self, store: DataStore | None = None):
        self.store = store or get_store()

    def run_all(self) -> dict:
        """Run all enrichment passes. Returns counts by type."""
        results = {}
        results["legal_cost_links"] = self._link_provisions_to_costs()
        results["legal_system_links"] = self._link_provisions_to_systems()
        results["regulatory_conflicts"] = self._detect_regulatory_conflicts()
        results["coordination_opportunities"] = self._score_coordination_opportunities()
        results["fragmentation_hotspots"] = self._detect_fragmentation_hotspots()
        results["parcel_opportunities"] = self._score_parcel_opportunities()
        total = sum(results.values())
        logger.info(f"Enrichment completed: {total} new insights across {len(results)} passes")
        return results

    def _link_provisions_to_costs(self) -> int:
        """Cross-reference legal provisions with cost data they affect."""
        provisions = self.store.get_provisions(limit=500)
        costs = self.store.get_costs(limit=500)
        count = 0

        # Build cost lookup by category
        cost_by_cat = {}
        for c in costs:
            cat = c.get("category", "")
            cost_by_cat.setdefault(cat, []).append(c)

        # Map dome dimensions to cost categories
        dimension_to_cost = {
            "healthcare": ["healthcare", "fragmentation"],
            "housing": ["housing", "shelter"],
            "income": ["fragmentation"],
            "food": ["food"],
            "employment": ["education", "fragmentation"],
            "education": ["education"],
            "justice": ["incarceration"],
            "data_privacy": ["fragmentation"],
            "interoperability": ["fragmentation"],
        }

        for prov in provisions:
            dimension = prov.get("dome_dimension", "")
            cost_cats = dimension_to_cost.get(dimension, [])

            for cat in cost_cats:
                relevant_costs = cost_by_cat.get(cat, [])
                for cost in relevant_costs[:3]:  # Top 3 most relevant per category
                    self.store.add_enrichment(
                        enrichment_type="cross_ref",
                        source_table="provisions",
                        source_id=prov.get("id", 0),
                        target_table="cost_points",
                        target_id=cost.get("id", 0),
                        description=(
                            f"Provision {prov.get('citation', '')} ({dimension}) "
                            f"relates to cost: {cost.get('metric', '')} "
                            f"(${cost.get('value', 0):,.0f} {cost.get('unit', '')})"
                        ),
                        confidence=0.7,
                        data={
                            "provision_citation": prov.get("citation", ""),
                            "provision_dimension": dimension,
                            "cost_metric": cost.get("metric", ""),
                            "cost_value": cost.get("value", 0),
                            "cost_unit": cost.get("unit", ""),
                        },
                    )
                    count += 1

        return count

    def _link_provisions_to_systems(self) -> int:
        """Map legal provisions to the government systems they govern."""
        provisions = self.store.get_provisions(limit=500)
        systems = self.store.get_systems(limit=200)
        count = 0

        # Build system lookup by domain
        system_by_domain = {}
        for s in systems:
            domain = s.get("domain", "")
            system_by_domain.setdefault(domain, []).append(s)

        # Map dome dimensions to system domains
        dimension_to_domain = {
            "healthcare": ["health"],
            "housing": ["housing"],
            "income": ["income"],
            "food": ["food"],
            "employment": ["employment"],
            "education": ["education"],
            "justice": ["justice"],
            "data_privacy": ["health", "income", "housing"],
            "interoperability": ["health", "income", "housing", "food", "employment"],
        }

        for prov in provisions:
            dimension = prov.get("dome_dimension", "")
            domains = dimension_to_domain.get(dimension, [])
            body = (prov.get("body", "") or "").lower()

            for domain in domains:
                for sys in system_by_domain.get(domain, []):
                    # Check if provision text references this system's agency
                    agency = (sys.get("agency", "") or "").lower()
                    sys_name = (sys.get("name", "") or "").lower()

                    relevance = 0.5  # Base relevance for same domain
                    if any(word in body for word in agency.split()[:2] if len(word) > 3):
                        relevance = 0.8
                    if any(word in body for word in sys_name.split()[:2] if len(word) > 3):
                        relevance = 0.9

                    if relevance >= 0.5:
                        self.store.add_enrichment(
                            enrichment_type="cross_ref",
                            source_table="provisions",
                            source_id=prov.get("id", 0),
                            target_table="gov_systems",
                            target_id=sys.get("id", 0),
                            description=(
                                f"Provision {prov.get('citation', '')} governs/affects "
                                f"system: {sys.get('name', '')} ({sys.get('agency', '')})"
                            ),
                            confidence=relevance,
                            data={
                                "provision_citation": prov.get("citation", ""),
                                "system_code": sys.get("system_code", ""),
                                "system_name": sys.get("name", ""),
                                "relevance_score": relevance,
                            },
                        )
                        count += 1

        return count

    def _detect_regulatory_conflicts(self) -> int:
        """Find provisions that create conflicting requirements across systems."""
        links = self.store.get_system_links(limit=500)
        provisions = self.store.get_provisions(limit=500)
        count = 0

        # Focus on blocked links — these represent regulatory conflicts
        blocked = [l for l in links if l.get("link_type") == "blocked"]

        for link in blocked:
            source = link.get("source_system", "")
            target = link.get("target_system", "")
            authority = link.get("legal_authority", "")

            # Find provisions that reference either system's domain
            relevant_provs = []
            for p in provisions:
                body = (p.get("body", "") or "").lower()
                if (source.lower().split("_")[0] in body or
                    target.lower().split("_")[0] in body or
                    "privacy" in body or "confidentiality" in body or
                    "disclosure" in body):
                    relevant_provs.append(p)

            if relevant_provs:
                self.store.add_enrichment(
                    enrichment_type="conflict",
                    source_table="system_links",
                    source_id=link.get("id", 0),
                    target_table="provisions",
                    target_id=relevant_provs[0].get("id", 0),
                    description=(
                        f"REGULATORY CONFLICT: {source} ↔ {target} blocked by "
                        f"{authority}. {len(relevant_provs)} related provisions found. "
                        f"This barrier prevents coordination that could reduce "
                        f"fragmentation costs."
                    ),
                    confidence=0.85,
                    data={
                        "source_system": source,
                        "target_system": target,
                        "blocking_authority": authority,
                        "related_provisions": [p.get("citation", "") for p in relevant_provs[:5]],
                        "impact": "high",
                    },
                )
                count += 1

        return count

    def _score_coordination_opportunities(self) -> int:
        """Score possible but unimplemented cross-system connections."""
        links = self.store.get_system_links(limit=500)
        costs = self.store.get_costs(category="fragmentation", limit=50)
        count = 0

        possible = [l for l in links if l.get("link_type") == "possible"]

        # Get average coordination savings
        savings_per_person = 36336  # From seed data
        for c in costs:
            if "savings" in (c.get("metric", "") or "").lower():
                savings_per_person = c.get("value", savings_per_person)
                break

        for link in possible:
            source = link.get("source_system", "")
            target = link.get("target_system", "")
            consent = link.get("consent_barrier", "none")
            mechanism = link.get("mechanism", "unknown")

            # Score based on feasibility
            feasibility = 0.5
            if consent == "none":
                feasibility = 0.9
            elif consent == "agency":
                feasibility = 0.7
            elif consent == "individual":
                feasibility = 0.6
            elif consent == "statutory":
                feasibility = 0.3

            if mechanism in ("API", "batch"):
                feasibility = min(1.0, feasibility + 0.1)

            self.store.add_enrichment(
                enrichment_type="opportunity",
                source_table="system_links",
                source_id=link.get("id", 0),
                target_table=None,
                target_id=None,
                description=(
                    f"COORDINATION OPPORTUNITY: {source} → {target}. "
                    f"Feasibility: {feasibility:.0%}. Mechanism: {mechanism}. "
                    f"Consent barrier: {consent}. "
                    f"Estimated annual savings if implemented: significant."
                ),
                confidence=feasibility,
                data={
                    "source_system": source,
                    "target_system": target,
                    "feasibility": feasibility,
                    "consent_barrier": consent,
                    "mechanism": mechanism,
                    "legal_authority": link.get("legal_authority", ""),
                },
            )
            count += 1

        return count

    def _detect_fragmentation_hotspots(self) -> int:
        """Identify populations that fall through gaps between systems."""
        systems = self.store.get_systems(limit=200)
        links = self.store.get_system_links(limit=500)
        count = 0

        # Build adjacency map
        connected = set()
        blocked = set()
        for l in links:
            pair = (l.get("source_system", ""), l.get("target_system", ""))
            if l.get("link_type") in ("active", "one-way"):
                connected.add(pair)
            elif l.get("link_type") == "blocked":
                blocked.add(pair)

        # Identify systems with many blocked connections
        system_codes = [s.get("system_code", "") for s in systems]
        for code in system_codes:
            blocked_count = sum(1 for b in blocked if code in b)
            connected_count = sum(1 for c in connected if code in c)

            if blocked_count >= 2:
                system = next((s for s in systems if s.get("system_code") == code), {})
                self.store.add_enrichment(
                    enrichment_type="gap",
                    source_table="gov_systems",
                    source_id=system.get("id", 0),
                    target_table=None,
                    target_id=None,
                    description=(
                        f"FRAGMENTATION HOTSPOT: {system.get('name', code)} has "
                        f"{blocked_count} blocked connections vs {connected_count} active. "
                        f"Population served: {system.get('population_served', 'unknown')}. "
                        f"People in this system cannot easily coordinate with "
                        f"{blocked_count} other systems."
                    ),
                    confidence=0.8,
                    data={
                        "system_code": code,
                        "system_name": system.get("name", ""),
                        "blocked_connections": blocked_count,
                        "active_connections": connected_count,
                        "isolation_score": blocked_count / max(1, blocked_count + connected_count),
                    },
                )
                count += 1

        return count

    def _score_parcel_opportunities(self) -> int:
        """Score vacant parcels for dome/sphere activation potential."""
        parcels = self.store.get_parcels(vacant=True, limit=200)
        count = 0

        for parcel in parcels:
            extra = parcel.get("extra", "{}")
            if isinstance(extra, str):
                try:
                    extra = json.loads(extra)
                except (json.JSONDecodeError, TypeError):
                    extra = {}

            area = parcel.get("land_area_sqft", 0) or 0
            zoning = parcel.get("zoning", "") or ""
            neighborhood = parcel.get("neighborhood", "") or ""

            # Score based on development potential
            score = 0.3  # Base score for any vacant parcel

            # Size bonuses
            if area > 10000:
                score += 0.2
            elif area > 5000:
                score += 0.1

            # Zoning bonuses (commercial/mixed-use more versatile)
            if "CMX" in zoning:
                score += 0.15
            if "IRMX" in zoning:
                score += 0.2  # Industrial reuse opportunity

            # Special features
            if extra.get("opportunity_zone"):
                score += 0.15
            if extra.get("land_bank"):
                score += 0.1  # Easier acquisition
            if extra.get("near_transit"):
                score += 0.1
            if extra.get("brownfield"):
                score -= 0.1  # Remediation cost

            score = min(1.0, max(0.0, score))

            activation_types = []
            if area > 20000 and "CMX" in zoning:
                activation_types.append("community_hub")
            if area > 5000:
                activation_types.append("affordable_housing")
            if extra.get("eligible_garden") or extra.get("community_garden_potential"):
                activation_types.append("community_garden")
            if "IRMX" in zoning or "I-" in zoning:
                activation_types.append("maker_space")
            if area > 1000:
                activation_types.append("pocket_park")

            self.store.add_enrichment(
                enrichment_type="opportunity",
                source_table="parcels",
                source_id=parcel.get("id", 0),
                target_table=None,
                target_id=None,
                description=(
                    f"ACTIVATION OPPORTUNITY: {parcel.get('address', '')} "
                    f"({area:,.0f} sqft, {zoning}). Score: {score:.0%}. "
                    f"Potential uses: {', '.join(activation_types) or 'general development'}."
                ),
                confidence=score,
                data={
                    "parcel_id": parcel.get("parcel_id", ""),
                    "address": parcel.get("address", ""),
                    "area_sqft": area,
                    "zoning": zoning,
                    "neighborhood": neighborhood,
                    "activation_score": score,
                    "activation_types": activation_types,
                    "land_bank": extra.get("land_bank", False),
                    "opportunity_zone": extra.get("opportunity_zone", False),
                },
            )
            count += 1

        return count
