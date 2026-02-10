from sqlalchemy import Column, String, Integer, Float, Boolean, Text
from app.database import Base


class System(Base):
    """A government data system that holds information about people."""
    __tablename__ = "systems"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    acronym = Column(String, default="")
    agency = Column(String, default="")
    domain = Column(String, index=True)  # health, justice, housing, income, education, child_welfare
    description = Column(Text, default="")
    data_standard = Column(String, default="")  # HL7, FHIR, X12, flat_file, custom, mixed
    data_held = Column(Text, default="[]")  # JSON list of data categories
    who_can_access = Column(Text, default="[]")  # JSON list
    privacy_law = Column(String, default="")  # primary governing law
    privacy_laws = Column(Text, default="[]")  # JSON list of all applicable laws
    applies_when = Column(Text, default="[]")  # JSON: which circumstances trigger this system
    is_federal = Column(Boolean, default=False)
    state_operated = Column(Boolean, default=True)


class Connection(Base):
    """A data-sharing link between two systems."""
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(String, index=True)
    target_id = Column(String, index=True)
    direction = Column(String, default="bidirectional")  # unidirectional, bidirectional
    frequency = Column(String, default="batch")  # realtime, daily, batch, manual, none
    format = Column(String, default="")  # HL7, FHIR, X12, flat_file, manual_entry
    data_shared = Column(Text, default="[]")  # JSON list of what flows
    description = Column(Text, default="")
    reliability = Column(String, default="moderate")  # high, moderate, low


class Gap(Base):
    """A missing connection between two systems that SHOULD share data."""
    __tablename__ = "gaps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    system_a_id = Column(String, index=True)
    system_b_id = Column(String, index=True)
    barrier_type = Column(String, default="")  # legal, technical, political, funding, consent
    barrier_law = Column(String, default="")  # specific law creating barrier
    barrier_description = Column(Text, default="")
    impact = Column(Text, default="")  # plain English consequence
    what_it_would_take = Column(Text, default="")
    consent_closable = Column(Boolean, default=False)  # can the person close this gap?
    consent_mechanism = Column(Text, default="")  # how to close it
    severity = Column(String, default="high")  # critical, high, moderate, low
    applies_when = Column(Text, default="[]")  # JSON: which circumstances trigger this gap
