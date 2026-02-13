"""
vitality.py — The Architecture of Health Beyond Medicine

Clinical medicine accounts for only 10-20% of health outcomes. The rest — the
vast majority of what determines whether a person is well or unwell, vital or
depleted, alive or merely surviving — is determined by the conditions of their
life: what they eat, how they move, whether they sleep, the quality of their air
and water, the depth of their social connections, their sense of purpose, and
their relationship with the natural world.

The Vitality Dome maps health in its fullest sense: not as the absence of disease
but as the presence of flourishing in every dimension of embodied existence.
"""

from typing import Any


VITALITY_DOMAINS: list[dict[str, Any]] = [
    {
        "id": "clinical_care",
        "name": "Clinical Care",
        "percentage_of_health_outcomes": 20,
        "description": (
            "Clinical care — doctors, hospitals, medications, surgeries, diagnostic tests — "
            "is what most people think of when they think of 'health.' It is essential, "
            "especially in acute situations: a broken bone, a heart attack, a cancer diagnosis. "
            "But clinical care accounts for only about 20% of health outcomes. The vast "
            "majority of what determines health happens outside the clinic. A healthcare "
            "system organized entirely around clinical intervention is like a fire department "
            "that only fights fires and never addresses the conditions that cause them."
        ),
        "infrastructure_needed": [
            "Universal access to primary care, regardless of employment or income",
            "Community health centers embedded in every neighborhood",
            "Mental health parity — psychological care treated as seriously as physical care",
            "Integrated care models treating the whole person, not isolated symptoms",
            "Health data sovereignty — patients owning and controlling their own health records",
            "Preventive care and early detection programs available to all"
        ],
        "current_gaps": [
            "27 million Americans uninsured; millions more underinsured",
            "Primary care deserts in rural and low-income urban communities",
            "Average doctor visit lasts 15 minutes — insufficient for whole-person care",
            "Mental health provider shortage of over 150,000 professionals",
            "Fragmented specialist-based system that no one navigates for the patient",
            "Racial disparities in care quality, pain management, and outcomes"
        ]
    },
    {
        "id": "nutrition_food",
        "name": "Nutrition & Food",
        "percentage_of_health_outcomes": 15,
        "description": (
            "Food is the most intimate environmental factor in health — we literally build "
            "our bodies from what we eat. Nutritional health is not about dieting or "
            "restriction; it is about access to real food — grown in living soil, prepared "
            "with care, shared in community. The industrialization of food has produced a "
            "paradox: abundant calories and widespread malnutrition. Cheap processed food "
            "fills stomachs while leaving cells starving for nutrients. Food deserts are "
            "health deserts, and food sovereignty — the right to choose, grow, and access "
            "real food — is a health intervention more powerful than most medications."
        ),
        "infrastructure_needed": [
            "Universal access to affordable fresh produce within walking distance",
            "Community kitchens and cooking education in every neighborhood",
            "School meal programs providing real food, not processed commodities",
            "Urban agriculture infrastructure: community gardens, rooftop farms, food forests",
            "Local food systems connecting regional farms with community institutions",
            "Nutrition education that teaches cooking and food literacy, not just calorie counting"
        ],
        "current_gaps": [
            "23.5 million Americans live in food deserts",
            "Diet-related disease is the leading cause of death in the US",
            "Fresh produce costs 2-3x more per calorie than processed food",
            "School meal programs rely heavily on processed commodity foods",
            "Agricultural subsidies favor commodity crops over fruits and vegetables",
            "Nutrition education reduced to misleading labels and fad diet culture"
        ]
    },
    {
        "id": "movement_fitness",
        "name": "Movement & Fitness",
        "percentage_of_health_outcomes": 10,
        "description": (
            "The human body was built to move — to walk, run, climb, carry, stretch, dance, "
            "and labor. For most of human history, movement was not exercise; it was life. "
            "The modern built environment has engineered movement out of daily existence, "
            "replacing walking with driving, physical labor with desk work, and active play "
            "with screen time. The result is an epidemic of sedentary disease that no amount "
            "of gym memberships can fully counter, because the problem is not individual "
            "motivation but environmental design."
        ),
        "infrastructure_needed": [
            "Walkable, bikeable neighborhoods designed for human movement, not car storage",
            "Free public recreation facilities: pools, courts, tracks, fitness equipment",
            "Active transportation infrastructure: protected bike lanes, safe sidewalks, trails",
            "Workplace movement policies: standing desks, walking meetings, movement breaks",
            "School physical education that develops lifelong movement habits, not athletic competition",
            "Accessible fitness programming for people of all ages, abilities, and body types"
        ],
        "current_gaps": [
            "Only 23% of Americans meet federal physical activity guidelines",
            "80% of Americans live in car-dependent communities with limited walkability",
            "Public recreation facilities are underfunded and deteriorating in many communities",
            "School recess and PE have been cut in favor of test preparation",
            "Fitness culture is dominated by expensive gyms and body-shaming marketing",
            "People with disabilities face systematic barriers to physical activity"
        ]
    },
    {
        "id": "mental_wellness",
        "name": "Mental Wellness",
        "percentage_of_health_outcomes": 15,
        "description": (
            "Mental health is not a separate category from health; it is health experienced "
            "from the inside. Depression, anxiety, trauma, addiction, and psychosis are not "
            "moral failures or character flaws; they are conditions of suffering that arise "
            "from the interaction of biology, experience, and environment. Mental wellness — "
            "the positive dimension — is the capacity for emotional regulation, meaningful "
            "relationships, realistic self-perception, resilience in adversity, and the "
            "experience of life as worth living."
        ),
        "infrastructure_needed": [
            "Mental health care integrated into primary care, not siloed as a separate system",
            "Community mental health centers in every neighborhood, not just hospitals",
            "Peer support networks and recovery communities as formal care infrastructure",
            "Trauma-informed design of all public institutions: schools, courts, hospitals, shelters",
            "Crisis response alternatives to police for mental health emergencies",
            "Mental health education and emotional literacy in schools from earliest grades"
        ],
        "current_gaps": [
            "Over 50% of Americans with mental illness receive no treatment",
            "Average wait for a therapy appointment exceeds 6 weeks in most areas",
            "Police remain the primary responders to mental health crises",
            "Youth mental health crisis: anxiety and depression rates doubled in a decade",
            "Severe shortage of psychiatrists, especially for children and adolescents",
            "Stigma still prevents millions from seeking help"
        ]
    },
    {
        "id": "sleep_rest",
        "name": "Sleep & Rest",
        "percentage_of_health_outcomes": 10,
        "description": (
            "Sleep is not downtime. It is the body's primary maintenance and restoration "
            "system — consolidating memory, repairing tissue, regulating hormones, processing "
            "emotion, and clearing metabolic waste from the brain. Chronic sleep deprivation "
            "is linked to heart disease, diabetes, obesity, depression, and cognitive decline. "
            "Yet modern society treats sleep as optional — a luxury for the lazy, an obstacle "
            "to productivity. The cultural devaluation of rest is itself a public health crisis."
        ),
        "infrastructure_needed": [
            "Work schedules that respect circadian biology: no mandatory overnight shifts without recovery time",
            "School start times aligned with adolescent sleep biology (no earlier than 8:30 AM)",
            "Housing quality standards that ensure quiet, dark, temperature-controlled sleeping environments",
            "Employer policies recognizing rest as essential infrastructure, not laziness",
            "Public education on sleep hygiene and the biology of rest",
            "Nap infrastructure in workplaces, transit hubs, and public buildings"
        ],
        "current_gaps": [
            "35% of Americans get less than the recommended 7 hours of sleep",
            "Shift workers — disproportionately low-income — suffer chronic circadian disruption",
            "Most schools start too early for adolescent biology, creating chronic teen sleep debt",
            "Noise pollution in urban environments disrupts sleep for millions",
            "Hustle culture glorifies sleep deprivation as a badge of dedication",
            "Sleep disorders are underdiagnosed and undertreated, especially in communities of color"
        ]
    },
    {
        "id": "nature_environment",
        "name": "Nature & Environment",
        "percentage_of_health_outcomes": 10,
        "description": (
            "Human beings evolved in nature. Our nervous systems are calibrated to natural "
            "stimuli — birdsong, moving water, dappled sunlight, the smell of soil after rain. "
            "Exposure to nature reduces cortisol, lowers blood pressure, improves mood, "
            "enhances immune function, and accelerates healing. The Japanese practice of "
            "shinrin-yoku (forest bathing) is not mysticism; it is evidence-based medicine. "
            "Conversely, environmental degradation — air pollution, water contamination, "
            "heat islands, noise — is a direct attack on human health."
        ),
        "infrastructure_needed": [
            "Green space within a 10-minute walk of every home",
            "Urban tree canopy targets of at least 30% in every neighborhood",
            "Clean air and water as non-negotiable public health standards",
            "Nature prescriptions integrated into clinical care",
            "Environmental remediation of contaminated sites in overburdened communities",
            "Biophilic design principles in all public buildings: daylight, plants, natural materials"
        ],
        "current_gaps": [
            "100 million Americans live in areas that fail to meet clean air standards",
            "Urban heat islands can be 15-20 degrees hotter than surrounding areas",
            "Low-income communities have 44% less green space than high-income areas",
            "Children spend 90% of their time indoors",
            "Environmental health hazards are concentrated in communities of color",
            "Nature access is treated as recreation rather than health infrastructure"
        ]
    },
    {
        "id": "social_connection",
        "name": "Social Connection",
        "percentage_of_health_outcomes": 10,
        "description": (
            "Loneliness kills. This is not metaphor; it is epidemiology. Social isolation "
            "increases mortality risk by 26% — comparable to smoking 15 cigarettes a day. "
            "Conversely, strong social connections improve immune function, reduce inflammation, "
            "accelerate healing, and extend life. The health impact of social connection is "
            "mediated through multiple pathways: emotional regulation, stress buffering, "
            "health behavior reinforcement, and the direct biological effects of touch, "
            "presence, and belonging."
        ),
        "infrastructure_needed": [
            "Third places — free, accessible gathering spaces in every neighborhood",
            "Community health workers and social prescribing programs",
            "Intergenerational housing and programming that reduces age segregation",
            "Walkable neighborhoods that create incidental social contact",
            "Community meals, festivals, and gathering traditions",
            "Loneliness screening integrated into routine healthcare"
        ],
        "current_gaps": [
            "The Surgeon General declared loneliness an epidemic in 2023",
            "One in three adults over 45 reports feeling lonely",
            "Social infrastructure — community centers, gathering places — is chronically underfunded",
            "Car-dependent design eliminates the casual social encounters that build community",
            "Remote work, while flexible, has increased social isolation for many workers",
            "Elder isolation is pervasive, with millions of seniors going days without conversation"
        ]
    },
    {
        "id": "purpose_meaning_health",
        "name": "Purpose & Meaning",
        "percentage_of_health_outcomes": 5,
        "description": (
            "Having a sense of purpose in life is independently associated with reduced "
            "risk of heart attack, stroke, dementia, and early death. Purpose provides a "
            "reason to take care of oneself, a framework for making health-promoting choices, "
            "and a buffer against the despair that drives self-destructive behavior. Viktor "
            "Frankl's observation that those who survived the concentration camps often had "
            "a sense of purpose has been confirmed by decades of research: meaning is medicine."
        ),
        "infrastructure_needed": [
            "Work that provides autonomy, mastery, and contribution — not just income",
            "Volunteer and service infrastructure that connects people to purpose",
            "Retirement transitions that preserve sense of contribution and relevance",
            "Narrative therapy and meaning-making support in healthcare settings",
            "Community roles and responsibilities that give every person a valued function",
            "Education that helps people explore and articulate their sense of purpose"
        ],
        "current_gaps": [
            "Majority of workers report feeling disengaged or actively disengaged at work",
            "Retirement often triggers depression due to loss of purpose and identity",
            "Deaths of despair — suicide, overdose, alcohol-related death — reflect meaning crises",
            "Young adults report historically high rates of purposelessness and existential anxiety",
            "Healthcare rarely addresses meaning and purpose as health determinants",
            "Cultural emphasis on consumption rather than contribution erodes sense of purpose"
        ]
    },
    {
        "id": "spiritual_health",
        "name": "Spiritual Health",
        "percentage_of_health_outcomes": 5,
        "description": (
            "Spiritual health — whether expressed through religion, meditation, nature connection, "
            "artistic practice, or philosophical reflection — is associated with better mental "
            "health outcomes, greater resilience in illness, reduced substance abuse, stronger "
            "social connections, and longer life. The mechanism is not supernatural; it is the "
            "combined effect of community belonging, meaning-making, contemplative practice, "
            "hope, and the stress-buffering effects of a relationship with something larger "
            "than oneself."
        ),
        "infrastructure_needed": [
            "Chaplaincy and spiritual care in hospitals, hospices, and prisons",
            "Contemplative spaces — meditation rooms, gardens, quiet rooms — in public buildings",
            "Interfaith and secular spiritual programming accessible to all",
            "Integration of existential and spiritual dimensions into mental health care",
            "Protection of sacred sites and natural sanctuaries",
            "Education that includes philosophical and ethical inquiry"
        ],
        "current_gaps": [
            "Hospital chaplaincy programs are being cut as cost-saving measures",
            "Declining religious participation has not been matched by secular alternatives",
            "Spiritual care is rarely integrated into outpatient healthcare",
            "Contemplative spaces are absent from most schools, workplaces, and public buildings",
            "Mental health treatment often ignores spiritual and existential dimensions",
            "People leaving religious institutions often lose community along with belief"
        ]
    }
]


