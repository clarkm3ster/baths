"""Claude API explanation engine for DOMES.

Generates plain-English explanations of legal provisions tailored to a
specific person's circumstances using the Anthropic Claude API.
"""

import json
import os

import anthropic
from pydantic import BaseModel

# The Anthropic client reads ANTHROPIC_API_KEY from the environment.
_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


# ---------------------------------------------------------------------------
# Response model
# ---------------------------------------------------------------------------

class ExplanationResult(BaseModel):
    plain_english: str
    what_it_means_for_you: str
    your_rights: list[str]
    enforcement_steps: list[str]
    key_deadlines: list[str]
    who_to_contact: list[str]


# ---------------------------------------------------------------------------
# Prompt template
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = (
    "You are a disability rights attorney explaining a legal provision to a "
    "client. Your job is to make complex law genuinely accessible. "
    "Do NOT say 'consult a lawyer' as the only advice. Give actionable steps "
    "the person can take themselves FIRST."
)

_USER_TEMPLATE = """\
The person's situation:
{profile_summary}

The legal provision:
Citation: {citation}
Title: {title}
Full text: {full_text}
Domain: {domain}
Type: {provision_type}

Explain this provision in plain English as if speaking to the person directly.
Be specific about THEIR rights based on THEIR circumstances.
Include concrete enforcement steps — not vague advice, but specific actions \
with specific agencies and deadlines.

Respond ONLY with a JSON object (no markdown fences) matching this structure:
{{
  "plain_english": "What this law means in everyday language",
  "what_it_means_for_you": "Specifically how this applies to YOUR situation",
  "your_rights": ["Right 1", "Right 2"],
  "enforcement_steps": [
    "Step 1: File a complaint with...",
    "Step 2: Contact your state...",
    "Step 3: If denied, appeal by..."
  ],
  "key_deadlines": ["30 days to appeal", "90 days to file"],
  "who_to_contact": ["State Medicaid office", "Legal aid: lawhelp.org"]
}}
"""


def _summarize_profile(profile: dict) -> str:
    """Create a concise human-readable summary of a person's profile."""
    parts: list[str] = []

    if profile.get("insurance"):
        parts.append(f"Health insurance: {', '.join(profile['insurance'])}")
    if profile.get("disabilities"):
        parts.append(f"Disabilities/conditions: {', '.join(profile['disabilities'])}")
    if profile.get("age_group"):
        parts.append(f"Age group: {profile['age_group']}")
    if profile.get("pregnant"):
        parts.append("Pregnant")
    if profile.get("housing"):
        parts.append(f"Housing: {', '.join(profile['housing'])}")
    if profile.get("income"):
        parts.append(f"Income/benefits: {', '.join(profile['income'])}")
    if profile.get("system_involvement"):
        parts.append(f"System involvement: {', '.join(profile['system_involvement'])}")
    if profile.get("veteran"):
        parts.append("Veteran")
    if profile.get("dv_survivor"):
        parts.append("Domestic violence survivor")
    if profile.get("immigrant"):
        parts.append("Immigrant")
    if profile.get("lgbtq"):
        parts.append("LGBTQ+")
    if profile.get("rural"):
        parts.append("Rural area resident")
    if profile.get("state"):
        parts.append(f"State: {profile['state']}")

    return "; ".join(parts) if parts else "General public"


# ---------------------------------------------------------------------------
# Core explanation function
# ---------------------------------------------------------------------------

async def explain_provision(provision: dict, person_profile: dict) -> ExplanationResult:
    """Generate a plain-English explanation of *provision* for *person_profile*.

    Calls the Anthropic Claude API and parses the structured response.
    """
    client = _get_client()

    user_message = _USER_TEMPLATE.format(
        profile_summary=_summarize_profile(person_profile),
        citation=provision.get("citation", ""),
        title=provision.get("title", ""),
        full_text=provision.get("full_text", ""),
        domain=provision.get("domain", ""),
        provision_type=provision.get("provision_type", ""),
    )

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        system=_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw_text = message.content[0].text.strip()

    # Parse the JSON response from Claude
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        # If Claude wraps the JSON in markdown fences, strip them
        cleaned = raw_text
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        data = json.loads(cleaned.strip())

    return ExplanationResult(**data)


# ---------------------------------------------------------------------------
# FastAPI router
# ---------------------------------------------------------------------------

from fastapi import APIRouter, HTTPException  # noqa: E402

router = APIRouter()


class ExplainRequest(BaseModel):
    provision_id: int
    person_profile: dict


@router.post("/api/explain", response_model=ExplanationResult)
async def explain_endpoint(req: ExplainRequest):
    """POST /api/explain — generate a plain-English explanation."""
    from app.database import SessionLocal
    from app.models import Provision

    db = SessionLocal()
    try:
        provision = db.query(Provision).filter(Provision.id == req.provision_id).first()
        if not provision:
            raise HTTPException(status_code=404, detail="Provision not found")

        provision_dict = {
            "citation": provision.citation,
            "title": provision.title,
            "full_text": provision.full_text,
            "domain": provision.domain,
            "provision_type": provision.provision_type,
        }
    finally:
        db.close()

    # Check for API key before calling Claude
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="ANTHROPIC_API_KEY not configured. Claude explanations unavailable.",
        )

    try:
        result = await explain_provision(provision_dict, req.person_profile)
    except anthropic.APIError as exc:
        raise HTTPException(status_code=502, detail=f"Claude API error: {exc}")

    return result
