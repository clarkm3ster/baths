"""
SQLAlchemy ORM models and CRUD operations for the Discovery Engine.
Mirrors the Pydantic schemas in discovery_models.py.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Optional, Sequence

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
    create_engine,
    func,
    desc,
)
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from discovery_models import (
    Discovery,
    DiscoverySource,
    DiscoveryStats,
    DiscoveryStatus,
    ImpactLevel,
    SourceType,
)

logger = logging.getLogger(__name__)

Base = declarative_base()


# ---------------------------------------------------------------------------
# ORM Tables
# ---------------------------------------------------------------------------

class DiscoveryRecord(Base):
    """Persisted discovery item."""
    __tablename__ = "discoveries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_type = Column(String(32), nullable=False, index=True)
    title = Column(String(512), nullable=False)
    summary = Column(Text, nullable=False)
    url = Column(String(1024), nullable=False)
    relevance_score = Column(Integer, nullable=False, default=50)
    impact_level = Column(String(16), nullable=False, default="medium")
    status = Column(String(16), nullable=False, default="new", index=True)
    discovered_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    metadata_json = Column(Text, nullable=False, default="{}")
    tags = Column(Text, nullable=False, default="[]")  # JSON array

    def to_pydantic(self) -> Discovery:
        return Discovery(
            id=self.id,
            source_type=SourceType(self.source_type),
            title=self.title,
            summary=self.summary,
            url=self.url,
            relevance_score=self.relevance_score,
            impact_level=ImpactLevel(self.impact_level),
            status=DiscoveryStatus(self.status),
            discovered_at=self.discovered_at,
            reviewed_at=self.reviewed_at,
            metadata_json=json.loads(self.metadata_json) if self.metadata_json else {},
            tags=json.loads(self.tags) if self.tags else [],
        )


class DiscoverySourceRecord(Base):
    """Persisted scanner source configuration."""
    __tablename__ = "discovery_sources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False, unique=True)
    source_type = Column(String(32), nullable=False)
    base_url = Column(String(1024), nullable=False)
    last_scanned = Column(DateTime, nullable=True)
    scan_frequency_hours = Column(Integer, nullable=False, default=24)
    active = Column(Boolean, nullable=False, default=True)
    description = Column(Text, nullable=False, default="")

    def to_pydantic(self) -> DiscoverySource:
        return DiscoverySource(
            id=self.id,
            name=self.name,
            source_type=SourceType(self.source_type),
            base_url=self.base_url,
            last_scanned=self.last_scanned,
            scan_frequency_hours=self.scan_frequency_hours,
            active=self.active,
            description=self.description,
        )


# ---------------------------------------------------------------------------
# Engine / Session Factory
# ---------------------------------------------------------------------------

_engine = None
_SessionLocal = None


def get_engine(db_url: str = "sqlite:///./domes_brain.db"):
    global _engine
    if _engine is None:
        _engine = create_engine(db_url, connect_args={"check_same_thread": False})
    return _engine


def get_session_factory(db_url: str = "sqlite:///./domes_brain.db") -> sessionmaker:
    global _SessionLocal
    if _SessionLocal is None:
        engine = get_engine(db_url)
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _SessionLocal


def get_db():
    """FastAPI dependency that yields a DB session."""
    session_factory = get_session_factory()
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


def create_tables(db_url: str = "sqlite:///./domes_brain.db") -> None:
    """Create all discovery tables if they don't exist."""
    engine = get_engine(db_url)
    Base.metadata.create_all(bind=engine)
    logger.info("Discovery tables created/verified.")
    _seed_default_sources(engine)


# ---------------------------------------------------------------------------
# Seed Data
# ---------------------------------------------------------------------------

_DEFAULT_SOURCES = [
    {
        "name": "Federal Register",
        "source_type": "federal_register",
        "base_url": "https://api.federalregister.gov/v1",
        "scan_frequency_hours": 24,
        "description": "Official journal of the federal government. Monitors rules, proposed rules, and notices related to human services programs.",
    },
    {
        "name": "eCFR",
        "source_type": "ecfr",
        "base_url": "https://www.ecfr.gov/api",
        "scan_frequency_hours": 12,
        "description": "Electronic Code of Federal Regulations. Tracks regulatory text changes in titles covering public health, welfare, housing, benefits, and education.",
    },
    {
        "name": "State Legislation Tracker",
        "source_type": "state_legislation",
        "base_url": "https://api.legiscan.com",
        "scan_frequency_hours": 6,
        "description": "Multi-state legislation monitor for PA, NJ, NY, CA, TX, FL. Tracks bills on human services coordination and system integration.",
    },
    {
        "name": "Semantic Scholar",
        "source_type": "academic",
        "base_url": "https://api.semanticscholar.org/graph/v1",
        "scan_frequency_hours": 48,
        "description": "Academic research search for super-utilizer populations, care coordination, social determinants, and cross-system integration studies.",
    },
    {
        "name": "News Monitor",
        "source_type": "news",
        "base_url": "https://newsapi.org/v2",
        "scan_frequency_hours": 4,
        "description": "News aggregator tracking policy changes, system failures, benefits cliff events, and human services technology developments.",
    },
    {
        "name": "DOMES Gap Analyzer",
        "source_type": "gap_analysis",
        "base_url": "http://localhost",
        "scan_frequency_hours": 24,
        "description": "Internal analyzer that audits coverage across all DOMES services, identifying domain gaps, stale data, and missing jurisdictions.",
    },
]


