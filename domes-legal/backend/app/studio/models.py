"""SQLAlchemy ORM models for the Dome Studio (Showrunner Layer)."""
import json
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey
from app.database import Base


class StudioCharacter(Base):
    __tablename__ = "studio_characters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(Text, nullable=False, unique=True, index=True)
    character_type = Column(Text, nullable=False)
    name_or_alias = Column(Text, nullable=False)
    consent_tier = Column(Text, nullable=False)
    fictionalization_rules = Column(Text, default="{}")
    circumstances_summary = Column(Text, default="")
    initial_conditions = Column(Text, default="{}")
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "character_id": self.character_id,
            "character_type": self.character_type,
            "name_or_alias": self.name_or_alias,
            "consent_tier": self.consent_tier,
            "fictionalization_rules": json.loads(self.fictionalization_rules or "{}"),
            "circumstances_summary": self.circumstances_summary,
            "initial_conditions": json.loads(self.initial_conditions or "{}"),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class StudioProduction(Base):
    __tablename__ = "studio_productions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    production_id = Column(Text, nullable=False, unique=True, index=True)
    title = Column(Text, nullable=False)
    medium = Column(Text, nullable=False)
    character_id = Column(Text, ForeignKey("studio_characters.character_id"), nullable=False, index=True)
    stage = Column(Text, nullable=False, default="greenlit")
    budget_total = Column(Float, default=0.0)
    financing_sources = Column(Text, default="[]")
    generated_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "production_id": self.production_id,
            "title": self.title,
            "medium": self.medium,
            "character_id": self.character_id,
            "stage": self.stage,
            "budget_total": self.budget_total,
            "financing_sources": json.loads(self.financing_sources or "[]"),
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }


class StudioProductionStage(Base):
    __tablename__ = "studio_production_stages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    production_id = Column(Text, ForeignKey("studio_productions.production_id"), nullable=False, index=True)
    stage = Column(Text, nullable=False)
    start_date = Column(Text)
    end_date = Column(Text)
    cost_cap = Column(Float, default=0.0)
    deliverables = Column(Text, default="[]")
    risk_register = Column(Text, default="[]")

    def to_dict(self):
        return {
            "production_id": self.production_id,
            "stage": self.stage,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "cost_cap": self.cost_cap,
            "deliverables": json.loads(self.deliverables or "[]"),
            "risk_register": json.loads(self.risk_register or "[]"),
        }


class StudioTalentRole(Base):
    __tablename__ = "studio_talent_roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    production_id = Column(Text, ForeignKey("studio_productions.production_id"), nullable=False, index=True)
    person_or_entity = Column(Text, nullable=False)
    role = Column(Text, nullable=False)
    rate_type = Column(Text, nullable=False)
    rate = Column(Float, default=0.0)

    def to_dict(self):
        return {
            "production_id": self.production_id,
            "person_or_entity": self.person_or_entity,
            "role": self.role,
            "rate_type": self.rate_type,
            "rate": self.rate,
        }


class StudioGap(Base):
    __tablename__ = "studio_gaps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    gap_id = Column(Text, nullable=False, unique=True, index=True)
    production_id = Column(Text, ForeignKey("studio_productions.production_id"), nullable=False, index=True)
    character_id = Column(Text, ForeignKey("studio_characters.character_id"), nullable=False, index=True)
    discovered_at = Column(DateTime, default=datetime.utcnow)
    area = Column(Text, nullable=False, index=True)
    severity = Column(Text, nullable=False, index=True)
    description = Column(Text, nullable=False)
    reproduction_steps = Column(Text, default="[]")
    proposed_fix = Column(Text)
    owner_module = Column(Text, index=True)
    status = Column(Text, nullable=False, default="new")

    def to_dict(self):
        return {
            "gap_id": self.gap_id,
            "production_id": self.production_id,
            "character_id": self.character_id,
            "discovered_at": self.discovered_at.isoformat() if self.discovered_at else None,
            "area": self.area,
            "severity": self.severity,
            "description": self.description,
            "reproduction_steps": json.loads(self.reproduction_steps or "[]"),
            "proposed_fix": self.proposed_fix,
            "owner_module": self.owner_module,
            "status": self.status,
        }


class StudioIPAsset(Base):
    __tablename__ = "studio_ip_assets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Text, nullable=False, unique=True, index=True)
    production_id = Column(Text, ForeignKey("studio_productions.production_id"), nullable=False, index=True)
    asset_type = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    storage_uri = Column(Text)
    contributors = Column(Text, default="[]")
    rights = Column(Text, default="{}")
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "asset_id": self.asset_id,
            "production_id": self.production_id,
            "asset_type": self.asset_type,
            "title": self.title,
            "storage_uri": self.storage_uri,
            "contributors": json.loads(self.contributors or "[]"),
            "rights": json.loads(self.rights or "{}"),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class StudioLearningPackage(Base):
    __tablename__ = "studio_learning_packages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    learning_id = Column(Text, nullable=False, unique=True, index=True)
    production_id = Column(Text, ForeignKey("studio_productions.production_id"), nullable=False, index=True)
    summary = Column(Text, nullable=False)
    gap_ids = Column(Text, default="[]")
    proposed_os_changes = Column(Text, default="[]")
    validation_needed = Column(Text, default="[]")
    generated_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "learning_id": self.learning_id,
            "production_id": self.production_id,
            "summary": self.summary,
            "gap_ids": json.loads(self.gap_ids or "[]"),
            "proposed_os_changes": json.loads(self.proposed_os_changes or "[]"),
            "validation_needed": json.loads(self.validation_needed or "[]"),
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }
