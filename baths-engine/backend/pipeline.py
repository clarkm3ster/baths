"""
BATHS Game Engine - Production Pipeline Director
Orchestrates player through Development -> Pre -> Prod -> Post -> Distribution
With demo mode fallback when backend APIs aren't running
"""

import os
import httpx
import random
from typing import Dict, Any, List, Optional
from models import (
    GameType, ProductionStage, ProductionState, StageResult,
    CosmDimensions, ChronDimensions
)

DEMO_DATA = {
    "domes-profile-research": {
        "profile": {
            "name": "Demo Subject",
            "age": 34,
            "needs": ["healthcare", "housing", "legal aid", "financial coaching"],
            "risk_factors": ["uninsured", "data fragmented"],
            "strengths": ["employed", "community connected"]
        }
    },
    "domes-data-research": {
        "systems": [
            {"name": "SSA", "domain": "Social Security", "connected": True},
            {"name": "CMS", "domain": "Healthcare", "connected": True},
            {"name": "IRS", "domain": "Finance", "connected": True},
            {"name": "HUD", "domain": "Housing", "connected": True},
            {"name": "DOL", "domain": "Labor", "connected": True},
            {"name": "ED", "domain": "Education", "connected": True},
            {"name": "VA", "domain": "Veterans", "connected": False},
            {"name": "SNAP", "domain": "Nutrition", "connected": True}
        ]
    },
    "domes-legal": {
        "provisions": [
            {"code": "ACA-1332", "domain": "Health Insurance", "description": "State Innovation Waiver"},
            {"code": "HIPAA-164", "domain": "Data Privacy", "description": "Health Data Portability"},
            {"code": "FCRA-604", "domain": "Finance", "description": "Fair Credit Reporting"},
            {"code": "ADA-302", "domain": "Health Access", "description": "Public Accommodation"},
            {"code": "FERPA-99", "domain": "Education Data", "description": "Education Records Privacy"},
            {"code": "SSA-205", "domain": "Social Security", "description": "Benefit Claims Process"}
        ]
    },
    "domes-architect": {
        "architecture": {
            "type": "full_dome",
            "layers": ["legal", "data", "fiscal", "coordination", "flourishing", "narrative"],
            "coverage": 0.85
        }
    },
    "domes-datamap": {
        "person_map": {
            "systems_connected": 6,
            "data_flows": 14,
            "gaps_identified": 3
        }
    },
    "domes-flourishing": {
        "index": 72.5,
        "dimensions": {
            "health": 68,
            "economic": 75,
            "social": 80,
            "civic": 65,
            "environmental": 74
        }
    },
    "domes-contracts": {
        "agreements": [
            {"type": "Government Data Sharing", "status": "executed", "parties": ["SSA", "CMS"]},
            {"type": "Healthcare Coverage", "status": "executed", "parties": ["ACA Marketplace"]},
            {"type": "Financial Coaching", "status": "executed", "parties": ["CFPB Partner"]},
            {"type": "Government Benefits Coordination", "status": "pending", "parties": ["HUD", "DOL"]}
        ]
    },
    "domes-profiles": {
        "profile_complete": True,
        "coverage_score": 0.82,
        "gaps_remaining": 2
    },
    "domes-brain": {
        "verification": {
            "complete": True,
            "coverage": 0.88,
            "gaps": ["VA integration pending", "SNAP auto-renewal needed"],
            "recommendations": ["Connect VA benefits", "Enable SNAP auto-renewal"]
        }
    },
    "domes-lab": {
        "innovations": ["Portable Benefits Protocol", "Cross-Agency Data Bridge", "Flourishing Index v2"],
        "patents": ["Personal Data Dome Architecture", "Government API Orchestration Method"],
        "protocols": ["Dome Verification Standard v1"]
    },
    "domes-viz": {
        "sections": [
            {"title": "The Problem", "content": "Fragmented government systems leave individuals without a coherent safety net."},
            {"title": "The Dome", "content": "A complete protective dome built from every relevant government program."},
            {"title": "The Impact", "content": "One person, fully covered. A patent on the process of personal protection."},
            {"title": "The Innovation", "content": "Portable Benefits Protocol enables dome replication at scale."},
            {"title": "Industries Changed", "content": "Insurance, Healthcare, Government Contracting fundamentally altered."}
        ]
    },
    "spheres-assets": {
        "parcel": {
            "id": "demo-parcel",
            "address": "123 Main St",
            "city": "Demo City",
            "area_sqm": 2500.0,
            "zoning": "mixed-use",
            "status": "available"
        }
    },
    "spheres-legal": {
        "permits": [
            {"type": "temporary_use", "status": "approved"},
            {"type": "public_assembly", "status": "approved"},
            {"type": "food_service", "status": "pending"}
        ],
        "policy_changes": ["Temporary Use Ordinance Update", "Public Space Activation Framework", "Community Benefit Agreement"]
    },
    "spheres-studio": {
        "design": {
            "id": "design-001",
            "name": "Community Activation Hub",
            "type": "mixed-use public space",
            "access_hours": 720.0,
            "features": ["gathering space", "market area", "performance stage", "garden"]
        },
        "cost": {
            "total": 125000,
            "breakdown": {"construction": 80000, "permits": 15000, "programming": 30000}
        },
        "timeline": {
            "duration_years": 3.0,
            "phases": ["design", "permits", "build", "activate", "sustain"]
        },
        "world": {
            "activated": True,
            "sqm_activated": 2500,
            "events_capacity": 500
        }
    },
    "spheres-viz": {
        "episodes": [
            {"title": "Ground Breaking", "date": "Week 1", "impact": "Community engagement begins"},
            {"title": "First Market Day", "date": "Week 8", "impact": "200 visitors, 15 vendors"},
            {"title": "Community Festival", "date": "Week 16", "impact": "1000 attendees, media coverage"}
        ]
    },
    "spheres-lab": {
        "innovations": ["Modular Public Space Kit", "Community Ownership Protocol", "Impact Measurement Dashboard"],
        "patents": [],
        "protocols": ["Sphere Activation Standard v1"]
    },
    "spheres-brain": {
        "metrics": {
            "connected_projects": 7,
            "total_visitors": 15000,
            "economic_impact": 450000,
            "community_rating": 4.7
        }
    }
}


