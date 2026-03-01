"""
Cascade Definitions for THE DOME
==================================

Six canonical cascade types that model the most common adverse-event chains
observed in cross-system data.  Each cascade is an ordered list of
``CascadeLink`` objects describing cause-effect transitions with empirically
grounded transition probabilities, lag windows, and evidence-strength scores.

Each cascade represents a documented causal pathway through which an initial
adverse event propagates across DOME layers, accumulating fiscal impact at
each stage.  The six cascades collectively cover the primary pathways by
which individuals transition from self-sufficiency into high-cost program
utilization.

Usage::

    from dome.data.cascades import CASCADE_DEFINITIONS
    econ_cascade = CASCADE_DEFINITIONS[0]  # econ_psych_bio_fiscal

    # Look up by ID
    from dome.data.cascades import get_cascade
    legal_cascade = get_cascade("legal_econ_social_geo_bio_fiscal")

Sources:
    - Paul & Moser (2009) "Unemployment impairs mental health" -- meta-analysis
    - Katon (2011) "Epidemiology and treatment of depression in diabetes"
    - Lanphear et al. (2005) "Low-level lead exposure and children's IQ"
    - Needleman et al. (2004) "Lead exposure and educational outcomes"
    - Pager (2003) "The Mark of a Criminal Record"
    - Western (2018) "Homeward: Life in the Year After Prison"
    - Cacioppo & Hawkley (2009) "Social isolation and health"
    - Holt-Lunstad et al. (2015) "Loneliness and social isolation as risk factors"
    - EPA Integrated Science Assessments for criteria pollutants
    - Conger et al. (2002) "The Family Stress Model"
    - Dube et al. (2006) "Adverse childhood experiences and substance use"
    - Bureau of Justice Statistics recidivism studies (2023)
    - HUD Annual Homeless Assessment Report (AHAR)
    - Fazel et al. (2014) "Health of homeless people"
    - Culhane et al. (2002) "Public service reductions with Housing First"
"""

from __future__ import annotations

from typing import Any, Dict, List

from dome.models.cascade import CascadeDefinition, CascadeLink


