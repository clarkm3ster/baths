"""
BATHS Game Engine — Pipeline Director
Orchestrates player through Development -> Pre -> Prod -> Post -> Distribution.

Now powered by the elite data engines. Every response is grounded in real
federal regulations, real cost data, real government systems, and real
Philadelphia parcel records. Data gets richer with every scrape cycle.
"""

import os
import json
import httpx
import logging
from typing import Dict, Any, List, Optional

from models import (
    GameType, ProductionStage, ProductionState, StageResult,
    CosmDimensions, ChronDimensions
)
from data.store import get_store
from data.legal import SEED_PROVISIONS
from data.costs import SEED_COST_POINTS
from data.systems import SEED_SYSTEMS, SEED_LINKS
from data.parcels import SEED_PARCELS, ZONING_REFERENCE
from data.coordination import COORDINATION_MODELS, recommend_models
from data.flourishing import (
    FRAMEWORKS, FLOURISHING_INDICATORS, get_flourishing_score
)

logger = logging.getLogger("baths.pipeline")


class PipelineDirector:
    def __init__(self, api_registry: Dict[str, Any]):
        self.api_registry = api_registry
        self.client = httpx.AsyncClient(timeout=10.0)
        self.store = get_store()

    # ── Helper: try backend API, fall back to data engine ─────────────

    async def _call_api(self, service_name: str, endpoint: str,
                        method: str = "GET", data: Optional[Dict] = None) -> Dict[str, Any] | None:
        """Try to reach a backend API. Returns None if unavailable."""
        try:
            game_type = "domes" if service_name.startswith("domes") else "spheres"
            service = self.api_registry.get(game_type, {}).get(service_name)
            if service:
                port = service["port"]
                url = f"http://localhost:{port}{endpoint}"
                if method == "GET":
                    response = await self.client.get(url)
                else:
                    response = await self.client.post(url, json=data or {})
                if response.status_code == 200:
                    return response.json()
        except Exception:
            pass
        return None

    # ══════════════════════════════════════════════════════════════════
    # DOMES PIPELINE — powered by legal, costs, systems, coordination,
    # flourishing data engines
    # ══════════════════════════════════════════════════════════════════

    async def domes_development(self, production: ProductionState,
                                action_data: Dict[str, Any]) -> StageResult:
        """DEVELOPMENT: Research the subject — legal landscape, costs, systems."""
        subject = production.subject

        # 1. Legal provisions from data engine
        provisions = self.store.get_provisions(limit=30)
        if not provisions:
            provisions = SEED_PROVISIONS[:20]
        provisions_by_dimension = {}
        for p in provisions:
            dim = p.get("dome_dimension", "general")
            provisions_by_dimension.setdefault(dim, []).append({
                "citation": p.get("citation", ""),
                "title": p.get("title_text", ""),
                "body": p.get("body", ""),
                "authority": p.get("authority", ""),
                "source_url": p.get("source_url", ""),
            })

        # 2. Cost landscape from data engine
        costs = self.store.get_costs(limit=40)
        if not costs:
            costs = SEED_COST_POINTS[:20]
        costs_by_category = {}
        for c in costs:
            cat = c.get("category", "general")
            costs_by_category.setdefault(cat, []).append({
                "metric": c.get("metric", ""),
                "value": c.get("value", 0),
                "unit": c.get("unit", ""),
                "source": c.get("source", ""),
                "source_year": c.get("source_year", 0),
            })

        # 3. Government systems from data engine
        systems = self.store.get_systems(limit=30)
        if not systems:
            systems = SEED_SYSTEMS[:15]
        system_list = []
        for s in systems:
            fields = s.get("data_fields", "[]")
            if isinstance(fields, str):
                try:
                    fields = json.loads(fields)
                except (json.JSONDecodeError, TypeError):
                    fields = []
            system_list.append({
                "code": s.get("system_code", ""),
                "name": s.get("name", ""),
                "agency": s.get("agency", ""),
                "level": s.get("level", ""),
                "domain": s.get("domain", ""),
                "data_fields": fields,
                "population_served": s.get("population_served", ""),
                "consent_required": s.get("consent_required", ""),
            })

        # 4. System links (connections and gaps)
        links = self.store.get_system_links(limit=50)
        if not links:
            links = SEED_LINKS[:20]
        link_list = []
        for l in links:
            link_list.append({
                "source": l.get("source_system", ""),
                "target": l.get("target_system", ""),
                "type": l.get("link_type", ""),
                "mechanism": l.get("mechanism", ""),
                "latency": l.get("latency", ""),
                "consent_barrier": l.get("consent_barrier", ""),
                "legal_authority": l.get("legal_authority", ""),
            })

        # 5. Profile archetype for subject
        profile = self._build_profile(subject, provisions_by_dimension, costs_by_category)

        # 6. Data engine stats (show the player how much data backs this)
        stats = self.store.stats()

        research = {
            "profile": profile,
            "legal_provisions": provisions_by_dimension,
            "provision_count": len(provisions),
            "cost_landscape": costs_by_category,
            "cost_point_count": len(costs),
            "government_systems": system_list,
            "system_count": len(system_list),
            "system_links": link_list,
            "link_count": len(link_list),
            "active_links": len([l for l in link_list if l["type"] == "active"]),
            "blocked_links": len([l for l in link_list if l["type"] == "blocked"]),
            "possible_links": len([l for l in link_list if l["type"] == "possible"]),
            "data_engine_stats": stats,
        }

        return StageResult(
            success=True,
            message=(
                f"Research complete for {subject}. "
                f"Found {len(provisions)} legal provisions across "
                f"{len(provisions_by_dimension)} dimensions, "
                f"{len(costs)} cost data points, "
                f"{len(system_list)} government systems with "
                f"{len([l for l in link_list if l['type'] == 'active'])} active connections "
                f"and {len([l for l in link_list if l['type'] == 'blocked'])} blocked connections. "
                f"Ready for Pre-Production."
            ),
            new_stage=ProductionStage.PRE_PRODUCTION,
            progress=20.0,
            data=research,
        )

    async def domes_pre_production(self, production: ProductionState,
                                   action_data: Dict[str, Any]) -> StageResult:
        """PRE-PRODUCTION: Design the dome architecture."""
        subject = production.subject
        dev_data = production.stage_data.get("development", {})

        # 1. Recommend coordination models based on subject needs
        profile = dev_data.get("profile", {})
        needs = profile.get("needs", ["healthcare", "housing", "income"])
        recommended = recommend_models(needs, top_n=4)
        models = []
        for m in recommended:
            models.append({
                "id": m["id"],
                "name": m["name"],
                "description": m["description"],
                "real_examples": m["real_examples"],
                "legal_authority": m["legal_authority"],
                "systems_connected": m["systems_connected"],
                "consent_model": m["consent_model"],
                "estimated_savings_pct": m["estimated_savings_pct"],
                "implementation_cost": m["implementation_cost"],
                "fit_score": m["fit_score"],
            })

        # 2. Flourishing framework + scores
        flourishing_scores = {}
        for dim in ["healthcare", "housing", "income", "food", "employment"]:
            flourishing_scores[dim] = get_flourishing_score(dim)

        overall_score = sum(s["score"] for s in flourishing_scores.values()) / max(1, len(flourishing_scores))
        overall_gap = sum(s["gap"] for s in flourishing_scores.values()) / max(1, len(flourishing_scores))

        # 3. Dome architecture — layers mapped to real data
        provisions_by_dim = dev_data.get("legal_provisions", {})
        prov_strength = min(1.0, sum(len(v) for v in provisions_by_dim.values()) / 20)
        data_strength = dev_data.get("active_links", 0) / max(1, dev_data.get("link_count", 1))
        coord_strength = models[0]["fit_score"] if models else 0

        architecture = {
            "type": "full_dome",
            "layers": [
                {
                    "name": "Legal Foundation",
                    "provisions": sum(len(v) for v in provisions_by_dim.values()),
                    "dimensions_covered": list(provisions_by_dim.keys()),
                    "strength": prov_strength,
                },
                {
                    "name": "Data Infrastructure",
                    "systems": dev_data.get("system_count", 0),
                    "active_connections": dev_data.get("active_links", 0),
                    "blocked_connections": dev_data.get("blocked_links", 0),
                    "strength": data_strength,
                },
                {
                    "name": "Fiscal Layer",
                    "cost_points": dev_data.get("cost_point_count", 0),
                    "fragmentation_cost": self._get_fragmentation_cost(),
                    "coordination_savings": self._get_coordination_savings(),
                    "strength": 0.7,
                },
                {
                    "name": "Coordination Layer",
                    "models_available": len(COORDINATION_MODELS),
                    "models_recommended": len(models),
                    "best_fit": models[0]["name"] if models else "None",
                    "estimated_savings": models[0]["estimated_savings_pct"] if models else 0,
                    "strength": coord_strength,
                },
                {
                    "name": "Flourishing Layer",
                    "framework": "Nussbaum Central Capabilities + OECD Better Life",
                    "current_score": round(overall_score, 3),
                    "gap_to_threshold": round(overall_gap, 3),
                    "dimensions_measured": len(flourishing_scores),
                    "strength": overall_score,
                },
                {
                    "name": "Narrative Layer",
                    "purpose": "Communicate the dome's protection to the subject and stakeholders",
                    "strength": 0.5,
                },
            ],
            "overall_coverage": round(
                (prov_strength + data_strength + 0.7 + coord_strength + overall_score + 0.5) / 6, 3
            ),
        }

        # 4. Enrichment insights
        enrichments = self.store.get_enrichments(limit=20)
        insights = []
        for e in enrichments:
            insights.append({
                "type": e.get("enrichment_type", ""),
                "description": e.get("description", ""),
                "confidence": e.get("confidence", 0),
            })

        design = {
            "architecture": architecture,
            "coordination_models": models,
            "flourishing": {
                "scores": flourishing_scores,
                "overall_score": round(overall_score, 3),
                "overall_gap": round(overall_gap, 3),
                "frameworks_available": len(FRAMEWORKS),
            },
            "enrichment_insights": insights[:10],
            "subject": subject,
        }

        return StageResult(
            success=True,
            message=(
                f"Dome architecture designed. "
                f"Coverage: {architecture['overall_coverage']:.0%}. "
                f"Best coordination model: {models[0]['name'] if models else 'None'} "
                f"(estimated {models[0]['estimated_savings_pct']}% savings). "
                f"Flourishing score: {overall_score:.1%} (gap: {overall_gap:.1%}). "
                f"Ready for Production."
            ),
            new_stage=ProductionStage.PRODUCTION,
            progress=40.0,
            data=design,
        )

    async def domes_production(self, production: ProductionState,
                               action_data: Dict[str, Any]) -> StageResult:
        """PRODUCTION: Build the dome — execute contracts, connect systems."""
        subject = production.subject
        pre_data = production.stage_data.get("pre_production", {})
        dev_data = production.stage_data.get("development", {})

        # 1. Generate contracts from coordination models
        models = pre_data.get("coordination_models", [])
        contracts = []
        for model in models:
            systems = model.get("systems_connected", [])
            contracts.append({
                "type": model.get("name", "Unknown"),
                "status": "executed",
                "parties": systems,
                "legal_authority": model.get("legal_authority", ""),
                "consent_model": model.get("consent_model", ""),
                "estimated_savings_pct": model.get("estimated_savings_pct", 0),
            })

        # 2. Build the profile — aggregate all dome data for this person
        profile = dev_data.get("profile", {})
        provisions_count = dev_data.get("provision_count", 0)
        systems_count = dev_data.get("system_count", 0)

        dome_profile = {
            "subject": subject,
            "dome_complete": True,
            "provisions_applied": provisions_count,
            "systems_connected": systems_count,
            "contracts_executed": len(contracts),
            "coverage_dimensions": list(dev_data.get("legal_provisions", {}).keys()),
            "coordination_model": models[0].get("name", "") if models else "",
            "needs_addressed": profile.get("needs", []),
        }

        build = {
            "contracts": {"agreements": contracts},
            "profile": dome_profile,
        }

        return StageResult(
            success=True,
            message=(
                f"Dome built for {subject}. "
                f"{len(contracts)} coordination agreements executed, "
                f"connecting {systems_count} systems under {provisions_count} provisions. "
                f"Ready for Post-Production verification."
            ),
            new_stage=ProductionStage.POST_PRODUCTION,
            progress=60.0,
            data=build,
        )

    async def domes_post_production(self, production: ProductionState,
                                    action_data: Dict[str, Any]) -> StageResult:
        """POST-PRODUCTION: Verify dome completeness and generate innovations."""
        subject = production.subject
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        prod_data = production.stage_data.get("production", {})

        # 1. Verification — check coverage across all dimensions
        provisions_by_dim = dev_data.get("legal_provisions", {})
        all_dimensions = {"healthcare", "housing", "income", "food", "employment",
                          "education", "justice", "data_privacy", "interoperability"}
        covered = set(provisions_by_dim.keys())
        gaps = all_dimensions - covered

        blocked_links = dev_data.get("blocked_links", 0)

        verification = {
            "complete": len(gaps) == 0,
            "coverage": round(len(covered) / len(all_dimensions), 3),
            "dimensions_covered": sorted(covered),
            "gaps": sorted(gaps),
            "blocked_connections": blocked_links,
            "recommendations": [],
        }

        if gaps:
            for g in gaps:
                verification["recommendations"].append(f"Extend dome to cover {g} dimension")
        if blocked_links > 0:
            verification["recommendations"].append(
                f"Address {blocked_links} blocked system connections to strengthen dome"
            )

        # 2. Innovations generated from this dome
        coordination_model = prod_data.get("profile", {}).get("coordination_model", "")
        innovations = {
            "innovations": [
                f"Person-Centered Dome Architecture for {subject}",
                f"Cross-System Consent Protocol ({coordination_model})",
                "Fragmentation Cost Calculator (real data-backed)",
                "Portable Benefits Bridge Protocol",
            ],
            "patents": [
                "Personal Data Dome Architecture — method for constructing comprehensive "
                "protective coverage using every relevant government program",
                f"Government API Orchestration Method — real-time coordination of "
                f"{dev_data.get('system_count', 0)} federal/state/local data systems",
            ],
            "protocols": [
                "Dome Verification Standard v1 — completeness scoring across 9 dimensions",
                "Flourishing Index Protocol — measuring outcomes not just outputs",
            ],
        }

        post = {
            "verification": verification,
            "innovations": innovations,
        }

        return StageResult(
            success=True,
            message=(
                f"Verification: {verification['coverage']:.0%} dome coverage across "
                f"{len(covered)}/{len(all_dimensions)} dimensions. "
                f"{'COMPLETE' if verification['complete'] else f'{len(gaps)} gaps remaining'}. "
                f"Generated {len(innovations['innovations'])} innovations. "
                f"Ready for Distribution."
            ),
            new_stage=ProductionStage.DISTRIBUTION,
            progress=80.0,
            data=post,
        )

    async def domes_distribution(self, production: ProductionState,
                                 action_data: Dict[str, Any]) -> StageResult:
        """DISTRIBUTION: Final narrative, COSM calculation, IP extraction."""
        subject = production.subject
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        prod_data = production.stage_data.get("production", {})
        post_data = production.stage_data.get("post_production", {})

        # 1. Build narrative grounded in real data
        fragmentation_cost = self._get_fragmentation_cost()
        coordination_savings = self._get_coordination_savings()
        provision_count = dev_data.get("provision_count", 0)
        system_count = dev_data.get("system_count", 0)
        verification = post_data.get("verification", {})

        narrative = {
            "sections": [
                {
                    "title": "The Problem: Fragmentation",
                    "content": (
                        f"The US spends an estimated ${fragmentation_cost:,.0f} per person per year "
                        f"on uncoordinated care for multi-system individuals. {system_count} government "
                        f"data systems hold pieces of a person's life — but "
                        f"{dev_data.get('blocked_links', 0)} connections between them are blocked "
                        f"by regulatory barriers."
                    ),
                },
                {
                    "title": "The Subject",
                    "content": (
                        f"{subject}: a real person navigating {len(dev_data.get('legal_provisions', {}))} "
                        f"regulatory dimensions — from {', '.join(list(dev_data.get('legal_provisions', {}).keys())[:4])} "
                        f"and beyond. Each dimension has its own application, its own caseworker, "
                        f"its own data system, its own rules."
                    ),
                },
                {
                    "title": "The Dome",
                    "content": (
                        f"A complete protective dome built from {provision_count} real legal provisions, "
                        f"coordinated across {system_count} systems, using "
                        f"{prod_data.get('profile', {}).get('coordination_model', 'integrated')} "
                        f"architecture. Coverage: {verification.get('coverage', 0):.0%} across "
                        f"{len(verification.get('dimensions_covered', []))} dimensions."
                    ),
                },
                {
                    "title": "The Savings",
                    "content": (
                        f"Coordination produces estimated ${coordination_savings:,.0f}/year in savings "
                        f"per person served. For the dome subject: moving from fragmented services "
                        f"(${fragmentation_cost:,.0f}/year) to coordinated care "
                        f"(${fragmentation_cost - coordination_savings:,.0f}/year). "
                        f"Every dollar is sourced from CMS, HUD, Vera, and HCUP data."
                    ),
                },
                {
                    "title": "The Innovation",
                    "content": (
                        f"This dome produced {len(post_data.get('innovations', {}).get('patents', []))} "
                        f"patentable methods and {len(post_data.get('innovations', {}).get('protocols', []))} "
                        f"protocols. The Portable Benefits Bridge Protocol enables dome "
                        f"replication at scale — any person, any city."
                    ),
                },
            ]
        }

        # 2. Calculate COSM
        cosm = self._calculate_cosm(production)

        # 3. Extract IP
        ip = self._extract_ip(production)

        # 4. Assess industries changed
        industries = self._assess_industries_changed(production)

        # 5. Innovations
        innovations = self._extract_innovations(production)

        distribution = {
            "narrative": narrative,
            "cosm": cosm.model_dump(),
            "ip": ip,
            "innovations": innovations,
            "industries_changed": industries,
            "data_engine_stats": self.store.stats(),
        }

        return StageResult(
            success=True,
            message=f"DOME COMPLETE for {subject}. Total Cosm: {cosm.total:.2f}",
            new_stage=None,
            progress=100.0,
            data=distribution,
        )

    # ══════════════════════════════════════════════════════════════════
    # SPHERES PIPELINE — powered by parcels, zoning, permits data engines
    # ══════════════════════════════════════════════════════════════════

    async def spheres_development(self, production: ProductionState,
                                  action_data: Dict[str, Any]) -> StageResult:
        """DEVELOPMENT: Research the parcel — real property data."""
        parcel_query = production.subject

        # Try to find parcel in data engine
        parcels = self.store.get_parcels(limit=20)
        target_parcel = None
        for p in parcels:
            if (parcel_query in (p.get("parcel_id", "") or "") or
                parcel_query.lower() in (p.get("address", "") or "").lower() or
                parcel_query.lower() in (p.get("neighborhood", "") or "").lower()):
                target_parcel = p
                break

        if not target_parcel and parcels:
            target_parcel = parcels[0]
        elif not target_parcel:
            target_parcel = SEED_PARCELS[0]

        # Parse extra data
        extra = target_parcel.get("extra", "{}")
        if isinstance(extra, str):
            try:
                extra = json.loads(extra)
            except (json.JSONDecodeError, TypeError):
                extra = {}

        # Get zoning reference
        zoning_code = target_parcel.get("zoning", "")
        zoning_info = ZONING_REFERENCE.get(zoning_code, {
            "name": zoning_code, "description": "Custom zoning district"
        })

        # Get enrichment insights for this parcel
        enrichments = self.store.get_enrichments(enrichment_type="opportunity", limit=20)
        parcel_insights = []
        for e in enrichments:
            edata = e.get("data", "{}")
            if isinstance(edata, str):
                try:
                    edata = json.loads(edata)
                except (json.JSONDecodeError, TypeError):
                    edata = {}
            if edata.get("parcel_id") == target_parcel.get("parcel_id"):
                parcel_insights.append({
                    "description": e.get("description", ""),
                    "activation_score": edata.get("activation_score", 0),
                    "activation_types": edata.get("activation_types", []),
                })

        # Get nearby parcels (same neighborhood)
        neighborhood = target_parcel.get("neighborhood", "")
        nearby = self.store.get_parcels(neighborhood=neighborhood, limit=10)
        nearby_list = []
        for n in nearby:
            if n.get("parcel_id") != target_parcel.get("parcel_id"):
                nearby_list.append({
                    "parcel_id": n.get("parcel_id", ""),
                    "address": n.get("address", ""),
                    "zoning": n.get("zoning", ""),
                    "vacant": bool(n.get("vacant", 0)),
                    "total_val": n.get("total_val", 0),
                })

        parcel_data = {
            "parcel_id": target_parcel.get("parcel_id", ""),
            "address": target_parcel.get("address", ""),
            "owner": target_parcel.get("owner", ""),
            "zoning": zoning_code,
            "zoning_info": zoning_info,
            "land_area_sqft": target_parcel.get("land_area_sqft", 0),
            "improvement_val": target_parcel.get("improvement_val", 0),
            "land_val": target_parcel.get("land_val", 0),
            "total_val": target_parcel.get("total_val", 0),
            "vacant": bool(target_parcel.get("vacant", 0)),
            "lat": target_parcel.get("lat", 0),
            "lon": target_parcel.get("lon", 0),
            "neighborhood": neighborhood,
            "council_district": target_parcel.get("council_district", 0),
            "extra": extra,
        }

        # Standard permits needed
        standard_permits = [
            {"type": "Temporary Use Permit", "status": "required",
             "description": "Required for any non-permanent activation of vacant land"},
            {"type": "Public Assembly Permit", "status": "required",
             "description": "Required for gatherings over 50 people"},
            {"type": "Food Service License", "status": "required",
             "description": "Required for any food preparation or distribution"},
            {"type": "Zoning Variance", "status": "conditional",
             "description": f"May be required depending on {zoning_code} permitted uses"},
            {"type": "Building Permit", "status": "conditional",
             "description": "Required for any permanent structure over 200 sqft"},
        ]

        research = {
            "parcel": parcel_data,
            "permits": {"standard_permits": standard_permits},
            "insights": parcel_insights,
            "nearby_parcels": nearby_list,
            "data_engine_stats": self.store.stats(),
        }

        return StageResult(
            success=True,
            message=(
                f"Research complete for {parcel_data['address']}. "
                f"{parcel_data['land_area_sqft']:,.0f} sqft, zoned {zoning_code} "
                f"({zoning_info.get('name', '')}). "
                f"{'VACANT' if parcel_data['vacant'] else 'IMPROVED'}. "
                f"Assessed at ${parcel_data['total_val']:,.0f}. "
                f"{len(nearby_list)} nearby parcels in {neighborhood}. "
                f"Ready for Pre-Production."
            ),
            new_stage=ProductionStage.PRE_PRODUCTION,
            progress=20.0,
            data=research,
        )

    async def spheres_pre_production(self, production: ProductionState,
                                     action_data: Dict[str, Any]) -> StageResult:
        """PRE-PRODUCTION: Design the sphere activation."""
        dev_data = production.stage_data.get("development", {})
        parcel = dev_data.get("parcel", {})

        area_sqft = parcel.get("land_area_sqft", 2500)
        zoning = parcel.get("zoning", "CMX-2")
        zoning_info = parcel.get("zoning_info", {})

        # Determine activation type based on parcel characteristics
        activation_types = []
        if area_sqft > 20000:
            activation_types.extend(["community_hub", "market", "performance_venue"])
        elif area_sqft > 5000:
            activation_types.extend(["community_garden", "pocket_park", "popup_market"])
        else:
            activation_types.extend(["pocket_park", "art_installation", "seating_area"])

        if "CMX" in zoning:
            activation_types.append("retail_popup")
        if "IRMX" in zoning:
            activation_types.append("maker_space")

        # Cost estimation
        cost_per_sqft_light = 12
        cost_per_sqft_moderate = 45
        cost_per_sqft_full = 95

        design = {
            "id": f"design-{parcel.get('parcel_id', '001')}",
            "name": f"Sphere Activation: {parcel.get('address', 'Unknown')}",
            "type": "community activation",
            "activation_types": activation_types,
            "access_hours": area_sqft * 0.3,
            "features": [],
        }

        feature_map = {
            "community_hub": ["gathering pavilion", "community board", "wifi", "seating"],
            "community_garden": ["raised beds", "tool shed", "water access", "composting"],
            "pocket_park": ["benches", "shade trees", "pathways", "lighting"],
            "popup_market": ["vendor stalls", "canopy structures", "power hookups"],
            "maker_space": ["workshop area", "tool library", "material storage"],
            "performance_venue": ["stage platform", "seating area", "sound system"],
            "art_installation": ["installation base", "lighting", "interpretive signage"],
        }
        for at in activation_types[:3]:
            design["features"].extend(feature_map.get(at, []))

        total_light = area_sqft * cost_per_sqft_light
        total_moderate = area_sqft * cost_per_sqft_moderate
        total_full = area_sqft * cost_per_sqft_full

        cost = {
            "light_activation": {"total": total_light, "per_sqft": cost_per_sqft_light,
                                 "includes": "Landscaping, seating, signage, basic lighting"},
            "moderate_activation": {"total": total_moderate, "per_sqft": cost_per_sqft_moderate,
                                    "includes": "Temporary structures, utilities, programming, staffing"},
            "full_buildout": {"total": total_full, "per_sqft": cost_per_sqft_full,
                              "includes": "Permanent structures, full utilities, ongoing operations"},
            "recommended": "moderate_activation" if area_sqft > 3000 else "light_activation",
            "recommended_total": total_moderate if area_sqft > 3000 else total_light,
        }

        timeline = {
            "phases": [
                {"name": "Design & Community Input", "weeks": 4},
                {"name": "Permits & Approvals", "weeks": 6},
                {"name": "Site Preparation", "weeks": 3},
                {"name": "Build / Install", "weeks": 4 if area_sqft < 5000 else 8},
                {"name": "Activate & Program", "weeks": 52},
                {"name": "Sustain & Iterate", "weeks": 104},
            ],
        }
        timeline["total_weeks"] = sum(p["weeks"] for p in timeline["phases"])
        timeline["duration_years"] = round(timeline["total_weeks"] / 52, 1)

        prep = {"design": design, "cost": cost, "timeline": timeline, "zoning_info": zoning_info}

        return StageResult(
            success=True,
            message=(
                f"Design complete for {parcel.get('address', '')}. "
                f"Recommended: {cost['recommended']} (${cost['recommended_total']:,.0f}). "
                f"Activation types: {', '.join(activation_types[:3])}. "
                f"Timeline: {timeline['duration_years']} years. "
                f"Ready for Production."
            ),
            new_stage=ProductionStage.PRODUCTION,
            progress=40.0,
            data=prep,
        )

    async def spheres_production(self, production: ProductionState,
                                 action_data: Dict[str, Any]) -> StageResult:
        """PRODUCTION: Build the sphere — permits, construction, activation."""
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        parcel = dev_data.get("parcel", {})

        standard_permits = dev_data.get("permits", {}).get("standard_permits", [])
        executed_permits = []
        for p in standard_permits:
            executed_permits.append({
                **p, "status": "approved" if p.get("status") != "conditional" else "waived",
            })

        policy_changes = [
            f"Temporary Use Ordinance expansion for {parcel.get('zoning', '')} zones",
            "Community Benefit Agreement framework for public land activation",
            "Streamlined permit pathway for community-initiated development",
        ]

        design = pre_data.get("design", {})
        cost = pre_data.get("cost", {})
        area = parcel.get("land_area_sqft", 2500)

        world = {
            "activated": True,
            "sqft_activated": area,
            "features_installed": design.get("features", []),
            "activation_types": design.get("activation_types", []),
            "investment": cost.get("recommended_total", 0),
            "events_capacity": max(50, area // 20),
        }

        build = {"permits": {"permits": executed_permits, "policy_changes": policy_changes}, "world": world}

        return StageResult(
            success=True,
            message=(
                f"Sphere built at {parcel.get('address', '')}. "
                f"{area:,.0f} sqft activated. "
                f"{len(executed_permits)} permits executed. "
                f"{len(policy_changes)} policy changes enabled. "
                f"Capacity: {world['events_capacity']} people. "
                f"Ready for Post-Production."
            ),
            new_stage=ProductionStage.POST_PRODUCTION,
            progress=60.0,
            data=build,
        )

    async def spheres_post_production(self, production: ProductionState,
                                      action_data: Dict[str, Any]) -> StageResult:
        """POST-PRODUCTION: Measure impact, document innovations."""
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        prod_data = production.stage_data.get("production", {})
        parcel = dev_data.get("parcel", {})
        world = prod_data.get("world", {})

        address = parcel.get("address", "Unknown")
        area = world.get("sqft_activated", 2500)
        capacity = world.get("events_capacity", 100)

        episodes = {
            "episodes": [
                {"title": "Ground Breaking", "date": "Week 1",
                 "impact": f"Community gathers at {address}. {capacity // 4} residents attend.",
                 "metrics": {"attendees": capacity // 4, "media_mentions": 2}},
                {"title": "First Programming", "date": "Week 8",
                 "impact": f"Weekly farmers market launches. {capacity // 3} visitors, 12 local vendors.",
                 "metrics": {"visitors": capacity // 3, "vendors": 12, "revenue": 3500}},
                {"title": "Community Festival", "date": "Week 16",
                 "impact": f"Full activation event. {capacity} attendees, live music, food trucks.",
                 "metrics": {"attendees": capacity, "vendors": 25, "revenue": 12000, "media_mentions": 8}},
                {"title": "Six Month Review", "date": "Week 26",
                 "impact": f"Space serves {capacity * 10} cumulative visitors. Property values up 3.2%.",
                 "metrics": {"cumulative_visitors": capacity * 10, "property_value_increase": 3.2}},
            ]
        }

        innovations = {
            "innovations": [
                "Modular Public Space Activation Kit",
                "Community Ownership Protocol",
                "Impact Measurement Dashboard (real-time)",
                f"{parcel.get('neighborhood', 'Neighborhood')} Activation Playbook",
            ],
            "patents": [],
            "protocols": [
                "Sphere Activation Standard v1",
                f"Zoning Overlay Protocol for {parcel.get('zoning', 'CMX-2')} activation",
            ],
        }

        investment = pre_data.get("cost", {}).get("recommended_total", 50000)
        metrics = {
            "connected_projects": len(dev_data.get("nearby_parcels", [])),
            "total_visitors": capacity * 10,
            "economic_impact": investment * 3.2,
            "community_rating": 4.7,
            "jobs_created": max(3, area // 2000),
            "property_value_impact_pct": 3.2,
        }

        post = {"episodes": episodes, "innovations": innovations, "metrics": metrics}

        return StageResult(
            success=True,
            message=(
                f"Impact documented. {capacity * 10:,} cumulative visitors. "
                f"${metrics['economic_impact']:,.0f} economic impact (3.2x multiplier). "
                f"{metrics['jobs_created']} jobs created. "
                f"Ready for Distribution."
            ),
            new_stage=ProductionStage.DISTRIBUTION,
            progress=80.0,
            data=post,
        )

    async def spheres_distribution(self, production: ProductionState,
                                    action_data: Dict[str, Any]) -> StageResult:
        """DISTRIBUTION: Final CHRON calculation and narrative."""
        post_data = production.stage_data.get("post_production", {})
        chron = self._calculate_chron(production)
        innovations = self._extract_innovations(production)

        distribution = {
            "metrics": post_data.get("metrics", {}),
            "chron": chron.model_dump(),
            "innovations": innovations,
            "data_engine_stats": self.store.stats(),
        }

        return StageResult(
            success=True,
            message=f"SPHERE COMPLETE. Total Chron: {chron.total:.2f}",
            new_stage=None,
            progress=100.0,
            data=distribution,
        )

    # ══════════════════════════════════════════════════════════════════
    # STAGE ROUTER
    # ══════════════════════════════════════════════════════════════════

    async def advance_stage(self, production: ProductionState,
                            action_data: Dict[str, Any]) -> StageResult:
        handlers = {
            (GameType.DOMES, ProductionStage.DEVELOPMENT): self.domes_development,
            (GameType.DOMES, ProductionStage.PRE_PRODUCTION): self.domes_pre_production,
            (GameType.DOMES, ProductionStage.PRODUCTION): self.domes_production,
            (GameType.DOMES, ProductionStage.POST_PRODUCTION): self.domes_post_production,
            (GameType.DOMES, ProductionStage.DISTRIBUTION): self.domes_distribution,
            (GameType.SPHERES, ProductionStage.DEVELOPMENT): self.spheres_development,
            (GameType.SPHERES, ProductionStage.PRE_PRODUCTION): self.spheres_pre_production,
            (GameType.SPHERES, ProductionStage.PRODUCTION): self.spheres_production,
            (GameType.SPHERES, ProductionStage.POST_PRODUCTION): self.spheres_post_production,
            (GameType.SPHERES, ProductionStage.DISTRIBUTION): self.spheres_distribution,
        }

        handler = handlers.get((production.game_type, production.stage))
        if not handler:
            return StageResult(
                success=False,
                message=f"No handler for {production.game_type}/{production.stage}",
                progress=production.progress,
            )

        return await handler(production, action_data)

    # ══════════════════════════════════════════════════════════════════
    # INTERNAL HELPERS
    # ══════════════════════════════════════════════════════════════════

    def _build_profile(self, subject: str, provisions: dict, costs: dict) -> dict:
        dimensions = list(provisions.keys())
        needs = []
        dim_map = {
            "healthcare": "healthcare", "housing": "housing", "income": "income_support",
            "food": "food_security", "employment": "employment", "education": "education",
            "justice": "reentry_support",
        }
        for dim in dimensions:
            if dim in dim_map:
                needs.append(dim_map[dim])

        frag_cost = self._get_fragmentation_cost()

        return {
            "name": subject,
            "needs": needs,
            "dimensions_affected": dimensions,
            "estimated_annual_fragmentation_cost": frag_cost,
            "systems_involved": len(dimensions) * 2,
            "risk_factors": [
                "Data fragmented across multiple systems",
                f"Navigating {len(dimensions)} separate bureaucracies",
                f"Estimated ${frag_cost:,.0f}/year in fragmentation costs",
            ],
            "strengths": [
                "Identified for dome construction",
                "All regulatory dimensions mapped",
                "Coordination models available",
            ],
        }

    def _get_fragmentation_cost(self) -> float:
        costs = self.store.get_costs(category="fragmentation", limit=10)
        for c in costs:
            if "uncoordinated" in (c.get("metric", "") or "").lower():
                return c.get("value", 78168)
        return 78168

    def _get_coordination_savings(self) -> float:
        costs = self.store.get_costs(category="fragmentation", limit=10)
        for c in costs:
            if "savings" in (c.get("metric", "") or "").lower():
                return c.get("value", 36336)
        return 36336

    def _calculate_cosm(self, production: ProductionState) -> CosmDimensions:
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        dist_data = production.stage_data.get("distribution", {})

        provision_count = dev_data.get("provision_count", 0)
        legal_score = min(100.0, provision_count * 4.0)

        active_links = dev_data.get("active_links", 0)
        total_links = dev_data.get("link_count", 1)
        data_score = min(100.0, (active_links / max(1, total_links)) * 120)

        cost_count = dev_data.get("cost_point_count", 0)
        fiscal_score = min(100.0, cost_count * 2.5)

        models = pre_data.get("coordination_models", [])
        best_savings = max([m.get("estimated_savings_pct", 0) for m in models], default=0)
        coord_score = min(100.0, len(models) * 15 + best_savings)

        flour_data = pre_data.get("flourishing", {})
        flour_score = flour_data.get("overall_score", 0.5) * 100

        narrative = dist_data.get("narrative", {})
        narrative_score = min(100.0, len(narrative.get("sections", [])) * 20)

        return CosmDimensions(
            legal=round(legal_score, 1),
            data=round(data_score, 1),
            fiscal=round(fiscal_score, 1),
            coordination=round(coord_score, 1),
            flourishing=round(flour_score, 1),
            narrative=round(narrative_score, 1),
        )

    def _calculate_chron(self, production: ProductionState) -> ChronDimensions:
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        prod_data = production.stage_data.get("production", {})
        post_data = production.stage_data.get("post_production", {})

        parcel = dev_data.get("parcel", {})
        unlock = parcel.get("land_area_sqft", 2500)

        design = pre_data.get("design", {})
        access = design.get("access_hours", 360.0)

        timeline = pre_data.get("timeline", {})
        permanence = min(1.0, timeline.get("duration_years", 1.0) / 10.0)

        metrics = post_data.get("metrics", {})
        catalyst = min(1.0, metrics.get("connected_projects", 0) / 10.0)

        permits = prod_data.get("permits", {})
        policy = min(1.0, len(permits.get("policy_changes", [])) / 5.0)

        return ChronDimensions(
            unlock=unlock, access=access, permanence=permanence,
            catalyst=catalyst, policy=policy,
        )

    def _extract_ip(self, production: ProductionState) -> List[str]:
        ip_list = []
        post_data = production.stage_data.get("post_production", {})
        innovations = post_data.get("innovations", {})
        ip_list.extend(innovations.get("patents", []))
        ip_list.extend(innovations.get("protocols", []))
        return ip_list if ip_list else ["Generated IP"]

    def _extract_innovations(self, production: ProductionState) -> List[str]:
        post_data = production.stage_data.get("post_production", {})
        innovations = post_data.get("innovations", {})
        return innovations.get("innovations", [])

    def _assess_industries_changed(self, production: ProductionState) -> List[str]:
        industries = set()
        dev_data = production.stage_data.get("development", {})
        provisions = dev_data.get("legal_provisions", {})

        dim_map = {
            "healthcare": "Healthcare", "housing": "Housing & Real Estate",
            "income": "Financial Services", "food": "Food & Agriculture",
            "employment": "Workforce Development", "education": "Education",
            "justice": "Criminal Justice", "data_privacy": "Data Privacy & Technology",
            "interoperability": "Government Technology",
        }

        for dim in provisions.keys():
            industry = dim_map.get(dim)
            if industry:
                industries.add(industry)

        prod_data = production.stage_data.get("production", {})
        contracts = prod_data.get("contracts", {})
        if contracts.get("agreements"):
            industries.add("Government Contracting")

        return sorted(industries) if industries else ["Cross-Sector Impact"]
