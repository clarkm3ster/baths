"""SQLAlchemy database setup for DOMES Brain.

Central persistence layer using SQLite for query logs,
webhook subscriptions, API keys, and activity tracking.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./brain.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db() -> None:
    """Create all tables if they do not exist."""
    from models import (  # noqa: F401 — side-effect import to register models
        Service,
        QueryLog,
        WebhookSubscription,
        ApiKey,
        ActivityLog,
    )
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
