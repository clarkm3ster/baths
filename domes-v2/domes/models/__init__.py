"""
DOMES v2 — Models Package

Exports all SQLAlchemy models. Import all models here to ensure Alembic
autogenerate can see them and to provide a convenient single import point.

Usage:
    from domes.models import Person, Dome, BiometricReading, Consent
    from domes.models import Base  # For Alembic target_metadata

Import order matters for circular reference avoidance:
    base → enums → person → (all others)
"""
from domes.models.assessment import Assessment
from domes.models.base import (
    AuditMixin,
    DOMESBase,
    FHIRMixin,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)
from domes.models.biometric import BiometricReading
from domes.models.condition import Condition
from domes.models.consent import Consent, ConsentAuditEntry
from domes.models.dome import Dome
from domes.models.encounter import Encounter
from domes.models.enrollment import Enrollment
from domes.models.environment import EnvironmentReading
from domes.models.flourishing import FlourishingScore
from domes.models.fragment import Fragment
from domes.models.gap import DataGap, Provision
from domes.models.medication import Medication
from domes.models.observation import Observation
from domes.models.person import Person
from domes.models.system import GovernmentSystem

# Alias for Alembic
Base = DOMESBase

__all__ = [
    # Base
    "Base",
    "DOMESBase",
    "AuditMixin",
    "FHIRMixin",
    "SoftDeleteMixin",
    "TimestampMixin",
    "UUIDPrimaryKeyMixin",
    # Core entities
    "Person",
    "Consent",
    "ConsentAuditEntry",
    "Fragment",
    "GovernmentSystem",
    "DataGap",
    "Provision",
    # Clinical
    "Observation",
    "Encounter",
    "Condition",
    "Medication",
    "Assessment",
    "Enrollment",
    # Time-series
    "BiometricReading",
    "EnvironmentReading",
    # Digital twin
    "Dome",
    "FlourishingScore",
]
