"""Cross-reference engine and gap finder for DOMES.

* ``build_cross_references`` links related provisions (statute -> regulation,
  right -> enforcement mechanism, etc.)
* ``find_gaps`` identifies provisions a person *should* benefit from but
  likely isn't receiving.
"""

from __future__ import annotations

import json
import re
from typing import Any

from app.circumstances import CrossReference, MatchResult, PersonProfile
from app.matching import _parse_applies_when, _parse_json_list, match_provisions

# ---------------------------------------------------------------------------
# Citation normalisation helpers
# ---------------------------------------------------------------------------

_USC_RE = re.compile(
    r"(\d+)\s*U\.?S\.?C\.?\s*[§]?\s*(\d+[a-z]*)",
    re.IGNORECASE,
)
_CFR_RE = re.compile(
    r"(\d+)\s*C\.?F\.?R\.?\s*(?:Part\s*|[§]\s*)?(\d+)",
    re.IGNORECASE,
)


def _extract_usc_parts(citation: str) -> list[tuple[str, str]]:
    return _USC_RE.findall(citation)


def _extract_cfr_parts(citation: str) -> list[tuple[str, str]]:
    return _CFR_RE.findall(citation)


# Well-known statute-to-regulation mappings (title-section pairs).
_STATUTE_TO_REG: dict[tuple[str, str], list[tuple[str, str]]] = {
    # Medicaid statute -> Medicaid managed-care regs
    ("42", "1396"): [("42", "438"), ("42", "440"), ("42", "441")],
    ("42", "1396a"): [("42", "438"), ("42", "440")],
    ("42", "1396d"): [("42", "441")],
    ("42", "1396n"): [("42", "441")],
    # Mental Health Parity -> implementing regs
    ("29", "1185a"): [("45", "146"), ("29", "2590")],
    # EMTALA
    ("42", "1395dd"): [("42", "489")],
    # ADA
    ("42", "12132"): [("28", "35")],
    ("42", "12182"): [("28", "36")],
    # Rehab Act
    ("29", "794"): [("34", "104")],
    # Fair Housing
    ("42", "3604"): [("24", "100")],
    # IDEA
    ("20", "1400"): [("34", "300")],
    # SSI
    ("42", "1382"): [("20", "416")],
    # SSDI
    ("42", "423"): [("20", "404")],
    # SNAP
    ("7", "2011"): [("7", "273")],
}


def _domain_matches(a: str, b: str) -> bool:
    return a == b


# ---------------------------------------------------------------------------
# Build cross-references
# ---------------------------------------------------------------------------