def build_personal_vitality_dome(
    age: int,
    priorities: list[str],
    conditions: list[str],
    environment: str
) -> dict[str, Any]:
    """
    Build a personalized vitality assessment across all health domains.
    
    This is not a medical diagnosis. It is a map of the conditions —
    biological, environmental, social, psychological, and spiritual —
    that together determine a person's vitality.
    
    Args:
        age: Current age
        priorities: List of vitality domain IDs the person wants to focus on
        conditions: List of existing health conditions or concerns
        environment: Description of living environment (urban, suburban, rural)
    
    Returns:
        A personalized vitality dome assessment
    """
    # Environment-based baseline scores
    env_baselines = {
        "urban": {
            "clinical_care": 72, "nutrition_food": 55, "movement_fitness": 50,
            "mental_wellness": 48, "sleep_rest": 42, "nature_environment": 35,
            "social_connection": 58, "purpose_meaning_health": 52, "spiritual_health": 48
        },
        "suburban": {
            "clinical_care": 68, "nutrition_food": 62, "movement_fitness": 42,
            "mental_wellness": 52, "sleep_rest": 58, "nature_environment": 48,
            "social_connection": 45, "purpose_meaning_health": 50, "spiritual_health": 50
        },
        "rural": {
            "clinical_care": 45, "nutrition_food": 68, "movement_fitness": 55,
            "mental_wellness": 50, "sleep_rest": 65, "nature_environment": 72,
            "social_connection": 55, "purpose_meaning_health": 55, "spiritual_health": 58
        }
    }
    
    baseline = env_baselines.get(environment, env_baselines["urban"])
    
    # Age adjustments
    age_adjustments = {}
    if age < 30:
        age_adjustments = {
            "clinical_care": 5, "movement_fitness": 8, "mental_wellness": -5,
            "sleep_rest": -8, "social_connection": 5, "purpose_meaning_health": -8,
            "spiritual_health": -5
        }
    elif age < 50:
        age_adjustments = {
            "clinical_care": 0, "movement_fitness": -3, "mental_wellness": 2,
            "sleep_rest": -3, "social_connection": -2, "purpose_meaning_health": 5,
            "spiritual_health": 3
        }
    elif age < 70:
        age_adjustments = {
            "clinical_care": -5, "movement_fitness": -8, "mental_wellness": 5,
            "sleep_rest": 5, "social_connection": -5, "purpose_meaning_health": 8,
            "spiritual_health": 8
        }
    else:
        age_adjustments = {
            "clinical_care": -10, "movement_fitness": -12, "mental_wellness": 3,
            "sleep_rest": 3, "social_connection": -8, "purpose_meaning_health": 10,
            "spiritual_health": 12
        }
    
    # Condition impacts
    condition_impacts = {
        "chronic_pain": {"movement_fitness": -15, "sleep_rest": -12, "mental_wellness": -10},
        "diabetes": {"nutrition_food": -10, "clinical_care": -8, "movement_fitness": -5},
        "depression": {"mental_wellness": -20, "social_connection": -12, "purpose_meaning_health": -15, "sleep_rest": -10},
        "anxiety": {"mental_wellness": -15, "sleep_rest": -12, "social_connection": -8},
        "heart_disease": {"clinical_care": -12, "movement_fitness": -10, "nutrition_food": -8},
        "obesity": {"movement_fitness": -10, "nutrition_food": -8, "sleep_rest": -5, "mental_wellness": -5},
        "addiction": {"mental_wellness": -15, "social_connection": -10, "purpose_meaning_health": -12, "spiritual_health": -8},
        "loneliness": {"social_connection": -20, "mental_wellness": -12, "purpose_meaning_health": -10},
        "insomnia": {"sleep_rest": -25, "mental_wellness": -10, "clinical_care": -5},
        "none": {}
    }
    
    # Priority boosts (representing focused attention)
    priority_boost = 8
    
    # Calculate scores
    domain_assessments = []
    for domain in VITALITY_DOMAINS:
        did = domain["id"]
        score = baseline.get(did, 50)
        
        # Apply age adjustments
        score += age_adjustments.get(did, 0)
        
        # Apply condition impacts
        for condition in conditions:
            impacts = condition_impacts.get(condition, {})
            score += impacts.get(did, 0)
        
        # Apply priority boosts
        if did in priorities:
            score += priority_boost
        
        # Clamp to 0-100
        score = max(0, min(100, score))
        
        # Generate status
        if score >= 75:
            status = "flourishing"
            recommendation = "Maintain and deepen current practices. Consider mentoring others in this domain."
        elif score >= 55:
            status = "developing"
            recommendation = "Solid foundation exists. Focus on consistency and deepening engagement."
        elif score >= 35:
            status = "vulnerable"
            recommendation = "Active attention needed. Identify one concrete step to strengthen this domain."
        else:
            status = "critical"
            recommendation = "Immediate support needed. This domain is undermining overall vitality."
        
        domain_assessments.append({
            "domain_id": did,
            "domain_name": domain["name"],
            "score": score,
            "status": status,
            "percentage_of_outcomes": domain["percentage_of_health_outcomes"],
            "recommendation": recommendation,
            "infrastructure_gap": domain["current_gaps"][0] if domain["current_gaps"] else "No specific gap identified"
        })
    
    # Sort by score ascending (most needy first)
    domain_assessments.sort(key=lambda x: x["score"])
    
    # Calculate composite
    composite_score = round(
        sum(
            d["score"] * d["percentage_of_outcomes"] / 100
            for d in domain_assessments
        )
    )
    
    # Overall assessment
    if composite_score >= 70:
        overall = "flourishing"
        overall_message = (
            "Your vitality dome is strong. The conditions of your life actively support "
            "your health across most dimensions. Focus on maintaining what works and "
            "strengthening the domains that score lowest."
        )
    elif composite_score >= 50:
        overall = "developing"
        overall_message = (
            "Your vitality dome has a solid foundation but significant areas need attention. "
            "The domains scoring below 50 are likely undermining your overall health in ways "
            "that clinical care alone cannot address."
        )
    elif composite_score >= 30:
        overall = "vulnerable"
        overall_message = (
            "Your vitality dome has critical gaps that are likely affecting your daily "
            "experience of health and energy. Addressing the lowest-scoring domains — even "
            "modestly — could produce significant improvements across the board."
        )
    else:
        overall = "critical"
        overall_message = (
            "Your vitality dome is under severe stress across multiple dimensions. No single "
            "intervention will be sufficient. A coordinated approach addressing foundation "
            "domains — clinical care, nutrition, social connection, sleep — is needed."
        )
    
    return {
        "person": {
            "age": age,
            "priorities": priorities,
            "conditions": conditions,
            "environment": environment
        },
        "composite_score": composite_score,
        "overall_status": overall,
        "overall_message": overall_message,
        "domain_assessments": domain_assessments,
        "key_insight": (
            "Remember: clinical care accounts for only 20% of health outcomes. "
            "The remaining 80% is determined by the conditions mapped in your vitality dome. "
            "The most powerful health interventions may not be medical at all — they may be "
            "a walk in the park, a meal with friends, a full night's sleep, or the discovery "
            "of something worth living for."
        ),
        "top_priority": domain_assessments[0]["domain_name"] if domain_assessments else "None identified",
        "greatest_strength": domain_assessments[-1]["domain_name"] if domain_assessments else "None identified"
    }
