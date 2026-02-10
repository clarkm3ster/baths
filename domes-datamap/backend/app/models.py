import json
from sqlalchemy import Column, String, Text, Boolean, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class System(Base):
    __tablename__ = "systems"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    acronym = Column(String, nullable=False)
    agency = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    data_standard = Column(String, nullable=False)
    _fields_held = Column("fields_held", Text, nullable=False, default="[]")
    api_availability = Column(String, nullable=False)
    update_frequency = Column(String, nullable=False)
    privacy_law = Column(String, nullable=False)
    _privacy_laws = Column("privacy_laws", Text, nullable=False, default="[]")
    is_federal = Column(Boolean, nullable=False, default=False)
    state_operated = Column(Boolean, nullable=False, default=False)
    _applies_when = Column("applies_when", Text, nullable=False, default="[]")

    outgoing_connections = relationship(
        "Connection", foreign_keys="Connection.source_id", back_populates="source"
    )
    incoming_connections = relationship(
        "Connection", foreign_keys="Connection.target_id", back_populates="target"
    )

    @property
    def fields_held(self):
        return json.loads(self._fields_held) if self._fields_held else []

    @fields_held.setter
    def fields_held(self, value):
        self._fields_held = json.dumps(value) if value else "[]"

    @property
    def privacy_laws(self):
        return json.loads(self._privacy_laws) if self._privacy_laws else []

    @privacy_laws.setter
    def privacy_laws(self, value):
        self._privacy_laws = json.dumps(value) if value else "[]"

    @property
    def applies_when(self):
        return json.loads(self._applies_when) if self._applies_when else []

    @applies_when.setter
    def applies_when(self, value):
        self._applies_when = json.dumps(value) if value else "[]"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "acronym": self.acronym,
            "agency": self.agency,
            "domain": self.domain,
            "description": self.description,
            "data_standard": self.data_standard,
            "fields_held": self.fields_held,
            "api_availability": self.api_availability,
            "update_frequency": self.update_frequency,
            "privacy_law": self.privacy_law,
            "privacy_laws": self.privacy_laws,
            "is_federal": self.is_federal,
            "state_operated": self.state_operated,
            "applies_when": self.applies_when,
        }


class Connection(Base):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(String, ForeignKey("systems.id"), nullable=False)
    target_id = Column(String, ForeignKey("systems.id"), nullable=False)
    direction = Column(String, nullable=False)
    format = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    _data_shared = Column("data_shared", Text, nullable=False, default="[]")
    governing_agreement = Column(String, nullable=False)
    privacy_law = Column(String, nullable=False)
    reliability = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    source = relationship("System", foreign_keys=[source_id], back_populates="outgoing_connections")
    target = relationship("System", foreign_keys=[target_id], back_populates="incoming_connections")

    @property
    def data_shared(self):
        return json.loads(self._data_shared) if self._data_shared else []

    @data_shared.setter
    def data_shared(self, value):
        self._data_shared = json.dumps(value) if value else "[]"

    def to_dict(self):
        return {
            "id": self.id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "source_name": self.source.name if self.source else None,
            "target_name": self.target.name if self.target else None,
            "direction": self.direction,
            "format": self.format,
            "frequency": self.frequency,
            "data_shared": self.data_shared,
            "governing_agreement": self.governing_agreement,
            "privacy_law": self.privacy_law,
            "reliability": self.reliability,
            "description": self.description,
        }


class Gap(Base):
    __tablename__ = "gaps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    system_a_id = Column(String, ForeignKey("systems.id"), nullable=False)
    system_b_id = Column(String, ForeignKey("systems.id"), nullable=False)
    barrier_type = Column(String, nullable=False)
    barrier_law = Column(String, nullable=True)
    barrier_description = Column(Text, nullable=False)
    impact = Column(Text, nullable=False)
    severity = Column(String, nullable=False)
    cost_to_bridge = Column(String, nullable=False)
    timeline_to_bridge = Column(String, nullable=False)
    consent_closable = Column(Boolean, nullable=False, default=False)
    consent_mechanism = Column(String, nullable=True)
    what_it_would_take = Column(Text, nullable=False)
    _applies_when = Column("applies_when", Text, nullable=False, default="[]")

    system_a = relationship("System", foreign_keys=[system_a_id])
    system_b = relationship("System", foreign_keys=[system_b_id])
    bridges = relationship("Bridge", back_populates="gap", cascade="all, delete-orphan")

    @property
    def applies_when(self):
        return json.loads(self._applies_when) if self._applies_when else []

    @applies_when.setter
    def applies_when(self, value):
        self._applies_when = json.dumps(value) if value else "[]"

    def to_dict(self):
        return {
            "id": self.id,
            "system_a_id": self.system_a_id,
            "system_b_id": self.system_b_id,
            "system_a_name": self.system_a.name if self.system_a else None,
            "system_b_name": self.system_b.name if self.system_b else None,
            "barrier_type": self.barrier_type,
            "barrier_law": self.barrier_law,
            "barrier_description": self.barrier_description,
            "impact": self.impact,
            "severity": self.severity,
            "cost_to_bridge": self.cost_to_bridge,
            "timeline_to_bridge": self.timeline_to_bridge,
            "consent_closable": self.consent_closable,
            "consent_mechanism": self.consent_mechanism,
            "what_it_would_take": self.what_it_would_take,
            "applies_when": self.applies_when,
        }


class Bridge(Base):
    __tablename__ = "bridges"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gap_id = Column(Integer, ForeignKey("gaps.id"), nullable=False)
    bridge_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    technical_requirements = Column(Text, nullable=True)
    legal_requirements = Column(Text, nullable=True)
    estimated_cost = Column(String, nullable=False)
    timeline = Column(String, nullable=False)
    who_pays = Column(String, nullable=False)
    priority_score = Column(Float, nullable=False)
    impact_score = Column(Float, nullable=False)
    effort_score = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="proposed")

    gap = relationship("Gap", back_populates="bridges")

    def to_dict(self):
        return {
            "id": self.id,
            "gap_id": self.gap_id,
            "bridge_type": self.bridge_type,
            "title": self.title,
            "description": self.description,
            "technical_requirements": self.technical_requirements,
            "legal_requirements": self.legal_requirements,
            "estimated_cost": self.estimated_cost,
            "timeline": self.timeline,
            "who_pays": self.who_pays,
            "priority_score": self.priority_score,
            "impact_score": self.impact_score,
            "effort_score": self.effort_score,
            "status": self.status,
        }
