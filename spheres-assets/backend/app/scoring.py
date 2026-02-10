"""Activation scoring engine for Spheres Assets.

Each parcel gets a 0-100 score based on weighted factors indicating
how suitable it is for temporary activation (events, film, pop-up, etc.).
"""

from __future__ import annotations

import json
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Parcel

# Zoning flexibility tiers
_ZONING_SCORES: dict[str, int] = {}
# Commercial mixed-use = most flexible
for z in ("CMX5", "CMX4", "CMX3", "CMX2.5", "CMX2", "CMX1"):
    _ZONING_SCORES[z] = 15
# Commercial auto
for z in ("CA1", "CA2"):
    _ZONING_SCORES[z] = 12
# Industrial mixed-use
for z in ("ICMX", "IRMX"):
    _ZONING_SCORES[z] = 12
# Residential mixed-use
for z in ("RMX1", "RMX2", "RMX3"):
    _ZONING_SCORES[z] = 10
# Multi-family residential
for z in ("RM1", "RM2", "RM3", "RM4"):
    _ZONING_SCORES[z] = 8
# Industrial
for z in ("I1", "I2", "I3", "IP"):
    _ZONING_SCORES[z] = 6
# Special purpose
for z in ("SPAIR", "SPCIV", "SPENT", "SPINS", "SPPOA", "SPPOP", "SPSTA"):
    _ZONING_SCORES[z] = 4
# Single-family residential = least flexible
for z in ("RSA1", "RSA2", "RSA3", "RSA4", "RSA5", "RSA6",
          "RSD1", "RSD2", "RSD3", "RTA1", "RTA2"):
    _ZONING_SCORES[z] = 2


def score_parcel(parcel: Parcel) -> int:
    """Compute an activation score from 0-100."""
    score = 0.0

    # --- Size (0-20) ---
    area = parcel.total_area_sqft or 0
    if area > 0:
        # Log scale: 500sqft=5, 5000sqft=12, 50000sqft=20
        score += min(20, max(0, math.log10(max(area, 1)) * 5.4 - 9))

    # --- Vacancy (0-25) ---
    cat = parcel.category_code or ""
    if cat in ("6", "12", "13"):
        score += 25  # explicitly vacant land
    elif parcel.exterior_condition in ("6", "7"):
        score += 15  # poor condition = likely underused
    elif parcel.exterior_condition in ("4", "5"):
        score += 8
    else:
        score += 3  # occupied but public = some potential

    # --- Accessibility / Zoning (0-15) ---
    zoning = (parcel.zoning or "").upper()
    score += _ZONING_SCORES.get(zoning, 3)

    # --- Infrastructure (0-15) ---
    infra = 5  # base: public parcel, has address
    if parcel.market_value and parcel.market_value > 0:
        infra += 3  # assessed = known to city
    if parcel.taxable_building and parcel.taxable_building > 0:
        infra += 4  # has a building = utilities likely
    if zoning.startswith("CMX") or zoning.startswith("CA"):
        infra += 3  # commercial zone = better infrastructure
    score += min(15, infra)

    # --- Condition opportunity (0-10) ---
    ext = parcel.exterior_condition or ""
    if ext in ("6", "7"):
        score += 10  # worst condition = most opportunity
    elif ext in ("4", "5"):
        score += 6
    elif ext in ("2", "3"):
        score += 3
    else:
        score += 1

    # --- Surroundings / zoning bonus (0-15) ---
    surr = 5  # base
    if zoning.startswith("CMX"):
        surr += 5  # commercial mixed-use area
    if parcel.frontage and parcel.frontage > 40:
        surr += 3  # street presence
    if area > 10000:
        surr += 2  # large site in any context
    score += min(15, surr)

    return max(0, min(100, round(score)))


def categorize_parcel(parcel: Parcel) -> str:
    """Return a JSON list of activation category strings."""
    cats: list[str] = []
    area = parcel.total_area_sqft or 0
    zoning = (parcel.zoning or "").upper()
    is_vacant = parcel.category_code in ("6", "12", "13")
    frontage = parcel.frontage or 0

    if area > 5000 and is_vacant:
        cats.append("film")
    if area > 5000 and (zoning.startswith("CMX") or zoning.startswith("I")):
        cats.append("events")
    if zoning.startswith("CMX") and frontage > 20:
        cats.append("pop_up_commercial")
    if is_vacant and zoning.startswith("R"):
        cats.append("green_garden")
    if is_vacant and area < 5000 and frontage > 15:
        cats.append("art_installation")
    if area > 10000 and is_vacant:
        cats.append("recreation")

    if not cats:
        cats.append("general")

    return json.dumps(cats)
