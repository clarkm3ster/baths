"""
main.py — The Flourishing Dome API

This is the capstone of the DOMES project. Every previous app — legal research,
public assets, data constellations, profile building, contract generation,
coordination architecture — was a preparation for this. The Flourishing Dome
asks the largest question: What would it look like to design a complete
architecture for human flourishing?

Not a safety net. Not a benefits system. Not a case management platform.
A cathedral.

Port: 8005
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any

from domains import FLOURISHING_DOMAINS, DOMAIN_RESOURCES
from philosophy import PHILOSOPHICAL_TRADITIONS, PHILOSOPHICAL_SYNTHESIS
from finance import FINANCE_MODELS, NEW_INSTRUMENTS, GLOBAL_FINANCE, build_personal_architecture
from culture import CULTURE_DOMAINS, CULTURE_ASSETS, CULTURE_DESERTS
from vitality import VITALITY_DOMAINS, build_personal_vitality_dome


app = FastAPI(
    title="Domes Flourishing",
    description=(
        "The Architecture of Human Flourishing. "
        "Twelve domains. Eight philosophical traditions. "
        "One cathedral of becoming."
    ),
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────
# Request Models
# ──────────────────────────────────────────────

class PersonalArchitectureRequest(BaseModel):
    age: int
    income_level: str  # "low", "moderate", "high"
    aspirations: list[str]  # List of domain IDs
    location: str


class PersonalVitalityRequest(BaseModel):
    age: int
    priorities: list[str]  # List of vitality domain IDs
    conditions: list[str]  # List of health conditions
    environment: str  # "urban", "suburban", "rural"


class FlourishingDomeRequest(BaseModel):
    name: str
    age: int
    aspirations: list[str]  # List of domain IDs
    values: list[str]  # List of philosophical tradition IDs
    income_level: str
    environment: str
    health_conditions: list[str]
    location: str


# ──────────────────────────────────────────────
# Domains Endpoints
# ──────────────────────────────────────────────

@app.get("/api/domains")
def get_domains() -> list[dict[str, Any]]:
    """Return all twelve flourishing domains."""
    return FLOURISHING_DOMAINS


@app.get("/api/domains/{domain_id}")
def get_domain(domain_id: str) -> dict[str, Any]:
    """Return a single flourishing domain by ID."""
    for domain in FLOURISHING_DOMAINS:
        if domain["id"] == domain_id:
            return domain
    raise HTTPException(status_code=404, detail=f"Domain '{domain_id}' not found")


@app.get("/api/domains/{domain_id}/resources")
def get_domain_resources(domain_id: str) -> dict[str, Any]:
    """Return resources for a specific flourishing domain."""
    if domain_id not in DOMAIN_RESOURCES:
        raise HTTPException(status_code=404, detail=f"Resources for domain '{domain_id}' not found")
    
    # Find the domain for context
    domain_name = domain_id
    for domain in FLOURISHING_DOMAINS:
        if domain["id"] == domain_id:
            domain_name = domain["name"]
            break
    
    resources = DOMAIN_RESOURCES[domain_id]
    avg_coverage = round(sum(r["coverage"] for r in resources) / len(resources))
    
    return {
        "domain_id": domain_id,
        "domain_name": domain_name,
        "resources": resources,
        "average_coverage": avg_coverage,
        "resource_count": len(resources),
        "by_type": {
            rtype: [r for r in resources if r["type"] == rtype]
            for rtype in ["public", "communal", "private", "personal", "natural"]
        }
    }


# ──────────────────────────────────────────────
# Philosophy Endpoints
# ──────────────────────────────────────────────

@app.get("/api/philosophy")
def get_philosophy() -> dict[str, Any]:
    """Return all philosophical traditions and the synthesis."""
    return {
        "traditions": PHILOSOPHICAL_TRADITIONS,
        "synthesis": PHILOSOPHICAL_SYNTHESIS
    }


@app.get("/api/philosophy/{tradition_id}")
def get_tradition(tradition_id: str) -> dict[str, Any]:
    """Return a single philosophical tradition by ID."""
    for tradition in PHILOSOPHICAL_TRADITIONS:
        if tradition["id"] == tradition_id:
            return tradition
    raise HTTPException(status_code=404, detail=f"Tradition '{tradition_id}' not found")


# ──────────────────────────────────────────────
# Finance Endpoints
# ──────────────────────────────────────────────

@app.get("/api/finance/models")
def get_finance_models() -> dict[str, Any]:
    """Return all financial models and proposed instruments."""
    return {
        "existing_models": FINANCE_MODELS,
        "new_instruments": NEW_INSTRUMENTS,
        "total_per_person_impact": sum(m["per_person_impact"] for m in FINANCE_MODELS),
        "message": (
            "The financial infrastructure for flourishing already exists in fragments. "
            "The question is not invention but integration — and the political will to "
            "direct capital toward human development rather than extraction."
        )
    }


@app.get("/api/finance/global")
def get_global_finance() -> dict[str, Any]:
    """Return global financial models for flourishing."""
    return {
        "models": GLOBAL_FINANCE,
        "insight": (
            "Every model on this list proves something important: that broad-based "
            "flourishing is achievable, that different paths can lead there, and that "
            "the constraints are political, not economic. The money exists. The knowledge "
            "exists. What is needed is the collective decision to build the architecture."
        )
    }


@app.post("/api/finance/personal-architecture")
def create_personal_architecture(request: PersonalArchitectureRequest) -> dict[str, Any]:
    """Build a personalized financial architecture for flourishing."""
    return build_personal_architecture(
        age=request.age,
        income_level=request.income_level,
        aspirations=request.aspirations,
        location=request.location
    )


# ──────────────────────────────────────────────
# Culture Endpoints
# ──────────────────────────────────────────────

@app.get("/api/culture/domains")
def get_culture_domains() -> list[dict[str, Any]]:
    """Return all cultural/creative domains."""
    return CULTURE_DOMAINS


@app.get("/api/culture/assets")
def get_culture_assets() -> dict[str, Any]:
    """Return available cultural infrastructure assets."""
    total_count = sum(a["count"] for a in CULTURE_ASSETS.values())
    avg_equity = round(
        sum(a["distribution_equity"] for a in CULTURE_ASSETS.values()) / len(CULTURE_ASSETS)
    )
    return {
        "assets": CULTURE_ASSETS,
        "total_cultural_assets": total_count,
        "average_distribution_equity": avg_equity,
        "assessment": (
            f"With {total_count:,} cultural assets and an average distribution equity score "
            f"of {avg_equity}/100, America has significant cultural infrastructure — but it "
            f"is profoundly maldistributed. The challenge is not scarcity but equity."
        )
    }


@app.get("/api/culture/deserts")
def get_culture_deserts() -> list[dict[str, Any]]:
    """Return cultural desert types and interventions."""
    return CULTURE_DESERTS


# ──────────────────────────────────────────────
# Vitality Endpoints
# ──────────────────────────────────────────────

@app.get("/api/vitality/domains")
def get_vitality_domains() -> dict[str, Any]:
    """Return all vitality domains with their health outcome percentages."""
    total_pct = sum(d["percentage_of_health_outcomes"] for d in VITALITY_DOMAINS)
    clinical_pct = next(
        d["percentage_of_health_outcomes"]
        for d in VITALITY_DOMAINS
        if d["id"] == "clinical_care"
    )
    non_clinical_pct = total_pct - clinical_pct
    
    return {
        "domains": VITALITY_DOMAINS,
        "total_percentage_mapped": total_pct,
        "clinical_care_percentage": clinical_pct,
        "non_clinical_percentage": non_clinical_pct,
        "key_insight": (
            f"Clinical care accounts for only {clinical_pct}% of health outcomes. "
            f"The remaining {non_clinical_pct}% is determined by the conditions of daily life: "
            f"food, movement, sleep, environment, relationships, purpose, and spiritual depth. "
            f"A healthcare system that addresses only clinical care is addressing only one-fifth "
            f"of what determines whether people are well."
        )
    }


@app.post("/api/vitality/personal-dome")
def create_personal_vitality_dome(request: PersonalVitalityRequest) -> dict[str, Any]:
    """Build a personalized vitality dome assessment."""
    return build_personal_vitality_dome(
        age=request.age,
        priorities=request.priorities,
        conditions=request.conditions,
        environment=request.environment
    )


# ──────────────────────────────────────────────
# Flourishing Index — Nations Comparison
# ──────────────────────────────────────────────

@app.get("/api/flourishing-index")
def get_flourishing_index() -> dict[str, Any]:
    """
    Composite flourishing index comparing nations and the theoretical maximum.
    
    This is not GDP. This is not HDI. This is a composite measure of what it
    actually feels like to be a human being in a given society — across all
    twelve domains of flourishing.
    """
    nations = [
        {
            "name": "Finland",
            "score": 89,
            "population": "5.5M",
            "strengths": ["Education", "Social trust", "Environmental quality", "Safety"],
            "gaps": ["Cultural homogeneity challenges", "Winter mental health", "Immigration integration"],
            "insight": "Proves that sustained public investment in human development produces the highest flourishing outcomes on Earth."
        },
        {
            "name": "Denmark",
            "score": 87,
            "population": "5.9M",
            "strengths": ["Work-life balance", "Social safety net", "Democratic engagement", "Design culture"],
            "gaps": ["Immigrant integration", "Rising inequality", "Housing costs in Copenhagen"],
            "insight": "The Danish concept of 'hygge' — coziness, warmth, togetherness — is not just a lifestyle brand but a cultural infrastructure of belonging."
        },
        {
            "name": "Singapore",
            "score": 82,
            "population": "5.9M",
            "strengths": ["Economic security", "Public infrastructure", "Education", "Healthcare"],
            "gaps": ["Civil liberties", "Work-life balance", "Creative freedom", "Domestic worker rights"],
            "insight": "Demonstrates that strategic governance and forced savings can rapidly build prosperity — but flourishing requires more than material security."
        },
        {
            "name": "Costa Rica",
            "score": 79,
            "population": "5.2M",
            "strengths": ["Life expectancy", "Environmental protection", "Social bonds", "Joy and wellbeing"],
            "gaps": ["Economic inequality", "Infrastructure", "Youth unemployment"],
            "insight": "Consistently ranks among the happiest nations despite modest GDP — proving that community, nature, and 'pura vida' matter more than wealth."
        },
        {
            "name": "Kerala",
            "score": 76,
            "population": "35M",
            "strengths": ["Literacy (96%)", "Life expectancy", "Healthcare access", "Gender equity"],
            "gaps": ["Economic growth", "Youth emigration", "Environmental challenges"],
            "insight": "The most powerful proof that human development does not require wealth — political will and public investment can overcome economic constraints."
        },
        {
            "name": "Bhutan",
            "score": 74,
            "population": "0.8M",
            "strengths": ["Gross National Happiness framework", "Environmental conservation", "Cultural preservation", "Spiritual depth"],
            "gaps": ["Youth unemployment", "Brain drain", "Modernization pressures", "Economic development"],
            "insight": "The only nation that measures success by happiness rather than GDP — proving that what you measure is what you manage."
        },
        {
            "name": "United States",
            "score": 68,
            "population": "335M",
            "strengths": ["Innovation capacity", "Higher education", "Cultural production", "Economic dynamism"],
            "gaps": ["Healthcare access", "Income inequality", "Social cohesion", "Life expectancy decline", "Gun violence", "Incarceration"],
            "insight": "The wealthiest nation in history demonstrates that GDP alone does not produce flourishing. America has the resources but not yet the architecture."
        },
        {
            "name": "What's Possible",
            "score": 97,
            "population": "Any",
            "strengths": [
                "Universal healthcare and vitality infrastructure",
                "Economic security through UBI/UBS and cooperative economics",
                "Creative infrastructure in every community",
                "Environmental harmony as organizing principle",
                "Deep social connection and community belonging",
                "Purpose and meaning accessible to all",
                "Beauty as a public good",
                "Spiritual depth honored across traditions"
            ],
            "gaps": ["Has not yet been built — but every component exists somewhere"],
            "insight": (
                "No nation has achieved full flourishing. But every component of full "
                "flourishing has been achieved somewhere. Finland's education, Denmark's "
                "work-life balance, Singapore's infrastructure, Costa Rica's joy, Kerala's "
                "equity, Bhutan's measurement framework — combined, they point toward what "
                "is possible. The architecture exists in fragments. The task is integration."
            )
        }
    ]
    
    return {
        "title": "The Flourishing Index",
        "description": (
            "A composite measure of human flourishing across all twelve domains. "
            "Score reflects the average person's real capabilities — not national wealth, "
            "not reported happiness, but what people are actually able to do and to be."
        ),
        "methodology": (
            "Composite of health outcomes, economic security, educational access, "
            "environmental quality, social cohesion, creative infrastructure, civic "
            "participation, and subjective wellbeing — weighted by the Capability Approach's "
            "central human capabilities."
        ),
        "nations": nations,
        "maximum_possible": 100,
        "current_global_average": 52,
        "message": (
            "The gap between 52 (global average) and 97 (what's possible) is not a gap "
            "of resources or knowledge. It is a gap of political will, institutional design, "
            "and collective imagination. Everything needed to close this gap already exists. "
            "The question is whether we will build the architecture."
        )
    }


# ──────────────────────────────────────────────
# Personal Flourishing Dome — The Capstone
# ──────────────────────────────────────────────

@app.post("/api/flourishing-dome")
def build_flourishing_dome(request: FlourishingDomeRequest) -> dict[str, Any]:
    """
    Build a complete personal flourishing dome.
    
    This is the capstone endpoint — integrating domains, philosophy, finance,
    culture, and vitality into a single architecture for one human being.
    """
    # Find matching philosophical traditions
    selected_traditions = []
    for tradition in PHILOSOPHICAL_TRADITIONS:
        if tradition["id"] in request.values:
            selected_traditions.append({
                "id": tradition["id"],
                "name": tradition["name"],
                "thinker": tradition["thinker"],
                "core_idea": tradition["core_idea"],
                "quote": tradition["quote"]
            })
    
    # Build domain assessments
    domain_assessments = []
    for domain in FLOURISHING_DOMAINS:
        is_aspiration = domain["id"] in request.aspirations
        resources = DOMAIN_RESOURCES.get(domain["id"], [])
        avg_coverage = round(sum(r["coverage"] for r in resources) / len(resources)) if resources else 0
        
        domain_assessments.append({
            "id": domain["id"],
            "name": domain["name"],
            "color": domain["color"],
            "icon": domain["icon"],
            "layer": domain["layer"],
            "is_personal_aspiration": is_aspiration,
            "resource_coverage": avg_coverage,
            "flourishing_looks_like": domain["flourishing_looks_like"] if is_aspiration else None,
            "top_threats": domain["threats"][:3],
            "top_protections": domain["de_risked_by"][:3]
        })
    
    # Build financial architecture
    financial = build_personal_architecture(
        age=request.age,
        income_level=request.income_level,
        aspirations=request.aspirations,
        location=request.location
    )
    
    # Build vitality dome
    vitality = build_personal_vitality_dome(
        age=request.age,
        priorities=[
            d for d in ["clinical_care", "nutrition_food", "movement_fitness",
                       "mental_wellness", "sleep_rest", "nature_environment",
                       "social_connection", "purpose_meaning_health", "spiritual_health"]
            if any(a in d for a in request.aspirations[:3])
        ] or ["mental_wellness", "social_connection"],
        conditions=request.health_conditions,
        environment=request.environment
    )
    
    # Compose the dome
    aspiration_domains = [d for d in domain_assessments if d["is_personal_aspiration"]]
    foundation_domains = [d for d in domain_assessments if d["layer"] == "foundation"]
    transcendence_domains = [d for d in domain_assessments if d["layer"] == "transcendence"]
    
    # Find weakest area
    weakest = min(domain_assessments, key=lambda d: d["resource_coverage"])
    strongest = max(domain_assessments, key=lambda d: d["resource_coverage"])
    
    return {
        "dome": {
            "title": f"The Flourishing Dome of {request.name}",
            "subtitle": "A Complete Architecture for Human Flourishing",
            "person": {
                "name": request.name,
                "age": request.age,
                "environment": request.environment,
                "location": request.location
            },
            "philosophical_foundation": {
                "traditions": selected_traditions,
                "synthesis_title": PHILOSOPHICAL_SYNTHESIS["title"],
                "guiding_principle": (
                    "You are not a case to be managed, a problem to be solved, or a consumer "
                    "to be satisfied. You are a human being in the fullness of your complexity, "
                    "and this dome is designed to honor every dimension of your existence."
                )
            },
            "domain_architecture": {
                "total_domains": 12,
                "foundation_layer": {
                    "name": "Foundation",
                    "description": "The bedrock conditions without which flourishing cannot begin",
                    "domains": [d for d in domain_assessments if d["layer"] == "foundation"]
                },
                "aspiration_layer": {
                    "name": "Aspiration",
                    "description": "The dimensions that elevate life from adequate to magnificent",
                    "domains": [d for d in domain_assessments if d["layer"] == "aspiration"]
                },
                "transcendence_layer": {
                    "name": "Transcendence",
                    "description": "The realms where human experience touches something beyond itself",
                    "domains": [d for d in domain_assessments if d["layer"] == "transcendence"]
                }
            },
            "personal_aspirations": aspiration_domains,
            "financial_architecture": {
                "total_annual_value": financial["total_annual_architecture"],
                "layers": financial["layers"]
            },
            "vitality_assessment": {
                "composite_score": vitality["composite_score"],
                "overall_status": vitality["overall_status"],
                "top_priority": vitality["top_priority"],
                "greatest_strength": vitality["greatest_strength"]
            },
            "weakest_domain": {
                "name": weakest["name"],
                "coverage": weakest["resource_coverage"],
                "message": f"Your dome is most vulnerable in {weakest['name']}. Strengthening this domain will strengthen all others."
            },
            "strongest_domain": {
                "name": strongest["name"],
                "coverage": strongest["resource_coverage"],
                "message": f"Your dome is strongest in {strongest['name']}. This is a foundation to build from."
            },
            "closing_message": (
                f"This is not a report about what you lack. It is an architecture of what is "
                f"possible. Every domain can be strengthened. Every gap can be narrowed. Every "
                f"aspiration can be pursued. The dome is not a destination — it is a practice. "
                f"And {request.name}, you are not just a beneficiary of this architecture. "
                f"You are its architect."
            )
        }
    }


# ──────────────────────────────────────────────
# Run
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
