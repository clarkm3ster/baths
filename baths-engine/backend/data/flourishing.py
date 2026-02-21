"""
Flourishing Frameworks — Real philosophical and measurement frameworks
for what human flourishing means and how to measure it.

The DOMES game doesn't just coordinate services — it defines what
coordination is FOR. These frameworks ground the dome's purpose
in real intellectual traditions.
"""

# ── Flourishing Frameworks ────────────────────────────────────────────

FRAMEWORKS = [
    {
        "id": "nussbaum_capabilities",
        "name": "Martha Nussbaum's Central Capabilities",
        "tradition": "Capabilities Approach (Aristotelian / Liberal)",
        "source": "Nussbaum, M. (2011). Creating Capabilities: The Human Development Approach. Harvard UP.",
        "description": "Ten central capabilities that a just society must secure for all "
                       "citizens at a threshold level. The political goal is not to maximize "
                       "but to ensure each person reaches the threshold.",
        "capabilities": [
            {"name": "Life", "description": "Being able to live to the end of a human life of normal length",
             "dome_relevance": "Healthcare dome ensures access to care that preserves life",
             "indicators": ["life_expectancy", "infant_mortality", "preventable_death_rate"]},
            {"name": "Bodily Health", "description": "Being able to have good health, including reproductive health, adequate nourishment, adequate shelter",
             "dome_relevance": "Healthcare + Housing + Food domes directly",
             "indicators": ["chronic_disease_prevalence", "nutrition_status", "housing_quality"]},
            {"name": "Bodily Integrity", "description": "Being able to move freely; secure against assault including sexual assault and domestic violence",
             "dome_relevance": "Justice dome — safety from violence; housing security",
             "indicators": ["violent_crime_rate", "DV_incidence", "incarceration_rate"]},
            {"name": "Senses, Imagination, Thought", "description": "Being able to use senses, imagine, think, and reason — in a truly human way informed by education",
             "dome_relevance": "Education dome — access to learning that enables full human expression",
             "indicators": ["literacy_rate", "educational_attainment", "arts_participation"]},
            {"name": "Emotions", "description": "Being able to have attachments to things and people; not having emotional development blighted by fear and anxiety",
             "dome_relevance": "Healthcare (behavioral health) + Housing (stability) domes",
             "indicators": ["mental_health_prevalence", "social_connectedness", "ACE_scores"]},
            {"name": "Practical Reason", "description": "Being able to form a conception of the good and engage in critical reflection about planning one's life",
             "dome_relevance": "The dome itself — enabling people to plan rather than just survive",
             "indicators": ["agency_measures", "future_orientation", "goal_setting"]},
            {"name": "Affiliation", "description": "Being able to live with and toward others; having social bases of self-respect and non-humiliation",
             "dome_relevance": "All domes — dignity in how services are delivered",
             "indicators": ["social_capital", "discrimination_indices", "community_belonging"]},
            {"name": "Other Species", "description": "Being able to live with concern for animals, plants, and nature",
             "dome_relevance": "Environmental dimensions of sphere activation",
             "indicators": ["green_space_access", "environmental_quality"]},
            {"name": "Play", "description": "Being able to laugh, play, and enjoy recreational activities",
             "dome_relevance": "Beyond survival — the flourishing purpose of coordination",
             "indicators": ["leisure_time", "recreation_access", "life_satisfaction"]},
            {"name": "Control Over Environment", "description": "Political: being able to participate effectively in political choices. Material: being able to hold property and seek employment on equal basis",
             "dome_relevance": "Income + Employment + Housing domes — material foundation",
             "indicators": ["voter_participation", "property_ownership", "employment_rate", "wage_levels"]},
        ],
    },
    {
        "id": "sen_capabilities",
        "name": "Amartya Sen's Capability Approach",
        "tradition": "Development Economics / Freedom-Centered",
        "source": "Sen, A. (1999). Development as Freedom. Knopf.",
        "description": "Freedom is both the primary end and principal means of development. "
                       "Capabilities are the substantive freedoms a person has to achieve "
                       "functionings they value. Unlike Nussbaum, Sen deliberately does not "
                       "provide a fixed list — the relevant capabilities should emerge from "
                       "democratic deliberation in each context.",
        "key_concepts": [
            {"name": "Functionings", "description": "What a person actually does and is — beings and doings (being nourished, being housed, participating in community)",
             "dome_relevance": "Each dome dimension maps to a functioning"},
            {"name": "Capabilities", "description": "The real freedom to achieve functionings — not just outcomes but the range of options available",
             "dome_relevance": "The dome expands capability sets, not just delivers services"},
            {"name": "Agency", "description": "The ability to act on behalf of what you value — not being a passive recipient",
             "dome_relevance": "Person-centered coordination must enhance agency, not just compliance"},
            {"name": "Conversion Factors", "description": "Personal, social, and environmental factors that affect converting resources into capabilities",
             "dome_relevance": "Coordination addresses conversion factors — why $X in benefits doesn't produce $X in capability"},
        ],
    },
    {
        "id": "oecd_better_life",
        "name": "OECD Better Life Index",
        "tradition": "International Development / Measurement",
        "source": "OECD (2020). How's Life? Measuring Well-being. OECD Publishing.",
        "description": "11 dimensions of well-being measured across OECD countries. "
                       "Each dimension has 1-4 headline indicators. The US ranks highly on "
                       "income and housing space but poorly on health, work-life balance, "
                       "and safety — consistent with the BATHS thesis that raw resources "
                       "without coordination underperform.",
        "dimensions": [
            {"name": "Housing", "value_us": 7.9, "value_oecd_avg": 6.6, "indicators": ["rooms_per_person", "housing_expenditure", "basic_facilities"]},
            {"name": "Income", "value_us": 10.0, "value_oecd_avg": 5.5, "indicators": ["household_net_adjusted_disposable_income", "household_net_wealth"]},
            {"name": "Jobs", "value_us": 7.5, "value_oecd_avg": 6.5, "indicators": ["employment_rate", "long_term_unemployment", "personal_earnings"]},
            {"name": "Community", "value_us": 7.3, "value_oecd_avg": 6.3, "indicators": ["quality_of_support_network"]},
            {"name": "Education", "value_us": 7.1, "value_oecd_avg": 6.2, "indicators": ["educational_attainment", "student_skills", "years_in_education"]},
            {"name": "Environment", "value_us": 6.9, "value_oecd_avg": 6.2, "indicators": ["air_pollution", "water_quality"]},
            {"name": "Civic Engagement", "value_us": 7.1, "value_oecd_avg": 5.5, "indicators": ["voter_turnout", "stakeholder_engagement"]},
            {"name": "Health", "value_us": 5.5, "value_oecd_avg": 6.9, "indicators": ["life_expectancy", "self_reported_health"]},
            {"name": "Life Satisfaction", "value_us": 6.9, "value_oecd_avg": 6.5, "indicators": ["life_satisfaction_score"]},
            {"name": "Safety", "value_us": 4.8, "value_oecd_avg": 7.8, "indicators": ["homicide_rate", "assault_rate", "feeling_safe_at_night"]},
            {"name": "Work-Life Balance", "value_us": 5.2, "value_oecd_avg": 6.4, "indicators": ["employees_working_long_hours", "time_devoted_to_leisure"]},
        ],
    },
    {
        "id": "gnh",
        "name": "Gross National Happiness (Bhutan)",
        "tradition": "Buddhist Economics / Holistic Measurement",
        "source": "Centre for Bhutan & GNH Studies. GNH Index methodology.",
        "description": "Nine domains measured through 33 indicators in the GNH Index. "
                       "A person is 'happy' if they achieve sufficiency in 6+ of 9 domains. "
                       "Policy is evaluated by whether it increases the percentage of people "
                       "who are happy and the breadth of sufficiency among the not-yet-happy.",
        "domains": [
            {"name": "Living Standards", "dome_map": ["income", "housing"]},
            {"name": "Health", "dome_map": ["healthcare"]},
            {"name": "Education", "dome_map": ["education"]},
            {"name": "Governance", "dome_map": ["interoperability"]},
            {"name": "Ecological Diversity & Resilience", "dome_map": []},
            {"name": "Time Use", "dome_map": ["employment"]},
            {"name": "Psychological Well-being", "dome_map": ["healthcare"]},
            {"name": "Community Vitality", "dome_map": ["housing"]},
            {"name": "Cultural Resilience & Promotion", "dome_map": []},
        ],
    },
    {
        "id": "maslow_extended",
        "name": "Maslow's Hierarchy (Extended for Systems Design)",
        "tradition": "Humanistic Psychology",
        "source": "Maslow, A. (1943). A Theory of Human Motivation. Psychological Review, 50(4).",
        "description": "The classic hierarchy reframed as a systems design principle: "
                       "coordination must address lower levels before higher ones become "
                       "accessible. A person cannot engage in job training (esteem) while "
                       "food-insecure (physiological) or housing-unstable (safety).",
        "levels": [
            {"level": 1, "name": "Physiological", "dome_dimensions": ["food", "healthcare"],
             "systems_needed": ["USDA_SNAP", "CMS_MMIS"],
             "insight": "Cannot address any other need until nutrition and basic health are met"},
            {"level": 2, "name": "Safety", "dome_dimensions": ["housing", "income", "justice"],
             "systems_needed": ["HUD_IMS_PIC", "HUD_HMIS", "SSA_SSR", "DOJ_NCIC"],
             "insight": "Housing stability and income security are prerequisites for engagement"},
            {"level": 3, "name": "Love/Belonging", "dome_dimensions": ["housing", "education"],
             "systems_needed": ["PHL_CARES", "ACF_CCDF"],
             "insight": "Community connection requires stable base — why PSH outperforms shelters"},
            {"level": 4, "name": "Esteem", "dome_dimensions": ["employment", "education"],
             "systems_needed": ["DOL_UI", "ED_NSLDS"],
             "insight": "Meaningful work and learning build self-efficacy and agency"},
            {"level": 5, "name": "Self-Actualization", "dome_dimensions": ["all"],
             "systems_needed": ["all"],
             "insight": "Full flourishing requires all dome dimensions functioning — the whole dome"},
        ],
    },
]

