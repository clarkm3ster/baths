"""
Lifetime Fiscal Trajectory Archetypes
========================================

Five archetypes that classify an individual's lifetime net fiscal position
(taxes paid minus government spending consumed).  The DOME engine assigns
each simulated person to a trajectory and uses the associated ROI range to
estimate the cost-effectiveness of cascade-breaking interventions.

NPV values are expressed in current (2024) USD using a 3 % real discount rate.

Usage::

    from dome.data.fiscal_trajectories import FISCAL_TRAJECTORIES
    high_cost = next(t for t in FISCAL_TRAJECTORIES if t["name"] == "high_net_cost")

Sources:
    - CBO Distribution of Household Income and Federal Taxes
    - Urban Institute LifeSim microsimulation model
    - Raj Chetty et al. "Where is the Land of Opportunity?" mobility data
    - MACPAC super-utilizer analyses
"""

from __future__ import annotations

from typing import Any, Dict, List


FISCAL_TRAJECTORIES: List[Dict[str, Any]] = [
    # --------------------------------------------------------------------- 1
    {
        "name": "net_contributor",
        "display_name": "Net Contributor",
        "description": (
            "Individuals whose lifetime tax contributions substantially exceed "
            "government spending on their behalf.  Typically characterized by "
            "stable employment, employer-sponsored insurance, and minimal "
            "means-tested program utilization."
        ),
        "npv_min": 100_000,
        "npv_max": None,  # unbounded above
        "npv_description": "NPV > +$100K (lifetime net positive to government)",
        "typical_characteristics": [
            "Stable full-time employment across career",
            "Employer-sponsored health insurance for majority of working years",
            "Minimal means-tested program utilization",
            "Homeownership with mortgage-interest deduction usage",
            "Retirement income from Social Security plus private savings",
            "Medicare utilization in later years within normal cost range",
        ],
        "dome_roi_range": {"min": 2.0, "max": 3.0},
        "dome_roi_description": (
            "2:1 to 3:1 -- interventions here are preventive, keeping "
            "individuals from slipping into costlier trajectories"
        ),
        "population_prevalence": 0.40,
        "example_annual_tax_contribution": 18_000,
        "example_annual_govt_cost": 8_000,
        "cascade_risk": "low",
    },
    # --------------------------------------------------------------------- 2
    {
        "name": "break_even",
        "display_name": "Break-Even",
        "description": (
            "Individuals whose lifetime taxes paid roughly equal the government "
            "spending they consume.  Often experience periods of program "
            "dependence (unemployment, Medicaid) interspersed with employment."
        ),
        "npv_min": -50_000,
        "npv_max": 100_000,
        "npv_description": "NPV between -$50K and +$100K",
        "typical_characteristics": [
            "Intermittent employment with periodic unemployment spells",
            "Transitional Medicaid or ACA marketplace coverage",
            "Occasional SNAP or TANF usage during income gaps",
            "Moderate use of EITC and Child Tax Credit",
            "May use Section 8 housing for limited periods",
            "Low savings; Social Security is primary retirement income",
        ],
        "dome_roi_range": {"min": 3.0, "max": 5.0},
        "dome_roi_description": (
            "3:1 to 5:1 -- modest investment in income bridges and "
            "employment support prevents downward cascade"
        ),
        "population_prevalence": 0.25,
        "example_annual_tax_contribution": 10_000,
        "example_annual_govt_cost": 9_500,
        "cascade_risk": "moderate",
    },
    # --------------------------------------------------------------------- 3
    {
        "name": "moderate_net_cost",
        "display_name": "Moderate Net Cost",
        "description": (
            "Individuals who consume moderately more in government services "
            "than they contribute in taxes.  Chronic conditions, disability, "
            "or prolonged unemployment drive higher-than-average program "
            "enrollment."
        ),
        "npv_min": -500_000,
        "npv_max": -50_000,
        "npv_description": "NPV between -$500K and -$50K",
        "typical_characteristics": [
            "One or more chronic health conditions (diabetes, COPD, depression)",
            "SSDI or SSI receipt for part of working life",
            "Extended Medicaid enrollment",
            "Regular SNAP and possibly Section 8 utilization",
            "Limited work history or low-wage employment",
            "Higher-than-average ER utilization",
        ],
        "dome_roi_range": {"min": 5.0, "max": 10.0},
        "dome_roi_description": (
            "5:1 to 10:1 -- care coordination and chronic-disease management "
            "can significantly reduce downstream costs"
        ),
        "population_prevalence": 0.20,
        "example_annual_tax_contribution": 4_000,
        "example_annual_govt_cost": 18_000,
        "cascade_risk": "high",
    },
    # --------------------------------------------------------------------- 4
    {
        "name": "high_net_cost",
        "display_name": "High Net Cost",
        "description": (
            "Individuals with very high lifetime government costs driven by "
            "multi-system involvement: justice, behavioral health, housing "
            "instability, and chronic medical conditions.  Many are 'super-"
            "utilizers' in at least one system."
        ),
        "npv_min": -2_000_000,
        "npv_max": -500_000,
        "npv_description": "NPV between -$2M and -$500K",
        "typical_characteristics": [
            "Justice system involvement (incarceration, probation/parole)",
            "Chronic homelessness or severe housing instability",
            "Co-occurring mental health and substance use disorders",
            "Frequent ER visits and inpatient stays (super-utilizer pattern)",
            "Multi-program enrollment (Medicaid, SNAP, SSI, shelter, justice)",
            "Minimal lifetime tax contributions due to employment barriers",
        ],
        "dome_roi_range": {"min": 10.0, "max": 25.0},
        "dome_roi_description": (
            "10:1 to 25:1 -- housing-first, MAT, and supported employment "
            "can generate very large fiscal returns"
        ),
        "population_prevalence": 0.10,
        "example_annual_tax_contribution": 1_000,
        "example_annual_govt_cost": 55_000,
        "cascade_risk": "very_high",
    },
    # --------------------------------------------------------------------- 5
    {
        "name": "catastrophic_net_cost",
        "display_name": "Catastrophic Net Cost",
        "description": (
            "The highest-cost individuals in the population.  Lifetime "
            "government costs exceed $2 million, driven by decades of "
            "institutional placement (prison, psychiatric facilities, "
            "nursing homes) and crisis-driven healthcare.  Represents the "
            "top ~5 %% of the cost distribution."
        ),
        "npv_min": None,  # unbounded below
        "npv_max": -2_000_000,
        "npv_description": "NPV < -$2M (lifetime net cost exceeds $2 million)",
        "typical_characteristics": [
            "Multiple prison sentences (10+ cumulative years incarcerated)",
            "Chronic homelessness spanning decades",
            "Severe, persistent mental illness (schizophrenia, bipolar I)",
            "Poly-substance dependence with repeated treatment episodes",
            "Dozens of ER visits per year at peak utilization",
            "Long-term institutional placement (state psychiatric, nursing home)",
            "Near-zero lifetime tax contribution",
        ],
        "dome_roi_range": {"min": 25.0, "max": 50.0},
        "dome_roi_description": (
            "25:1 to 50:1 -- even modest reductions in institutional placement "
            "yield enormous fiscal savings; PACE, permanent supportive housing, "
            "and assertive community treatment are highest-value interventions"
        ),
        "population_prevalence": 0.05,
        "example_annual_tax_contribution": 0,
        "example_annual_govt_cost": 120_000,
        "cascade_risk": "extreme",
    },
]
"""list[dict]: Five lifetime fiscal trajectory archetypes.

Each entry contains:

- **name** / **display_name**: Machine and human-readable identifiers.
- **npv_min** / **npv_max**: Net present value range boundaries (``None``
  indicates an unbounded end).
- **typical_characteristics**: List of descriptive strings.
- **dome_roi_range**: ``{"min": float, "max": float}`` representing the
  expected ROI multiplier for DOME interventions targeting this trajectory.
- **population_prevalence**: Estimated share of the US population in this
  trajectory (sums to 1.0 across all five).
- **cascade_risk**: Qualitative risk level (low / moderate / high /
  very_high / extreme).
"""
