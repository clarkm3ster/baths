"""Circumstance taxonomy and result models for DOMES matching engine."""

from pydantic import BaseModel


class PersonProfile(BaseModel):
    """A person's circumstances used to match applicable legal provisions.

    All fields use plain identifiers (e.g. "medicaid", "mental_health") so the
    matching engine can compare them directly against the ``applies_when`` JSON
    stored in each provision row.
    """

    # Health Insurance
    insurance: list[str] = []  # medicaid, medicare, private, uninsured, chip

    # Disabilities / Conditions
    disabilities: list[str] = []  # mental_health, sud, idd, physical, chronic_illness

    # Age
    age_group: str = ""  # under_18, 18_to_21, 22_to_64, 65_plus
    pregnant: bool = False

    # Housing
    housing: list[str] = []  # section_8, public_housing, homeless, private_rental, homeowner

    # Income / Benefits
    income: list[str] = []  # ssi, ssdi, snap, tanf, below_poverty, unemployed

    # System Involvement
    system_involvement: list[str] = []  # incarcerated, recently_released, probation, juvenile_justice, foster_care

    # Other
    veteran: bool = False
    dv_survivor: bool = False
    immigrant: bool = False
    lgbtq: bool = False
    rural: bool = False

    # Location
    state: str = ""


# ---------------------------------------------------------------------------
# Helpers: map age_group values to the broader categories used in applies_when
# ---------------------------------------------------------------------------

AGE_EXPANSIONS: dict[str, list[str]] = {
    "under_18": ["under_18", "under_21"],
    "18_to_21": ["18_to_21", "under_21"],
    "22_to_64": ["22_to_64", "adult"],
    "65_plus": ["65_plus", "adult", "elderly"],
}


class MatchResult(BaseModel):
    """A single provision that matched a person's profile."""

    provision_id: int
    citation: str
    title: str
    domain: str
    provision_type: str
    relevance_score: float  # 0.0 to 1.0
    match_reasons: list[str]  # human-readable explanations of why this matched
    enforcement_steps: list[str]
    is_gap: bool = False  # True when the person *should* have this but likely doesn't
    full_text: str = ""
    source_url: str = ""
    cross_references: list[str] = []


class CrossReference(BaseModel):
    """A link between two provisions."""

    target_id: int
    target_citation: str
    relationship: str  # implements, enforces, extends, conflicts, related
    description: str
