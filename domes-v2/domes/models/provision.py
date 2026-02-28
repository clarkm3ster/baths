"""
DOMES v2 — Provision Model (Legal Provisions)

Separate module re-exporting from gap.py for cleaner imports.
The Provision model lives in gap.py alongside DataGap since they
are conceptually linked in the DOMES legal engine.
"""
from domes.models.gap import Provision  # noqa: F401
