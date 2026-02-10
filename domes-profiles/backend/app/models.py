"""
Database models for DOMES Profiles.
Profile, ProfileDomain, and ProfileVersion tables.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship

from .database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)
    circumstances = Column(JSON, nullable=False, default=dict)
    systems_involved = Column(JSON, nullable=False, default=list)
    total_annual_cost = Column(Float, nullable=False, default=0.0)
    coordinated_annual_cost = Column(Float, nullable=False, default=0.0)
    savings_annual = Column(Float, nullable=False, default=0.0)
    five_year_projection = Column(Float, nullable=False, default=0.0)
    lifetime_estimate = Column(Float, nullable=False, default=0.0)
    narrative = Column(Text, nullable=True, default="")
    is_sample = Column(Boolean, nullable=False, default=False)

    domains = relationship(
        "ProfileDomain",
        back_populates="profile",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    versions = relationship(
        "ProfileVersion",
        back_populates="profile",
        cascade="all, delete-orphan",
        order_by="ProfileVersion.version.desc()",
    )

    def to_summary(self) -> dict:
        """Return a lightweight summary (no domains)."""
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "circumstances": self.circumstances or {},
            "systems_involved": self.systems_involved or [],
            "total_annual_cost": self.total_annual_cost,
            "coordinated_annual_cost": self.coordinated_annual_cost,
            "savings_annual": self.savings_annual,
            "five_year_projection": self.five_year_projection,
            "lifetime_estimate": self.lifetime_estimate,
            "is_sample": self.is_sample,
        }

    def to_full(self) -> dict:
        """Return full profile with domains."""
        data = self.to_summary()
        data["narrative"] = self.narrative or ""
        data["domains"] = [d.to_dict() for d in (self.domains or [])]
        return data


class ProfileDomain(Base):
    __tablename__ = "profile_domains"

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(String, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    domain = Column(String, nullable=False)
    domain_label = Column(String, nullable=False)
    systems = Column(JSON, nullable=False, default=list)
    provisions_count = Column(Integer, nullable=False, default=0)
    annual_cost = Column(Float, nullable=False, default=0.0)
    coordinated_cost = Column(Float, nullable=False, default=0.0)
    savings = Column(Float, nullable=False, default=0.0)
    top_provisions = Column(JSON, nullable=False, default=list)
    gaps = Column(JSON, nullable=False, default=list)
    bridges = Column(JSON, nullable=False, default=list)

    profile = relationship("Profile", back_populates="domains")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "domain": self.domain,
            "domain_label": self.domain_label,
            "systems": self.systems or [],
            "provisions_count": self.provisions_count,
            "annual_cost": self.annual_cost,
            "coordinated_cost": self.coordinated_cost,
            "savings": self.savings,
            "top_provisions": self.top_provisions or [],
            "gaps": self.gaps or [],
            "bridges": self.bridges or [],
        }


class ProfileVersion(Base):
    __tablename__ = "profile_versions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(String, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    version = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    circumstances = Column(JSON, nullable=False, default=dict)
    total_annual_cost = Column(Float, nullable=False, default=0.0)
    coordinated_annual_cost = Column(Float, nullable=False, default=0.0)
    change_description = Column(String, nullable=True, default="")

    profile = relationship("Profile", back_populates="versions")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "version": self.version,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "circumstances": self.circumstances or {},
            "total_annual_cost": self.total_annual_cost,
            "coordinated_annual_cost": self.coordinated_annual_cost,
            "change_description": self.change_description or "",
        }
