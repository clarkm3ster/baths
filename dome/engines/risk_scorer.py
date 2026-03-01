"""Cross-domain risk scorer engine for THE DOME (Step 4).

Computes risk scores (0-100) across nine life domains by examining the
person's ``DynamicState`` and ``DomeMetrics``.  Each domain scorer
applies evidence-informed weights to risk indicators and accumulates
points up to a cap of 100.  A weighted composite score summarises
overall risk across all domains.

Domain weights for the composite reflect policy-informed prioritisation:
    healthcare   0.20
    mental_health 0.15
    economic     0.15
    housing      0.15
    justice      0.10
    education    0.10
    social       0.10
    environmental 0.05

Usage::

    scorer = RiskScorer()
    result = scorer.score(person_state, dome_metrics)
    print(result["composite"])      # 0-100
    print(result["domain_scores"])  # dict of 9 domain scores
"""

from __future__ import annotations

from typing import Any


# ---------------------------------------------------------------------------
# Domain weight configuration for composite score
# ---------------------------------------------------------------------------

DOMAIN_WEIGHTS: dict[str, float] = {
    "healthcare": 0.20,
    "mental_health": 0.15,
    "economic": 0.15,
    "housing": 0.15,
    "justice": 0.10,
    "education": 0.10,
    "social": 0.10,
    "environmental": 0.05,
}


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _safe_float(val: Any, default: float = 0.0) -> float:
    """Coerce a value to float, returning default on failure."""
    if val is None:
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def _safe_int(val: Any, default: int = 0) -> int:
    """Coerce a value to int, returning default on failure."""
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def _safe_bool(val: Any, default: bool = False) -> bool:
    """Coerce a value to bool, returning default on failure."""
    if val is None:
        return default
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.lower() in ("true", "1", "yes", "y")
    return bool(val)


def _cap(score: float) -> float:
    """Cap a score at 0-100 range."""
    return max(0.0, min(100.0, score))


def _get_nested(data: dict, *keys: str, default: Any = None) -> Any:
    """Traverse nested dicts safely."""
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        else:
            return default
        if current is None:
            return default
    return current


# ---------------------------------------------------------------------------
# RiskScorer class
# ---------------------------------------------------------------------------

