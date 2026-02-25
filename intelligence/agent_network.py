"""
BATHS Intelligence — Agent Network Architecture

This defines how multiple AI agents coordinate on complex BATHS tasks.
Not a theoretical framework — a working coordination system that can be
used NOW with single-agent implementations and SCALE as multi-agent
capabilities mature.

Architecture:
- Each production capability (legal_navigation, activation_design, etc.)
  maps to a specialist agent type
- Agents communicate through a shared task graph
- The orchestrator decomposes production stages into agent-sized tasks
- Agents can request work from other agents (legal agent asks economics
  agent for cost data)
- All agent outputs feed into the memory system

The agent network starts simple (one LLM call per agent task) and scales
toward true multi-agent coordination as the frontier matures.
"""

from typing import List, Dict, Optional, Any
from datetime import datetime

from intelligence.models import (
    AgentCapabilityProfile, AgentTask,
)


# ── Agent Type Registry ─────────────────────────────────────────

DOME_AGENTS = {
    "legal_navigator": AgentCapabilityProfile(
        agent_type="legal_navigator",
        description=(
            "Navigates legal entitlement landscapes. Maps eligibility, "
            "application pathways, deadlines, and inter-system conflicts. "
            "Produces legal landscape maps, coordination blueprints, and "
            "policy briefs."
        ),
        tool_access=[
            "legal_database_search", "government_portal_navigation",
            "eligibility_checker", "deadline_tracker",
        ],
        data_access=[
            "character_brief", "key_systems", "prior_dome_learnings",
            "person_world_model",
        ],
        output_types=[
            "legal_landscape_map", "coordination_blueprint",
            "policy_brief", "stress_test_report",
        ],
    ),
    "systems_analyst": AgentCapabilityProfile(
        agent_type="systems_analyst",
        description=(
            "Models government system interactions, fragmentation costs, "
            "and coordination economics. Produces fragmentation indexes, "
            "cost models, bond structures, and digital twins."
        ),
        tool_access=[
            "cost_modeling", "simulation_engine", "data_analysis",
            "financial_modeling",
        ],
        data_access=[
            "character_brief", "legal_landscape_map", "prior_cost_data",
            "person_world_model",
        ],
        output_types=[
            "fragmentation_model", "cost_comparison", "bond_structure",
            "digital_twin", "coordination_model",
        ],
        requires_agents=["legal_navigator"],
    ),
    "narrative_producer": AgentCapabilityProfile(
        agent_type="narrative_producer",
        description=(
            "Creates the documentary treatment, production narrative, and "
            "final cut plans. Ensures the dome story is told with dignity, "
            "not as a rescue narrative."
        ),
        tool_access=[
            "documentary_framework", "narrative_structure",
            "media_production",
        ],
        data_access=[
            "character_brief", "all_stage_deliverables",
            "prior_dome_narratives",
        ],
        output_types=[
            "documentary_treatment", "narrative_framework",
            "first_cut_plan", "final_cut", "premiere_package",
        ],
    ),
    "flourishing_designer": AgentCapabilityProfile(
        agent_type="flourishing_designer",
        description=(
            "Designs the dome environment — every system, transition, and "
            "threshold designed for dignity and flourishing. Integrates awe "
            "design principles. Measures outcomes."
        ),
        tool_access=[
            "flourishing_framework", "awe_design_toolkit",
            "impact_measurement",
        ],
        data_access=[
            "character_brief", "legal_landscape_map", "cost_model",
            "person_world_model", "prior_awe_data",
        ],
        output_types=[
            "flourishing_assessment", "dome_architecture",
            "design_package", "impact_assessment",
        ],
        requires_agents=["legal_navigator", "systems_analyst"],
    ),
}

