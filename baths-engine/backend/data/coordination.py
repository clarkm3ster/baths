"""
Coordination Models — Real frameworks for cross-system integration.

These are the architectural patterns that the DOMES game teaches players
to design. Each model has real precedent, real legal authority, and
real cost/benefit data.
"""

# ── Real Coordination Models ──────────────────────────────────────────

COORDINATION_MODELS = [
    {
        "id": "hub_spoke",
        "name": "Hub-and-Spoke (Centralized Intake)",
        "description": "Single point of entry routes individuals to multiple services. "
                       "One intake worker screens for all programs simultaneously.",
        "real_examples": [
            "No Wrong Door (NWD) — CMS/ACL initiative for aging/disability",
            "Community Health Workers in Medicaid managed care",
            "American Job Center co-location (WIOA § 121)",
        ],
        "legal_authority": "WIOA § 121 (one-stop); ACA § 2703 (health homes); "
                          "Older Americans Act § 306(a) (aging network)",
        "systems_connected": ["CMS_MMIS", "SSA_SSR", "USDA_SNAP", "HUD_HMIS"],
        "consent_model": "Universal consent form signed at intake covers all hub partners",
        "estimated_savings_pct": 15,
        "implementation_cost": "medium",
        "time_to_implement": "12-18 months",
        "key_barrier": "Requires MOU between all participating agencies; "
                       "42 CFR Part 2 carve-out for SUD records",
        "dome_dimensions": ["healthcare", "income", "housing", "food"],
    },
    {
        "id": "shared_care_plan",
        "name": "Shared Care Plan (Person-Centered)",
        "description": "Individual has one care plan visible to all authorized providers. "
                       "Updates propagate in real-time. Person controls access.",
        "real_examples": [
            "Comprehensive Primary Care Plus (CPC+) — CMMI model",
            "Certified Community Behavioral Health Clinics (CCBHCs)",
            "VA PACT (Patient Aligned Care Teams)",
        ],
        "legal_authority": "SSA § 1115A (CMMI authority); 42 CFR § 438.208 "
                          "(Medicaid managed care coordination); MISSION Act (VA)",
        "systems_connected": ["CMS_MMIS", "CMS_MEDICARE_EDB", "VA_VISTA", "HUD_HMIS"],
        "consent_model": "HIPAA-compliant consent with granular sharing preferences; "
                        "patient portal access",
        "estimated_savings_pct": 22,
        "implementation_cost": "high",
        "time_to_implement": "18-24 months",
        "key_barrier": "Requires FHIR-capable systems across all partners; "
                       "ONC certification (45 CFR § 170.315)",
        "dome_dimensions": ["healthcare", "housing", "justice"],
    },
    {
        "id": "data_trust",
        "name": "Data Trust (Governed Sharing)",
        "description": "Independent third-party holds and governs cross-system data. "
                       "Agencies contribute data under agreed protocols. "
                       "Trust enforces privacy rules and manages access.",
        "real_examples": [
            "Actionable Intelligence for Social Policy (AISP) — UPenn",
            "Western PA Regional Data Center",
            "Allegheny County DHS predictive analytics",
        ],
        "legal_authority": "CIPSEA (Confidential Information Protection and "
                          "Statistical Efficiency Act); state-level data governance statutes; "
                          "IRB oversight for research use",
        "systems_connected": ["CMS_MMIS", "ACF_TANF", "USDA_SNAP", "DOL_UI",
                              "HUD_HMIS", "ED_NSLDS"],
        "consent_model": "De-identified data for aggregate analysis; "
                        "re-identification requires individual consent + IRB approval",
        "estimated_savings_pct": 12,
        "implementation_cost": "high",
        "time_to_implement": "24-36 months",
        "key_barrier": "Building trust between agencies; sustained funding for "
                       "governance infrastructure; political will",
        "dome_dimensions": ["data_privacy", "interoperability"],
    },
    {
        "id": "categorical_auto_enroll",
        "name": "Categorical Auto-Enrollment",
        "description": "Eligibility for one program automatically confers eligibility "
                       "for related programs. No separate application required.",
        "real_examples": [
            "Express Lane Eligibility — CHIP/Medicaid using SNAP data (42 U.S.C. § 1396a(e)(13))",
            "SSI categorical Medicaid eligibility (§ 1634 states)",
            "SNAP → free school meals (categorical eligibility)",
        ],
        "legal_authority": "SSA § 1634 (SSI/Medicaid); 42 U.S.C. § 1396a(e)(13) "
                          "(Express Lane); 42 U.S.C. § 1758(b)(2) (school meals)",
        "systems_connected": ["SSA_SSR", "CMS_MMIS", "USDA_SNAP"],
        "consent_model": "Statutory authority — no individual consent needed; "
                        "data flows between agencies by operation of law",
        "estimated_savings_pct": 18,
        "implementation_cost": "low",
        "time_to_implement": "6-12 months (state plan amendment)",
        "key_barrier": "Requires state opt-in; IT system modifications; "
                       "some states resist due to fiscal concerns about increased enrollment",
        "dome_dimensions": ["healthcare", "food", "income"],
    },
    {
        "id": "community_health_worker",
        "name": "Community Health Worker Navigation",
        "description": "Trusted community members serve as bridges between "
                       "individuals and multiple systems. CHWs help with applications, "
                       "appointments, referrals, and advocacy.",
        "real_examples": [
            "Oregon CHW program — Medicaid reimbursable since 2013",
            "Pennsylvania CHW certification (Act 19 of 2023)",
            "NYC Public Health Corps",
        ],
        "legal_authority": "ACA § 5313 (CHW grants); 42 CFR § 440.130 (Medicaid "
                          "preventive services); state CHW certification laws",
        "systems_connected": ["CMS_MMIS", "PA_COMPASS", "PHL_CARES"],
        "consent_model": "Individual authorizes CHW as representative; "
                        "limited PHI sharing under HIPAA minimum necessary",
        "estimated_savings_pct": 10,
        "implementation_cost": "low",
        "time_to_implement": "3-6 months",
        "key_barrier": "Sustainable funding (Medicaid reimbursement varies by state); "
                       "CHW workforce pipeline",
        "dome_dimensions": ["healthcare", "housing", "food", "income"],
    },
    {
        "id": "health_home",
        "name": "Medicaid Health Home (§ 2703)",
        "description": "ACA created 'health homes' for Medicaid beneficiaries with "
                       "chronic conditions — comprehensive care management, care "
                       "coordination, health promotion, referrals, and IT support. "
                       "90% federal match for first 8 quarters.",
        "real_examples": [
            "Missouri Primary Care Health Homes",
            "New York Health Home program (serves 200,000+)",
            "Rhode Island Integrated Health Home",
        ],
        "legal_authority": "SSA § 1945 (added by ACA § 2703); 42 CFR § 441.900 et seq.",
        "systems_connected": ["CMS_MMIS", "CMS_CCW", "HUD_HMIS"],
        "consent_model": "Opt-in enrollment with comprehensive consent; "
                        "designated provider coordinates all care",
        "estimated_savings_pct": 20,
        "implementation_cost": "medium",
        "time_to_implement": "12-18 months (state plan amendment + provider readiness)",
        "key_barrier": "After 8-quarter enhanced match, states must sustain at regular FMAP; "
                       "requires providers capable of whole-person care",
        "dome_dimensions": ["healthcare", "housing", "income"],
    },
    {
        "id": "social_impact_bond",
        "name": "Social Impact Bond / Pay for Success",
        "description": "Private investors fund coordination interventions. Government "
                       "pays investors back (with return) only if measurable outcomes "
                       "are achieved. Shifts risk from taxpayers to investors.",
        "real_examples": [
            "South Carolina Nurse-Family Partnership SIB (2016)",
            "Cuyahoga County Partnering for Family Success SIB (2014)",
            "Massachusetts Chronic Homelessness Pay for Success (2014)",
        ],
        "legal_authority": "SIPPRA (Social Impact Partnerships to Pay for Results Act, "
                          "P.L. 115-123, Division H); state enabling legislation",
        "systems_connected": ["CMS_MMIS", "HUD_HMIS", "ACF_TANF"],
        "consent_model": "Program participation consent; outcome data shared with "
                        "evaluator under research protocols",
        "estimated_savings_pct": 25,
        "implementation_cost": "high (but externally funded)",
        "time_to_implement": "18-30 months (structuring + fundraising)",
        "key_barrier": "High transaction costs; complex evaluation design; "
                       "limited number of investors with social sector expertise",
        "dome_dimensions": ["housing", "healthcare", "justice"],
    },
    {
        "id": "braided_funding",
        "name": "Braided/Blended Funding",
        "description": "Multiple funding streams (federal, state, local, private) "
                       "combined to serve the whole person, not just the slice each "
                       "funder cares about. Each funder still tracks their dollars "
                       "(braided) or they merge into one pool (blended).",
        "real_examples": [
            "Accountable Health Communities (CMMI) — braided Medicaid + HRSA + SAMHSA",
            "Head Start + Title I + CCDF braided early childhood funding",
            "Medicaid 1115 waivers for housing-related services",
        ],
        "legal_authority": "Varies by stream; 42 CFR § 433.51 (Medicaid FFP rules); "
                          "OMB Uniform Guidance 2 CFR Part 200 (cost allocation)",
        "systems_connected": ["CMS_MMIS", "ACF_CCDF", "HUD_IMS_PIC", "ED_NSLDS"],
        "consent_model": "Typically program-level; no individual consent for funding allocation",
        "estimated_savings_pct": 15,
        "implementation_cost": "medium",
        "time_to_implement": "12-24 months",
        "key_barrier": "OMB cost allocation rules; each stream has its own audit requirements; "
                       "fear of audit findings if costs are misallocated",
        "dome_dimensions": ["healthcare", "education", "housing", "employment"],
    },
]

# ── Coordination Scoring Framework ────────────────────────────────────

def score_coordination_model(model: dict, target_dimensions: list[str]) -> float:
    """Score how well a coordination model fits target dome dimensions."""
    model_dims = set(model.get("dome_dimensions", []))
    target_dims = set(target_dimensions)
    overlap = len(model_dims & target_dims)
    coverage = overlap / max(1, len(target_dims))

    savings = model.get("estimated_savings_pct", 0) / 100

    cost_factor = {"low": 0.9, "medium": 0.7, "high": 0.5}.get(
        model.get("implementation_cost", "medium"), 0.7
    )

    return round(coverage * 0.4 + savings * 0.4 + cost_factor * 0.2, 3)


def recommend_models(target_dimensions: list[str], top_n: int = 3) -> list[dict]:
    """Recommend top coordination models for given dome dimensions."""
    scored = []
    for model in COORDINATION_MODELS:
        score = score_coordination_model(model, target_dimensions)
        scored.append({**model, "fit_score": score})
    scored.sort(key=lambda x: x["fit_score"], reverse=True)
    return scored[:top_n]
