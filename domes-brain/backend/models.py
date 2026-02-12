"""SQLAlchemy models for DOMES Brain.

Persistent storage for the service registry, query logs, webhook
subscriptions, API keys, and activity feed.
"""

from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Float,
    DateTime,
)

from database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Service(Base):
    """Registered DOMES micro-service."""

    __tablename__ = "services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    slug = Column(String(64), unique=True, nullable=False, index=True)
    base_url = Column(String(256), nullable=False)
    port = Column(Integer, nullable=False)
    description = Column(Text, default="")
    status = Column(String(16), default="offline")  # online / offline / degraded
    last_checked = Column(DateTime, nullable=True)
    last_healthy = Column(DateTime, nullable=True)
    response_time_ms = Column(Float, nullable=True)
    data_freshness = Column(String(32), default="unknown")
    endpoint_count = Column(Integer, default=0)


class QueryLog(Base):
    """Log of every unified query that passes through the brain."""

    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    query_text = Column(Text, nullable=False)
    circumstances = Column(Text, default="{}")  # JSON
    timestamp = Column(DateTime, default=_utcnow)
    duration_ms = Column(Float, default=0.0)
    services_queried = Column(Text, default="[]")  # JSON list of slugs
    result_count = Column(Integer, default=0)


class WebhookSubscription(Base):
    """Webhook subscription for service events."""

    __tablename__ = "webhook_subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_slug = Column(String(64), nullable=False, index=True)
    event_type = Column(String(64), nullable=False)  # e.g. "status_change", "query", "error"
    callback_url = Column(String(512), nullable=False)
    secret = Column(String(128), default="")
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=_utcnow)


class ApiKey(Base):
    """API key for authenticated access to the brain."""

    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key_hash = Column(String(256), unique=True, nullable=False)
    name = Column(String(128), nullable=False)
    rate_limit = Column(Integer, default=100)  # requests per minute
    created_at = Column(DateTime, default=_utcnow)
    last_used = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True)


class ActivityLog(Base):
    """Chronological activity feed across all services."""

    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_slug = Column(String(64), nullable=False, index=True)
    event_type = Column(String(64), nullable=False)
    description = Column(Text, default="")
    timestamp = Column(DateTime, default=_utcnow)
    metadata_json = Column(Text, default="{}")
