"""
Published Unit Costs for Government Services and Placements
=============================================================

Per-unit cost figures sourced from CMS, BJS, HUD, USDA, and other federal
agency publications.  Values represent national midpoint estimates in current
(2024) USD unless otherwise noted.

These costs feed into the fiscal-cascade engine to convert utilization events
(ER visits, jail days, shelter nights, etc.) into dollar amounts for NPV
calculations and ROI projections.

Usage::

    from dome.data.unit_costs import UNIT_COSTS
    er_cost = UNIT_COSTS["er_visit"]  # 2200

Sources:
    - CMS Medicare Provider Analysis & Review (MedPAR)
    - Bureau of Justice Statistics (BJS) annual expenditure reports
    - HUD Annual Homeless Assessment Report (AHAR)
    - USDA Food and Nutrition Service cost-per-participant data
    - Kaiser Family Foundation Medicaid spending estimates
    - Congressional Budget Office (CBO) baseline projections
"""

from __future__ import annotations

from typing import Dict


UNIT_COSTS: Dict[str, float] = {
    # -------------------------------------------------------------------------
    # Healthcare — Acute / Inpatient
    # -------------------------------------------------------------------------
    "er_visit": 2_200.00,
    "inpatient_day": 2_883.00,
    "icu_day": 5_800.00,
    "nursing_home_day": 290.00,
    "home_health_visit": 150.00,

    # -------------------------------------------------------------------------
    # Healthcare — Outpatient / Specialty
    # -------------------------------------------------------------------------
    "outpatient_visit": 350.00,
    "mental_health_session": 175.00,
    "substance_abuse_treatment_day": 200.00,
    "prescription_monthly": 150.00,
    "dental_visit": 200.00,
    "vision_exam": 150.00,
    "dme_monthly": 250.00,

    # -------------------------------------------------------------------------
    # Healthcare — Transport and Ancillary
    # -------------------------------------------------------------------------
    "ambulance_transport": 1_200.00,

    # -------------------------------------------------------------------------
    # Healthcare — Per-Beneficiary Annual Averages
    # -------------------------------------------------------------------------
    "medicaid_per_adult_annual": 16_500.00,
    "medicaid_per_child_annual": 4_000.00,
    "medicaid_per_disabled_annual": 22_000.00,
    "medicare_per_beneficiary_annual": 15_000.00,

    # -------------------------------------------------------------------------
    # Justice System
    # -------------------------------------------------------------------------
    "jail_day": 160.00,
    "prison_year": 47_500.00,
    "prison_day": 130.14,          # 47500 / 365
    "probation_annual": 4_500.00,
    "parole_annual": 5_200.00,
    "juvenile_detention_day": 410.00,
    "drug_court_episode": 5_000.00,

    # -------------------------------------------------------------------------
    # Housing / Shelter
    # -------------------------------------------------------------------------
    "shelter_night": 103.50,
    "section_8_voucher_annual": 11_500.00,
    "public_housing_unit_annual": 10_800.00,
    "permanent_supportive_housing_annual": 22_000.00,
    "rapid_rehousing_episode": 8_000.00,

    # -------------------------------------------------------------------------
    # Income Support
    # -------------------------------------------------------------------------
    "ssdi_annual": 21_000.00,
    "ssi_annual": 10_500.00,
    "tanf_annual": 6_500.00,
    "snap_per_person_monthly": 275.00,
    "snap_per_person_annual": 3_300.00,
    "wic_per_person_annual": 600.00,

    # -------------------------------------------------------------------------
    # Education
    # -------------------------------------------------------------------------
    "k12_per_pupil_annual": 16_000.00,
    "special_ed_additional_annual": 20_000.00,
    "head_start_per_child_annual": 11_000.00,
    "pell_grant_average": 4_600.00,

    # -------------------------------------------------------------------------
    # Employment / Workforce
    # -------------------------------------------------------------------------
    "unemployment_insurance_weekly": 380.00,
    "job_corps_per_participant_annual": 32_000.00,
    "vocational_rehab_per_case": 7_500.00,

    # -------------------------------------------------------------------------
    # Child Welfare
    # -------------------------------------------------------------------------
    "foster_care_monthly": 2_000.00,
    "foster_care_annual": 24_000.00,
    "adoption_assistance_annual": 10_000.00,
    "child_care_subsidy_annual": 8_500.00,

    # -------------------------------------------------------------------------
    # Energy / Utilities
    # -------------------------------------------------------------------------
    "liheap_average_benefit": 500.00,
    "weatherization_per_home": 7_500.00,
}
"""dict[str, float]: National midpoint unit costs in current USD.

Keys follow a ``snake_case`` naming convention. Values are expressed in
nominal 2024 dollars. The cascade engine applies inflation adjustment via
:data:`dome.data.population_baselines.POPULATION_BASELINES["inflation_rate"]`
when projecting future-year costs.
"""
