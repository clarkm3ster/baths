"""IP Rights Registry for Dome Studio.

Manages intellectual property: ownership, licensing, contributor splits,
rights chains, and consent-aligned ethics checks.
"""
from __future__ import annotations

from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel, Field


# ── Models ─────────────────────────────────────────────────────────

class ContributorSplit(BaseModel):
    contributor: str
    role: str
    share_percent: float
    agreed_date: Optional[str] = None


class LicenseGrant(BaseModel):
    licensee: str
    scope: Literal["exclusive", "non_exclusive", "open_source", "cc_by", "cc_by_nc"]
    territory: str = "worldwide"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    terms: str = ""


class RightsBundle(BaseModel):
    asset_id: str
    owner: str
    contributors: list[ContributorSplit] = Field(default_factory=list)
    licenses: list[LicenseGrant] = Field(default_factory=list)
    restrictions: list[str] = Field(default_factory=list)
    chain_of_title: list[dict] = Field(default_factory=list)


# ── Core Functions ─────────────────────────────────────────────────

def create_rights_bundle(
    asset_id: str,
    owner: str,
    contributors: list[dict],
) -> RightsBundle:
    """Create a rights bundle. Validates shares sum to 100%."""
    splits = [ContributorSplit(**c) for c in contributors]
    total = sum(s.share_percent for s in splits)

    if splits and abs(total - 100.0) > 0.01:
        raise ValueError(
            f"Contributor shares must sum to 100%, got {total:.2f}%"
        )

    return RightsBundle(
        asset_id=asset_id,
        owner=owner,
        contributors=splits,
        chain_of_title=[{"event": "created", "owner": owner}],
    )


def add_license(bundle: RightsBundle, license_data: dict) -> RightsBundle:
    """Add a license grant. Checks for exclusive conflicts."""
    grant = LicenseGrant(**license_data)

    # Check for existing exclusive licenses
    for existing in bundle.licenses:
        if existing.scope == "exclusive" and grant.scope == "exclusive":
            if existing.territory == grant.territory or existing.territory == "worldwide":
                raise ValueError(
                    f"Exclusive license conflict: existing exclusive grant to "
                    f"'{existing.licensee}' in territory '{existing.territory}'"
                )

    new_licenses = bundle.licenses + [grant]
    new_chain = bundle.chain_of_title + [{
        "event": "license_granted",
        "licensee": grant.licensee,
        "scope": grant.scope,
    }]

    return bundle.model_copy(update={
        "licenses": new_licenses,
        "chain_of_title": new_chain,
    })


def validate_rights_chain(bundle: RightsBundle) -> tuple[bool, list[str]]:
    """Validate a rights bundle for completeness and consistency."""
    issues: list[str] = []

    # Shares must sum to 100
    if bundle.contributors:
        total = sum(c.share_percent for c in bundle.contributors)
        if abs(total - 100.0) > 0.01:
            issues.append(f"Contributor shares sum to {total:.2f}%, expected 100%")

    # No overlapping exclusives in same territory
    exclusives = [l for l in bundle.licenses if l.scope == "exclusive"]
    territories_seen: set[str] = set()
    for exc in exclusives:
        if exc.territory in territories_seen:
            issues.append(f"Duplicate exclusive license in territory '{exc.territory}'")
        territories_seen.add(exc.territory)

    # All contributors should have agreed dates
    for c in bundle.contributors:
        if not c.agreed_date:
            issues.append(f"Contributor '{c.contributor}' missing agreed_date")

    # Owner should be in contributors
    contributor_names = {c.contributor for c in bundle.contributors}
    if bundle.contributors and bundle.owner not in contributor_names:
        issues.append(f"Owner '{bundle.owner}' is not listed as a contributor")

    return (len(issues) == 0, issues)


def calculate_revenue_split(
    bundle: RightsBundle,
    gross_revenue: float,
) -> dict[str, float]:
    """Split revenue by contributor shares."""
    if not bundle.contributors:
        return {bundle.owner: gross_revenue}

    return {
        c.contributor: round(gross_revenue * c.share_percent / 100.0, 2)
        for c in bundle.contributors
    }


def generate_rights_summary(bundle: RightsBundle) -> str:
    """Generate a human-readable rights summary."""
    lines = [
        f"Rights Summary for Asset: {bundle.asset_id}",
        f"Owner: {bundle.owner}",
        "",
    ]

    if bundle.contributors:
        lines.append("Contributors:")
        for c in bundle.contributors:
            lines.append(f"  - {c.contributor} ({c.role}): {c.share_percent}%")
        lines.append("")

    if bundle.licenses:
        lines.append("Licenses:")
        for lic in bundle.licenses:
            end = f" until {lic.end_date}" if lic.end_date else " (perpetual)"
            lines.append(f"  - {lic.licensee}: {lic.scope} in {lic.territory}{end}")
        lines.append("")

    if bundle.restrictions:
        lines.append("Restrictions:")
        for r in bundle.restrictions:
            lines.append(f"  - {r}")
        lines.append("")

    lines.append(f"Chain of title: {len(bundle.chain_of_title)} events")

    return "\n".join(lines)


# ── Ethics / Consent Checks ───────────────────────────────────────

def check_consent_alignment(
    bundle: RightsBundle,
    character_consent_tier: str,
    asset_type: str = "",
) -> tuple[bool, list[str]]:
    """Ensure IP usage respects the character's consent tier.

    Rules:
    - tier3_sensitive / tier4_highest: no open_source licensing
    - Exclusive licenses on real-character assets need explicit consent
    - dataset_synthetic assets require synthetic data certification
    """
    issues: list[str] = []
    high_sensitivity = character_consent_tier in ("tier3_sensitive", "tier4_highest")

    for lic in bundle.licenses:
        # No open source for sensitive tiers
        if high_sensitivity and lic.scope in ("open_source", "cc_by"):
            issues.append(
                f"License scope '{lic.scope}' to '{lic.licensee}' is not "
                f"permitted for consent tier '{character_consent_tier}'"
            )

        # Exclusive on sensitive data requires explicit terms
        if high_sensitivity and lic.scope == "exclusive" and not lic.terms:
            issues.append(
                f"Exclusive license to '{lic.licensee}' requires explicit "
                f"consent terms for tier '{character_consent_tier}'"
            )

    # Synthetic data needs certification
    if asset_type == "dataset_synthetic":
        has_cert = any(
            "synthetic" in r.lower() or "certification" in r.lower()
            for r in bundle.restrictions
        )
        if not has_cert:
            issues.append(
                "dataset_synthetic assets require a synthetic data "
                "certification restriction"
            )

    return (len(issues) == 0, issues)
