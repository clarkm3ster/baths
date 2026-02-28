"""
DOMES v2 — Provision Model (Legal Provisions)

Separate module re-exporting from gap.py for cleaner imports.
The Provision model is defined in gap.py alongside DataGap.
"""
from domes.models.gap import Provision  # noqa: F401

__all__ = ["Provision"]