def build_cross_references(
    provisions: list[dict[str, Any]],
) -> dict[int, list[CrossReference]]:
    """Return a mapping from provision id -> list of CrossReference objects.

    Relationships detected:
    - implements: a CFR regulation that implements a USC statute
    - enforces: provision whose enforcement_mechanisms reference another
    - extends: provision that explicitly lists another in cross_references
    - related: provisions in the same domain with overlapping applies_when
    """

    xrefs: dict[int, list[CrossReference]] = {}
    id_to_prov: dict[int, dict] = {p["id"]: p for p in provisions}

    # Pre-index citations for fast lookup
    usc_index: dict[tuple[str, str], list[int]] = {}
    cfr_index: dict[tuple[str, str], list[int]] = {}

    for p in provisions:
        pid = p["id"]
        citation = p.get("citation", "")
        for title, section in _extract_usc_parts(citation):
            usc_index.setdefault((title, section), []).append(pid)
        for title, part in _extract_cfr_parts(citation):
            cfr_index.setdefault((title, part), []).append(pid)

    def _add(src: int, ref: CrossReference) -> None:
        xrefs.setdefault(src, []).append(ref)

    # 1. Statute <-> regulation links via known mappings
    for (stat_title, stat_sec), reg_keys in _STATUTE_TO_REG.items():
        stat_ids = usc_index.get((stat_title, stat_sec), [])
        for reg_title, reg_part in reg_keys:
            reg_ids = cfr_index.get((reg_title, reg_part), [])
            for sid in stat_ids:
                for rid in reg_ids:
                    if sid == rid:
                        continue
                    _add(
                        sid,
                        CrossReference(
                            target_id=rid,
                            target_citation=id_to_prov[rid]["citation"],
                            relationship="implements",
                            description=(
                                f"{id_to_prov[rid]['citation']} implements "
                                f"{id_to_prov[sid]['citation']}"
                            ),
                        ),
                    )
                    _add(
                        rid,
                        CrossReference(
                            target_id=sid,
                            target_citation=id_to_prov[sid]["citation"],
                            relationship="implements",
                            description=(
                                f"Implements {id_to_prov[sid]['citation']}"
                            ),
                        ),
                    )

    # 2. Explicit cross_references field
    citation_to_id: dict[str, int] = {}
    for p in provisions:
        citation_to_id[p["citation"]] = p["id"]

    for p in provisions:
        refs_raw = p.get("cross_references", "[]")
        refs = _parse_json_list(refs_raw)
        for ref_cite in refs:
            target_id = citation_to_id.get(ref_cite)
            if target_id and target_id != p["id"]:
                _add(
                    p["id"],
                    CrossReference(
                        target_id=target_id,
                        target_citation=ref_cite,
                        relationship="related",
                        description=f"Cross-referenced by {p['citation']}",
                    ),
                )

    # 3. Same-domain provisions with overlapping applies_when -> related
    by_domain: dict[str, list[dict]] = {}
    for p in provisions:
        by_domain.setdefault(p.get("domain", ""), []).append(p)

    for domain, domain_provs in by_domain.items():
        for i, a in enumerate(domain_provs):
            a_conds = _parse_applies_when(a.get("applies_when", "{}"))
            if not a_conds:
                continue
            a_keys = set(a_conds.keys())
            for b in domain_provs[i + 1 :]:
                b_conds = _parse_applies_when(b.get("applies_when", "{}"))
                if not b_conds:
                    continue
                overlap = a_keys & set(b_conds.keys())
                if len(overlap) >= 2:
                    # Check value overlap in at least one key
                    for k in overlap:
                        a_vals = set(a_conds[k]) if isinstance(a_conds[k], list) else {a_conds[k]}
                        b_vals = set(b_conds[k]) if isinstance(b_conds[k], list) else {b_conds[k]}
                        if a_vals & b_vals or "any" in a_vals or "any" in b_vals:
                            _add(
                                a["id"],
                                CrossReference(
                                    target_id=b["id"],
                                    target_citation=b["citation"],
                                    relationship="related",
                                    description=(
                                        f"Both apply in {domain} domain with "
                                        f"overlapping conditions"
                                    ),
                                ),
                            )
                            _add(
                                b["id"],
                                CrossReference(
                                    target_id=a["id"],
                                    target_citation=a["citation"],
                                    relationship="related",
                                    description=(
                                        f"Both apply in {domain} domain with "
                                        f"overlapping conditions"
                                    ),
                                ),
                            )
                            break  # one overlapping key is enough

    # Deduplicate per provision
    for pid in xrefs:
        seen: set[tuple[int, str]] = set()
        deduped: list[CrossReference] = []
        for ref in xrefs[pid]:
            key = (ref.target_id, ref.relationship)
            if key not in seen:
                seen.add(key)
                deduped.append(ref)
        xrefs[pid] = deduped

    return xrefs


# ---------------------------------------------------------------------------
# Gap finder
# ---------------------------------------------------------------------------

# Gap rules: (condition_check, provision_domain_keywords, gap_description)
# Each rule is a callable that takes the profile and returns True if the
# person's circumstances suggest they should have access to certain provisions.

_GAP_RULES: list[
    tuple[
        str,  # rule name
        # condition: callable(PersonProfile) -> bool
        Any,
        # provision filter: callable(dict) -> bool -- identifies candidate provisions
        Any,
        # gap message
        str,
    ]
] = []


def _register_gap_rule(
    name: str,
    condition: Any,
    provision_filter: Any,
    message: str,
) -> None:
    _GAP_RULES.append((name, condition, provision_filter, message))


# --- Gap rules ---