class PipelineDirector:
    def __init__(self, api_registry: Dict[str, Any]):
        self.api_registry = api_registry
        self.client = httpx.AsyncClient(timeout=10.0)
        self.demo_mode = os.environ.get("BATHS_DEMO_MODE", "true").lower() == "true"

    async def call_api(self, service_name: str, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict[str, Any]:
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
                return response.json()
        except Exception:
            pass

        return DEMO_DATA.get(service_name, {"status": "demo", "message": f"Demo data for {service_name}"})

    async def domes_development(self, production: ProductionState, action_data: Dict[str, Any]) -> StageResult:
        subject = production.subject
        profile_data = await self.call_api("domes-profile-research", f"/api/profiles?name={subject}")
        if "profile" in profile_data:
            profile_data["profile"]["name"] = subject
        data_systems = await self.call_api("domes-data-research", "/api/systems")
        legal_provisions = await self.call_api("domes-legal", "/api/provisions")

        research = {
            "profile": profile_data,
            "data_systems": data_systems,
            "legal_provisions": legal_provisions
        }

        return StageResult(
            success=True,
            message=f"Research complete for {subject}. Ready for Pre-Production.",
            new_stage=ProductionStage.PRE_PRODUCTION,
            progress=20.0,
            data=research
        )

    async def domes_pre_production(self, production: ProductionState, action_data: Dict[str, Any]) -> StageResult:
        architecture = await self.call_api("domes-architect", "/api/architectures")
        person_map = await self.call_api("domes-datamap", "/api/person-map", "POST", {"person": production.subject})
        flourishing = await self.call_api("domes-flourishing", "/api/flourishing-index", "POST", {"person": production.subject})

        design = {
            "architecture": architecture,
            "person_map": person_map,
            "flourishing": flourishing
        }

        return StageResult(
            success=True,
            message="Dome design complete. Ready for Production.",
            new_stage=ProductionStage.PRODUCTION,
            progress=40.0,
            data=design
        )

    async def domes_production(self, production: ProductionState, action_data: Dict[str, Any]) -> StageResult:
        contracts = await self.call_api("domes-contracts", "/api/agreements", "POST", {"subject": production.subject})
        final_profile = await self.call_api("domes-profiles", "/api/profiles", "POST", {"name": production.subject})

        build = {
            "contracts": contracts,
            "profile": final_profile
        }

        return StageResult(
            success=True,
            message="Dome built. Ready for Post-Production verification.",
            new_stage=ProductionStage.POST_PRODUCTION,
            progress=60.0,
            data=build
        )

    async def domes_post_production(self, production: ProductionState, action_data: Dict[str, Any]) -> StageResult:
        verification = await self.call_api("domes-brain", "/api/query", "POST",
                                          {"query": f"Verify dome completeness for {production.subject}"})
        innovations = await self.call_api("domes-lab", "/api/generate", "POST",
                                         {"context": f"Dome for {production.subject}"})

        post = {
            "verification": verification,
            "innovations": innovations
        }

        return StageResult(
            success=True,
            message="Post-production complete. Ready for Distribution.",
            new_stage=ProductionStage.DISTRIBUTION,
            progress=80.0,
            data=post
        )

    async def domes_distribution(self, production: ProductionState, action_data: Dict[str, Any]) -> StageResult:
        narrative = await self.call_api("domes-viz", "/api/narrative/sections")
        cosm = self._calculate_cosm(production)
        ip = self._extract_ip(production)
        innovations = self._extract_innovations(production)
        industries = self._assess_industries_changed(production)

        distribution = {
            "narrative": narrative,
            "cosm": cosm.model_dump(),
            "ip": ip,
            "innovations": innovations,
            "industries_changed": industries
        }

        return StageResult(
            success=True,
            message=f"DOME COMPLETE. Total Cosm: {cosm.total:.2f}",
            new_stage=None,
            progress=100.0,
            data=distribution
        )

    async def spheres_development(self, production: ProductionState, action_data: Dict[str, Any]) -> StageResult:
        parcel_id = production.subject
        parcel = await self.call_api("spheres-assets", f"/api/parcels/{parcel_id}")
        permits = await self.call_api("spheres-legal", "/api/permits")

        research = {
            "parcel": parcel.get("parcel", parcel),
            "permits": permits
        }

        return StageResult(
            success=True,
            message=f"Research complete for parcel {parcel_id}. Ready for Pre-Production.",
            new_stage=ProductionStage.PRE_PRODUCTION,
            progress=20.0,
            data=research
        )

    async def spheres_pre_production(self, production: ProductionState, action_data: Dict[str, Any]) -> StageResult:
        studio_data = await self.call_api("spheres-studio", "/api/designs", "POST", {"parcel": production.subject})
        design = studio_data.get("design", studio_data)
        cost = studio_data.get("cost", {})
        timeline = studio_data.get("timeline", {})

        prep = {
            "design": design,
            "cost": cost,
            "timeline": timeline
        }

        return StageResult(
            success=True,
            message="Design complete. Ready for Production.",
            new_stage=ProductionStage.PRODUCTION,
            progress=40.0,
            data=prep
        )

    async def spheres_production(self, production: ProductionState, action_data: Dict[str, Any]) -> StageResult:
        legal_data = await self.call_api("spheres-legal", "/api/permits", "POST", {"parcel": production.subject})
        studio_data = await self.call_api("spheres-studio", "/api/world", "POST", {"parcel": production.subject})

        build = {
            "permits": legal_data,
            "world": studio_data.get("world", studio_data)
        }

        return StageResult(
            success=True,
            message="Sphere built. Ready for Post-Production.",
            new_stage=ProductionStage.POST_PRODUCTION,
            progress=60.0,
            data=build
        )

    async def spheres_post_production(self, production: ProductionState, action_data: Dict[str, Any]) -> StageResult:
        episodes = await self.call_api("spheres-viz", "/api/episodes")
        innovations = await self.call_api("spheres-lab", "/api/generate", "POST",
                                         {"context": f"Sphere at {production.subject}"})
        metrics = await self.call_api("spheres-brain", "/api/metrics", "POST",
                                     {"parcel": production.subject})

        post = {
            "episodes": episodes,
            "innovations": innovations,
            "metrics": metrics.get("metrics", metrics)
        }

        return StageResult(
            success=True,
            message="Post-production complete. Ready for Distribution.",
            new_stage=ProductionStage.DISTRIBUTION,
            progress=80.0,
            data=post
        )

    async def spheres_distribution(self, production: ProductionState, action_data: Dict[str, Any]) -> StageResult:
        metrics = await self.call_api("spheres-brain", "/api/metrics", "POST", {"parcel": production.subject})
        chron = self._calculate_chron(production)
        innovations = self._extract_innovations(production)

        distribution = {
            "metrics": metrics,
            "chron": chron.model_dump(),
            "innovations": innovations
        }

        return StageResult(
            success=True,
            message=f"SPHERE COMPLETE. Total Chron: {chron.total:.2f}",
            new_stage=None,
            progress=100.0,
            data=distribution
        )

    async def advance_stage(self, production: ProductionState, action_data: Dict[str, Any]) -> StageResult:
        game = production.game_type
        stage = production.stage

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

        handler = handlers.get((game, stage))
        if not handler:
            return StageResult(
                success=False,
                message=f"No handler for {game}/{stage}",
                progress=production.progress
            )

        return await handler(production, action_data)

    def _calculate_cosm(self, production: ProductionState) -> CosmDimensions:
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        prod_data = production.stage_data.get("production", {})
        post_data = production.stage_data.get("post_production", {})
        dist_data = production.stage_data.get("distribution", {})

        legal_provisions = dev_data.get("legal_provisions", {})
        legal_score = len(legal_provisions.get("provisions", [])) * 10.0

        data_systems = dev_data.get("data_systems", {})
        data_score = len(data_systems.get("systems", [])) * 12.0

        fiscal_data = prod_data.get("profile", {})
        fiscal_score = 80.0 if fiscal_data else 50.0

        contracts = prod_data.get("contracts", {})
        coord_score = len(contracts.get("agreements", [])) * 15.0

        flourishing_data = pre_data.get("flourishing", {})
        flour_score = flourishing_data.get("index", 75.0)

        narrative = dist_data.get("narrative", {})
        narrative_score = len(narrative.get("sections", [])) * 18.0

        return CosmDimensions(
            legal=min(legal_score, 100.0),
            data=min(data_score, 100.0),
            fiscal=min(fiscal_score, 100.0),
            coordination=min(coord_score, 100.0),
            flourishing=min(flour_score, 100.0),
            narrative=min(narrative_score, 100.0)
        )

    def _calculate_chron(self, production: ProductionState) -> ChronDimensions:
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        prod_data = production.stage_data.get("production", {})
        post_data = production.stage_data.get("post_production", {})

        parcel = dev_data.get("parcel", {})
        unlock_m2 = parcel.get("area_sqm", 500.0)

        design = pre_data.get("design", {})
        access_hrs = design.get("access_hours", 360.0)

        timeline = pre_data.get("timeline", {})
        permanence = timeline.get("duration_years", 1.0) / 10.0

        metrics = post_data.get("metrics", {})
        catalyst = min(metrics.get("connected_projects", 0) / 10.0, 1.0)

        permits = prod_data.get("permits", {})
        policy = len(permits.get("policy_changes", [])) / 5.0

        return ChronDimensions(
            unlock=unlock_m2,
            access=access_hrs,
            permanence=min(permanence, 1.0),
            catalyst=catalyst,
            policy=min(policy, 1.0)
        )

    def _extract_ip(self, production: ProductionState) -> List[str]:
        ip_list = []
        post_data = production.stage_data.get("post_production", {})
        innovations = post_data.get("innovations", {})
        ip_list.extend(innovations.get("patents", []))
        ip_list.extend(innovations.get("protocols", []))

        dist_data = production.stage_data.get("distribution", {})
        narrative = dist_data.get("narrative", {})
        for section in narrative.get("sections", []):
            if "patent" in section.get("content", "").lower():
                ip_list.append(section.get("title", "Unnamed IP"))

        return ip_list if ip_list else ["Generated IP (placeholder)"]

    def _extract_innovations(self, production: ProductionState) -> List[str]:
        post_data = production.stage_data.get("post_production", {})
        innovations = post_data.get("innovations", {})
        return innovations.get("innovations", [])

    def _assess_industries_changed(self, production: ProductionState) -> List[str]:
        industries = set()
        dev_data = production.stage_data.get("development", {})
        legal_provisions = dev_data.get("legal_provisions", {})
        for prov in legal_provisions.get("provisions", []):
            domain = prov.get("domain", "").lower()
            if "insurance" in domain:
                industries.add("Insurance")
            if "health" in domain:
                industries.add("Healthcare")
            if "finance" in domain:
                industries.add("Finance")
            if "data" in domain:
                industries.add("Data Privacy")

        prod_data = production.stage_data.get("production", {})
        contracts = prod_data.get("contracts", {})
        for contract in contracts.get("agreements", []):
            if "government" in contract.get("type", "").lower():
                industries.add("Government Contracting")

        return list(industries) if industries else ["Unspecified Industry Impact"]
