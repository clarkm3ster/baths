"""
SPHERES Innovation Laboratory — SQLAlchemy ORM models.
"""

import json
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Teammate(Base):
    __tablename__ = "teammates"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    color = Column(String, nullable=False)
    icon_symbol = Column(String, nullable=False)
    status = Column(String, default="idle")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    innovations = relationship("Innovation", back_populates="teammate")

    def to_dict(self, include_innovations=False):
        d = {
            "id": self.id,
            "slug": self.slug,
            "name": self.name,
            "title": self.title,
            "domain": self.domain,
            "description": self.description,
            "color": self.color,
            "icon_symbol": self.icon_symbol,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "innovation_count": len(self.innovations) if self.innovations else 0,
        }
        if include_innovations:
            d["innovations"] = [i.to_dict() for i in self.innovations]
        return d


class Innovation(Base):
    __tablename__ = "innovations"

    id = Column(Integer, primary_key=True, index=True)
    teammate_id = Column(Integer, ForeignKey("teammates.id"), nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    domain = Column(String, nullable=False)
    category = Column(String, nullable=False)
    impact_level = Column(Integer, nullable=False)
    feasibility = Column(Integer, nullable=False)
    novelty = Column(Integer, nullable=False)
    time_horizon = Column(String, nullable=False)
    status = Column(String, default="draft")
    details = Column(Text, default="{}")
    tags = Column(String, default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    teammate = relationship("Teammate", back_populates="innovations")

    def to_dict(self):
        details = {}
        try:
            details = json.loads(self.details) if self.details else {}
        except (json.JSONDecodeError, TypeError):
            pass
        tags = [t.strip() for t in self.tags.split(",") if t.strip()] if self.tags else []
        return {
            "id": self.id,
            "teammate_id": self.teammate_id,
            "title": self.title,
            "summary": self.summary,
            "domain": self.domain,
            "category": self.category,
            "impact_level": self.impact_level,
            "feasibility": self.feasibility,
            "novelty": self.novelty,
            "time_horizon": self.time_horizon,
            "status": self.status,
            "details": details,
            "tags": tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Collaboration(Base):
    __tablename__ = "collaborations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    status = Column(String, default="proposed")
    teammate_ids = Column(String, default="")
    innovations = Column(Text, default="[]")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        tid = [int(x) for x in self.teammate_ids.split(",") if x.strip()] if self.teammate_ids else []
        innov = []
        try:
            innov = json.loads(self.innovations) if self.innovations else []
        except (json.JSONDecodeError, TypeError):
            pass
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "status": self.status,
            "teammate_ids": tid,
            "innovations": innov,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class LabSession(Base):
    __tablename__ = "lab_sessions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    focus_domain = Column(String, nullable=False)
    status = Column(String, default="planning")
    participants = Column(String, default="")
    findings = Column(Text, default="[]")
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)

    def to_dict(self):
        parts = [p.strip() for p in self.participants.split(",") if p.strip()] if self.participants else []
        finds = []
        try:
            finds = json.loads(self.findings) if self.findings else []
        except (json.JSONDecodeError, TypeError):
            pass
        return {
            "id": self.id,
            "name": self.name,
            "focus_domain": self.focus_domain,
            "status": self.status,
            "participants": parts,
            "findings": finds,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
