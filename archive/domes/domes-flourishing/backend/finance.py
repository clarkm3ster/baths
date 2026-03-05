"""
finance.py — The Financial Architecture of Flourishing

Money is not the point. But money is the medium through which a society expresses
its priorities. The financial architecture of the Dome asks: What would it look like
if we financed human flourishing with the same sophistication, creativity, and scale
that we currently devote to financing extraction?

This module maps existing financial models, proposes new instruments, surveys global
approaches, and provides tools for building personal financial architectures.
"""

from typing import Any


FINANCE_MODELS: list[dict[str, Any]] = [
    {
        "id": "sovereign_wealth",
        "name": "Sovereign Wealth Funds",
        "layer": "public",
        "description": (
            "Sovereign wealth funds transform finite resource extraction into permanent "
            "collective capital. Norway's Government Pension Fund — worth over $1.5 trillion — "
            "converts North Sea oil revenue into a perpetual endowment for its citizens. "
            "Alaska's Permanent Fund distributes annual dividends to every resident. These "
            "funds embody the principle that natural resources belong to the people, not "
            "just the generation that happens to extract them. They are intergenerational "
            "justice made financial: the inheritance of the commons, invested wisely and "
            "shared equitably."
        ),
        "examples": [
            "Norway Government Pension Fund ($1.5T, invests globally, funds social services)",
            "Alaska Permanent Fund ($80B, pays annual dividend to every resident)",
            "Singapore GIC ($700B, funds national infrastructure and development)",
            "Abu Dhabi Investment Authority ($900B, diversifies beyond oil dependence)"
        ],
        "per_person_impact": 14200
    },
    {
        "id": "public_finance",
        "name": "Progressive Public Finance",
        "layer": "public",
        "description": (
            "Taxation is the mechanism by which a society pools resources for collective "
            "flourishing. Progressive public finance — where those with the most contribute "
            "the most — is not punishment for success but the structural recognition that "
            "no fortune is created in isolation. Every billionaire relied on public roads, "
            "public education, public courts, public research, and the labor of workers "
            "whose productivity they captured. Progressive taxation returns a portion of "
            "that collectively created value to the commons."
        ),
        "examples": [
            "Nordic tax systems (40-55% effective rates funding universal services)",
            "Land value taxation (taxing unearned land appreciation rather than productive labor)",
            "Financial transaction taxes (small levies on speculation funding public investment)",
            "Corporate profit sharing (mandatory allocation of profits to workers and communities)"
        ],
        "per_person_impact": 22800
    },
    {
        "id": "impact_investing",
        "name": "Impact Investing",
        "layer": "private",
        "description": (
            "Impact investing redirects private capital toward measurable social and "
            "environmental outcomes alongside financial returns. It represents a growing "
            "recognition that the binary between 'making money' and 'doing good' is false — "
            "that capital can be deployed to finance affordable housing, clean energy, "
            "community health, and education while generating competitive returns. The "
            "$1.2 trillion impact investing market demonstrates that profit and purpose "
            "are not enemies but potential allies."
        ),
        "examples": [
            "Community Development Financial Institutions (CDFIs) lending in underserved areas",
            "Green bonds financing renewable energy and climate adaptation infrastructure",
            "Social impact bonds tying investor returns to measurable social outcomes",
            "Microfinance institutions providing credit to entrepreneurs excluded from banking"
        ],
        "per_person_impact": 5400
    },
    {
        "id": "cooperative_economics",
        "name": "Cooperative Economics",
        "layer": "communal",
        "description": (
            "Cooperative economics distributes ownership to those who create value. Worker "
            "cooperatives, consumer cooperatives, housing cooperatives, and credit unions "
            "demonstrate that enterprise need not be organized around the extraction of "
            "profit by distant shareholders. The Mondragon Corporation in Spain — with "
            "80,000 worker-owners — proves that cooperative enterprise can operate at scale, "
            "in competitive markets, while maintaining democratic governance and equitable "
            "distribution of surplus."
        ),
        "examples": [
            "Mondragon Corporation (80,000 worker-owners, $12B revenue, Spain)",
            "REI (consumer cooperative, $3.8B revenue, member-owned outdoor retailer)",
            "Credit unions ($2.2T in assets, member-owned alternative to profit-driven banks)",
            "Emilia-Romagna cooperative ecosystem (30% of regional GDP, Italy)"
        ],
        "per_person_impact": 8600
    },
    {
        "id": "ubi_ubs",
        "name": "Universal Basic Income & Services",
        "layer": "public",
        "description": (
            "Universal Basic Income (UBI) provides every citizen with a guaranteed cash "
            "floor sufficient to meet basic needs, while Universal Basic Services (UBS) "
            "ensures free access to essential services — healthcare, education, housing, "
            "transit, information. Together they represent the most direct financial "
            "architecture of the foundation layer: the unconditional guarantee that no "
            "one falls below the threshold of dignity. Pilot programs from Stockton to "
            "Finland have demonstrated that when people receive a guaranteed income, they "
            "do not stop working — they start living."
        ),
        "examples": [
            "Stockton SEED program ($500/month, reduced income volatility, improved mental health)",
            "Finland basic income experiment (reduced stress, improved trust in institutions)",
            "GiveDirectly programs (cash transfers in Kenya showing sustained economic gains)",
            "NHS as UBS model (universal healthcare as proof of concept for universal services)"
        ],
        "per_person_impact": 18000
    },
    {
        "id": "philanthropic",
        "name": "Philanthropic & Commons-Based",
        "layer": "communal",
        "description": (
            "Philanthropy — from the Greek 'love of humanity' — represents the voluntary "
            "redistribution of private wealth toward public purpose. At its best, philanthropy "
            "funds innovation that government cannot risk and markets will not attempt: "
            "experimental schools, bold research, community organizing, artistic creation. "
            "At its worst, it substitutes the preferences of the wealthy for the priorities "
            "of the public. The commons-based approach adds the principle that some things — "
            "knowledge, culture, natural resources — should be owned by no one and shared by all."
        ),
        "examples": [
            "Community foundations pooling local giving for lasting impact ($90B in US assets)",
            "Wikipedia as commons-based knowledge creation (free, collaborative, global)",
            "Open source software as voluntary collective creation ($13T estimated value)",
            "Mutual aid societies providing reciprocal support outside institutional channels"
        ],
        "per_person_impact": 3200
    }
]