# EPSDT for Medicaid youth
_register_gap_rule(
    "epsdt",
    lambda p: "medicaid" in p.insurance and p.age_group in ("under_18", "18_to_21"),
    lambda prov: "epsdt" in prov.get("title", "").lower()
    or "1396d(r)" in prov.get("citation", ""),
    "As a Medicaid-enrolled person under 21, you are entitled to EPSDT "
    "(Early and Periodic Screening, Diagnostic and Treatment) services. "
    "This is one of the most comprehensive health benefits in federal law.",
)

# McKinney-Vento for homeless
_register_gap_rule(
    "mckinney_vento",
    lambda p: "homeless" in p.housing,
    lambda prov: "mckinney" in prov.get("title", "").lower()
    or "mckinney-vento" in prov.get("title", "").lower()
    or "11431" in prov.get("citation", ""),
    "As a person experiencing homelessness, you have rights under the "
    "McKinney-Vento Act, including education stability for children and "
    "access to emergency services.",
)

# ADA reasonable accommodation for disabled
_register_gap_rule(
    "ada_accommodation",
    lambda p: len(p.disabilities) > 0,
    lambda prov: (
        "reasonable accommodation" in prov.get("title", "").lower()
        or "ada" in prov.get("title", "").lower()
        or "12132" in prov.get("citation", "")
        or "12182" in prov.get("citation", "")
    ),
    "As a person with a disability, you may be entitled to reasonable "
    "accommodations under the ADA and Section 504.",
)

# Section 504 for disabled
_register_gap_rule(
    "section_504",
    lambda p: len(p.disabilities) > 0,
    lambda prov: "504" in prov.get("title", "")
    or "794" in prov.get("citation", ""),
    "Section 504 of the Rehabilitation Act prohibits disability "
    "discrimination in any program receiving federal funding.",
)

# IDEA for children with disabilities
_register_gap_rule(
    "idea",
    lambda p: len(p.disabilities) > 0 and p.age_group in ("under_18", "18_to_21"),
    lambda prov: "idea" in prov.get("title", "").lower()
    or "1400" in prov.get("citation", ""),
    "As a young person with a disability, you may be entitled to a free "
    "appropriate public education under IDEA, including an IEP.",
)

# Mental Health Parity for insured people with MH/SUD
_register_gap_rule(
    "mh_parity",
    lambda p: ("mental_health" in p.disabilities or "sud" in p.disabilities)
    and len(p.insurance) > 0
    and "uninsured" not in p.insurance,
    lambda prov: "parity" in prov.get("title", "").lower()
    or "1185a" in prov.get("citation", ""),
    "If you have mental health or substance use conditions and health "
    "insurance, the Mental Health Parity Act requires equal coverage for "
    "behavioral health and medical/surgical benefits.",
)

# SNAP for low-income
_register_gap_rule(
    "snap",
    lambda p: "below_poverty" in p.income or "unemployed" in p.income,
    lambda prov: "snap" in prov.get("title", "").lower()
    or "2011" in prov.get("citation", ""),
    "Based on your income, you may be eligible for SNAP (food assistance) "
    "benefits.",
)

# SSI for disabled low-income
_register_gap_rule(
    "ssi",
    lambda p: len(p.disabilities) > 0
    and ("below_poverty" in p.income or "unemployed" in p.income)
    and "ssi" not in p.income,
    lambda prov: "ssi" in prov.get("title", "").lower()
    or "1382" in prov.get("citation", ""),
    "As a person with a disability and limited income, you may be eligible "
    "for Supplemental Security Income (SSI).",
)

# VAWA for DV survivors
_register_gap_rule(
    "vawa_housing",
    lambda p: p.dv_survivor,
    lambda prov: "vawa" in prov.get("title", "").lower()
    or "violence against women" in prov.get("title", "").lower(),
    "As a survivor of domestic violence, VAWA provides housing protections "
    "including the right to remain in federally assisted housing.",
)

# Foster care Chafee/extended benefits for youth aging out
_register_gap_rule(
    "foster_care_aging_out",
    lambda p: "foster_care" in p.system_involvement
    and p.age_group in ("under_18", "18_to_21"),
    lambda prov: "foster" in prov.get("title", "").lower()
    or "chafee" in prov.get("title", "").lower()
    or "677" in prov.get("citation", ""),
    "As a young person in foster care, you may be entitled to extended "
    "benefits and independent living services under the Chafee Act.",
)