CASCADE_DEFINITIONS: list[CascadeDefinition] = [
    # ================================================================== 1
    # econ_psych_bio_fiscal
    # Economic -> Psychological -> Biological -> Fiscal
    # job_loss -> depression -> chronic_disease -> high_utilization
    # ================================================================== 1
    CascadeDefinition(
        cascade_id="econ_psych_bio_fiscal",
        name="Economic-Psychological-Biomedical Fiscal Cascade",
        links=[
            CascadeLink(
                cause="job_loss",
                effect="depression",
                probability=0.45,
                lag_months_min=1,
                lag_months_max=6,
                strength=0.6,
            ),
            CascadeLink(
                cause="depression",
                effect="chronic_disease",
                probability=0.30,
                lag_months_min=6,
                lag_months_max=24,
                strength=0.5,
            ),
            CascadeLink(
                cause="chronic_disease",
                effect="high_utilization",
                probability=0.60,
                lag_months_min=3,
                lag_months_max=12,
                strength=0.7,
            ),
        ],
    ),
    # ================================================================== 2
    # env_cog_edu_econ_fiscal
    # Environmental -> Cognitive -> Educational -> Economic -> Fiscal
    # lead_exposure -> cognitive_impairment -> educational_failure
    #   -> low_earnings -> program_dependence
    # ================================================================== 2
    CascadeDefinition(
        cascade_id="env_cog_edu_econ_fiscal",
        name="Environmental-Cognitive-Educational-Economic Fiscal Cascade",
        links=[
            CascadeLink(
                cause="lead_exposure",
                effect="cognitive_impairment",
                probability=0.35,
                lag_months_min=12,
                lag_months_max=60,
                strength=0.5,
            ),
            CascadeLink(
                cause="cognitive_impairment",
                effect="educational_failure",
                probability=0.40,
                lag_months_min=12,
                lag_months_max=48,
                strength=0.6,
            ),
            CascadeLink(
                cause="educational_failure",
                effect="low_earnings",
                probability=0.55,
                lag_months_min=60,
                lag_months_max=120,
                strength=0.7,
            ),
            CascadeLink(
                cause="low_earnings",
                effect="program_dependence",
                probability=0.50,
                lag_months_min=6,
                lag_months_max=24,
                strength=0.5,
            ),
        ],
    ),
    # ================================================================== 3
    # legal_econ_social_geo_bio_fiscal
    # Legal -> Economic -> Social -> Geographic -> Biological -> Fiscal
    # incarceration -> employment_barrier -> social_isolation
    #   -> housing_instability -> health_deterioration -> high_cost_utilization
    # ================================================================== 3
    CascadeDefinition(
        cascade_id="legal_econ_social_geo_bio_fiscal",
        name="Legal-Economic-Social-Geographic-Biomedical Fiscal Cascade",
        links=[
            CascadeLink(
                cause="incarceration",
                effect="employment_barrier",
                probability=0.70,
                lag_months_min=0,
                lag_months_max=6,
                strength=0.8,
            ),
            CascadeLink(
                cause="employment_barrier",
                effect="social_isolation",
                probability=0.45,
                lag_months_min=3,
                lag_months_max=12,
                strength=0.5,
            ),
            CascadeLink(
                cause="social_isolation",
                effect="housing_instability",
                probability=0.40,
                lag_months_min=1,
                lag_months_max=6,
                strength=0.5,
            ),
            CascadeLink(
                cause="housing_instability",
                effect="health_deterioration",
                probability=0.50,
                lag_months_min=3,
                lag_months_max=18,
                strength=0.6,
            ),
            CascadeLink(
                cause="health_deterioration",
                effect="high_cost_utilization",
                probability=0.55,
                lag_months_min=1,
                lag_months_max=12,
                strength=0.7,
            ),
        ],
    ),
    # ================================================================== 4
    # social_psych_bio_fiscal
    # Social -> Psychological -> Biological -> Fiscal
    # social_isolation -> depression -> substance_use -> medical_crisis
    # ================================================================== 4
    CascadeDefinition(
        cascade_id="social_psych_bio_fiscal",
        name="Social-Psychological-Biomedical Fiscal Cascade",
        links=[
            CascadeLink(
                cause="social_isolation",
                effect="depression",
                probability=0.40,
                lag_months_min=1,
                lag_months_max=12,
                strength=0.5,
            ),
            CascadeLink(
                cause="depression",
                effect="substance_use",
                probability=0.30,
                lag_months_min=3,
                lag_months_max=12,
                strength=0.5,
            ),
            CascadeLink(
                cause="substance_use",
                effect="medical_crisis",
                probability=0.45,
                lag_months_min=1,
                lag_months_max=6,
                strength=0.7,
            ),
        ],
    ),
    # ================================================================== 5
    # env_bio_econ_fiscal
    # Environmental -> Biological -> Economic -> Fiscal
    # environmental_hazard -> respiratory_disease -> work_limitation -> income_loss
    # ================================================================== 5
    CascadeDefinition(
        cascade_id="env_bio_econ_fiscal",
        name="Environmental-Biomedical-Economic Fiscal Cascade",
        links=[
            CascadeLink(
                cause="environmental_hazard",
                effect="respiratory_disease",
                probability=0.25,
                lag_months_min=6,
                lag_months_max=36,
                strength=0.4,
            ),
            CascadeLink(
                cause="respiratory_disease",
                effect="work_limitation",
                probability=0.35,
                lag_months_min=3,
                lag_months_max=12,
                strength=0.5,
            ),
            CascadeLink(
                cause="work_limitation",
                effect="income_loss",
                probability=0.50,
                lag_months_min=1,
                lag_months_max=6,
                strength=0.6,
            ),
        ],
    ),
    # ================================================================== 6
    # econ_social_legal_fiscal
    # Economic -> Social -> Legal -> Fiscal
    # poverty -> family_stress -> substance_use -> justice_involvement
    #   -> incarceration_cost
    # ================================================================== 6
    CascadeDefinition(
        cascade_id="econ_social_legal_fiscal",
        name="Economic-Social-Legal Fiscal Cascade",
        links=[
            CascadeLink(
                cause="poverty",
                effect="family_stress",
                probability=0.50,
                lag_months_min=1,
                lag_months_max=6,
                strength=0.5,
            ),
            CascadeLink(
                cause="family_stress",
                effect="substance_use",
                probability=0.25,
                lag_months_min=3,
                lag_months_max=12,
                strength=0.4,
            ),
            CascadeLink(
                cause="substance_use",
                effect="justice_involvement",
                probability=0.30,
                lag_months_min=1,
                lag_months_max=12,
                strength=0.6,
            ),
            CascadeLink(
                cause="justice_involvement",
                effect="incarceration_cost",
                probability=0.40,
                lag_months_min=1,
                lag_months_max=6,
                strength=0.7,
            ),
        ],
    ),
]
"""list[CascadeDefinition]: The six canonical cascade definitions.

Each definition contains an ordered list of :class:`CascadeLink` objects.
Transition probabilities are derived from published longitudinal studies
and adjusted for the general US population.

Cascades:
    1. ``econ_psych_bio_fiscal`` -- Job loss -> Depression -> Chronic disease -> High utilization
    2. ``env_cog_edu_econ_fiscal`` -- Lead exposure -> Cognitive impairment -> Ed failure -> Low earnings -> Program dependence
    3. ``legal_econ_social_geo_bio_fiscal`` -- Incarceration -> Employment barrier -> Social isolation -> Housing instability -> Health deterioration -> High-cost utilization
    4. ``social_psych_bio_fiscal`` -- Social isolation -> Depression -> Substance use -> Medical crisis
    5. ``env_bio_econ_fiscal`` -- Environmental hazard -> Respiratory disease -> Work limitation -> Income loss
    6. ``econ_social_legal_fiscal`` -- Poverty -> Family stress -> Substance use -> Justice involvement -> Incarceration cost
"""