NEW_INSTRUMENTS: list[dict[str, Any]] = [
    {
        "id": "flourishing_bonds",
        "name": "Flourishing Bonds",
        "description": (
            "Municipal and sovereign bonds whose returns are tied to composite flourishing "
            "indices rather than conventional economic metrics. Instead of measuring success "
            "by GDP growth, Flourishing Bonds mature based on improvements in health outcomes, "
            "educational attainment, environmental quality, social cohesion, and creative "
            "output in the issuing jurisdiction. Investors profit when communities genuinely "
            "thrive — aligning capital markets with human wellbeing for the first time."
        ),
        "mechanism": (
            "Bonds are issued by municipalities or sovereign entities. Returns are calculated "
            "using a composite Flourishing Index combining health metrics (life expectancy, "
            "mental health prevalence), social metrics (social cohesion, civic participation), "
            "environmental metrics (air quality, biodiversity), and capability metrics "
            "(educational attainment, economic mobility). Independent auditors verify outcomes. "
            "Higher flourishing scores yield higher returns, creating a direct financial "
            "incentive for governments to invest in genuine human development."
        ),
        "projected_return": "4.2-6.8% annually, with variance tied to community flourishing outcomes"
    },
    {
        "id": "flourishing_index_fund",
        "name": "Flourishing Index Fund",
        "description": (
            "A publicly available investment fund that tracks companies scored on their "
            "contribution to human and ecological flourishing rather than market capitalization "
            "alone. Companies are evaluated on worker wellbeing (wages, benefits, autonomy), "
            "community impact (local investment, environmental stewardship), product quality "
            "(does this product genuinely improve human life?), and governance (democratic "
            "structures, stakeholder representation). The fund proves that investing in "
            "companies that treat people well is not charitable — it is strategic."
        ),
        "mechanism": (
            "An independent rating body evaluates publicly traded companies across four "
            "flourishing dimensions: Worker Flourishing (compensation, safety, autonomy, growth), "
            "Community Flourishing (local economic impact, environmental practices, civic "
            "engagement), Consumer Flourishing (product quality, accessibility, honest marketing), "
            "and Governance Flourishing (stakeholder representation, transparency, long-term "
            "orientation). The top 200 scoring companies comprise the index. Quarterly rebalancing "
            "ensures accountability."
        ),
        "projected_return": "7.1-9.4% annually, historically outperforming conventional indices over 10+ year horizons"
    },
    {
        "id": "community_wealth_engines",
        "name": "Community Wealth Engines",
        "description": (
            "Integrated local economic development structures that combine anchor institution "
            "procurement, cooperative enterprise development, community land trusts, local "
            "investment vehicles, and public banking into a single wealth-building ecosystem. "
            "Modeled on the Preston Model in the UK and the Evergreen Cooperatives in Cleveland, "
            "Community Wealth Engines recirculate local spending, build local ownership, and "
            "ensure that economic growth benefits the community that generates it rather than "
            "leaking to distant shareholders."
        ),
        "mechanism": (
            "Anchor institutions (hospitals, universities, local government) commit to "
            "redirecting procurement to local, cooperative, and minority-owned businesses. "
            "A community development entity incubates worker cooperatives to meet this demand. "
            "A community land trust preserves affordable commercial and residential space. "
            "A public bank or CDFI provides patient capital. A local investment fund allows "
            "community members to invest in their own neighborhood. The flywheel effect: "
            "local spending generates local wealth, which generates local investment, which "
            "generates local enterprise."
        ),
        "projected_return": "Community wealth multiplier of 2.8x — every $1 invested generates $2.80 in local economic activity"
    },
    {
        "id": "lifetime_flourishing_accounts",
        "name": "Lifetime Flourishing Accounts",
        "description": (
            "Universal asset accounts established at birth for every child, publicly funded "
            "at a level that provides meaningful economic foundation by adulthood. Unlike "
            "savings accounts that depend on family wealth, Flourishing Accounts are "
            "progressive — larger initial deposits for children born into less wealth — "
            "directly addressing intergenerational inequality. Funds can be used for education, "
            "homeownership, business creation, caregiving, or creative development, ensuring "
            "that every person enters adulthood with capital, not just income."
        ),
        "mechanism": (
            "At birth, every child receives a Flourishing Account with a base deposit of "
            "$5,000, plus progressive supplements up to $50,000 for children in the lowest "
            "wealth quintile. Accounts are invested in diversified portfolios managed by a "
            "public fiduciary. Annual public contributions of $500-$2,000 continue through "
            "age 18. By age 18, accounts range from $25,000 to $75,000. Withdrawals are "
            "permitted for approved flourishing purposes: education, homeownership, business "
            "creation, caregiving support, or creative/intellectual development."
        ),
        "projected_return": "Estimated ROI of 8:1 over lifetime — reduced public assistance costs, increased tax revenue, higher economic productivity"
    }
]


