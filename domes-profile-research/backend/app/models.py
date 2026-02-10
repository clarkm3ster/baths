import json
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class DocumentedCase(Base):
    """A real documented case from investigations, audits, reports."""
    __tablename__ = "documented_cases"

    id = Column(String, primary_key=True)
    source = Column(String, nullable=False)          # e.g. "ProPublica", "GAO", "Marshall Project"
    source_url = Column(String)
    source_title = Column(String, nullable=False)
    source_date = Column(String)                      # ISO date string
    source_type = Column(String)                      # investigation, audit, academic, news, gov_report
    domain = Column(String, nullable=False)           # health, justice, housing, income, education, child_welfare
    system_ids = Column(Text, default="[]")           # JSON array of system IDs involved
    circumstance_tags = Column(Text, default="[]")    # JSON tags: mental_health, substance_use, etc.
    age_range = Column(String)                        # child, youth, adult, elderly
    summary = Column(Text, nullable=False)
    finding = Column(Text, nullable=False)            # The key finding or data point
    cost_data = Column(Text)                          # JSON: extracted cost figures if any
    location = Column(String)                         # city/state
    year = Column(Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "source": self.source,
            "source_url": self.source_url,
            "source_title": self.source_title,
            "source_date": self.source_date,
            "source_type": self.source_type,
            "domain": self.domain,
            "system_ids": json.loads(self.system_ids or "[]"),
            "circumstance_tags": json.loads(self.circumstance_tags or "[]"),
            "age_range": self.age_range,
            "summary": self.summary,
            "finding": self.finding,
            "cost_data": json.loads(self.cost_data or "null"),
            "location": self.location,
            "year": self.year,
        }


class CostBenchmark(Base):
    """Published cost benchmarks from CMS, HCUP, Vera, HUD, etc."""
    __tablename__ = "cost_benchmarks"

    id = Column(String, primary_key=True)
    category = Column(String, nullable=False)        # er_visit, jail_day, shelter_night, etc.
    label = Column(String, nullable=False)
    cost_per_unit = Column(Float, nullable=False)
    unit = Column(String, nullable=False)            # per_visit, per_day, per_month, per_year
    source = Column(String, nullable=False)
    source_url = Column(String)
    year = Column(Integer)
    notes = Column(Text)

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "label": self.label,
            "cost_per_unit": self.cost_per_unit,
            "unit": self.unit,
            "source": self.source,
            "source_url": self.source_url,
            "year": self.year,
            "notes": self.notes,
        }


class SystemProfile(Base):
    """Template for a government system that appears in profiles."""
    __tablename__ = "system_profiles"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    acronym = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    data_held = Column(Text, default="[]")            # JSON
    annual_cost_per_person = Column(Float)
    typical_utilization = Column(Float, default=1.0)   # fraction of full annual cost a typical multi-system person uses
    cost_source = Column(String)
    applies_when = Column(Text, default="[]")         # JSON: circumstance tags

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "acronym": self.acronym,
            "domain": self.domain,
            "data_held": json.loads(self.data_held or "[]"),
            "annual_cost_per_person": self.annual_cost_per_person,
            "typical_utilization": self.typical_utilization or 1.0,
            "cost_source": self.cost_source,
            "applies_when": json.loads(self.applies_when or "[]"),
        }


class CompositeProfile(Base):
    """A generated composite profile."""
    __tablename__ = "composite_profiles"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    circumstances = Column(Text, default="{}")        # JSON: the input profile
    systems_involved = Column(Text, default="[]")     # JSON: system IDs
    timeline = Column(Text, default="[]")             # JSON: timeline events
    total_annual_cost = Column(Float)
    cost_breakdown = Column(Text, default="[]")       # JSON: cost line items
    citations = Column(Text, default="[]")            # JSON: case IDs used
    coordinated_cost = Column(Float)                  # cost if systems talked
    narrative = Column(Text)                          # generated narrative summary

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "circumstances": json.loads(self.circumstances or "{}"),
            "systems_involved": json.loads(self.systems_involved or "[]"),
            "timeline": json.loads(self.timeline or "[]"),
            "total_annual_cost": self.total_annual_cost,
            "cost_breakdown": json.loads(self.cost_breakdown or "[]"),
            "citations": json.loads(self.citations or "[]"),
            "coordinated_cost": self.coordinated_cost,
            "narrative": self.narrative,
        }