SPHERE_AGENTS = {
    "parcel_analyst": AgentCapabilityProfile(
        agent_type="parcel_analyst",
        description=(
            "Reads parcels — zoning, permits, regulatory landscape, "
            "environmental conditions. Produces legal analyses, permit "
            "pathway maps, and implementation plans."
        ),
        tool_access=[
            "zoning_database", "permit_portal", "gis_data",
            "environmental_assessment",
        ],
        data_access=[
            "parcel_brief", "constraints", "prior_sphere_learnings",
            "place_world_model",
        ],
        output_types=[
            "parcel_legal_analysis", "permit_pathway_map",
            "implementation_plan", "regulatory_lessons",
        ],
    ),
    "awe_designer": AgentCapabilityProfile(
        agent_type="awe_designer",
        description=(
            "Designs sphere activations using Keltner's 8 awe elicitors. "
            "Maps triggers to specific design elements with site rationale. "
            "Produces awe assessments, design frameworks, activation programs, "
            "and impact measurements."
        ),
        tool_access=[
            "awe_framework", "site_analysis", "design_tools",
            "measurement_protocols",
        ],
        data_access=[
            "parcel_brief", "parcel_legal_analysis", "community_context",
            "place_world_model", "prior_awe_data",
        ],
        output_types=[
            "awe_assessment", "awe_design_framework",
            "activation_program", "awe_impact_assessment",
        ],
        requires_agents=["parcel_analyst"],
    ),
    "activation_economist": AgentCapabilityProfile(
        agent_type="activation_economist",
        description=(
            "Models the economics of space activation — vacancy costs, "
            "activation benefits, community investment vehicles, and "
            "economic impact measurement."
        ),
        tool_access=[
            "economic_modeling", "property_data", "community_impact_analysis",
            "financial_structuring",
        ],
        data_access=[
            "parcel_brief", "parcel_legal_analysis",
            "place_world_model", "prior_economic_data",
        ],
        output_types=[
            "economics_baseline", "community_benefit_model",
            "investment_instrument", "economic_impact_report",
        ],
        requires_agents=["parcel_analyst"],
    ),
    "sphere_narrator": AgentCapabilityProfile(
        agent_type="sphere_narrator",
        description=(
            "Documents the community story and activation narrative. "
            "Archives oral histories. Produces documentaries that position "
            "the community as directors, not subjects."
        ),
        tool_access=[
            "documentary_framework", "oral_history_archive",
            "community_engagement",
        ],
        data_access=[
            "parcel_brief", "community_context",
            "all_stage_deliverables", "prior_sphere_narratives",
        ],
        output_types=[
            "community_story_archive", "narrative_plan",
            "production_documentary", "premiere_package",
        ],
    ),
}

# Cross-game agents that serve both domes and spheres
SHARED_AGENTS = {
    "memory_analyst": AgentCapabilityProfile(
        agent_type="memory_analyst",
        description=(
            "Queries the cross-project memory system for relevant learnings. "
            "Produces intelligence briefings that inform every stage of "
            "production. The bridge between past projects and current ones."
        ),
        tool_access=["memory_query", "learning_analysis"],
        data_access=[
            "project_memory_store", "person_world_model", "place_world_model",
        ],
        output_types=[
            "intelligence_briefing", "relevant_learnings",
            "corroboration_report", "pattern_alert",
        ],
    ),
    "frontier_scout": AgentCapabilityProfile(
        agent_type="frontier_scout",
        description=(
            "Monitors the frontier research map for capabilities that are "
            "approaching maturity transitions. Recommends integration "
            "priorities. Flags convergence zone activity."
        ),
        tool_access=["frontier_tracker", "research_search", "paper_analysis"],
        data_access=["frontier_map", "project_memory_store"],
        output_types=[
            "research_brief", "integration_recommendation",
            "convergence_alert", "maturity_update",
        ],
    ),
    "unlikely_collision_detector": AgentCapabilityProfile(
        agent_type="unlikely_collision_detector",
        description=(
            "Identifies unexpected connections between practitioner practices "
            "and project needs. Uses the memory system to find patterns of "
            "practices that produced surprising IP in prior productions."
        ),
        tool_access=["pattern_analysis", "body_of_work_analysis"],
        data_access=[
            "roster", "project_brief", "project_memory_store",
            "prior_unlikely_collisions",
        ],
        output_types=[
            "collision_prediction", "practice_mapping",
            "unexpected_ip_forecast",
        ],
    ),
}