# ── Flourishing Measurement Framework ─────────────────────────────────

FLOURISHING_INDICATORS = {
    "healthcare": {
        "input": [
            {"name": "Insurance coverage rate", "target": 100, "unit": "%",
             "current_us": 91.7, "source": "Census CPS 2023"},
            {"name": "Primary care providers per 100K", "target": 80, "unit": "per 100K",
             "current_us": 55.4, "source": "HRSA Area Health Resource File 2023"},
        ],
        "process": [
            {"name": "Preventable ER visits rate", "target": 0, "unit": "per 1000",
             "current_us": 48.3, "source": "AHRQ National Healthcare Quality Report 2022"},
            {"name": "Care coordination score", "target": 100, "unit": "index",
             "current_us": 52, "source": "Commonwealth Fund International Survey 2023"},
        ],
        "outcome": [
            {"name": "Life expectancy at birth", "target": 82, "unit": "years",
             "current_us": 77.5, "source": "CDC NCHS 2022"},
            {"name": "Infant mortality rate", "target": 3.5, "unit": "per 1000 live births",
             "current_us": 5.6, "source": "CDC NCHS 2022"},
        ],
    },
    "housing": {
        "input": [
            {"name": "Affordable units per 100 ELI renters", "target": 100, "unit": "units",
             "current_us": 33, "source": "NLIHC The Gap 2023"},
            {"name": "Voucher utilization rate", "target": 100, "unit": "%",
             "current_us": 87, "source": "HUD Picture of Subsidized Households 2023"},
        ],
        "process": [
            {"name": "Days from application to housed (HCV)", "target": 30, "unit": "days",
             "current_us": 270, "source": "HUD administrative data estimates"},
        ],
        "outcome": [
            {"name": "Homelessness rate", "target": 0, "unit": "per 10K population",
             "current_us": 20, "source": "HUD AHAR 2023"},
            {"name": "Cost-burdened renter households", "target": 0, "unit": "%",
             "current_us": 50.0, "source": "Harvard JCHS 2023"},
        ],
    },
    "income": {
        "input": [
            {"name": "Poverty rate (SPM)", "target": 0, "unit": "%",
             "current_us": 12.4, "source": "Census SPM 2022"},
            {"name": "EITC take-up rate", "target": 100, "unit": "%",
             "current_us": 78, "source": "IRS SOI / CBPP estimates 2023"},
        ],
        "outcome": [
            {"name": "Child poverty rate", "target": 0, "unit": "%",
             "current_us": 12.4, "source": "Census CPS ASEC 2023"},
            {"name": "Deep poverty rate", "target": 0, "unit": "%",
             "current_us": 5.3, "source": "Census CPS ASEC 2023"},
        ],
    },
    "food": {
        "input": [
            {"name": "SNAP participation rate (eligible)", "target": 100, "unit": "%",
             "current_us": 82, "source": "USDA FNS SNAP QC 2022"},
        ],
        "outcome": [
            {"name": "Food insecurity rate", "target": 0, "unit": "%",
             "current_us": 13.5, "source": "USDA ERS Household Food Security 2023"},
            {"name": "Very low food security rate", "target": 0, "unit": "%",
             "current_us": 5.1, "source": "USDA ERS 2023"},
        ],
    },
    "employment": {
        "input": [
            {"name": "Labor force participation rate", "target": 67, "unit": "%",
             "current_us": 62.7, "source": "BLS CPS December 2023"},
        ],
        "outcome": [
            {"name": "Unemployment rate (U-6)", "target": 5, "unit": "%",
             "current_us": 7.1, "source": "BLS December 2023"},
            {"name": "Working poverty rate", "target": 0, "unit": "%",
             "current_us": 5.6, "source": "BLS Profile of Working Poor 2022"},
        ],
    },
}


def get_flourishing_score(dimension: str) -> dict:
    """Calculate a flourishing score for a dome dimension.

    Score = average of (current/target) across all indicators, capped at 1.0.
    """
    indicators = FLOURISHING_INDICATORS.get(dimension, {})
    if not indicators:
        return {"dimension": dimension, "score": 0, "gap": 1.0}

    scores = []
    for phase in ["input", "process", "outcome"]:
        for ind in indicators.get(phase, []):
            current = ind.get("current_us", 0)
            target = ind.get("target", 1)
            if target == 0:
                # For indicators where lower is better (poverty rate, etc.)
                score = max(0, 1.0 - (current / 100)) if current > 0 else 1.0
            else:
                score = min(1.0, current / target)
            scores.append(score)

    avg_score = sum(scores) / max(1, len(scores))
    return {
        "dimension": dimension,
        "score": round(avg_score, 3),
        "gap": round(1.0 - avg_score, 3),
        "indicator_count": len(scores),
    }
