"""Value calculator for Spheres Assets.

Three tiers of value estimation for Philadelphia's public property portfolio.
"""

from __future__ import annotations

import json
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import Parcel

# Revenue assumptions per activation category ($/sqft/year)
_REVENUE_RATES: dict[str, float] = {
    "film": 8.00,
    "events": 6.00,
    "pop_up_commercial": 12.00,
    "green_garden": 2.00,
    "art_installation": 4.00,
    "recreation": 3.00,
    "general": 1.50,
}

# Utilization rates (fraction of year a parcel could be activated)
_UTILIZATION: dict[str, float] = {
    "film": 0.15,
    "events": 0.20,
    "pop_up_commercial": 0.40,
    "green_garden": 0.50,
    "art_installation": 0.30,
    "recreation": 0.35,
    "general": 0.10,
}


def static_value(db: Session) -> dict:
    """Total assessed market value of all public parcels, by agency."""
    rows = (
        db.query(
            Parcel.owner_agency,
            func.count(Parcel.parcel_number).label("count"),
            func.sum(Parcel.market_value).label("total_value"),
            func.sum(Parcel.total_area_sqft).label("total_area"),
        )
        .group_by(Parcel.owner_agency)
        .all()
    )

    by_agency = {}
    grand_total = 0.0
    total_parcels = 0
    total_area = 0.0

    for row in rows:
        val = float(row.total_value or 0)
        area = float(row.total_area or 0)
        by_agency[row.owner_agency] = {
            "count": row.count,
            "total_value": val,
            "total_area_sqft": area,
        }
        grand_total += val
        total_parcels += row.count
        total_area += area

    return {
        "total_value": grand_total,
        "total_parcels": total_parcels,
        "total_area_sqft": total_area,
        "total_acres": total_area / 43560,
        "by_agency": by_agency,
    }


def activation_value(db: Session) -> dict:
    """Projected annual revenue if parcels were activated as Spheres."""
    parcels = db.query(
        Parcel.owner_agency,
        Parcel.total_area_sqft,
        Parcel.activation_categories,
        Parcel.activation_score,
    ).all()

    total_revenue = 0.0
    by_agency: dict[str, float] = {}
    by_category: dict[str, float] = {}

    for p in parcels:
        area = p.total_area_sqft or 0
        cats = json.loads(p.activation_categories or "[]")
        if not cats:
            cats = ["general"]

        # Use the highest-revenue category for this parcel
        best_cat = max(cats, key=lambda c: _REVENUE_RATES.get(c, 1.5))
        rate = _REVENUE_RATES.get(best_cat, 1.5)
        util = _UTILIZATION.get(best_cat, 0.1)

        # Scale by activation score (higher score = more likely to be activated)
        score_factor = (p.activation_score or 0) / 100

        annual = area * rate * util * score_factor
        total_revenue += annual

        agency = p.owner_agency or "other"
        by_agency[agency] = by_agency.get(agency, 0) + annual
        by_category[best_cat] = by_category.get(best_cat, 0) + annual

    return {
        "annual_revenue": total_revenue,
        "by_agency": by_agency,
        "by_category": by_category,
    }


def leveraged_value(db: Session) -> dict:
    """Projected leveraged value: bonds, TIF, grants, private investment."""
    act = activation_value(db)
    annual = act["annual_revenue"]
    stat = static_value(db)

    bond_capacity = annual * 12  # ~12x annual revenue (conservative municipal bond)
    tif_potential = stat["total_value"] * 0.15  # 15% of assessed value as TIF
    grant_match = annual * 2  # 2:1 federal/state grant match potential
    private_multiplier = annual * 5  # private investment attracted

    return {
        "bond_capacity": bond_capacity,
        "tif_potential": tif_potential,
        "grant_match": grant_match,
        "private_investment": private_multiplier,
        "total_leveraged": bond_capacity + tif_potential + grant_match + private_multiplier,
        "annual_activation_revenue": annual,
        "static_assessed_value": stat["total_value"],
        "maintenance_cost_estimate": stat["total_area_sqft"] * 0.50,  # $0.50/sqft/year
        "net_activation_benefit": annual - (stat["total_area_sqft"] * 0.50),
    }