class AgentOrchestrator:
    """
    Coordinates agent tasks for a production stage.

    The orchestrator:
    1. Takes a production stage and its requirements
    2. Decomposes it into agent-sized tasks
    3. Resolves dependencies (legal before economics, etc.)
    4. Dispatches tasks to appropriate agents
    5. Collects and synthesizes results
    6. Feeds everything into the memory system

    Currently implements a sequential execution model.
    Designed to scale to parallel multi-agent execution
    as the infrastructure matures.
    """

    def __init__(self):
        self.task_graph: Dict[str, AgentTask] = {}
        self.execution_log: List[Dict] = []

    def plan_stage_execution(
        self,
        game_type: str,
        stage: str,
        project_context: Dict[str, Any],
        available_intelligence: Dict[str, Any],
    ) -> List[AgentTask]:
        """
        Plan the agent task graph for a production stage.

        Returns an ordered list of tasks respecting dependencies.
        """
        agent_registry = DOME_AGENTS if game_type == "domes" else SPHERE_AGENTS
        tasks = []

        # Phase 0: Memory analysis (always first)
        memory_task = AgentTask(
            agent_type="memory_analyst",
            task_description=(
                f"Query the memory system for all learnings relevant to this "
                f"{game_type} project at the {stage} stage. Produce an intelligence "
                f"briefing that informs all subsequent agent work."
            ),
            input_data={
                "game_type": game_type,
                "stage": stage,
                "project_context": project_context,
            },
        )
        tasks.append(memory_task)

        # Phase 1: Foundation agents (no inter-agent dependencies)
        foundation_agents = [
            agent_type for agent_type, profile in agent_registry.items()
            if not profile.requires_agents
        ]
        for agent_type in foundation_agents:
            profile = agent_registry[agent_type]
            task = AgentTask(
                agent_type=agent_type,
                task_description=(
                    f"Execute {agent_type} work for the {stage} stage. "
                    f"{profile.description}"
                ),
                input_data={
                    "project_context": project_context,
                    "intelligence_briefing": "from memory_analyst",
                    "stage": stage,
                },
                parent_task_id=memory_task.task_id,
            )
            memory_task.child_task_ids.append(task.task_id)
            tasks.append(task)

        # Phase 2: Dependent agents
        dependent_agents = [
            (agent_type, profile)
            for agent_type, profile in agent_registry.items()
            if profile.requires_agents
        ]
        for agent_type, profile in dependent_agents:
            # Find parent tasks
            parent_ids = []
            for required in profile.requires_agents:
                parent_task = next(
                    (t for t in tasks if t.agent_type == required), None
                )
                if parent_task:
                    parent_ids.append(parent_task.task_id)

            task = AgentTask(
                agent_type=agent_type,
                task_description=(
                    f"Execute {agent_type} work for the {stage} stage, "
                    f"building on outputs from {', '.join(profile.requires_agents)}. "
                    f"{profile.description}"
                ),
                input_data={
                    "project_context": project_context,
                    "intelligence_briefing": "from memory_analyst",
                    "prerequisite_outputs": f"from {', '.join(profile.requires_agents)}",
                    "stage": stage,
                },
            )
            if parent_ids:
                task.parent_task_id = parent_ids[0]
            tasks.append(task)

        # Store in task graph
        for task in tasks:
            self.task_graph[task.task_id] = task

        return tasks

    def get_execution_order(self, tasks: List[AgentTask]) -> List[List[AgentTask]]:
        """
        Return tasks grouped by execution phase.
        Tasks within a phase can run in parallel.
        Tasks across phases must be sequential.
        """
        # Phase 0: Memory analyst
        phase_0 = [t for t in tasks if t.agent_type == "memory_analyst"]

        # Phase 1: Foundation agents (no dependencies beyond memory)
        phase_1 = [
            t for t in tasks
            if t.agent_type != "memory_analyst"
            and t.parent_task_id in [p.task_id for p in phase_0]
        ]

        # Phase 2: Dependent agents
        phase_2 = [
            t for t in tasks
            if t not in phase_0 and t not in phase_1
        ]

        phases = [phase_0]
        if phase_1:
            phases.append(phase_1)
        if phase_2:
            phases.append(phase_2)

        return phases

    def record_execution(
        self,
        task: AgentTask,
        output: Dict[str, Any],
        duration_ms: int = 0,
    ) -> None:
        """Record that a task was executed and its output."""
        task.output_data = output
        task.status = "completed"
        task.completed_at = datetime.utcnow()

        self.execution_log.append({
            "task_id": task.task_id,
            "agent_type": task.agent_type,
            "status": "completed",
            "duration_ms": duration_ms,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def get_agent_profile(
        self,
        agent_type: str,
        game_type: Optional[str] = None,
    ) -> Optional[AgentCapabilityProfile]:
        """Look up an agent's capability profile."""
        if agent_type in SHARED_AGENTS:
            return SHARED_AGENTS[agent_type]
        if game_type == "domes" and agent_type in DOME_AGENTS:
            return DOME_AGENTS[agent_type]
        if game_type == "spheres" and agent_type in SPHERE_AGENTS:
            return SPHERE_AGENTS[agent_type]
        # Search all registries
        for registry in [DOME_AGENTS, SPHERE_AGENTS, SHARED_AGENTS]:
            if agent_type in registry:
                return registry[agent_type]
        return None

    def list_available_agents(
        self,
        game_type: Optional[str] = None,
    ) -> List[Dict]:
        """List all available agent types and their capabilities."""
        agents = []
        registries = [SHARED_AGENTS]
        if game_type == "domes" or game_type is None:
            registries.append(DOME_AGENTS)
        if game_type == "spheres" or game_type is None:
            registries.append(SPHERE_AGENTS)

        for registry in registries:
            for agent_type, profile in registry.items():
                agents.append({
                    "agent_type": agent_type,
                    "description": profile.description,
                    "outputs": profile.output_types,
                    "requires": profile.requires_agents,
                    "tasks_completed": profile.tasks_completed,
                })

        return agents

    def execution_summary(self) -> Dict:
        """Summarize all agent execution history."""
        if not self.execution_log:
            return {"total_tasks": 0}

        by_agent = {}
        for entry in self.execution_log:
            agent = entry["agent_type"]
            if agent not in by_agent:
                by_agent[agent] = {"count": 0, "total_ms": 0}
            by_agent[agent]["count"] += 1
            by_agent[agent]["total_ms"] += entry.get("duration_ms", 0)

        return {
            "total_tasks": len(self.execution_log),
            "by_agent_type": by_agent,
            "task_graph_size": len(self.task_graph),
        }
