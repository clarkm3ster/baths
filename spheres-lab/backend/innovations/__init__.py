"""
SPHERES Innovation Laboratory — Innovation seed data aggregator.
Imports seed innovations and generator templates from each domain module.
"""

from innovations.sphere_economist import INNOVATIONS as ECONOMIST_INNOVATIONS, TEMPLATES as ECONOMIST_TEMPLATES
from innovations.revenue_architect import INNOVATIONS as REVENUE_INNOVATIONS, TEMPLATES as REVENUE_TEMPLATES
from innovations.space_inventor import INNOVATIONS as SPACE_INNOVATIONS, TEMPLATES as SPACE_TEMPLATES
from innovations.culture_engineer import INNOVATIONS as CULTURE_INNOVATIONS, TEMPLATES as CULTURE_TEMPLATES
from innovations.platform_inventor import INNOVATIONS as PLATFORM_INNOVATIONS, TEMPLATES as PLATFORM_TEMPLATES
from innovations.world_builder import INNOVATIONS as WORLD_INNOVATIONS, TEMPLATES as WORLD_TEMPLATES
from innovations.policy_inventor import INNOVATIONS as POLICY_INNOVATIONS, TEMPLATES as POLICY_TEMPLATES
from innovations.city_replicator import INNOVATIONS as CITY_INNOVATIONS, TEMPLATES as CITY_TEMPLATES
from innovations.ecosystem_architect import INNOVATIONS as ECOSYSTEM_INNOVATIONS, TEMPLATES as ECOSYSTEM_TEMPLATES
from innovations.impact_scientist import INNOVATIONS as IMPACT_INNOVATIONS, TEMPLATES as IMPACT_TEMPLATES
from innovations.narrative_designer import INNOVATIONS as NARRATIVE_INNOVATIONS, TEMPLATES as NARRATIVE_TEMPLATES

# Aggregate all seed innovations keyed by teammate slug
SEED_INNOVATIONS: dict[str, list] = {
    "sphere-economist": ECONOMIST_INNOVATIONS,
    "revenue-architect": REVENUE_INNOVATIONS,
    "space-inventor": SPACE_INNOVATIONS,
    "culture-engineer": CULTURE_INNOVATIONS,
    "platform-inventor": PLATFORM_INNOVATIONS,
    "world-builder": WORLD_INNOVATIONS,
    "policy-inventor": POLICY_INNOVATIONS,
    "city-replicator": CITY_INNOVATIONS,
    "ecosystem-architect": ECOSYSTEM_INNOVATIONS,
    "impact-scientist": IMPACT_INNOVATIONS,
    "narrative-designer": NARRATIVE_INNOVATIONS,
}

# Aggregate all generator templates keyed by teammate slug
DOMAIN_TEMPLATES: dict[str, list] = {
    "sphere-economist": ECONOMIST_TEMPLATES,
    "revenue-architect": REVENUE_TEMPLATES,
    "space-inventor": SPACE_TEMPLATES,
    "culture-engineer": CULTURE_TEMPLATES,
    "platform-inventor": PLATFORM_TEMPLATES,
    "world-builder": WORLD_TEMPLATES,
    "policy-inventor": POLICY_TEMPLATES,
    "city-replicator": CITY_TEMPLATES,
    "ecosystem-architect": ECOSYSTEM_TEMPLATES,
    "impact-scientist": IMPACT_TEMPLATES,
    "narrative-designer": NARRATIVE_TEMPLATES,
}
