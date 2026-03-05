"""
Database models for the structured legal engine.

This is the canonical schema. All parsers normalize into these models.
All queries, taxonomy, and graph operations work against these tables.
"""
import json
from sqlalchemy import Column, Integer, Float, Text, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


# ---------- Core provision table ----------

class Provision(Base):
    """A single legal provision -- the atomic unit of law."""
    __tablename__ = "provisions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Citation and identification
    citation = Column(Text, nullable=False, unique=True, index=True)
    title = Column(Text, nullable=False)
    full_text = Column(Text, nullable=False)

    # Hierarchy: Title > Chapter > Part > Section > Subsection
    source_type = Column(Text, nullable=False)  # usc, cfr, fr, pa_statute, pa_reg
    title_number = Column(Text)       # e.g. "42" for Title 42
    chapter = Column(Text)
    part = Column(Text)
    section = Column(Text)
    subsection = Column(Text)

    # Classification
    domain = Column(Text, nullable=False, index=True)  # health, justice, housing, income, education, child_welfare
    provision_type = Column(Text, nullable=False, index=True)  # right, protection, obligation, enforcement
    applies_when = Column(Text, default="{}")  # JSON: conditions dict
    enforcement_mechanisms = Column(Text, default="[]")  # JSON: list of strings
    cross_references = Column(Text, default="[]")  # JSON: list of citation strings

    # Source metadata
    source_url = Column(Text)
    effective_date = Column(Text)
    last_amended = Column(Text)

    # Versioning
    version = Column(Integer, default=1)
    is_current = Column(Boolean, default=True)
    superseded_by = Column(Text)  # citation of superseding provision

    # Ingestion metadata
    ingested_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    raw_source = Column(Text)  # original XML/JSON/HTML before normalization

    # Taxonomy (populated by taxonomy-builder)
    tags = Column(Text, default="[]")  # JSON: list of tag strings
    populations = Column(Text, default="[]")  # JSON: list of population identifiers
    confidence_score = Column(Float, default=1.0)  # tag confidence 0-1

    # Graph (populated by graph-builder)
    # Relationships stored in ProvisionRelationship table

    def to_dict(self):
        return {
            "id": self.id,
            "citation": self.citation,
            "title": self.title,
            "full_text": self.full_text,
            "source_type": self.source_type,
            "title_number": self.title_number,
            "chapter": self.chapter,
            "part": self.part,
            "section": self.section,
            "subsection": self.subsection,
            "domain": self.domain,
            "provision_type": self.provision_type,
            "applies_when": json.loads(self.applies_when or "{}"),
            "enforcement_mechanisms": json.loads(self.enforcement_mechanisms or "[]"),
            "cross_references": json.loads(self.cross_references or "[]"),
            "source_url": self.source_url,
            "effective_date": self.effective_date,
            "last_amended": self.last_amended,
            "version": self.version,
            "is_current": self.is_current,
            "tags": json.loads(self.tags or "[]"),
            "populations": json.loads(self.populations or "[]"),
            "confidence_score": self.confidence_score,
        }


# ---------- Provision history ----------

class ProvisionHistory(Base):
    """Track changes to provisions over time."""
    __tablename__ = "provision_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    provision_id = Column(Integer, ForeignKey("provisions.id"), nullable=False)
    citation = Column(Text, nullable=False)
    field_changed = Column(Text, nullable=False)
    old_value = Column(Text)
    new_value = Column(Text)
    changed_at = Column(DateTime, default=datetime.utcnow)
    change_source = Column(Text)  # e.g. "fr_notice_2024-12345"

    def to_dict(self):
        return {
            "id": self.id,
            "provision_id": self.provision_id,
            "citation": self.citation,
            "field_changed": self.field_changed,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "changed_at": self.changed_at.isoformat() if self.changed_at else None,
            "change_source": self.change_source,
        }


# ---------- Relationship graph ----------

class ProvisionRelationship(Base):
    """Edge in the provision graph."""
    __tablename__ = "provision_relationships"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer, ForeignKey("provisions.id"), nullable=False, index=True)
    target_id = Column(Integer, ForeignKey("provisions.id"), nullable=False, index=True)
    relationship_type = Column(Text, nullable=False, index=True)
    # implements, interprets, cross_references, supersedes, triggers, enforces
    description = Column(Text)
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    source = relationship("Provision", foreign_keys=[source_id])
    target = relationship("Provision", foreign_keys=[target_id])

    def to_dict(self):
        return {
            "id": self.id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "source_citation": self.source.citation if self.source else None,
            "target_citation": self.target.citation if self.target else None,
            "relationship_type": self.relationship_type,
            "description": self.description,
            "confidence": self.confidence,
        }


# ---------- Taxonomy tags ----------

class TaxonomyTag(Base):
    """Controlled vocabulary for provision tags."""
    __tablename__ = "taxonomy_tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True, index=True)
    category = Column(Text, nullable=False)  # domain, population, circumstance, mechanism
    description = Column(Text)
    parent_tag = Column(Text)  # for hierarchical taxonomy

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "parent_tag": self.parent_tag,
        }


# ---------- Ingestion log ----------

class IngestionLog(Base):
    """Track what was ingested, when, from where."""
    __tablename__ = "ingestion_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_type = Column(Text, nullable=False)  # usc, cfr, fr, pa_statute, pa_reg
    source_url = Column(Text)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    provisions_added = Column(Integer, default=0)
    provisions_updated = Column(Integer, default=0)
    status = Column(Text, default="running")  # running, completed, failed
    error_message = Column(Text)

    def to_dict(self):
        return {
            "id": self.id,
            "source_type": self.source_type,
            "source_url": self.source_url,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "provisions_added": self.provisions_added,
            "provisions_updated": self.provisions_updated,
            "status": self.status,
            "error_message": self.error_message,
        }


# ---------- Update monitor ----------

class UpdateCheck(Base):
    """Track source checks for changes."""
    __tablename__ = "update_checks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_type = Column(Text, nullable=False)
    checked_at = Column(DateTime, default=datetime.utcnow)
    changes_found = Column(Integer, default=0)
    details = Column(Text, default="{}")  # JSON

    def to_dict(self):
        return {
            "id": self.id,
            "source_type": self.source_type,
            "checked_at": self.checked_at.isoformat() if self.checked_at else None,
            "changes_found": self.changes_found,
            "details": json.loads(self.details or "{}"),
        }