def _seed_default_sources(engine) -> None:
    """Insert default scanner sources if the table is empty."""
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        count = db.query(DiscoverySourceRecord).count()
        if count == 0:
            for src in _DEFAULT_SOURCES:
                db.add(DiscoverySourceRecord(**src))
            db.commit()
            logger.info("Seeded %d default discovery sources.", len(_DEFAULT_SOURCES))
    except Exception:
        db.rollback()
        logger.exception("Failed to seed default sources.")
    finally:
        db.close()


# ---------------------------------------------------------------------------
# CRUD Operations
# ---------------------------------------------------------------------------

def create_discovery(db: Session, item: Discovery) -> DiscoveryRecord:
    """Insert a new discovery record. Returns the persisted record."""
    record = DiscoveryRecord(
        source_type=item.source_type.value,
        title=item.title,
        summary=item.summary,
        url=item.url,
        relevance_score=item.relevance_score,
        impact_level=item.impact_level.value,
        status=item.status.value,
        discovered_at=item.discovered_at,
        reviewed_at=item.reviewed_at,
        metadata_json=json.dumps(item.metadata_json),
        tags=json.dumps(item.tags),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_discoveries(
    db: Session,
    *,
    source_type: Optional[str] = None,
    impact_level: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[DiscoveryRecord], int]:
    """
    Retrieve discoveries with optional filters.
    Returns (records, total_count).
    """
    query = db.query(DiscoveryRecord)

    if source_type:
        query = query.filter(DiscoveryRecord.source_type == source_type)
    if impact_level:
        query = query.filter(DiscoveryRecord.impact_level == impact_level)
    if status:
        query = query.filter(DiscoveryRecord.status == status)

    total = query.count()
    records = (
        query
        .order_by(desc(DiscoveryRecord.discovered_at))
        .offset(offset)
        .limit(limit)
        .all()
    )
    return records, total


def get_discovery_by_id(db: Session, discovery_id: int) -> Optional[DiscoveryRecord]:
    """Fetch a single discovery by primary key."""
    return db.query(DiscoveryRecord).filter(DiscoveryRecord.id == discovery_id).first()


def update_discovery_status(
    db: Session, discovery_id: int, new_status: str
) -> Optional[DiscoveryRecord]:
    """Update the status of a discovery. Sets reviewed_at when transitioning from 'new'."""
    record = get_discovery_by_id(db, discovery_id)
    if record is None:
        return None

    old_status = record.status
    record.status = new_status

    # Mark reviewed_at on first review action
    if old_status == "new" and new_status in ("reviewed", "queued", "ingested", "dismissed"):
        record.reviewed_at = datetime.utcnow()

    db.commit()
    db.refresh(record)
    return record


def get_queue(db: Session, limit: int = 50) -> list[DiscoveryRecord]:
    """
    Priority queue: discoveries with status 'new' or 'queued',
    ordered by relevance_score descending.
    """
    return (
        db.query(DiscoveryRecord)
        .filter(DiscoveryRecord.status.in_(["new", "queued"]))
        .order_by(desc(DiscoveryRecord.relevance_score))
        .limit(limit)
        .all()
    )


def get_sources(db: Session) -> list[DiscoverySourceRecord]:
    """List all scanner sources."""
    return db.query(DiscoverySourceRecord).all()


def update_source_last_scanned(db: Session, source_name: str) -> None:
    """Stamp a source's last_scanned to now."""
    record = (
        db.query(DiscoverySourceRecord)
        .filter(DiscoverySourceRecord.name == source_name)
        .first()
    )
    if record:
        record.last_scanned = datetime.utcnow()
        db.commit()


def get_stats(db: Session) -> DiscoveryStats:
    """Compute aggregate counts by source_type, impact_level, and status."""
    total = db.query(DiscoveryRecord).count()

    by_source: dict[str, int] = {}
    for row in db.query(DiscoveryRecord.source_type, func.count()).group_by(DiscoveryRecord.source_type).all():
        by_source[row[0]] = row[1]

    by_impact: dict[str, int] = {}
    for row in db.query(DiscoveryRecord.impact_level, func.count()).group_by(DiscoveryRecord.impact_level).all():
        by_impact[row[0]] = row[1]

    by_status: dict[str, int] = {}
    for row in db.query(DiscoveryRecord.status, func.count()).group_by(DiscoveryRecord.status).all():
        by_status[row[0]] = row[1]

    return DiscoveryStats(
        by_source=by_source,
        by_impact=by_impact,
        by_status=by_status,
        total=total,
    )


def discovery_url_exists(db: Session, url: str) -> bool:
    """Check if a discovery with the given URL already exists (dedup)."""
    return db.query(DiscoveryRecord).filter(DiscoveryRecord.url == url).first() is not None