GLOBAL_FINANCE: list[dict[str, Any]] = [
    {
        "id": "nordic",
        "name": "Nordic Social Democracy",
        "country": "Denmark / Sweden / Norway / Finland",
        "description": (
            "The Nordic model combines high taxation, universal public services, strong labor "
            "protections, and robust social safety nets with open, competitive market economies. "
            "The result is a population with among the highest levels of trust, health, education, "
            "and life satisfaction in the world. The Nordic model proves that high taxes and "
            "high prosperity are not contradictory — that when public investment is competent "
            "and transparent, citizens are willing to fund the commons generously because they "
            "see the returns in their daily lives."
        ),
        "tax_rate": "44-52%",
        "flourishing_score": 87,
        "key_insight": "High trust + high taxes + universal services = broad-based flourishing. The social contract works when people can see what their taxes buy."
    },
    {
        "id": "singapore_cpf",
        "name": "Singapore Central Provident Fund",
        "country": "Singapore",
        "description": (
            "Singapore's Central Provident Fund (CPF) is a mandatory comprehensive savings "
            "system where employees and employers contribute to individual accounts used for "
            "retirement, healthcare, housing, and education. Combined with world-class public "
            "infrastructure, meritocratic education, and strategic economic planning, Singapore "
            "has achieved first-world prosperity within a single generation. The CPF model "
            "demonstrates that forced savings, competently invested and flexibly deployed, "
            "can provide economic security without the scale of Nordic taxation."
        ),
        "tax_rate": "22%",
        "flourishing_score": 82,
        "key_insight": "Mandatory comprehensive savings + world-class public investment + strategic governance = rapid development with broad security."
    },
    {
        "id": "bhutan_gnh",
        "name": "Bhutan Gross National Happiness",
        "country": "Bhutan",
        "description": (
            "Bhutan measures national progress not by GDP but by Gross National Happiness (GNH), "
            "a composite index covering psychological wellbeing, health, education, time use, "
            "cultural resilience, good governance, community vitality, ecological diversity, "
            "and living standards. Every proposed policy must pass a GNH impact assessment. "
            "While Bhutan faces real development challenges, its framework demonstrates the "
            "radical possibility of organizing an entire nation around flourishing rather "
            "than growth."
        ),
        "tax_rate": "25%",
        "flourishing_score": 74,
        "key_insight": "What you measure is what you manage. Measuring happiness instead of GDP transforms every policy decision."
    },
    {
        "id": "kerala",
        "name": "Kerala Human Development Model",
        "country": "India (Kerala state)",
        "description": (
            "Kerala, with a per capita income far below the Indian average, achieves health, "
            "education, and social outcomes comparable to wealthy nations. Life expectancy "
            "matches the United States. Literacy exceeds 95%. Infant mortality is lower than "
            "many American states. This 'Kerala Model' was built through massive public "
            "investment in education and healthcare, land reform, strong local governance, "
            "and a culture that values social development over material accumulation. It proves "
            "that money is not the binding constraint on flourishing — political will is."
        ),
        "tax_rate": "18%",
        "flourishing_score": 76,
        "key_insight": "High human development is possible at low income levels. Political commitment to education and health can overcome economic constraints."
    },
    {
        "id": "mondragon",
        "name": "Mondragon Cooperative Ecosystem",
        "country": "Spain (Basque Country)",
        "description": (
            "The Mondragon Corporation is the world's largest federation of worker cooperatives: "
            "80,000 worker-owners across 96 cooperatives generating $12 billion in annual revenue. "
            "Founded in 1956 by a Catholic priest in one of Spain's poorest regions, Mondragon "
            "demonstrates that democratic enterprise can compete in global markets while maintaining "
            "pay ratios of 6:1 (vs. 300:1 in conventional corporations), reinvesting profits "
            "locally, and providing its worker-owners with education, healthcare, and economic "
            "security. When the 2008 financial crisis hit, Mondragon cooperatives cut hours "
            "rather than laying off workers — because the workers are the owners."
        ),
        "tax_rate": "28%",
        "flourishing_score": 81,
        "key_insight": "Democratic ownership works at scale. When workers own the enterprise, prosperity is shared and resilience is built into the structure."
    },
    {
        "id": "preston",
        "name": "Preston Model (Community Wealth Building)",
        "country": "United Kingdom (Preston, Lancashire)",
        "description": (
            "Preston, once one of the most deprived cities in England, transformed its economic "
            "trajectory by redirecting anchor institution spending — hospitals, universities, "
            "local government — to local businesses and cooperatives. By 2018, an additional "
            "£74 million was being spent locally each year. The city established a cooperative "
            "development program, explored public banking, and implemented a living wage. "
            "The Preston Model proves that local government, without waiting for national "
            "policy, can restructure local economies around community wealth rather than "
            "extractive growth."
        ),
        "tax_rate": "33%",
        "flourishing_score": 72,
        "key_insight": "Local governments can restructure local economies without waiting for national policy. Redirecting existing spending is a powerful lever."
    }
]


