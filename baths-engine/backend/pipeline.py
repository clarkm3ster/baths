"""
BATHS Game Engine - Production Pipeline Director
Orchestrates player through Development → Pre → Prod → Post → Distribution
"""

import httpx
from typing import Dict, Any, List, Optional
from models import (
    GameType, ProductionStage, ProductionState, StageResult,
    CosmDimensions, ChronDimensions
)


class PipelineDirector:
    """
    Orchestrates production stages and API calls
    """
    
    def __init__(self, api_registry: Dict[str, Any]):
        self.api_registry = api_registry
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def call_api(self, service_name: str, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict[str, Any]:
        """Call a backend API service"""
        game_type = "domes" if service_name.startswith("domes") else "spheres"
        service = self.api_registry[game_type].get(service_name)
        
        if not service:
            raise ValueError(f"Service {service_name} not found in registry")
        
        port = service["port"]
        url = f"http://localhost:{port}{endpoint}"
        
        if method == "GET":
            response = await self.client.get(url)
        elif method == "POST":
            response = await self.client.post(url, json=data or {})
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return response.json()
    
    # ========== DOMES PIPELINE ==========
    
    async def domes_development(self, production: ProductionState, action_data: Dict[str, Any]) -> StageResult:
        """
        DOMES Development: Research subject, identify needs
        APIs: domes-profile-research, domes-data-research, domes-legal
        """
        subject = production.subject
        
        # Call research APIs
        profile_data = await self.call_api("domes-profile-research", f"/api/profiles?name={subject}")
        data_systems = await self.call_api("domes-data-research", "/api/systems")
        legal_provisions = await self.call_api("domes-legal", "/api/provisions")
        
        # Store research in stage_data
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
        """
        DOMES Pre-Production: Design dome architecture, map systems
        APIs: domes-architect, domes-datamap, domes-flourishing
        """
        # Design dome architecture
        architecture = await self.call_api("domes-architect", "/api/architectures")
        
        # Map data systems
        person_map = await self.call_api("domes-datamap", "/api/person-map", "POST", 
                                         {"person": production.subject})
        
        # Assess flourishing dimensions
        flourishing = await self.call_api("domes-flourishing", "/api/flourishing-index", "POST",
                                         {"person": production.subject})
        
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
        """
        DOMES Production: Execute contracts, build the dome
        APIs: domes-contracts, domes-profiles
        """
        # Execute contracts
        contracts = await self.call_api("domes-contracts", "/api/agreements", "POST",
                                       {"subject": production.subject})
        
        # Finalize profile
        final_profile = await self.call_api("domes-profiles", "/api/profiles", "POST",
                                           {"name": production.subject})
        
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
        """
        DOMES Post-Production: Verify completeness, generate innovations
        APIs: domes-brain, domes-lab
        """
        # Verify with brain
        verification = await self.call_api("domes-brain", "/api/query", "POST",
                                          {"query": f"Verify dome completeness for {production.subject}"})
        
        # Generate innovations
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
        """
        DOMES Distribution: Package story, calculate Cosm, measure impact
        APIs: domes-viz
        """
        # Generate narrative
        narrative = await self.call_api("domes-viz", "/api/narrative/sections")
        
        # Calculate Cosm dimensions (from accumulated stage data)
        cosm = self._calculate_cosm(production)
        
        # Package IP and innovations
        ip = self._extract_ip(production)
        innovations = self._extract_innovations(production)
        industries = self._assess_industries_changed(production)
        
        distribution = {
            "narrative": narrative,
            "cosm": cosm.dict(),
            "ip": ip,
            "innovations": innovations,
            "industries_changed": industries
        }
        
        return StageResult(
            success=True,
            message=f"DOME COMPLETE. Total Cosm: {cosm.total:.2f}",
            new_stage=None,  # Production finished
            progress=100.0,
            data=distribution
        )
    
    # ========== SPHERES PIPELINE ==========
    
    async def spheres_development(self, production: ProductionState, action_data: Dict[str, Any]) -> StageResult:
        """
        SPHERES Development: Identify parcels, research legal
        APIs: spheres-assets, spheres-legal
        """
        parcel_id = production.subject
        
        # Get parcel data
        parcel = await self.call_api("spheres-assets", f"/api/parcels/{parcel_id}")
        
        # Research permits
        permits = await self.call_api("spheres-legal", "/api/permits")
        
        research = {
            "parcel": parcel,
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
        """
        SPHERES Pre-Production: Design activation, model cost/timeline
        APIs: spheres-studio
        """
        # Design activation
        design = await self.call_api("spheres-studio", "/api/designs", "POST",
                                    {"parcel": production.subject})
        
        # Model cost
        cost = await self.call_api("spheres-studio", "/api/cost", "POST",
                                  {"design_id": design.get("id")})
        
        # Timeline
        timeline = await self.call_api("spheres-studio", "/api/timeline", "POST",
                                      {"design_id": design.get("id")})
        
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
        """
        SPHERES Production: Execute permits, build sphere
        APIs: spheres-legal, spheres-studio
        """
        # Execute permits
        executed_permits = await self.call_api("spheres-legal", "/api/permits", "POST",
                                              {"parcel": production.subject})
        
        # Build world
        world = await self.call_api("spheres-studio", "/api/world", "POST",
                                   {"parcel": production.subject})
        
        build = {
            "permits": executed_permits,
            "world": world
        }
        
        return StageResult(
            success=True,
            message="Sphere built. Ready for Post-Production.",
            new_stage=ProductionStage.POST_PRODUCTION,
            progress=60.0,
            data=build
        )
    
    async def spheres_post_production(self, production: ProductionState, action_data: Dict[str, Any]) -> StageResult:
        """
        SPHERES Post-Production: Document episodes, generate innovations
        APIs: spheres-viz, spheres-lab
        """
        # Capture episodes
        episodes = await self.call_api("spheres-viz", "/api/episodes")
        
        # Generate innovations
        innovations = await self.call_api("spheres-lab", "/api/generate", "POST",
                                         {"context": f"Sphere at {production.subject}"})
        
        post = {
            "episodes": episodes,
            "innovations": innovations
        }
        
        return StageResult(
            success=True,
            message="Post-production complete. Ready for Distribution.",
            new_stage=ProductionStage.DISTRIBUTION,
            progress=80.0,
            data=post
        )
    
    async def spheres_distribution(self, production: ProductionState, action_data: Dict[str, Any]) -> StageResult:
        """
        SPHERES Distribution: Calculate Chron, measure impact
        APIs: spheres-brain
        """
        # Query metrics
        metrics = await self.call_api("spheres-brain", "/api/metrics", "POST",
                                     {"parcel": production.subject})
        
        # Calculate Chron dimensions
        chron = self._calculate_chron(production)
        
        # Extract innovations
        innovations = self._extract_innovations(production)
        
        distribution = {
            "metrics": metrics,
            "chron": chron.dict(),
            "innovations": innovations
        }
        
        return StageResult(
            success=True,
            message=f"SPHERE COMPLETE. Total Chron: {chron.total:.2f}",
            new_stage=None,
            progress=100.0,
            data=distribution
        )
    
    # ========== ROUTING ==========
    
    async def advance_stage(self, production: ProductionState, action_data: Dict[str, Any]) -> StageResult:
        """Route to appropriate stage handler"""
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
    
    # ========== SCORING ==========
    
    def _calculate_cosm(self, production: ProductionState) -> CosmDimensions:
        """Calculate COSM dimensions from production data"""
        # Extract scores from accumulated stage data
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        prod_data = production.stage_data.get("production", {})
        post_data = production.stage_data.get("post_production", {})
        dist_data = production.stage_data.get("distribution", {})
        
        # Legal Cosm: count of legal provisions matched
        legal_provisions = dev_data.get("legal_provisions", {})
        legal_score = len(legal_provisions.get("provisions", [])) * 10.0
        
        # Data Cosm: count of data systems connected
        data_systems = dev_data.get("data_systems", {})
        data_score = len(data_systems.get("systems", [])) * 12.0
        
        # Fiscal Cosm: cost model completeness
        fiscal_data = prod_data.get("profile", {})
        fiscal_score = 80.0 if fiscal_data else 50.0
        
        # Coordination Cosm: contracts executed
        contracts = prod_data.get("contracts", {})
        coord_score = len(contracts.get("agreements", [])) * 15.0
        
        # Flourishing Cosm: flourishing index
        flourishing_data = pre_data.get("flourishing", {})
        flour_score = flourishing_data.get("index", 75.0)
        
        # Narrative Cosm: narrative sections generated
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
        """Calculate CHRON dimensions from production data"""
        dev_data = production.stage_data.get("development", {})
        pre_data = production.stage_data.get("pre_production", {})
        prod_data = production.stage_data.get("production", {})
        post_data = production.stage_data.get("post_production", {})
        
        # Unlock Chron: square meters from parcel data
        parcel = dev_data.get("parcel", {})
        unlock_m2 = parcel.get("area_sqm", 500.0)
        
        # Access Chron: estimated public access hours
        design = pre_data.get("design", {})
        access_hrs = design.get("access_hours", 360.0)
        
        # Permanence: duration multiplier from timeline
        timeline = pre_data.get("timeline", {})
        permanence = timeline.get("duration_years", 1.0) / 10.0  # normalized to 0-1
        
        # Catalyst: ripple effects (count of connected projects)
        metrics = post_data.get("metrics", {})
        catalyst = min(metrics.get("connected_projects", 0) / 10.0, 1.0)
        
        # Policy: policy changes unlocked
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
        """Extract IP created during production"""
        ip_list = []
        
        # Extract from innovations
        post_data = production.stage_data.get("post_production", {})
        innovations = post_data.get("innovations", {})
        ip_list.extend(innovations.get("patents", []))
        ip_list.extend(innovations.get("protocols", []))
        
        # Extract from narrative
        dist_data = production.stage_data.get("distribution", {})
        narrative = dist_data.get("narrative", {})
        for section in narrative.get("sections", []):
            if "patent" in section.get("content", "").lower():
                ip_list.append(section.get("title", "Unnamed IP"))
        
        return ip_list if ip_list else ["Generated IP (placeholder)"]
    
    def _extract_innovations(self, production: ProductionState) -> List[str]:
        """Extract innovations from lab outputs"""
        post_data = production.stage_data.get("post_production", {})
        innovations = post_data.get("innovations", {})
        return innovations.get("innovations", [])
    
    def _assess_industries_changed(self, production: ProductionState) -> List[str]:
        """Assess which industries were fundamentally changed"""
        industries = set()
        
        # Analyze legal provisions for industry impact
        dev_data = production.stage_data.get("development", {})
        legal_provisions = dev_data.get("legal_provisions", {})
        for prov in legal_provisions.get("provisions", []):
            if "insurance" in prov.get("domain", "").lower():
                industries.add("Insurance")
            if "health" in prov.get("domain", "").lower():
                industries.add("Healthcare")
            if "finance" in prov.get("domain", "").lower():
                industries.add("Finance")
            if "data" in prov.get("domain", "").lower():
                industries.add("Data Privacy")
        
        # Analyze contracts for industry scope
        prod_data = production.stage_data.get("production", {})
        contracts = prod_data.get("contracts", {})
        for contract in contracts.get("agreements", []):
            if "government" in contract.get("type", "").lower():
                industries.add("Government Contracting")
        
        return list(industries) if industries else ["Unspecified Industry Impact"]
