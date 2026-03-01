"""
Intervention Definitions for THE DOME
========================================

Evidence-based interventions catalogued by the cascade link they target,
their cost envelope, expected probability of breaking the cascade, and
time-to-effect.  Each intervention maps to one or more ``cause->effect``
link labels used in :mod:`dome.data.cascades`.

The DOME engine uses these definitions to simulate counterfactual
scenarios: "What happens if we apply intervention X at link Y?"

There are 12 core interventions covering all six cascades, ensuring that
every cascade link with a viable evidence-based response has at least one
matching intervention.

Usage::

    from dome.data.interventions import INTERVENTION_DEFINITIONS
    housing = next(
        i for i in INTERVENTION_DEFINITIONS
        if i.intervention_id == "housing_first"
    )
    print(housing.break_probability)  # 0.65

    # Get all interventions for a cascade link
    from dome.data.interventions import INTERVENTION_INDEX
    options = INTERVENTION_INDEX["substance_use->medical_crisis"]

Sources:
    - MDRC WorkAdvance and emergency cash-transfer evaluations
    - Butler et al. (2006) CBT meta-analysis for depression outcomes
    - Aizer et al. (2018) Lead remediation cost-benefit analysis
    - Stefancic & Tsemberis (2007) Housing First randomized trial
    - Larimer et al. (2009) Housing First cost outcomes
    - Mattick et al. (2014) Methadone and buprenorphine meta-analysis
    - Bond et al. (2008) IPS Supported Employment 27-RCT review
    - Henwood et al. (2015) Rapid rehousing evaluation
    - Brown et al. (2019) Care coordination for high utilizers
    - Heckman et al. (2010) Perry Preschool long-term follow-up
    - Lattimore & Visher (2021) SVORI reentry program evaluation
    - Liddle et al. (2018) MDFT family therapy outcomes
    - ALA (2023) Pulmonary rehabilitation evidence base
"""

from __future__ import annotations

from typing import Dict, List

from dome.models.intervention import InterventionDefinition