# -------------------------------------------------------------------------
# Convenience index and helpers
# -------------------------------------------------------------------------

CASCADE_INDEX: Dict[str, CascadeDefinition] = {
    c.cascade_id: c for c in CASCADE_DEFINITIONS
}
"""dict mapping cascade_id to CascadeDefinition for O(1) lookup."""


def get_cascade(cascade_id: str) -> CascadeDefinition:
    """Look up a cascade definition by its ID.

    Parameters
    ----------
    cascade_id:
        One of the six cascade identifiers
        (e.g. ``"econ_psych_bio_fiscal"``).

    Returns
    -------
    CascadeDefinition
        The matching cascade definition.

    Raises
    ------
    KeyError
        If no cascade with the given ID exists.
    """
    try:
        return CASCADE_INDEX[cascade_id]
    except KeyError:
        raise KeyError(
            f"No cascade with id '{cascade_id}'. "
            f"Valid IDs: {list(CASCADE_INDEX.keys())}"
        )


def get_link(cascade_id: str, cause: str, effect: str) -> CascadeLink:
    """Look up a specific link within a cascade by cause->effect labels.

    Parameters
    ----------
    cascade_id:
        The cascade identifier.
    cause:
        The cause label (e.g. ``"job_loss"``).
    effect:
        The effect label (e.g. ``"depression"``).

    Returns
    -------
    CascadeLink
        The matching link.

    Raises
    ------
    KeyError
        If the cascade or link is not found.
    """
    cascade = get_cascade(cascade_id)
    for link in cascade.links:
        if link.cause == cause and link.effect == effect:
            return link
    raise KeyError(
        f"No link '{cause}->{effect}' in cascade '{cascade_id}'"
    )


def all_link_labels() -> List[str]:
    """Return a flat list of every ``cause->effect`` label across all cascades.

    Useful for validating intervention ``targets_cascade_link`` references.

    Returns
    -------
    list[str]
        Labels in ``"cause->effect"`` format.
    """
    labels: List[str] = []
    for cascade in CASCADE_DEFINITIONS:
        for link in cascade.links:
            labels.append(f"{link.cause}->{link.effect}")
    return labels
