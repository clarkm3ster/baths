"""
BATHS Game Engine — Pipeline Director
Orchestrates producer through Development -> Pre -> Prod -> Post -> Distribution.

Production terminology throughout — StudioBinder meets Bloomberg Terminal.
Powered by elite data engines. Every response grounded in real federal
regulations, real cost data, real government systems, real Philadelphia
parcel records. Data gets richer with every scrape cycle.

IP Generation Engine produces intellectual property across 8 domains.
Bond Pricing Engine prices Dome Bonds and Chron Bonds from scores.
"""

import os
import json
import hashlib
import httpx
import logging
from typing import Dict, Any, List, Optional

from models import (
    GameType, ProductionStage, ProductionState, StageResult,
    CosmDimensions, ChronDimensions, IPOutput, IPDomain,
    DomeBond, ChronBond
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
    # DOMES PIPELINE — Professional Production Environment
    # Development → Pre-Production → Production → Post-Production → Distribution
    # ══════════════════════════════════════════════════════════════════

    async def domes_development(self, production: ProductionState,
                                action_data: Dict[str, Any]) -> StageResult:
        """
        DEVELOPMENT: Rights acquisition, market research, development deal.
        Deliverables: rights package, market analysis, deal memo.
        """
        subject = production.subject

        # 1. Rights Acquisition — legal provisions from data engine
        provisions = self.store.get_provisions(limit=30)
        if not provisions:
            provisions = SEED_PROVISIONS[:20]
        rights_package = {}
        for p in provisions:
            dim = p.get("dome_dimension", "general")
            rights_package.setdefault(dim, []).append({
                "citation": p.get("citation", ""),
                "title": p.get("title_text", ""),
                "body": p.get("body", ""),
                "authority": p.get("authority", ""),
                "source_url": p.get("source_url", ""),
            })

        # 2. Market Research — cost landscape from data engine
        costs = self.store.get_costs(limit=40)
        if not costs:
            costs = SEED_COST_POINTS[:20]
        market_analysis = {}
        for c in costs:
            cat = c.get("category", "general")
            market_analysis.setdefault(cat, []).append({
                "metric": c.get("metric", ""),
                "value": c.get("value", 0),
                "unit": c.get("unit", ""),
                "source": c.get("source", ""),
                "source_year": c.get("source_year", 0),
            })

        # 3. Development Deal — government systems mapping
        systems = self.store.get_systems(limit=30)
        if not systems:
            systems = SEED_SYSTEMS[:15]
        cast_list = []
        for s in systems:
            fields = s.get("data_fields", "[]")
            if isinstance(fields, str):
                try:
                    fields = json.loads(fields)
                except (json.JSONDecodeError, TypeError):
                    fields = []
            cast_list.append({
                "code": s.get("system_code", ""),
                "name": s.get("name", ""),
                "agency": s.get("agency", ""),
                "level": s.get("level", ""),
                "domain": s.get("domain", ""),
                "data_fields": fields,
                "population_served": s.get("population_served", ""),
                "consent_required": s.get("consent_required", ""),
            })

        # 4. System connections (the deal structure)
        links = self.store.get_system_links(limit=50)
        if not links:
            links = SEED_LINKS[:20]
        deal_structure = []
        for l in links:
            deal_structure.append({
                "source": l.get("source_system", ""),
                "target": l.get("target_system", ""),
                "type": l.get("link_type", ""),
                "mechanism": l.get("mechanism", ""),
                "latency": l.get("latency", ""),
                "consent_barrier": l.get("consent_barrier", ""),
                "legal_authority": l.get("legal_authority", ""),
            })

        # 5. Subject profile (the talent)
        profile = self._build_profile(subject, rights_package, market_analysis)

        # 6. Data engine stats
        stats = self.store.stats()

        active_links = len([l for l in deal_structure if l["type"] == "active"])
        blocked_links = len([l for l in deal_structure if l["type"] == "blocked"])

        research = {
            "profile": profile,
            "rights_package": rights_package,
            "rights_count": len(provisions),
            "market_analysis": market_analysis,
            "cost_point_count": len(costs),
            "cast_list": cast_list,
            "system_count": len(cast_list),
            "deal_structure": deal_structure,
            "link_count": len(deal_structure),
            "active_links": active_links,
            "blocked_links": blocked_links,
            "possible_links": len([l for l in deal_structure if l["type"] == "possible"]),
            "data_engine_stats": stats,
        }

        return StageResult(
            success=True,
            message=(
                f"Development complete for {subject}. "
                f"Rights: {len(provisions)} provisions across "
                f"{len(rights_package)} regulatory dimensions. "
                f"Market: {len(costs)} cost data points. "
                f"Deal: {len(cast_list)} government systems — "
                f"{active_links} active, {blocked_links} blocked connections. "
                f"Ready for Pre-Production."
            ),
            new_stage=ProductionStage.PRE_PRODUCTION,
            progress=20.0,
            data=research,
        )

    async def domes_pre_production(self, production: ProductionState,
                                   action_data: Dict[str, Any]) -> StageResult:
        """
        PRE-PRODUCTION: Script (dome blueprint), budget (fiscal model),
        cast & crew (coordination architecture).
        Deliverables: shooting script, budget top sheet, cast list, crew plan.
        """
        subject = production.subject
        dev_data = production.stage_data.get("development", {})

        # 1. Script — dome architecture blueprint
        profile = dev_data.get("profile", {})
        needs = profile.get("needs", ["healthcare", "housing", "income"])
        recommended = recommend_models(needs, top_n=4)
        coordination_crew = []
        for m in recommended:
            coordination_crew.append({
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

        # 2. Budget — flourishing framework + fiscal model
        flourishing_scores = {}
        for dim in ["healthcare", "housing", "income", "food", "employment"]:
            flourishing_scores[dim] = get_flourishing_score(dim)

        overall_score = sum(s["score"] for s in flourishing_scores.values()) / max(1, len(flourishing_scores))
        overall_gap = sum(s["gap"] for s in flourishing_scores.values()) / max(1, len(flourishing_scores))

        # 3. Shooting Script — dome architecture layers
        rights_package = dev_data.get("rights_package", {})
        rights_strength = min(1.0, sum(len(v) for v in rights_package.values()) / 20)
        research_strength = dev_data.get("active_links", 0) / max(1, dev_data.get("link_count", 1))
        package_strength = coordination_crew[0]["fit_score"] if coordination_crew else 0

        shooting_script = {
            "type": "full_dome",
            "layers": [
                {
                    "name": "Rights Foundation",
                    "provisions": sum(len(v) for v in rights_package.values()),
                    "dimensions_covered": list(rights_package.keys()),
                    "strength": rights_strength,
                },
                {
                    "name": "Research Infrastructure",
                    "systems": dev_data.get("system_count", 0),
                    "active_connections": dev_data.get("active_links", 0),
                    "blocked_connections": dev_data.get("blocked_links", 0),
                    "strength": research_strength,
                },
                {
                    "name": "Budget Layer",
                    "cost_points": dev_data.get("cost_point_count", 0),
                    "fragmentation_cost": self._get_fragmentation_cost(),
                    "coordination_savings": self._get_coordination_savings(),
                    "strength": 0.7,
                },
                {
                    "name": "Package Layer",
                    "models_available": len(COORDINATION_MODELS),
                    "models_recommended": len(coordination_crew),
                    "best_fit": coordination_crew[0]["name"] if coordination_crew else "None",
                    "estimated_savings": coordination_crew[0]["estimated_savings_pct"] if coordination_crew else 0,
                    "strength": package_strength,
                },
                {
                    "name": "Deliverables Layer",
                    "framework": "Nussbaum Central Capabilities + OECD Better Life",
                    "current_score": round(overall_score, 3),
                    "gap_to_threshold": round(overall_gap, 3),
                    "dimensions_measured": len(flourishing_scores),
                    "strength": overall_score,
                },
                {
                    "name": "Pitch Layer",
                    "purpose": "Communicate the dome's protection to stakeholders and markets",
                    "strength": 0.5,
                },
            ],
            "overall_coverage": round(
                (rights_strength + research_strength + 0.7 + package_strength + overall_score + 0.5) / 6, 3
            ),
        }

        # 4. Budget Top Sheet
        frag_cost = self._get_fragmentation_cost()
        coord_savings = self._get_coordination_savings()
        budget_top_sheet = {
            "above_the_line": {
                "rights_acquisition": len(dev_data.get("rights_package", {})) * 2500,
                "research": dev_data.get("cost_point_count", 0) * 150,
                "talent": dev_data.get("system_count", 0) * 5000,
            },
            "below_the_line": {
                "coordination_infrastructure": coordination_crew[0]["implementation_cost"] if coordination_crew else "medium",
                "data_systems": dev_data.get("system_count", 0) * 8000,
                "consent_protocols": dev_data.get("active_links", 0) * 3000,
            },
            "annual_fragmentation_cost": frag_cost,
            "annual_coordination_savings": coord_savings,
            "annual_dome_value": frag_cost - (frag_cost - coord_savings),
        }

        # 5. Enrichment insights
        enrichments = self.store.get_enrichments(limit=20)
        intelligence = []
        for e in enrichments:
            intelligence.append({
                "type": e.get("enrichment_type", ""),
                "description": e.get("description", ""),
                "confidence": e.get("confidence", 0),
            })

        design = {
            "shooting_script": shooting_script,
            "coordination_crew": coordination_crew,
            "budget_top_sheet": budget_top_sheet,
            "flourishing": {
                "scores": flourishing_scores,
                "overall_score": round(overall_score, 3),
                "overall_gap": round(overall_gap, 3),
                "frameworks_available": len(FRAMEWORKS),
            },
            "intelligence": intelligence[:10],
            "subject": subject,
        }

        return StageResult(
            success=True,
            message=(
                f"Pre-Production locked. "
                f"Script: {shooting_script['overall_coverage']:.0%} dome coverage. "
                f"Budget: ${frag_cost:,.0f} fragmentation → ${frag_cost - coord_savings:,.0f} coordinated. "
                f"Crew: {coordination_crew[0]['name'] if coordination_crew else 'None'} "
                f"({coordination_crew[0]['estimated_savings_pct']}% savings). "
                f"Deliverables index: {overall_score:.1%}. "
                f"Ready for Production."
            ),
            new_stage=ProductionStage.PRODUCTION,
            progress=40.0,
            data=design,
        )

    async def domes_production(self, production: ProductionState,
                               action_data: Dict[str, Any]) -> StageResult:
        """
        PRODUCTION: Principal photography — execute contracts, connect systems,
        build the dome. Data capture. VFX (enrichment cross-references).
        Deliverables: executed agreements, data bridge status, enrichment report.
        """
        subject = production.subject
        pre_data = production.stage_data.get("pre_production", {})
        dev_data = production.stage_data.get("development", {})

        # 1. Executed Agreements from coordination crew
        crew = pre_data.get("coordination_crew", [])
        executed_agreements = []
        for model in crew:
            systems = model.get("systems_connected", [])
            executed_agreements.append({
                "type": model.get("name", "Unknown"),
                "status": "executed",
                "parties": systems,
                "legal_authority": model.get("legal_authority", ""),
                "consent_model": model.get("consent_model", ""),
                "estimated_savings_pct": model.get("estimated_savings_pct", 0),
            })

        # 2. Call Sheet — daily production status
        rights_count = dev_data.get("rights_count", 0)
        systems_count = dev_data.get("system_count", 0)

        call_sheet = {
            "subject": subject,
            "dome_status": "under_construction",
            "rights_applied": rights_count,
            "systems_connected": systems_count,
            "agreements_executed": len(executed_agreements),
            "coverage_dimensions": list(dev_data.get("rights_package", {}).keys()),
            "coordination_model": crew[0].get("name", "") if crew else "",
            "needs_addressed": dev_data.get("profile", {}).get("needs", []),
        }

        # 3. VFX Report — enrichment cross-references
        enrichments = self.store.get_enrichments(limit=15)
        vfx_report = []
        for e in enrichments:
            vfx_report.append({
                "type": e.get("enrichment_type", ""),
                "description": e.get("description", ""),
                "confidence": e.get("confidence", 0),
            })

        build = {
            "executed_agreements": executed_agreements,
            "call_sheet": call_sheet,
            "vfx_report": vfx_report,
        }

        return StageResult(
            success=True,
            message=(
                f"Production wrapped for {subject}. "
                f"{len(executed_agreements)} agreements executed across "
                f"{systems_count} systems under {rights_count} provisions. "
                f"{len(vfx_report)} enrichment cross-references captured. "
                f"Ready for Post-Production."
            ),
            new_stage=ProductionStage.POST_PRODUCTION,
            progress=60.0,
            data=build,
        )

    async def domes_post_production(self, production: ProductionState,
                                    action_data: Dict[str, Any]) -> StageResult:
        """
        POST-PRODUCTION: Assembly cut (verification), color grade (flourishing),
        sound mix (narrative), VFX finals (innovation extraction).
        Deliverables: verified dome, flourishing index, narrative package,
        innovation portfolio.
        """
        subject = production.subject
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        prod_data = production.stage_data.get("production", {})

        # 1. Assembly Cut — verification across all dimensions
        rights_package = dev_data.get("rights_package", {})
        all_dimensions = {"healthcare", "housing", "income", "food", "employment",
                          "education", "justice", "data_privacy", "interoperability"}
        covered = set(rights_package.keys())
        gaps = all_dimensions - covered
        blocked_links = dev_data.get("blocked_links", 0)

        assembly_cut = {
            "complete": len(gaps) == 0,
            "coverage": round(len(covered) / len(all_dimensions), 3),
            "dimensions_covered": sorted(covered),
            "gaps": sorted(gaps),
            "blocked_connections": blocked_links,
            "notes": [],
        }
        if gaps:
            for g in gaps:
                assembly_cut["notes"].append(f"Extend dome to cover {g} dimension")
        if blocked_links > 0:
            assembly_cut["notes"].append(
                f"Address {blocked_links} blocked system connections to strengthen dome"
            )

        # 2. Color Grade — flourishing optimization
        flour_data = pre_data.get("flourishing", {})
        color_grade = {
            "overall_score": flour_data.get("overall_score", 0.5),
            "overall_gap": flour_data.get("overall_gap", 0.3),
            "dimensions": flour_data.get("scores", {}),
            "grade": self._grade_from_score(flour_data.get("overall_score", 0.5)),
        }

        # 3. Sound Mix — narrative generation
        coordination_model = prod_data.get("call_sheet", {}).get("coordination_model", "")
        sound_mix = {
            "sections": self._build_narrative_sections(subject, dev_data, pre_data, prod_data, assembly_cut),
        }

        # 4. VFX Finals — innovation extraction
        vfx_finals = self._extract_innovations_from_production(
            subject, dev_data, pre_data, prod_data, coordination_model
        )

        # 5. IP Generation — across 8 domains
        ip_outputs = self._generate_ip(
            production, subject, dev_data, pre_data, prod_data, assembly_cut
        )

        post = {
            "assembly_cut": assembly_cut,
            "color_grade": color_grade,
            "sound_mix": sound_mix,
            "vfx_finals": vfx_finals,
            "ip_outputs": [ip.model_dump() for ip in ip_outputs],
        }

        return StageResult(
            success=True,
            message=(
                f"Post-Production locked. "
                f"Assembly: {assembly_cut['coverage']:.0%} coverage across "
                f"{len(covered)}/{len(all_dimensions)} dimensions. "
                f"Grade: {color_grade['grade']}. "
                f"IP: {len(ip_outputs)} outputs across {len(set(ip.domain for ip in ip_outputs))} domains. "
                f"Ready for Distribution."
            ),
            new_stage=ProductionStage.DISTRIBUTION,
            progress=80.0,
            data=post,
        )

    async def domes_distribution(self, production: ProductionState,
                                 action_data: Dict[str, Any]) -> StageResult:
        """
        DISTRIBUTION: Theatrical release (COSM reveal), home video (IP package),
        streaming (Dome Bond pricing), international (replication kit).
        Deliverables: final COSM, IP catalog, bond term sheet, replication playbook.
        """
        subject = production.subject
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        prod_data = production.stage_data.get("production", {})
        post_data = production.stage_data.get("post_production", {})

        # 1. Theatrical Release — COSM calculation
        cosm = self._calculate_cosm(production)

        # 2. Home Video — IP catalog
        ip_outputs = post_data.get("ip_outputs", [])

        # 3. Streaming — Dome Bond pricing
        dome_bond = self._price_dome_bond(production, cosm)

        # 4. International — replication kit
        replication_kit = {
            "subject_archetype": dev_data.get("profile", {}).get("needs", []),
            "rights_template": len(dev_data.get("rights_package", {})),
            "coordination_model": prod_data.get("call_sheet", {}).get("coordination_model", ""),
            "coverage": post_data.get("assembly_cut", {}).get("coverage", 0),
            "estimated_savings": self._get_coordination_savings(),
            "transferable": True,
        }

        # 5. Narrative from post-production
        narrative = post_data.get("sound_mix", {})

        # 6. Industries changed
        industries = self._assess_industries_changed(production)

        # 7. Innovations
        innovations = post_data.get("vfx_finals", {}).get("innovations", [])

        distribution = {
            "narrative": narrative,
            "cosm": cosm.model_dump(),
            "ip_catalog": ip_outputs,
            "dome_bond": dome_bond.model_dump(),
            "replication_kit": replication_kit,
            "innovations": innovations,
            "industries_changed": industries,
            "data_engine_stats": self.store.stats(),
        }

        return StageResult(
            success=True,
            message=(
                f"DOME COMPLETE — {subject}. "
                f"COSM: {cosm.total:.1f} (R:{cosm.rights:.0f} Re:{cosm.research:.0f} "
                f"B:{cosm.budget:.0f} P:{cosm.package:.0f} D:{cosm.deliverables:.0f} Pi:{cosm.pitch:.0f}). "
                f"Bond: {dome_bond.rating} rated, ${dome_bond.face_value:,.0f} face, "
                f"{dome_bond.coupon_rate:.1f}% coupon. "
                f"IP: {len(ip_outputs)} outputs."
            ),
            new_stage=None,
            progress=100.0,
            data=distribution,
        )

    # ══════════════════════════════════════════════════════════════════
    # SPHERES PIPELINE — Professional Production for Space Activation
    # ══════════════════════════════════════════════════════════════════

    async def spheres_development(self, production: ProductionState,
                                  action_data: Dict[str, Any]) -> StageResult:
        """
        DEVELOPMENT: Location scouting, rights & permits, development deal.
        Deliverables: location report, rights assessment, deal memo.
        """
        parcel_query = production.subject

        # Location scouting — find parcel in data engine
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

        extra = target_parcel.get("extra", "{}")
        if isinstance(extra, str):
            try:
                extra = json.loads(extra)
            except (json.JSONDecodeError, TypeError):
                extra = {}

        zoning_code = target_parcel.get("zoning", "")
        zoning_info = ZONING_REFERENCE.get(zoning_code, {
            "name": zoning_code, "description": "Custom zoning district"
        })

        # Enrichment insights for this parcel
        enrichments = self.store.get_enrichments(enrichment_type="opportunity", limit=20)
        location_insights = []
        for e in enrichments:
            edata = e.get("data", "{}")
            if isinstance(edata, str):
                try:
                    edata = json.loads(edata)
                except (json.JSONDecodeError, TypeError):
                    edata = {}
            if edata.get("parcel_id") == target_parcel.get("parcel_id"):
                location_insights.append({
                    "description": e.get("description", ""),
                    "activation_score": edata.get("activation_score", 0),
                    "activation_types": edata.get("activation_types", []),
                })

        # Nearby parcels (same neighborhood)
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

        location_report = {
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

        # Rights assessment — permits needed
        rights_assessment = [
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
            "location_report": location_report,
            "rights_assessment": {"permits": rights_assessment},
            "location_insights": location_insights,
            "nearby_parcels": nearby_list,
            "data_engine_stats": self.store.stats(),
        }

        return StageResult(
            success=True,
            message=(
                f"Location scouted: {location_report['address']}. "
                f"{location_report['land_area_sqft']:,.0f} sqft, zoned {zoning_code} "
                f"({zoning_info.get('name', '')}). "
                f"{'VACANT — ready for activation' if location_report['vacant'] else 'IMPROVED — adaptive reuse potential'}. "
                f"Assessed at ${location_report['total_val']:,.0f}. "
                f"{len(nearby_list)} nearby parcels in {neighborhood}. "
                f"Ready for Pre-Production."
            ),
            new_stage=ProductionStage.PRE_PRODUCTION,
            progress=20.0,
            data=research,
        )

    async def spheres_pre_production(self, production: ProductionState,
                                     action_data: Dict[str, Any]) -> StageResult:
        """
        PRE-PRODUCTION: Design (activation plan), budget (cost tiers),
        community cast, build crew.
        Deliverables: design board, budget model, cast & crew plan.
        """
        dev_data = production.stage_data.get("development", {})
        parcel = dev_data.get("location_report", {})

        area_sqft = parcel.get("land_area_sqft", 2500)
        zoning = parcel.get("zoning", "CMX-2")
        zoning_info = parcel.get("zoning_info", {})

        # Design Board — activation types based on parcel characteristics
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

        feature_map = {
            "community_hub": ["gathering pavilion", "community board", "wifi", "seating"],
            "community_garden": ["raised beds", "tool shed", "water access", "composting"],
            "pocket_park": ["benches", "shade trees", "pathways", "lighting"],
            "popup_market": ["vendor stalls", "canopy structures", "power hookups"],
            "maker_space": ["workshop area", "tool library", "material storage"],
            "performance_venue": ["stage platform", "seating area", "sound system"],
            "art_installation": ["installation base", "lighting", "interpretive signage"],
        }

        features = []
        for at in activation_types[:3]:
            features.extend(feature_map.get(at, []))

        design_board = {
            "id": f"design-{parcel.get('parcel_id', '001')}",
            "name": f"Sphere Activation: {parcel.get('address', 'Unknown')}",
            "type": "community activation",
            "activation_types": activation_types,
            "access_hours": area_sqft * 0.3,
            "features": features,
        }

        # Budget Model — three tiers
        cost_per_sqft = {"light": 12, "moderate": 45, "full": 95}
        budget_model = {
            "light_activation": {
                "total": area_sqft * cost_per_sqft["light"],
                "per_sqft": cost_per_sqft["light"],
                "includes": "Landscaping, seating, signage, basic lighting",
            },
            "moderate_activation": {
                "total": area_sqft * cost_per_sqft["moderate"],
                "per_sqft": cost_per_sqft["moderate"],
                "includes": "Temporary structures, utilities, programming, staffing",
            },
            "full_buildout": {
                "total": area_sqft * cost_per_sqft["full"],
                "per_sqft": cost_per_sqft["full"],
                "includes": "Permanent structures, full utilities, ongoing operations",
            },
            "recommended": "moderate_activation" if area_sqft > 3000 else "light_activation",
            "recommended_total": area_sqft * cost_per_sqft["moderate"] if area_sqft > 3000 else area_sqft * cost_per_sqft["light"],
        }

        # Production Timeline
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

        prep = {
            "design_board": design_board,
            "budget_model": budget_model,
            "timeline": timeline,
            "zoning_info": zoning_info,
        }

        return StageResult(
            success=True,
            message=(
                f"Pre-Production locked for {parcel.get('address', '')}. "
                f"Design: {', '.join(activation_types[:3])}. "
                f"Budget: {budget_model['recommended']} (${budget_model['recommended_total']:,.0f}). "
                f"Timeline: {timeline['duration_years']} years. "
                f"Ready for Production."
            ),
            new_stage=ProductionStage.PRODUCTION,
            progress=40.0,
            data=prep,
        )

    async def spheres_production(self, production: ProductionState,
                                 action_data: Dict[str, Any]) -> StageResult:
        """
        PRODUCTION: Build (construction), activate (programming launch),
        capture (documentation).
        Deliverables: build report, activation log, capture reel.
        """
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        parcel = dev_data.get("location_report", {})

        # Build Report — permits executed
        permits = dev_data.get("rights_assessment", {}).get("permits", [])
        executed_permits = []
        for p in permits:
            executed_permits.append({
                **p,
                "status": "approved" if p.get("status") != "conditional" else "waived",
            })

        policy_changes = [
            f"Temporary Use Ordinance expansion for {parcel.get('zoning', '')} zones",
            "Community Benefit Agreement framework for public land activation",
            "Streamlined permit pathway for community-initiated development",
        ]

        design = pre_data.get("design_board", {})
        budget = pre_data.get("budget_model", {})
        area = parcel.get("land_area_sqft", 2500)

        # Activation Log
        activation_log = {
            "activated": True,
            "sqft_activated": area,
            "features_installed": design.get("features", []),
            "activation_types": design.get("activation_types", []),
            "investment": budget.get("recommended_total", 0),
            "events_capacity": max(50, area // 20),
        }

        build = {
            "build_report": {
                "permits": executed_permits,
                "policy_changes": policy_changes,
            },
            "activation_log": activation_log,
        }

        return StageResult(
            success=True,
            message=(
                f"Production wrapped at {parcel.get('address', '')}. "
                f"{area:,.0f} sqft activated. "
                f"{len(executed_permits)} permits executed. "
                f"{len(policy_changes)} policy changes enabled. "
                f"Capacity: {activation_log['events_capacity']} people. "
                f"Ready for Post-Production."
            ),
            new_stage=ProductionStage.POST_PRODUCTION,
            progress=60.0,
            data=build,
        )

    async def spheres_post_production(self, production: ProductionState,
                                      action_data: Dict[str, Any]) -> StageResult:
        """
        POST-PRODUCTION: Measure (impact metrics), document (episodes),
        innovate (IP extraction).
        Deliverables: impact dashboard, episode timeline, innovation portfolio.
        """
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        prod_data = production.stage_data.get("production", {})
        parcel = dev_data.get("location_report", {})
        activation = prod_data.get("activation_log", {})

        address = parcel.get("address", "Unknown")
        area = activation.get("sqft_activated", 2500)
        capacity = activation.get("events_capacity", 100)

        # Impact Dashboard
        investment = pre_data.get("budget_model", {}).get("recommended_total", 50000)
        impact_dashboard = {
            "connected_projects": len(dev_data.get("nearby_parcels", [])),
            "total_visitors": capacity * 10,
            "economic_impact": investment * 3.2,
            "community_rating": 4.7,
            "jobs_created": max(3, area // 2000),
            "property_value_impact_pct": 3.2,
        }

        # Episode Timeline
        episode_timeline = [
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

        # Innovation Portfolio
        innovation_portfolio = {
            "innovations": [
                "Modular Public Space Activation Kit",
                "Community Ownership Protocol",
                "Impact Measurement Dashboard (real-time)",
                f"{parcel.get('neighborhood', 'Neighborhood')} Activation Playbook",
            ],
            "protocols": [
                "Sphere Activation Standard v1",
                f"Zoning Overlay Protocol for {parcel.get('zoning', 'CMX-2')} activation",
            ],
        }

        # IP Generation — across 8 domains
        ip_outputs = self._generate_sphere_ip(
            production, parcel, pre_data, prod_data, impact_dashboard
        )

        post = {
            "impact_dashboard": impact_dashboard,
            "episode_timeline": episode_timeline,
            "innovation_portfolio": innovation_portfolio,
            "ip_outputs": [ip.model_dump() for ip in ip_outputs],
        }

        return StageResult(
            success=True,
            message=(
                f"Post-Production locked. "
                f"{capacity * 10:,} cumulative visitors. "
                f"${impact_dashboard['economic_impact']:,.0f} economic impact (3.2x multiplier). "
                f"{impact_dashboard['jobs_created']} jobs created. "
                f"IP: {len(ip_outputs)} outputs across {len(set(ip.domain for ip in ip_outputs))} domains. "
                f"Ready for Distribution."
            ),
            new_stage=ProductionStage.DISTRIBUTION,
            progress=80.0,
            data=post,
        )

    async def spheres_distribution(self, production: ProductionState,
                                    action_data: Dict[str, Any]) -> StageResult:
        """
        DISTRIBUTION: CHRON reveal, Chron Bond pricing, replication kit.
        Deliverables: final CHRON, bond term sheet, replication playbook.
        """
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        post_data = production.stage_data.get("post_production", {})

        # 1. CHRON Reveal
        chron = self._calculate_chron(production)

        # 2. Chron Bond pricing
        chron_bond = self._price_chron_bond(production, chron)

        # 3. IP catalog from post
        ip_outputs = post_data.get("ip_outputs", [])

        # 4. Replication kit
        parcel = dev_data.get("location_report", {})
        replication_kit = {
            "parcel_type": "vacant" if parcel.get("vacant") else "improved",
            "zoning": parcel.get("zoning", ""),
            "activation_types": pre_data.get("design_board", {}).get("activation_types", []),
            "budget_tier": pre_data.get("budget_model", {}).get("recommended", ""),
            "transferable": True,
        }

        # 5. Innovations
        innovations = post_data.get("innovation_portfolio", {}).get("innovations", [])

        distribution = {
            "impact_dashboard": post_data.get("impact_dashboard", {}),
            "chron": chron.model_dump(),
            "chron_bond": chron_bond.model_dump(),
            "ip_catalog": ip_outputs,
            "replication_kit": replication_kit,
            "innovations": innovations,
            "data_engine_stats": self.store.stats(),
        }

        return StageResult(
            success=True,
            message=(
                f"SPHERE COMPLETE — {production.subject}. "
                f"CHRON: {chron.total:.1f} (U:{chron.unlock:.0f} A:{chron.access:.0f} "
                f"P:{chron.permanence:.2f} C:{chron.catalyst:.2f} Po:{chron.policy:.2f}). "
                f"Bond: {chron_bond.rating} rated, ${chron_bond.face_value:,.0f} face, "
                f"{chron_bond.coupon_rate:.1f}% coupon. "
                f"IP: {len(ip_outputs)} outputs."
            ),
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
    # IP GENERATION ENGINE
    # ══════════════════════════════════════════════════════════════════

    def _generate_ip(self, production, subject, dev_data, pre_data,
                     prod_data, assembly_cut) -> List[IPOutput]:
        """Generate IP across 8 domains from dome production data."""
        ip = []

        # Entertainment IP — narrative format
        ip.append(IPOutput(
            domain=IPDomain.ENTERTAINMENT,
            title=f"The Dome of {subject}",
            description=(
                f"Documentary structure following {subject} through "
                f"{len(dev_data.get('rights_package', {}))} regulatory dimensions "
                f"to complete dome coverage."
            ),
            format="documentary_structure",
            stage_originated=ProductionStage.POST_PRODUCTION,
            value_driver="Human story of navigating fragmented systems",
        ))

        # Technology IP — data systems & protocols
        system_count = dev_data.get("system_count", 0)
        ip.append(IPOutput(
            domain=IPDomain.TECHNOLOGY,
            title=f"Government API Orchestration Protocol",
            description=(
                f"Method for coordinating {system_count} federal/state/local "
                f"data systems with {dev_data.get('active_links', 0)} active connections."
            ),
            format="API_protocol",
            stage_originated=ProductionStage.PRODUCTION,
            value_driver="Cross-system interoperability method",
        ))

        # Financial Product IP — bond structure & cost models
        frag_cost = self._get_fragmentation_cost()
        coord_savings = self._get_coordination_savings()
        ip.append(IPOutput(
            domain=IPDomain.FINANCIAL_PRODUCT,
            title="Dome Bond Structure",
            description=(
                f"Financial instrument backed by ${coord_savings:,.0f}/year "
                f"coordination savings. Fragmented cost: ${frag_cost:,.0f}."
            ),
            format="bond_term_sheet",
            stage_originated=ProductionStage.DISTRIBUTION,
            value_driver="Quantified savings from coordination",
        ))

        # Policy IP — legal frameworks
        rights_dims = list(dev_data.get("rights_package", {}).keys())
        ip.append(IPOutput(
            domain=IPDomain.POLICY,
            title="Cross-System Consent Protocol",
            description=(
                f"Legal framework enabling data sharing across "
                f"{', '.join(rights_dims[:4])} dimensions with consent preservation."
            ),
            format="policy_framework",
            stage_originated=ProductionStage.DEVELOPMENT,
            value_driver="Consent-preserving data coordination",
        ))

        # Product IP — replication kit
        ip.append(IPOutput(
            domain=IPDomain.PRODUCT,
            title="Dome Construction Kit",
            description=(
                f"Replicable dome architecture covering {assembly_cut.get('coverage', 0):.0%} "
                f"of existence dimensions. Transferable to any geography."
            ),
            format="product_kit",
            stage_originated=ProductionStage.DISTRIBUTION,
            value_driver="Scalable dome replication",
        ))

        # Research IP — datasets & methodologies
        ip.append(IPOutput(
            domain=IPDomain.RESEARCH,
            title="Fragmentation Cost Index",
            description=(
                f"Methodology for calculating per-person fragmentation cost "
                f"across {len(rights_dims)} regulatory dimensions. "
                f"Backed by {dev_data.get('cost_point_count', 0)} data points."
            ),
            format="research_methodology",
            stage_originated=ProductionStage.DEVELOPMENT,
            value_driver="Novel cost measurement framework",
        ))

        # Housing IP — dome architecture
        coord_model = prod_data.get("call_sheet", {}).get("coordination_model", "")
        ip.append(IPOutput(
            domain=IPDomain.HOUSING,
            title="Person-Centered Dome Architecture",
            description=(
                f"Dome architecture using {coord_model} coordination model "
                f"to wrap {system_count} systems around one person."
            ),
            format="architecture_blueprint",
            stage_originated=ProductionStage.PRE_PRODUCTION,
            value_driver="Complete protective coverage model",
        ))

        # Healthcare IP — care coordination
        ip.append(IPOutput(
            domain=IPDomain.HEALTHCARE,
            title="Portable Benefits Bridge Protocol",
            description=(
                f"Protocol enabling continuous coverage across "
                f"healthcare, housing, income, and food dimensions "
                f"regardless of system boundaries."
            ),
            format="care_protocol",
            stage_originated=ProductionStage.PRODUCTION,
            value_driver="Cross-system care continuity",
        ))

        return ip

    def _generate_sphere_ip(self, production, parcel, pre_data,
                            prod_data, metrics) -> List[IPOutput]:
        """Generate IP across 8 domains from sphere production data."""
        ip = []
        address = parcel.get("address", "Unknown")
        neighborhood = parcel.get("neighborhood", "")
        area = parcel.get("land_area_sqft", 2500)

        # Entertainment IP
        ip.append(IPOutput(
            domain=IPDomain.ENTERTAINMENT,
            title=f"Sphere: {neighborhood}",
            description=(
                f"Place-based narrative of activating {area:,} sqft at {address}. "
                f"Community transformation documented across 4 episodes."
            ),
            format="docuseries_format",
            stage_originated=ProductionStage.POST_PRODUCTION,
            value_driver="Community transformation story",
        ))

        # Technology IP
        ip.append(IPOutput(
            domain=IPDomain.TECHNOLOGY,
            title="Impact Measurement Dashboard",
            description=(
                f"Real-time measurement system tracking visitors, economic impact, "
                f"property values, and community engagement for activated spaces."
            ),
            format="software_platform",
            stage_originated=ProductionStage.POST_PRODUCTION,
            value_driver="Quantified community impact",
        ))

        # Financial Product IP
        ip.append(IPOutput(
            domain=IPDomain.FINANCIAL_PRODUCT,
            title="Chron Bond Structure",
            description=(
                f"Financial instrument backed by ${metrics.get('economic_impact', 0):,.0f} "
                f"economic impact from {area:,} sqft activation."
            ),
            format="bond_term_sheet",
            stage_originated=ProductionStage.DISTRIBUTION,
            value_driver="Space activation ROI",
        ))

        # Policy IP
        policy_changes = prod_data.get("build_report", {}).get("policy_changes", [])
        ip.append(IPOutput(
            domain=IPDomain.POLICY,
            title="Streamlined Activation Ordinance",
            description=(
                f"{len(policy_changes)} policy changes enabling faster community-led "
                f"development in {parcel.get('zoning', '')} zones."
            ),
            format="model_ordinance",
            stage_originated=ProductionStage.PRODUCTION,
            value_driver="Reduced permitting friction",
        ))

        # Product IP
        ip.append(IPOutput(
            domain=IPDomain.PRODUCT,
            title="Modular Space Activation Kit",
            description=(
                f"Physical product kit for activating vacant parcels. "
                f"Includes {len(pre_data.get('design_board', {}).get('features', []))} components."
            ),
            format="product_kit",
            stage_originated=ProductionStage.PRE_PRODUCTION,
            value_driver="Scalable physical activation",
        ))

        # Research IP
        ip.append(IPOutput(
            domain=IPDomain.RESEARCH,
            title=f"{neighborhood} Activation Study",
            description=(
                f"Longitudinal study of space activation impact: "
                f"{metrics.get('total_visitors', 0):,} visitors, "
                f"{metrics.get('property_value_impact_pct', 0)}% property value increase."
            ),
            format="research_study",
            stage_originated=ProductionStage.POST_PRODUCTION,
            value_driver="Evidence base for space activation",
        ))

        # Housing IP
        ip.append(IPOutput(
            domain=IPDomain.HOUSING,
            title="Community Land Trust Integration Model",
            description=(
                f"Framework connecting activated public spaces to surrounding "
                f"housing stock. {len(prod_data.get('build_report', {}).get('permits', []))} "
                f"permits as precedent."
            ),
            format="integration_model",
            stage_originated=ProductionStage.PRODUCTION,
            value_driver="Space-housing value linkage",
        ))

        # Healthcare IP
        ip.append(IPOutput(
            domain=IPDomain.HEALTHCARE,
            title="Green Space Health Protocol",
            description=(
                f"Protocol for measuring health outcomes from public space access. "
                f"{area:,} sqft of activated therapeutic green space."
            ),
            format="health_protocol",
            stage_originated=ProductionStage.POST_PRODUCTION,
            value_driver="Public health through space activation",
        ))

        return ip

    # ══════════════════════════════════════════════════════════════════
    # BOND PRICING ENGINE
    # ══════════════════════════════════════════════════════════════════

    def _price_dome_bond(self, production: ProductionState,
                         cosm: CosmDimensions) -> DomeBond:
        """Price a Dome Bond from COSM score and production data."""
        dev_data = production.stage_data.get("development", {})
        post_data = production.stage_data.get("post_production", {})

        savings = self._get_coordination_savings()
        coverage = post_data.get("assembly_cut", {}).get("coverage", 0.5)
        rights_count = dev_data.get("rights_count", 0)

        # Face value = annual coordination savings * maturity
        maturity = 10 if coverage > 0.8 else 7 if coverage > 0.5 else 5
        face_value = savings * maturity

        # Rating from coverage + COSM
        score = cosm.total
        if score >= 80 and coverage >= 0.9:
            rating = "AAA"
        elif score >= 70 and coverage >= 0.8:
            rating = "AA"
        elif score >= 60 and coverage >= 0.7:
            rating = "A"
        elif score >= 50 and coverage >= 0.5:
            rating = "BBB"
        elif score >= 40:
            rating = "BB"
        else:
            rating = "B"

        # Coupon rate inversely related to rating (higher risk = higher coupon)
        coupon_map = {"AAA": 3.5, "AA": 4.0, "A": 4.5, "BBB": 5.5, "BB": 6.5, "B": 8.0}
        coupon = coupon_map.get(rating, 5.5)

        # YTM
        ytm = coupon + (0.5 if rating in ("BB", "B") else 0)

        bond_id = hashlib.md5(
            f"{production.production_id}-dome".encode()
        ).hexdigest()[:12]

        return DomeBond(
            bond_id=f"DOME-{bond_id.upper()}",
            subject=production.subject,
            face_value=round(face_value, 2),
            coupon_rate=coupon,
            maturity_years=maturity,
            rating=rating,
            cosm_score=round(cosm.total, 1),
            programs_backing=rights_count,
            yield_to_maturity=ytm,
        )

    def _price_chron_bond(self, production: ProductionState,
                          chron: ChronDimensions) -> ChronBond:
        """Price a Chron Bond from CHRON score and production data."""
        dev_data = production.stage_data.get("development", {})
        post_data = production.stage_data.get("post_production", {})
        pre_data = production.stage_data.get("pre_production", {})

        parcel = dev_data.get("location_report", {})
        metrics = post_data.get("impact_dashboard", {})
        area = parcel.get("land_area_sqft", 2500)

        economic_impact = metrics.get("economic_impact", 50000)

        # Maturity based on permanence
        perm = chron.permanence
        maturity = 15 if perm > 0.7 else 10 if perm > 0.4 else 5

        face_value = economic_impact

        # Rating from CHRON dimensions
        policy_score = chron.policy
        catalyst_score = chron.catalyst
        combined = (policy_score + catalyst_score + perm) / 3

        if combined >= 0.8:
            rating = "AAA"
        elif combined >= 0.65:
            rating = "AA"
        elif combined >= 0.5:
            rating = "A"
        elif combined >= 0.35:
            rating = "BBB"
        elif combined >= 0.2:
            rating = "BB"
        else:
            rating = "B"

        coupon_map = {"AAA": 3.0, "AA": 3.5, "A": 4.0, "BBB": 5.0, "BB": 6.0, "B": 7.5}
        coupon = coupon_map.get(rating, 5.0)
        ytm = coupon + (0.5 if rating in ("BB", "B") else 0)

        bond_id = hashlib.md5(
            f"{production.production_id}-chron".encode()
        ).hexdigest()[:12]

        return ChronBond(
            bond_id=f"CHRON-{bond_id.upper()}",
            parcel=parcel.get("address", production.subject),
            face_value=round(face_value, 2),
            coupon_rate=coupon,
            maturity_years=maturity,
            rating=rating,
            chron_score=round(chron.total, 1),
            sqft_backing=area,
            yield_to_maturity=ytm,
        )

    # ══════════════════════════════════════════════════════════════════
    # COSM / CHRON SCORING
    # ══════════════════════════════════════════════════════════════════

    def _calculate_cosm(self, production: ProductionState) -> CosmDimensions:
        """Calculate COSM across 6 production dimensions."""
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        post_data = production.stage_data.get("post_production", {})

        # Rights — from rights acquisition
        rights_count = dev_data.get("rights_count", 0)
        rights_score = min(100.0, rights_count * 4.0)

        # Research — from data systems connectivity
        active_links = dev_data.get("active_links", 0)
        total_links = dev_data.get("link_count", 1)
        research_score = min(100.0, (active_links / max(1, total_links)) * 120)

        # Budget — from cost landscape depth
        cost_count = dev_data.get("cost_point_count", 0)
        budget_score = min(100.0, cost_count * 2.5)

        # Package — from coordination architecture
        crew = pre_data.get("coordination_crew", [])
        best_savings = max([m.get("estimated_savings_pct", 0) for m in crew], default=0)
        package_score = min(100.0, len(crew) * 15 + best_savings)

        # Deliverables — from flourishing outcomes
        flour_data = pre_data.get("flourishing", {})
        deliverables_score = flour_data.get("overall_score", 0.5) * 100

        # Pitch — from narrative + IP generation
        sound_mix = post_data.get("sound_mix", {})
        ip_count = len(post_data.get("ip_outputs", []))
        pitch_score = min(100.0,
                          len(sound_mix.get("sections", [])) * 15 + ip_count * 5)

        return CosmDimensions(
            rights=round(rights_score, 1),
            research=round(research_score, 1),
            budget=round(budget_score, 1),
            package=round(package_score, 1),
            deliverables=round(deliverables_score, 1),
            pitch=round(pitch_score, 1),
        )

    def _calculate_chron(self, production: ProductionState) -> ChronDimensions:
        """Calculate CHRON across 5 space dimensions."""
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        prod_data = production.stage_data.get("production", {})
        post_data = production.stage_data.get("post_production", {})

        parcel = dev_data.get("location_report", {})
        unlock = parcel.get("land_area_sqft", 2500)

        design = pre_data.get("design_board", {})
        access = design.get("access_hours", 360.0)

        timeline = pre_data.get("timeline", {})
        permanence = min(1.0, timeline.get("duration_years", 1.0) / 10.0)

        metrics = post_data.get("impact_dashboard", {})
        catalyst = min(1.0, metrics.get("connected_projects", 0) / 10.0)

        build_report = prod_data.get("build_report", {})
        policy = min(1.0, len(build_report.get("policy_changes", [])) / 5.0)

        return ChronDimensions(
            unlock=unlock, access=access, permanence=permanence,
            catalyst=catalyst, policy=policy,
        )

    # ══════════════════════════════════════════════════════════════════
    # INTERNAL HELPERS
    # ══════════════════════════════════════════════════════════════════

    def _build_profile(self, subject: str, rights_package: dict, market_analysis: dict) -> dict:
        dimensions = list(rights_package.keys())
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

    def _grade_from_score(self, score: float) -> str:
        if score >= 0.9:
            return "A+"
        elif score >= 0.8:
            return "A"
        elif score >= 0.7:
            return "B+"
        elif score >= 0.6:
            return "B"
        elif score >= 0.5:
            return "C+"
        elif score >= 0.4:
            return "C"
        else:
            return "D"

    def _build_narrative_sections(self, subject, dev_data, pre_data, prod_data, assembly_cut):
        frag_cost = self._get_fragmentation_cost()
        coord_savings = self._get_coordination_savings()
        system_count = dev_data.get("system_count", 0)
        rights_count = dev_data.get("rights_count", 0)

        return [
            {
                "title": "The Problem: Fragmentation",
                "content": (
                    f"The US spends an estimated ${frag_cost:,.0f} per person per year "
                    f"on uncoordinated care for multi-system individuals. {system_count} government "
                    f"data systems hold pieces of a person's life — but "
                    f"{dev_data.get('blocked_links', 0)} connections between them are blocked "
                    f"by regulatory barriers."
                ),
            },
            {
                "title": "The Subject",
                "content": (
                    f"{subject}: navigating {len(dev_data.get('rights_package', {}))} "
                    f"regulatory dimensions — from {', '.join(list(dev_data.get('rights_package', {}).keys())[:4])} "
                    f"and beyond. Each dimension has its own application, its own caseworker, "
                    f"its own data system, its own rules."
                ),
            },
            {
                "title": "The Dome",
                "content": (
                    f"A complete protective dome built from {rights_count} legal provisions, "
                    f"coordinated across {system_count} systems, using "
                    f"{prod_data.get('call_sheet', {}).get('coordination_model', 'integrated')} "
                    f"architecture. Coverage: {assembly_cut.get('coverage', 0):.0%} across "
                    f"{len(assembly_cut.get('dimensions_covered', []))} dimensions."
                ),
            },
            {
                "title": "The Savings",
                "content": (
                    f"Coordination produces estimated ${coord_savings:,.0f}/year in savings "
                    f"per person. Moving from fragmented (${frag_cost:,.0f}/year) to coordinated "
                    f"(${frag_cost - coord_savings:,.0f}/year). "
                    f"Every dollar sourced from CMS, HUD, Vera, and HCUP data."
                ),
            },
            {
                "title": "The Bond",
                "content": (
                    f"This dome generates a Dome Bond — a financial instrument backed by "
                    f"${coord_savings:,.0f}/year in coordination savings. "
                    f"Rated by dome coverage ({assembly_cut.get('coverage', 0):.0%}) "
                    f"and COSM score. Replicable across any geography."
                ),
            },
        ]

    def _extract_innovations_from_production(self, subject, dev_data, pre_data,
                                              prod_data, coordination_model):
        return {
            "innovations": [
                f"Person-Centered Dome Architecture for {subject}",
                f"Cross-System Consent Protocol ({coordination_model})",
                "Fragmentation Cost Calculator (real data-backed)",
                "Portable Benefits Bridge Protocol",
                "Dome Bond Pricing Methodology",
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
                "Dome Bond Issuance Protocol — pricing coordination savings",
            ],
        }

    def _assess_industries_changed(self, production: ProductionState) -> List[str]:
        industries = set()
        dev_data = production.stage_data.get("development", {})
        rights_package = dev_data.get("rights_package", {})

        dim_map = {
            "healthcare": "Healthcare", "housing": "Housing & Real Estate",
            "income": "Financial Services", "food": "Food & Agriculture",
            "employment": "Workforce Development", "education": "Education",
            "justice": "Criminal Justice", "data_privacy": "Data Privacy & Technology",
            "interoperability": "Government Technology",
        }

        for dim in rights_package.keys():
            industry = dim_map.get(dim)
            if industry:
                industries.add(industry)

        prod_data = production.stage_data.get("production", {})
        if prod_data.get("executed_agreements"):
            industries.add("Government Contracting")

        # Bond issuance changes finance
        industries.add("Municipal Finance")

        return sorted(industries) if industries else ["Cross-Sector Impact"]