class RiskScorer:
    """Cross-domain risk scoring engine.

    Computes domain-specific risk scores and a weighted composite from
    a person's dynamic state and DOME metrics.

    The scoring approach is additive: each domain starts at 0 and
    accumulates points from individual risk indicators.  Points are
    assigned proportionally to the indicator's evidence-based
    contribution to adverse outcomes.  All scores are capped at 100.

    Parameters
    ----------
    domain_weights:
        Optional dict overriding the default composite domain weights.
        Keys must match the nine domain names; values should sum to 1.0.
    """

    def __init__(
        self,
        domain_weights: dict[str, float] | None = None,
    ) -> None:
        self.domain_weights = domain_weights or dict(DOMAIN_WEIGHTS)

    # ------------------------------------------------------------------ #
    #  Public API
    # ------------------------------------------------------------------ #

    def score(
        self,
        person_state: dict[str, Any] | Any,
        dome_metrics: dict[str, Any] | Any,
    ) -> dict[str, Any]:
        """Compute risk scores across all nine domains.

        Parameters
        ----------
        person_state:
            A ``DynamicState``-compatible dict (or Pydantic model) with
            sub-state dicts for bio, mental, econ, housing, family,
            justice, education, and program.
        dome_metrics:
            A ``DomeMetrics``-compatible dict (or Pydantic model) with
            nine layer dicts.

        Returns
        -------
        dict with keys:
            domain_scores: dict[str, float]
                Per-domain risk scores (0-100).
            composite: float
                Weighted composite across all domains (0-100).
            domain_details: dict[str, dict]
                Per-domain breakdown of contributing factors and points.
            risk_tier: str
                "low" (<25), "moderate" (25-50), "high" (50-75),
                "very_high" (>=75) based on composite.
        """
        # Normalise to dicts
        if hasattr(person_state, "model_dump"):
            ps = person_state.model_dump()
        elif hasattr(person_state, "dict"):
            ps = person_state.dict()
        elif isinstance(person_state, dict):
            ps = person_state
        else:
            ps = {}

        if hasattr(dome_metrics, "model_dump"):
            dm = dome_metrics.model_dump()
        elif hasattr(dome_metrics, "dict"):
            dm = dome_metrics.dict()
        elif isinstance(dome_metrics, dict):
            dm = dome_metrics
        else:
            dm = {}

        # Compute each domain
        healthcare_score, healthcare_detail = self._score_healthcare(ps, dm)
        mental_score, mental_detail = self._score_mental_health(ps, dm)
        economic_score, economic_detail = self._score_economic(ps, dm)
        housing_score, housing_detail = self._score_housing(ps, dm)
        justice_score, justice_detail = self._score_justice(ps, dm)
        education_score, education_detail = self._score_education(ps, dm)
        social_score, social_detail = self._score_social(ps, dm)
        environmental_score, environmental_detail = self._score_environmental(ps, dm)

        domain_scores = {
            "healthcare": healthcare_score,
            "mental_health": mental_score,
            "economic": economic_score,
            "housing": housing_score,
            "justice": justice_score,
            "education": education_score,
            "social": social_score,
            "environmental": environmental_score,
        }

        domain_details = {
            "healthcare": healthcare_detail,
            "mental_health": mental_detail,
            "economic": economic_detail,
            "housing": housing_detail,
            "justice": justice_detail,
            "education": education_detail,
            "social": social_detail,
            "environmental": environmental_detail,
        }

        # Composite: weighted average
        composite = 0.0
        weight_sum = 0.0
        for domain, weight in self.domain_weights.items():
            if domain in domain_scores:
                composite += domain_scores[domain] * weight
                weight_sum += weight

        if weight_sum > 0:
            composite = composite / weight_sum * 1.0  # already normalised if weights sum to 1
        composite = _cap(composite)

        # Risk tier
        if composite < 25:
            tier = "low"
        elif composite < 50:
            tier = "moderate"
        elif composite < 75:
            tier = "high"
        else:
            tier = "very_high"

        return {
            "domain_scores": domain_scores,
            "composite": round(composite, 2),
            "domain_details": domain_details,
            "risk_tier": tier,
        }

    # ------------------------------------------------------------------ #
    #  Domain 1: Healthcare Risk
    # ------------------------------------------------------------------ #

    def _score_healthcare(
        self,
        ps: dict[str, Any],
        dm: dict[str, Any],
    ) -> tuple[float, dict[str, Any]]:
        """Healthcare risk: chronic conditions, biometrics, utilization.

        Scoring rules:
            - Each chronic condition: +15
            - HbA1c > 7.0: +10
            - BMI > 30: +5
            - Each ER visit (12m): +8
            - Each hospitalization (12m): +12
            - Readmission in 30 days: +10
            - Polypharmacy (5+ meds): +5
            - No PCP visit in 12m: +8
            - Blood pressure >= stage 2: +7
            - Functional limitation score > 50: +10
        """
        bio = ps.get("bio_state", {}) or {}
        clinical = dm.get("clinical_layer", {}) or {}
        biometric = dm.get("biometric_layer", {}) or {}

        detail: dict[str, float] = {}
        score = 0.0

        # Chronic conditions
        conditions = bio.get("chronic_conditions", []) or clinical.get("chronic_conditions", []) or []
        n_chronic = len(conditions) if isinstance(conditions, list) else 0
        pts = n_chronic * 15
        detail["chronic_conditions"] = pts
        score += pts

        # HbA1c
        hba1c = _safe_float(bio.get("hba1c") or biometric.get("hba1c"), 0.0)
        if hba1c > 7.0:
            detail["hba1c_elevated"] = 10
            score += 10

        # BMI
        bmi = _safe_float(bio.get("bmi") or biometric.get("bmi"), 0.0)
        if bmi > 30:
            detail["bmi_obese"] = 5
            score += 5

        # ER visits
        er_visits = _safe_int(clinical.get("er_visits_12m"), 0)
        pts = er_visits * 8
        detail["er_visits"] = pts
        score += pts

        # Hospitalizations
        hospitalizations = _safe_int(clinical.get("hospitalizations_12m"), 0)
        pts = hospitalizations * 12
        detail["hospitalizations"] = pts
        score += pts

        # Readmission
        if _safe_bool(clinical.get("readmission_30d_flag")):
            detail["readmission_30d"] = 10
            score += 10

        # Polypharmacy
        if _safe_bool(clinical.get("polypharmacy_flag")):
            detail["polypharmacy"] = 5
            score += 5

        # No PCP visit
        last_pcp = clinical.get("last_pcp_visit_days_ago")
        pcp_visits = _safe_int(clinical.get("primary_care_visits_12m"), 0)
        if pcp_visits == 0 and (last_pcp is None or _safe_int(last_pcp, 999) > 365):
            detail["no_pcp_visit"] = 8
            score += 8

        # Blood pressure
        bp_cat = biometric.get("bp_category", "")
        if bp_cat in ("hypertension_stage_2", "hypertensive_crisis"):
            detail["hypertension_severe"] = 7
            score += 7

        # Functional limitations
        func_score = _safe_float(bio.get("functional_limitations_score") or biometric.get("functional_limitations_score"), 0.0)
        if func_score > 50:
            detail["functional_limitation"] = 10
            score += 10

        score = _cap(score)
        return score, detail

    # ------------------------------------------------------------------ #
    #  Domain 2: Mental Health Risk
    # ------------------------------------------------------------------ #

    def _score_mental_health(
        self,
        ps: dict[str, Any],
        dm: dict[str, Any],
    ) -> tuple[float, dict[str, Any]]:
        """Mental health risk: depression, SUD, psychosis, suicide risk.

        Scoring rules:
            - Depression (PHQ-9 >= 10): +20
            - SUD severity > 0: +25
            - Psychosis flag: +30
            - Suicide risk score > 0.3: +35
            - Anxiety (GAD-7 >= 10): +10
            - No treatment engagement (score < 0.3): +10
            - Substance use active: +5 (additive to SUD)
        """
        mental = ps.get("mental_state", {}) or {}
        behavioral = dm.get("behavioral_layer", {}) or {}

        detail: dict[str, float] = {}
        score = 0.0

        # Depression
        depression = _safe_float(mental.get("depression_severity"), 0.0)
        if depression >= 10:
            detail["depression"] = 20
            score += 20

        # SUD
        sud = _safe_float(mental.get("sud_severity") or behavioral.get("substance_use_severity"), 0.0)
        if sud > 0:
            detail["substance_use_disorder"] = 25
            score += 25

        # Psychosis
        if _safe_bool(mental.get("psychosis_flag")):
            detail["psychosis"] = 30
            score += 30

        # Suicide risk
        suicide_risk = _safe_float(mental.get("suicide_risk_score"), 0.0)
        if suicide_risk > 0.3:
            detail["suicide_risk"] = 35
            score += 35

        # Anxiety
        anxiety = _safe_float(mental.get("anxiety_severity"), 0.0)
        if anxiety >= 10:
            detail["anxiety"] = 10
            score += 10

        # Poor treatment engagement
        engagement = behavioral.get("treatment_engagement_score")
        if engagement is not None and _safe_float(engagement, 1.0) < 0.3:
            detail["poor_treatment_engagement"] = 10
            score += 10

        # Active substance use (additive signal beyond SUD diagnosis)
        if _safe_bool(behavioral.get("substance_use_any")) and sud == 0:
            detail["active_substance_use"] = 5
            score += 5

        score = _cap(score)
        return score, detail

    # ------------------------------------------------------------------ #
    #  Domain 3: Economic Risk
    # ------------------------------------------------------------------ #

    def _score_economic(
        self,
        ps: dict[str, Any],
        dm: dict[str, Any],
    ) -> tuple[float, dict[str, Any]]:
        """Economic risk: unemployment, income, assets, debt.

        Scoring rules:
            - Unemployed: +20
            - Income volatility > 0.5: +15
            - No assets (< $1000): +10
            - Income < 100% FPL: +15
            - Income 100-200% FPL: +8
            - Debt-to-income > 0.5: +10
            - Bankruptcy: +8
            - No employer benefits: +5
            - Negative net worth: +7
        """
        econ = ps.get("econ_state", {}) or {}
        econ_layer = dm.get("economic_layer", {}) or {}

        detail: dict[str, float] = {}
        score = 0.0

        # Unemployment
        emp_status = econ.get("employment_status") or econ_layer.get("employment_status")
        if emp_status in ("unemployed",):
            detail["unemployment"] = 20
            score += 20

        # Income volatility
        vol = _safe_float(
            econ.get("income_volatility_score") or econ_layer.get("income_volatility_score"), 0.0
        )
        if vol > 0.5:
            detail["income_volatility"] = 15
            score += 15

        # Assets
        assets = econ.get("assets_estimate") or econ_layer.get("total_assets")
        if assets is not None and _safe_float(assets, 0.0) < 1000:
            detail["no_assets"] = 10
            score += 10

        # Income relative to FPL
        income_pct_fpl = econ_layer.get("income_as_pct_fpl")
        if income_pct_fpl is not None:
            fpl = _safe_float(income_pct_fpl, 999)
            if fpl < 100:
                detail["deep_poverty"] = 15
                score += 15
            elif fpl < 200:
                detail["near_poverty"] = 8
                score += 8
        else:
            # Fallback: use raw income
            income = _safe_float(econ.get("current_annual_income") or econ_layer.get("annual_income"), 0.0)
            if income > 0 and income < 15_060:
                detail["deep_poverty"] = 15
                score += 15
            elif income > 0 and income < 30_120:
                detail["near_poverty"] = 8
                score += 8

        # Debt-to-income
        dti = econ_layer.get("debt_to_income_ratio")
        if dti is not None and _safe_float(dti, 0.0) > 0.5:
            detail["high_debt_burden"] = 10
            score += 10

        # Bankruptcy
        if _safe_bool(econ_layer.get("bankruptcy_flag")):
            detail["bankruptcy"] = 8
            score += 8

        # No employer benefits
        if not _safe_bool(econ_layer.get("employer_benefits_flag")) and emp_status not in ("retired", "disabled"):
            detail["no_employer_benefits"] = 5
            score += 5

        # Negative net worth
        net_worth = econ_layer.get("net_worth")
        if net_worth is not None and _safe_float(net_worth, 0.0) < 0:
            detail["negative_net_worth"] = 7
            score += 7

        score = _cap(score)
        return score, detail

    # ------------------------------------------------------------------ #
    #  Domain 4: Housing Risk
    # ------------------------------------------------------------------ #

    def _score_housing(
        self,
        ps: dict[str, Any],
        dm: dict[str, Any],
    ) -> tuple[float, dict[str, Any]]:
        """Housing risk: homelessness, instability, cost burden.

        Scoring rules:
            - Street homeless: +40
            - Shelter: +30
            - Cost burdened: +15
            - Homeless history flag: +10
            - Doubled up: +12
            - Housing quality < 30: +10
            - Rent-to-income > 0.5: +8
            - Nights homeless > 30 past year: +10
        """
        housing = ps.get("housing_state", {}) or {}

        detail: dict[str, float] = {}
        score = 0.0

        status = housing.get("housing_status", "stable")

        if status == "street":
            detail["street_homeless"] = 40
            score += 40
        elif status == "shelter":
            detail["shelter"] = 30
            score += 30
        elif status == "cost_burdened":
            detail["cost_burdened"] = 15
            score += 15
        elif status == "doubled_up":
            detail["doubled_up"] = 12
            score += 12

        if _safe_bool(housing.get("homelessness_history_flag")):
            detail["homeless_history"] = 10
            score += 10

        hq = housing.get("housing_quality_score")
        if hq is not None and _safe_float(hq, 100.0) < 30:
            detail["poor_housing_quality"] = 10
            score += 10

        rti = housing.get("rent_to_income_ratio")
        if rti is not None and _safe_float(rti, 0.0) > 0.5:
            detail["severe_rent_burden"] = 8
            score += 8

        nights = _safe_int(housing.get("nights_homeless_past_year"), 0)
        if nights > 30:
            detail["chronic_homelessness"] = 10
            score += 10

        score = _cap(score)
        return score, detail

    # ------------------------------------------------------------------ #
    #  Domain 5: Justice Risk
    # ------------------------------------------------------------------ #

    def _score_justice(
        self,
        ps: dict[str, Any],
        dm: dict[str, Any],
    ) -> tuple[float, dict[str, Any]]:
        """Justice risk: incarceration, supervision, contacts.

        Scoring rules:
            - Current incarceration (prison days > 300): +40
            - Recent jail (jail days > 0 past 12m): +20
            - Current supervision (probation/parole): +15
            - Police contacts > 2 past 12m: +10
            - Active court cases > 0: +8
            - Felony conviction: +10
            - Sex offender registry: +15
        """
        justice = ps.get("justice_state", {}) or {}
        legal = dm.get("legal_layer", {}) or {}

        detail: dict[str, float] = {}
        score = 0.0

        prison_days = _safe_int(justice.get("past_12m_prison_days") or legal.get("past_12m_prison_days"), 0)
        jail_days = _safe_int(justice.get("past_12m_jail_days") or legal.get("past_12m_jail_days"), 0)

        # Current incarceration
        current_incarcerated = _safe_bool(legal.get("current_incarceration_flag"))
        if current_incarcerated or prison_days > 300:
            detail["current_incarceration"] = 40
            score += 40

        # Recent jail
        if jail_days > 0:
            detail["recent_jail"] = 20
            score += 20

        # Supervision
        supervision = (
            justice.get("current_supervision_status")
            or legal.get("current_supervision_status")
        )
        if supervision is not None and supervision not in ("none", "", "None"):
            detail["supervision"] = 15
            score += 15

        # Police contacts
        contacts = _safe_int(
            justice.get("past_12m_police_contacts") or legal.get("past_12m_police_contacts"), 0
        )
        if contacts > 2:
            detail["frequent_police_contacts"] = 10
            score += 10

        # Active court cases
        active_cases = _safe_int(legal.get("active_court_cases"), 0)
        if active_cases > 0:
            detail["active_court_cases"] = 8
            score += 8

        # Felony conviction
        if _safe_bool(legal.get("felony_conviction_flag")):
            detail["felony_conviction"] = 10
            score += 10

        # Sex offender registry
        if _safe_bool(legal.get("sex_offender_registry_flag")):
            detail["sex_offender_registry"] = 15
            score += 15

        score = _cap(score)
        return score, detail

    # ------------------------------------------------------------------ #
    #  Domain 6: Education Risk
    # ------------------------------------------------------------------ #

    def _score_education(
        self,
        ps: dict[str, Any],
        dm: dict[str, Any],
    ) -> tuple[float, dict[str, Any]]:
        """Education risk: attainment, literacy, special education.

        Scoring rules:
            - Less than high school: +25
            - Special education history: +10
            - Low literacy (score < 200 on PIAAC scale): +15
            - Not enrolled when under 25 with <HS: +10
            - HS only with no post-secondary: +5
        """
        edu = ps.get("education_state", {}) or {}

        detail: dict[str, float] = {}
        score = 0.0

        credential = edu.get("highest_credential", "HS")

        if credential == "<HS":
            detail["less_than_hs"] = 25
            score += 25

            # Not enrolled: extra risk for young adults
            if not _safe_bool(edu.get("currently_enrolled_flag")):
                detail["not_enrolled_low_ed"] = 10
                score += 10
        elif credential == "HS":
            detail["hs_only"] = 5
            score += 5

        if _safe_bool(edu.get("special_ed_history_flag")):
            detail["special_ed_history"] = 10
            score += 10

        literacy = edu.get("literacy_score")
        if literacy is not None and _safe_float(literacy, 500) < 200:
            detail["low_literacy"] = 15
            score += 15

        score = _cap(score)
        return score, detail

    # ------------------------------------------------------------------ #
    #  Domain 7: Social Risk
    # ------------------------------------------------------------------ #

    def _score_social(
        self,
        ps: dict[str, Any],
        dm: dict[str, Any],
    ) -> tuple[float, dict[str, Any]]:
        """Social risk: isolation, network, caregiving, violence.

        Scoring rules:
            - Social isolation score >= 0.7: +20
            - No social network (size = 0): +15
            - Small network (size 1-2): +5
            - Caregiving burden score >= 60: +10
            - Domestic violence: +15
            - Language barrier: +8
            - No community engagement: +5
        """
        family = ps.get("family_state", {}) or {}
        social = dm.get("social_layer", {}) or {}

        detail: dict[str, float] = {}
        score = 0.0

        # Isolation
        isolation = _safe_float(
            family.get("social_isolation_score") or social.get("social_isolation_score"), 0.0
        )
        if isolation >= 0.7:
            detail["social_isolation"] = 20
            score += 20

        # Network size
        net_size = family.get("social_network_size") or social.get("social_network_size")
        if net_size is not None:
            ns = _safe_int(net_size, -1)
            if ns == 0:
                detail["no_network"] = 15
                score += 15
            elif ns <= 2:
                detail["very_small_network"] = 5
                score += 5

        # Caregiving burden
        caregiving = _safe_float(
            family.get("caregiving_burden_score") or social.get("caregiving_burden_score"), 0.0
        )
        if caregiving >= 60:
            detail["caregiving_burden"] = 10
            score += 10

        # Domestic violence
        if _safe_bool(social.get("domestic_violence_flag")):
            detail["domestic_violence"] = 15
            score += 15

        # Language barrier
        if _safe_bool(social.get("language_barrier_flag")):
            detail["language_barrier"] = 8
            score += 8

        # Community engagement
        community = social.get("community_engagement_score")
        if community is not None and _safe_float(community, 10.0) < 2.0:
            detail["no_community_engagement"] = 5
            score += 5

        score = _cap(score)
        return score, detail

    # ------------------------------------------------------------------ #
    #  Domain 8: Environmental Risk
    # ------------------------------------------------------------------ #

    def _score_environmental(
        self,
        ps: dict[str, Any],
        dm: dict[str, Any],
    ) -> tuple[float, dict[str, Any]]:
        """Environmental risk: ADI, housing quality, pollution, access.

        Scoring rules:
            - High ADI (national rank >= 80): +15
            - Poor housing quality (score < 40): +10
            - High lead exposure risk (>= 0.7): +10
            - Poor air quality (AQI > 150): +8
            - Food desert: +8
            - No internet access: +5
            - Superfund proximity: +7
            - High neighbourhood poverty (> 30%): +8
            - No transit access (score < 2): +5
        """
        env = dm.get("environmental_layer", {}) or {}
        housing = ps.get("housing_state", {}) or {}

        detail: dict[str, float] = {}
        score = 0.0

        # ADI
        adi = env.get("adi_national_rank")
        if adi is not None and _safe_float(adi, 0.0) >= 80:
            detail["high_adi"] = 15
            score += 15

        # Housing quality
        hq = _safe_float(
            housing.get("housing_quality_score") or env.get("housing_quality_score"), 100.0
        )
        if hq < 40:
            detail["poor_housing_quality"] = 10
            score += 10

        # Lead exposure
        lead = env.get("lead_exposure_risk")
        if lead is not None and _safe_float(lead, 0.0) >= 0.7:
            detail["lead_exposure"] = 10
            score += 10

        # Air quality
        aqi = env.get("air_quality_index")
        if aqi is not None and _safe_float(aqi, 0.0) > 150:
            detail["poor_air_quality"] = 8
            score += 8

        # Food desert
        if _safe_bool(env.get("food_desert_flag")):
            detail["food_desert"] = 8
            score += 8

        # Internet access
        internet = env.get("internet_access_flag")
        if internet is not None and not _safe_bool(internet):
            detail["no_internet"] = 5
            score += 5

        # Superfund
        if _safe_bool(env.get("superfund_proximity_flag")):
            detail["superfund_proximity"] = 7
            score += 7

        # Neighbourhood poverty
        poverty = env.get("census_tract_poverty_rate")
        if poverty is not None and _safe_float(poverty, 0.0) > 30:
            detail["high_poverty_rate"] = 8
            score += 8

        # Transit access
        transit = env.get("public_transit_access_score")
        if transit is not None and _safe_float(transit, 10.0) < 2.0:
            detail["no_transit"] = 5
            score += 5

        score = _cap(score)
        return score, detail