INTERVENTION_DEFINITIONS: list[InterventionDefinition] = [
    # ================================================================== 1
    # INCOME BRIDGE
    # Targets: job_loss -> depression (econ_psych_bio_fiscal link 0)
    # ================================================================== 1
    InterventionDefinition(
        intervention_id="income_bridge",
        name="Income Bridge / Emergency Cash Transfer",
        cost_min=3_000.0,
        cost_max=8_000.0,
        targets_cascade_link="job_loss->depression",
        break_probability=0.55,
        time_to_effect_months=3.0,
    ),
    # ================================================================== 2
    # CBT THERAPY
    # Targets: depression -> chronic_disease (econ_psych_bio_fiscal link 1)
    # ================================================================== 2
    InterventionDefinition(
        intervention_id="cbt_therapy",
        name="Cognitive Behavioral Therapy (CBT)",
        cost_min=2_000.0,
        cost_max=6_000.0,
        targets_cascade_link="depression->chronic_disease",
        break_probability=0.45,
        time_to_effect_months=6.0,
    ),
    # ================================================================== 3
    # LEAD REMEDIATION
    # Targets: lead_exposure -> cognitive_impairment (env_cog_edu_econ_fiscal link 0)
    # ================================================================== 3
    InterventionDefinition(
        intervention_id="lead_remediation",
        name="Residential Lead Hazard Remediation",
        cost_min=5_000.0,
        cost_max=15_000.0,
        targets_cascade_link="lead_exposure->cognitive_impairment",
        break_probability=0.80,
        time_to_effect_months=1.0,
    ),
    # ================================================================== 4
    # HOUSING FIRST
    # Targets: housing_instability -> health_deterioration (legal cascade link 3)
    # ================================================================== 4
    InterventionDefinition(
        intervention_id="housing_first",
        name="Housing First / Permanent Supportive Housing",
        cost_min=12_000.0,
        cost_max=22_000.0,
        targets_cascade_link="housing_instability->health_deterioration",
        break_probability=0.65,
        time_to_effect_months=3.0,
    ),
    # ================================================================== 5
    # MAT (MEDICATION-ASSISTED TREATMENT)
    # Targets: substance_use -> medical_crisis (social_psych_bio_fiscal link 2)
    # ================================================================== 5
    InterventionDefinition(
        intervention_id="mat_treatment",
        name="Medication-Assisted Treatment (MAT)",
        cost_min=5_000.0,
        cost_max=15_000.0,
        targets_cascade_link="substance_use->medical_crisis",
        break_probability=0.50,
        time_to_effect_months=6.0,
    ),
    # ================================================================== 6
    # SUPPORTED EMPLOYMENT (IPS MODEL)
    # Targets: employment_barrier -> social_isolation (legal cascade link 1)
    # ================================================================== 6
    InterventionDefinition(
        intervention_id="supported_employment",
        name="Individual Placement and Support (IPS) Supported Employment",
        cost_min=4_000.0,
        cost_max=10_000.0,
        targets_cascade_link="employment_barrier->social_isolation",
        break_probability=0.45,
        time_to_effect_months=6.0,
    ),
    # ================================================================== 7
    # RAPID REHOUSING
    # Targets: social_isolation -> housing_instability (legal cascade link 2)
    # ================================================================== 7
    InterventionDefinition(
        intervention_id="rapid_rehousing",
        name="Rapid Rehousing Program",
        cost_min=6_000.0,
        cost_max=14_000.0,
        targets_cascade_link="social_isolation->housing_instability",
        break_probability=0.55,
        time_to_effect_months=2.0,
    ),
    # ================================================================== 8
    # CARE COORDINATION
    # Targets: chronic_disease -> high_utilization (econ_psych_bio_fiscal link 2)
    # ================================================================== 8
    InterventionDefinition(
        intervention_id="care_coordination",
        name="Intensive Care Coordination / Health Home",
        cost_min=3_000.0,
        cost_max=8_000.0,
        targets_cascade_link="chronic_disease->high_utilization",
        break_probability=0.40,
        time_to_effect_months=3.0,
    ),
    # ================================================================== 9
    # EARLY CHILDHOOD EDUCATION
    # Targets: cognitive_impairment -> educational_failure (env_cog_edu_econ_fiscal link 1)
    # ================================================================== 9
    InterventionDefinition(
        intervention_id="early_childhood_ed",
        name="High-Quality Early Childhood Education",
        cost_min=8_000.0,
        cost_max=20_000.0,
        targets_cascade_link="cognitive_impairment->educational_failure",
        break_probability=0.50,
        time_to_effect_months=12.0,
    ),
    # ================================================================== 10
    # REENTRY SERVICES
    # Targets: incarceration -> employment_barrier (legal cascade link 0)
    # ================================================================== 10
    InterventionDefinition(
        intervention_id="reentry_services",
        name="Comprehensive Reentry Services",
        cost_min=4_000.0,
        cost_max=12_000.0,
        targets_cascade_link="incarceration->employment_barrier",
        break_probability=0.45,
        time_to_effect_months=6.0,
    ),
    # ================================================================== 11
    # FAMILY THERAPY
    # Targets: family_stress -> substance_use (econ_social_legal_fiscal link 1)
    # ================================================================== 11
    InterventionDefinition(
        intervention_id="family_therapy",
        name="Multidimensional Family Therapy (MDFT)",
        cost_min=3_000.0,
        cost_max=8_000.0,
        targets_cascade_link="family_stress->substance_use",
        break_probability=0.40,
        time_to_effect_months=6.0,
    ),
    # ================================================================== 12
    # RESPITE CARE / PULMONARY REHABILITATION
    # Targets: respiratory_disease -> work_limitation (env_bio_econ_fiscal link 1)
    # ================================================================== 12
    InterventionDefinition(
        intervention_id="respite_care",
        name="Pulmonary Rehabilitation and Occupational Respite",
        cost_min=2_000.0,
        cost_max=6_000.0,
        targets_cascade_link="respiratory_disease->work_limitation",
        break_probability=0.35,
        time_to_effect_months=3.0,
    ),
]
"""list[InterventionDefinition]: Twelve evidence-based interventions.

Each intervention specifies the cascade link it targets (in ``cause->effect``
format), its cost range, the probability of successfully breaking the link,
and the expected months until the intervention takes full effect.

Interventions by cascade:
    - **econ_psych_bio_fiscal**: income_bridge, cbt_therapy, care_coordination
    - **env_cog_edu_econ_fiscal**: lead_remediation, early_childhood_ed
    - **legal_econ_social_geo_bio_fiscal**: reentry_services, supported_employment, rapid_rehousing, housing_first
    - **social_psych_bio_fiscal**: mat_treatment
    - **env_bio_econ_fiscal**: respite_care
    - **econ_social_legal_fiscal**: family_therapy
"""


# -------------------------------------------------------------------------
# Convenience index: link label -> list of interventions targeting that link
# -------------------------------------------------------------------------
INTERVENTION_INDEX: Dict[str, List[InterventionDefinition]] = {}
"""dict mapping ``cause->effect`` link labels to interventions that target them."""

for _intv in INTERVENTION_DEFINITIONS:
    INTERVENTION_INDEX.setdefault(_intv.targets_cascade_link, []).append(_intv)


def get_intervention(intervention_id: str) -> InterventionDefinition:
    """Look up an intervention by its ID.

    Parameters
    ----------
    intervention_id:
        Unique intervention identifier (e.g. ``"housing_first"``).

    Returns
    -------
    InterventionDefinition
        The matching intervention.

    Raises
    ------
    KeyError
        If no intervention with the given ID exists.
    """
    for intv in INTERVENTION_DEFINITIONS:
        if intv.intervention_id == intervention_id:
            return intv
    raise KeyError(f"No intervention with id '{intervention_id}'")


def interventions_for_link(link_label: str) -> List[InterventionDefinition]:
    """Return all interventions targeting a given cascade link.

    Parameters
    ----------
    link_label:
        A link label in ``"cause->effect"`` format
        (e.g. ``"job_loss->depression"``).

    Returns
    -------
    list[InterventionDefinition]
        All interventions targeting this link (may be empty).
    """
    return INTERVENTION_INDEX.get(link_label, [])
