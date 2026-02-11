import json
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, func
from app.database import Base


class CoordinationModel(Base):
    """Known coordination model archetypes (ACO, Health Home, PACE, etc.)"""
    __tablename__ = "coordination_models"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    abbreviation = Column(String(20))
    category = Column(String(100))  # managed_care, community_based, hybrid, specialized
    description = Column(Text)
    target_population = Column(Text)  # JSON list
    domains_covered = Column(Text)  # JSON list of domain keys
    authority_type = Column(String(100))  # federal_waiver, state_plan, local_agreement, contractual
    funding_sources = Column(Text)  # JSON list
    typical_budget_range = Column(Text)  # JSON: {min, max, unit}
    staffing_model = Column(Text)  # JSON: roles and ratios
    governance_structure = Column(Text)
    key_features = Column(Text)  # JSON list
    limitations = Column(Text)  # JSON list
    evidence_rating = Column(String(50))  # strong, moderate, emerging, limited
    example_sites = Column(Text)  # JSON list
    regulatory_requirements = Column(Text)  # JSON list
    timeline_to_launch = Column(String(100))  # e.g. "12-18 months"
    political_feasibility = Column(String(50))  # high, moderate, low, contentious
    created_at = Column(DateTime, server_default=func.now())

    def _dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "abbreviation": self.abbreviation,
            "category": self.category,
            "description": self.description,
            "target_population": json.loads(self.target_population or "[]"),
            "domains_covered": json.loads(self.domains_covered or "[]"),
            "authority_type": self.authority_type,
            "funding_sources": json.loads(self.funding_sources or "[]"),
            "typical_budget_range": json.loads(self.typical_budget_range or "{}"),
            "staffing_model": json.loads(self.staffing_model or "{}"),
            "governance_structure": self.governance_structure,
            "key_features": json.loads(self.key_features or "[]"),
            "limitations": json.loads(self.limitations or "[]"),
            "evidence_rating": self.evidence_rating,
            "example_sites": json.loads(self.example_sites or "[]"),
            "regulatory_requirements": json.loads(self.regulatory_requirements or "[]"),
            "timeline_to_launch": self.timeline_to_launch,
            "political_feasibility": self.political_feasibility,
        }


class Architecture(Base):
    """A designed coordination architecture (user-created or generated)"""
    __tablename__ = "architectures"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="draft")  # draft, analysis, approved, implementing
    population_size = Column(Integer)
    population_description = Column(Text)
    annual_budget = Column(Float)
    geography = Column(String(200))
    political_context = Column(String(100))  # supportive, neutral, resistant, hostile
    time_horizon = Column(String(50))  # 1yr, 3yr, 5yr
    primary_model_id = Column(Integer)
    hybrid_model_ids = Column(Text)  # JSON list of model IDs
    model_rationale = Column(Text)
    domains_targeted = Column(Text)  # JSON list
    constraints = Column(Text)  # JSON: {regulatory, political, budget, workforce}
    scores = Column(Text)  # JSON: {coverage, feasibility, cost_efficiency, speed, sustainability}
    implementation_phases = Column(Text)  # JSON list of phases
    stakeholders = Column(Text)  # JSON list
    budget_breakdown = Column(Text)  # JSON
    risks = Column(Text)  # JSON list
    workforce_plan = Column(Text)  # JSON
    authority_map = Column(Text)  # JSON: what authority needed from whom
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def _dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "population_size": self.population_size,
            "population_description": self.population_description,
            "annual_budget": self.annual_budget,
            "geography": self.geography,
            "political_context": self.political_context,
            "time_horizon": self.time_horizon,
            "primary_model_id": self.primary_model_id,
            "hybrid_model_ids": json.loads(self.hybrid_model_ids or "[]"),
            "model_rationale": self.model_rationale,
            "domains_targeted": json.loads(self.domains_targeted or "[]"),
            "constraints": json.loads(self.constraints or "{}"),
            "scores": json.loads(self.scores or "{}"),
            "implementation_phases": json.loads(self.implementation_phases or "[]"),
            "stakeholders": json.loads(self.stakeholders or "[]"),
            "budget_breakdown": json.loads(self.budget_breakdown or "{}"),
            "risks": json.loads(self.risks or "[]"),
            "workforce_plan": json.loads(self.workforce_plan or "{}"),
            "authority_map": json.loads(self.authority_map or "{}"),
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None,
        }


class ComparisonSet(Base):
    """Side-by-side comparison of multiple architectures"""
    __tablename__ = "comparison_sets"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    architecture_ids = Column(Text)  # JSON list
    winner_id = Column(Integer, nullable=True)
    comparison_notes = Column(Text)  # JSON: dimension -> notes
    created_at = Column(DateTime, server_default=func.now())

    def _dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "architecture_ids": json.loads(self.architecture_ids or "[]"),
            "winner_id": self.winner_id,
            "comparison_notes": json.loads(self.comparison_notes or "{}"),
            "created_at": str(self.created_at) if self.created_at else None,
        }