# Veteran benefits
_register_gap_rule(
    "veteran_healthcare",
    lambda p: p.veteran,
    lambda prov: "veteran" in prov.get("title", "").lower()
    or "va " in prov.get("title", "").lower(),
    "As a veteran, you may be entitled to VA healthcare, disability "
    "compensation, and other benefits.",
)

# Reentry provisions for recently released
_register_gap_rule(
    "reentry",
    lambda p: "recently_released" in p.system_involvement,
    lambda prov: "reentry" in prov.get("title", "").lower()
    or "second chance" in prov.get("title", "").lower()
    or "expungement" in prov.get("title", "").lower(),
    "As a recently released individual, you may be entitled to reentry "
    "services, record expungement, and anti-discrimination protections.",
)

# Medicaid for recently released (Medicaid inmate exclusion policy ending)
_register_gap_rule(
    "medicaid_reentry",
    lambda p: "recently_released" in p.system_involvement
    and "medicaid" not in p.insurance,
    lambda prov: "medicaid" in prov.get("title", "").lower()
    and (
        "reentry" in prov.get("full_text", "").lower()
        or "release" in prov.get("full_text", "").lower()
        or "incarcerat" in prov.get("full_text", "").lower()
    ),
    "Upon release, you may be eligible to enroll in or reactivate Medicaid "
    "coverage. Many states now provide pre-release Medicaid enrollment.",
)

# Fair Housing for anyone in housing
_register_gap_rule(
    "fair_housing",
    lambda p: len(p.housing) > 0 and len(p.disabilities) > 0,
    lambda prov: "fair housing" in prov.get("title", "").lower()
    or "3604" in prov.get("citation", ""),
    "As a person with a disability in housing, the Fair Housing Act "
    "requires reasonable accommodations and prohibits discrimination.",
)

# Olmstead community integration
_register_gap_rule(
    "olmstead",
    lambda p: len(p.disabilities) > 0
    and ("incarcerated" in p.system_involvement or "idd" in p.disabilities),
    lambda prov: "olmstead" in prov.get("title", "").lower()
    or "community integration" in prov.get("title", "").lower(),
    "Under Olmstead v. L.C., you have the right to receive services in "
    "the most integrated setting appropriate to your needs.",
)


def find_gaps(
    profile: PersonProfile,
    matched: list[MatchResult],
    all_provisions: list[dict[str, Any]],
) -> list[MatchResult]:
    """Identify provisions the person likely qualifies for but may not be receiving.

    A provision is flagged as a gap when:
    1. The person's profile triggers a gap rule, AND
    2. The provision matches the rule's filter, AND
    3. The provision wasn't already in the high-relevance matched set
       (score >= 0.8), indicating the person may not know about it.
    """
    matched_ids_high = {
        m.provision_id for m in matched if m.relevance_score >= 0.8
    }

    gaps: list[MatchResult] = []
    seen_ids: set[int] = set()

    for rule_name, condition_fn, prov_filter_fn, gap_message in _GAP_RULES:
        if not condition_fn(profile):
            continue

        for prov in all_provisions:
            pid = prov.get("id", 0)
            if pid in seen_ids:
                continue

            if not prov_filter_fn(prov):
                continue

            # If already matched at high relevance, skip -- they probably
            # already know about this one.
            if pid in matched_ids_high:
                continue

            enforcement = _parse_json_list(
                prov.get("enforcement_mechanisms", "[]")
            )

            gaps.append(
                MatchResult(
                    provision_id=pid,
                    citation=prov.get("citation", ""),
                    title=prov.get("title", ""),
                    domain=prov.get("domain", ""),
                    provision_type=prov.get("provision_type", "right"),
                    relevance_score=0.9,
                    match_reasons=[gap_message],
                    enforcement_steps=enforcement,
                    is_gap=True,
                    full_text=prov.get("full_text", ""),
                    source_url=prov.get("source_url", ""),
                    cross_references=_parse_json_list(prov.get("cross_references", "[]")),
                )
            )
            seen_ids.add(pid)

    # Sort gaps by domain for readability
    gaps.sort(key=lambda g: g.domain)
    return gaps