def build_personal_architecture(
    age: int,
    income_level: str,
    aspirations: list[str],
    location: str
) -> dict[str, Any]:
    """
    Build a personalized financial architecture for flourishing.
    
    This is not a financial plan. It is a map of the financial structures —
    public, communal, private, and personal — that support a person's
    flourishing across their lifetime.
    
    Args:
        age: Current age of the person
        income_level: One of 'low', 'moderate', 'high'
        aspirations: List of domain IDs the person is most drawn to
        location: Geographic context (city/region)
    
    Returns:
        A four-layer financial architecture with specific instruments and values
    """
    # Base allocations vary by income level
    income_multipliers = {
        "low": {"foundation": 1.4, "safety": 1.3, "growth": 0.6, "aspiration": 0.5},
        "moderate": {"foundation": 1.0, "safety": 1.0, "growth": 1.0, "aspiration": 1.0},
        "high": {"foundation": 0.7, "safety": 0.8, "growth": 1.3, "aspiration": 1.5}
    }
    
    multiplier = income_multipliers.get(income_level, income_multipliers["moderate"])
    
    # Age-based adjustments
    if age < 25:
        age_factor = {"foundation": 1.2, "safety": 0.8, "growth": 1.3, "aspiration": 1.4}
    elif age < 40:
        age_factor = {"foundation": 1.0, "safety": 1.1, "growth": 1.2, "aspiration": 1.0}
    elif age < 60:
        age_factor = {"foundation": 0.9, "safety": 1.3, "growth": 1.0, "aspiration": 0.9}
    else:
        age_factor = {"foundation": 1.1, "safety": 1.4, "growth": 0.7, "aspiration": 1.1}
    
    # Map aspirations to financial priorities
    aspiration_map = {
        "health_vitality": "health_savings",
        "economic_prosperity": "wealth_building",
        "creative_expression": "creative_fund",
        "intellectual_growth": "education_fund",
        "spiritual_depth": "sabbatical_fund",
        "community_belonging": "community_investment",
        "environmental_harmony": "green_investment",
        "physical_space_beauty": "housing_fund",
        "love_relationships": "family_fund",
        "purpose_meaning": "career_transition",
        "play_joy": "recreation_fund",
        "legacy_contribution": "legacy_fund"
    }
    
    aspiration_instruments = []
    for asp in aspirations:
        mapped = aspiration_map.get(asp)
        if mapped:
            aspiration_instruments.append(mapped)
    
    base_values = {
        "foundation": 24000,
        "safety": 18000,
        "growth": 12000,
        "aspiration": 8000
    }
    
    architecture = {
        "person": {
            "age": age,
            "income_level": income_level,
            "aspirations": aspirations,
            "location": location
        },
        "layers": [
            {
                "name": "Foundation",
                "purpose": (
                    "The non-negotiable financial floor. These are the resources and "
                    "structures that ensure basic dignity: housing, food, healthcare, "
                    "and the absence of economic terror. No person can flourish while "
                    "worrying about whether they will eat tomorrow."
                ),
                "annual_value": round(base_values["foundation"] * multiplier["foundation"] * age_factor["foundation"]),
                "instruments": [
                    {
                        "name": "Universal Basic Services Access",
                        "type": "public",
                        "description": "Healthcare, education, transit, and digital access provided as public goods",
                        "annual_value": round(8400 * multiplier["foundation"])
                    },
                    {
                        "name": "Housing Stability Fund",
                        "type": "public",
                        "description": "Rental assistance, public housing, or homeownership support ensuring housing costs stay below 30% of income",
                        "annual_value": round(9600 * multiplier["foundation"])
                    },
                    {
                        "name": "Emergency Reserves",
                        "type": "personal",
                        "description": "Three to six months of essential expenses held in accessible, liquid form",
                        "annual_value": round(6000 * multiplier["foundation"])
                    }
                ]
            },
            {
                "name": "Safety",
                "purpose": (
                    "Protection against the shocks that can destroy a life: illness, "
                    "job loss, disability, natural disaster, family crisis. The safety "
                    "layer ensures that a single bad month does not become a permanent "
                    "catastrophe. It transforms precarity into resilience."
                ),
                "annual_value": round(base_values["safety"] * multiplier["safety"] * age_factor["safety"]),
                "instruments": [
                    {
                        "name": "Social Insurance",
                        "type": "public",
                        "description": "Unemployment insurance, disability coverage, and social security providing baseline income protection",
                        "annual_value": round(6000 * multiplier["safety"])
                    },
                    {
                        "name": "Mutual Aid Membership",
                        "type": "communal",
                        "description": "Participation in community emergency funds, lending circles, and reciprocal care networks",
                        "annual_value": round(2400 * multiplier["safety"])
                    },
                    {
                        "name": "Insurance Portfolio",
                        "type": "private",
                        "description": "Health, disability, life, and property insurance providing protection against catastrophic loss",
                        "annual_value": round(5400 * multiplier["safety"])
                    },
                    {
                        "name": "Skills & Adaptability",
                        "type": "personal",
                        "description": "Continuous learning that ensures employability and economic relevance across changing conditions",
                        "annual_value": round(4200 * multiplier["safety"])
                    }
                ]
            },
            {
                "name": "Growth",
                "purpose": (
                    "Capital that compounds over time, building wealth rather than "
                    "merely covering expenses. The growth layer transforms a person "
                    "from a consumer of income into a builder of assets — creating "
                    "the economic foundation for intergenerational flourishing."
                ),
                "annual_value": round(base_values["growth"] * multiplier["growth"] * age_factor["growth"]),
                "instruments": [
                    {
                        "name": "Flourishing Index Fund",
                        "type": "private",
                        "description": "Long-term investment in companies scored on worker wellbeing, community impact, and genuine value creation",
                        "annual_value": round(4800 * multiplier["growth"])
                    },
                    {
                        "name": "Community Investment",
                        "type": "communal",
                        "description": "Direct investment in local cooperatives, community land trusts, and neighborhood enterprises",
                        "annual_value": round(3600 * multiplier["growth"])
                    },
                    {
                        "name": "Lifetime Flourishing Account",
                        "type": "public",
                        "description": "Universal asset account growing since birth, available for education, homeownership, or enterprise creation",
                        "annual_value": round(3600 * multiplier["growth"])
                    }
                ]
            },
            {
                "name": "Aspiration",
                "purpose": (
                    "Resources dedicated not to survival or security but to becoming. "
                    "The aspiration layer funds the creative project, the sabbatical, "
                    "the pilgrimage, the career change, the dream. It is the financial "
                    "expression of Maslow's self-actualization and Ignatius's magis."
                ),
                "annual_value": round(base_values["aspiration"] * multiplier["aspiration"] * age_factor["aspiration"]),
                "instruments": [
                    {
                        "name": "Creative & Sabbatical Fund",
                        "type": "personal",
                        "description": "Dedicated savings for creative projects, career transitions, travel, and periods of intentional non-productivity",
                        "annual_value": round(3200 * multiplier["aspiration"])
                    },
                    {
                        "name": "Legacy & Giving Fund",
                        "type": "personal",
                        "description": "Resources earmarked for philanthropy, mentorship support, and intergenerational wealth transfer",
                        "annual_value": round(2400 * multiplier["aspiration"])
                    },
                    {
                        "name": "Cultural Patronage",
                        "type": "communal",
                        "description": "Contributions to arts organizations, community institutions, and cultural infrastructure that enrich shared life",
                        "annual_value": round(2400 * multiplier["aspiration"])
                    }
                ]
            }
        ],
        "total_annual_architecture": 0,
        "aspiration_priorities": aspiration_instruments,
        "philosophy": (
            "This architecture is not a budget. It is a map of the financial structures — "
            "public, communal, private, and personal — that together create the economic "
            "conditions for flourishing. Some of these structures already exist. Some must "
            "be built. The gap between the architecture we have and the architecture we need "
            "is the measure of our society's unfinished work."
        )
    }
    
    # Calculate total
    architecture["total_annual_architecture"] = sum(
        layer["annual_value"] for layer in architecture["layers"]
    )
    
    return architecture
