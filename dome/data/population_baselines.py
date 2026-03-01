"""
Population-Level Fiscal and Demographic Baselines
====================================================

Aggregate per-capita and population-wide parameters used by the DOME
fiscal-cascade engine to anchor individual-level simulations against
national averages.

All monetary values are in current (2024) USD.  Rates are expressed as
annual decimals (e.g. 0.025 = 2.5 %).

Usage::

    from dome.data.population_baselines import POPULATION_BASELINES
    discount = POPULATION_BASELINES["real_discount_rate"]  # 0.03

Sources:
    - Congressional Budget Office (CBO) Long-Term Budget Outlook
    - Bureau of Economic Analysis (BEA) Government Expenditure tables
    - CMS National Health Expenditure Accounts (NHEA)
    - Social Security Administration Actuarial tables
    - Census Bureau Current Population Survey (CPS)
    - HUD Annual Homeless Assessment Report (AHAR)
"""

from __future__ import annotations

from typing import Dict, Union


POPULATION_BASELINES: Dict[str, Union[float, int]] = {
    # -------------------------------------------------------------------------
    # Government Spending Per Capita
    # -------------------------------------------------------------------------
    "federal_spend_per_person_annual": 20_600.00,
    "state_spend_per_person_annual": 10_800.00,
    "local_spend_per_person_annual": 7_200.00,
    "total_govt_spend_per_person_annual": 38_600.00,  # sum of above three

    # -------------------------------------------------------------------------
    # Lifetime Fiscal Averages (undiscounted, in current USD)
    # -------------------------------------------------------------------------
    "average_lifetime_taxes_paid": 524_625.00,
    "average_lifetime_healthcare_spending": 316_600.00,
    "average_lifetime_govt_transfers_annual": 11_500.00,

    # -------------------------------------------------------------------------
    # Super-Utilizer Thresholds
    # -------------------------------------------------------------------------
    # The top 5 % of Medicaid enrollees account for ~54 % of total Medicaid
    # spending (MACPAC analysis of MAX/T-MSIS data).
    "super_utilizer_threshold_pct": 5,
    "super_utilizer_medicaid_spend_share": 0.54,

    # -------------------------------------------------------------------------
    # Chronic Homelessness
    # -------------------------------------------------------------------------
    # Includes shelter, ER, justice, and behavioral-health costs accumulated
    # by an individual experiencing chronic homelessness over a 12-month
    # period.  Midpoint of $30K-$50K range from published cost studies.
    "chronic_homelessness_annual_cost": 40_000.00,

    # -------------------------------------------------------------------------
    # Demographic / Actuarial
    # -------------------------------------------------------------------------
    "average_life_expectancy": 78.6,
    "median_age": 38.9,
    "total_us_population": 335_000_000,
    "labor_force_participation_rate": 0.624,
    "poverty_rate": 0.114,
    "uninsured_rate": 0.08,

    # -------------------------------------------------------------------------
    # Discount and Inflation
    # -------------------------------------------------------------------------
    "inflation_rate": 0.025,
    "real_discount_rate": 0.03,
    "nominal_discount_rate": 0.055,  # real + inflation, approximate

    # -------------------------------------------------------------------------
    # Healthcare Utilization Averages
    # -------------------------------------------------------------------------
    "avg_er_visits_per_person_annual": 0.43,
    "avg_inpatient_days_per_person_annual": 0.56,
    "avg_outpatient_visits_per_person_annual": 4.2,
    "avg_prescriptions_per_person_annual": 12.0,

    # -------------------------------------------------------------------------
    # Justice System Averages
    # -------------------------------------------------------------------------
    "incarceration_rate_per_100k": 531,
    "recidivism_rate_3yr": 0.44,

    # -------------------------------------------------------------------------
    # Housing
    # -------------------------------------------------------------------------
    "homelessness_point_in_time_count": 653_000,
    "chronic_homeless_count": 127_000,
    "avg_rent_burden_pct": 0.30,  # 30 % of income

    # -------------------------------------------------------------------------
    # Program Enrollment Aggregates (approximate millions)
    # -------------------------------------------------------------------------
    "medicaid_enrollees_millions": 93.0,
    "medicare_enrollees_millions": 67.0,
    "snap_participants_millions": 42.0,
    "section_8_households_millions": 2.3,
    "ssdi_beneficiaries_millions": 7.6,
    "ssi_recipients_millions": 7.5,
}
"""dict[str, float | int]: Population-level baselines.

Monetary values are in nominal 2024 USD.  Rates and shares are expressed as
decimals (0.0-1.0) or per-100K where noted.  Counts are integers or floats
(millions) per the key suffix.
"""
