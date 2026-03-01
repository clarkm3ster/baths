"""Metric ingestion engine for THE DOME (Step 3).

Populates all nine layers of the ``DomeMetrics`` model from heterogeneous
raw data sources.  Each layer extractor produces a typed dict of 10-20
metrics derived from clinical records, assessment instruments, economic
databases, environmental indices, and administrative system data.

Usage::

    ingestor = MetricIngestor()
    dome_metrics = ingestor.ingest(person_dict, raw_data)
"""

from __future__ import annotations

import math
from datetime import date, datetime
from typing import Any


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _safe_float(val: Any, default: float | None = None) -> float | None:
    """Coerce a value to float, returning *default* on failure."""
    if val is None:
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def _safe_int(val: Any, default: int | None = None) -> int | None:
    """Coerce a value to int, returning *default* on failure."""
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def _safe_bool(val: Any, default: bool = False) -> bool:
    """Coerce a value to bool, returning *default* on failure."""
    if val is None:
        return default
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.lower() in ("true", "1", "yes", "y")
    return bool(val)


def _clamp(val: float | None, lo: float, hi: float) -> float | None:
    """Clamp a value to [lo, hi], or return None if input is None."""
    if val is None:
        return None
    return max(lo, min(hi, val))


def _count_items(data: Any, key: str) -> int:
    """Count items in a list-valued field of a dict, safely."""
    items = data.get(key) if isinstance(data, dict) else None
    if isinstance(items, list):
        return len(items)
    return 0


def _age_from_dob(dob: Any) -> float | None:
    """Compute age in years from a date-of-birth value."""
    if dob is None:
        return None
    if isinstance(dob, str):
        try:
            dob = date.fromisoformat(dob)
        except ValueError:
            return None
    if isinstance(dob, datetime):
        dob = dob.date()
    if isinstance(dob, date):
        today = date.today()
        delta = today - dob
        return delta.days / 365.25
    return None


# ---------------------------------------------------------------------------
# BMI calculator
# ---------------------------------------------------------------------------

def _compute_bmi(
    weight_kg: float | None,
    height_cm: float | None,
    raw_bmi: float | None,
) -> float | None:
    """Compute BMI from weight/height, or return the raw value if provided."""
    if raw_bmi is not None:
        return _clamp(raw_bmi, 5.0, 100.0)
    if weight_kg and height_cm and height_cm > 0:
        height_m = height_cm / 100.0
        bmi = weight_kg / (height_m * height_m)
        return _clamp(round(bmi, 1), 5.0, 100.0)
    return None


# ---------------------------------------------------------------------------
# Blood-pressure classification
# ---------------------------------------------------------------------------

def _bp_category(systolic: float | None, diastolic: float | None) -> str:
    """Classify blood pressure into AHA categories."""
    if systolic is None or diastolic is None:
        return "unknown"
    if systolic < 120 and diastolic < 80:
        return "normal"
    if systolic < 130 and diastolic < 80:
        return "elevated"
    if systolic < 140 or diastolic < 90:
        return "hypertension_stage_1"
    if systolic >= 180 or diastolic >= 120:
        return "hypertensive_crisis"
    return "hypertension_stage_2"


# ---------------------------------------------------------------------------
# Debt-to-income ratio
# ---------------------------------------------------------------------------

def _debt_to_income(
    monthly_debt: float | None,
    annual_income: float | None,
) -> float | None:
    """Compute debt-to-income ratio."""
    if monthly_debt is None or annual_income is None:
        return None
    monthly_income = annual_income / 12.0
    if monthly_income <= 0:
        return None
    return round(monthly_debt / monthly_income, 4)


# ---------------------------------------------------------------------------
# MetricIngestor class
# ---------------------------------------------------------------------------

class MetricIngestor:
    """Populates the nine-layer DomeMetrics from heterogeneous raw data.

    The ``ingest`` method dispatches to per-layer extractors.  Each
    extractor accepts the person record and the raw data dict, and
    returns a typed dict of metrics.  Missing or uncomputable metrics
    are set to None rather than omitted, so that downstream engines
    can distinguish "not available" from "not applicable".

    Parameters
    ----------
    person:
        A Person-compatible dict or Pydantic model instance.  Must
        contain at least ``dynamic_state`` and ``identity_spine`` sub-
        structures.
    raw_data:
        Arbitrary dict whose keys map to data-source namespaces::

            {
                "clinical": {...},     # EHR / claims
                "assessments": {...},  # screenings, PHQ-9, etc.
                "economic": {...},     # tax, benefits, employment
                "environmental": {...},# census/ACS, EPA, HUD
                "social": {...},       # HMIS, case management
                "institutional": {...},# enrollment databases
                "legal": {...},        # court, DOC, probation
                "subjective": {...},   # self-report surveys
            }
    """

    def ingest(
        self,
        person: Any,
        raw_data: dict[str, Any],
    ) -> dict[str, dict[str, Any]]:
        """Ingest raw data and return a DomeMetrics-compatible dict.

        Returns
        -------
        dict with nine layer keys, each mapping to a dict of typed
        metrics.
        """
        # Normalise person to dict
        if hasattr(person, "model_dump"):
            person_dict = person.model_dump()
        elif hasattr(person, "dict"):
            person_dict = person.dict()
        elif isinstance(person, dict):
            person_dict = person
        else:
            person_dict = {}

        return {
            "biometric_layer": self._extract_biometric(person_dict, raw_data),
            "clinical_layer": self._extract_clinical(person_dict, raw_data),
            "behavioral_layer": self._extract_behavioral(person_dict, raw_data),
            "economic_layer": self._extract_economic(person_dict, raw_data),
            "environmental_layer": self._extract_environmental(person_dict, raw_data),
            "social_layer": self._extract_social(person_dict, raw_data),
            "institutional_layer": self._extract_institutional(person_dict, raw_data),
            "legal_layer": self._extract_legal(person_dict, raw_data),
            "subjective_wellbeing_layer": self._extract_subjective(person_dict, raw_data),
        }

    # ------------------------------------------------------------------ #
    #  Layer 1: Biometric
    # ------------------------------------------------------------------ #

    def _extract_biometric(
        self,
        person: dict[str, Any],
        raw: dict[str, Any],
    ) -> dict[str, Any]:
        """Extract biometric indicators from clinical and assessment data.

        Metrics:
            bmi, bmi_category, weight_kg, height_cm,
            blood_pressure_systolic, blood_pressure_diastolic,
            bp_category, hba1c, hba1c_controlled,
            total_cholesterol, ldl, hdl, triglycerides,
            functional_limitations_score, functional_category,
            resting_heart_rate, respiratory_rate, oxygen_saturation,
            pain_score, vision_acuity, hearing_status
        """
        clinical = raw.get("clinical", {}) or {}
        bio = person.get("dynamic_state", {}).get("bio_state", {}) or {}
        vitals = clinical.get("vitals", {}) or {}
        labs = clinical.get("labs", {}) or {}

        weight_kg = _safe_float(vitals.get("weight_kg") or bio.get("weight_kg"))
        height_cm = _safe_float(vitals.get("height_cm") or bio.get("height_cm"))
        raw_bmi = _safe_float(bio.get("bmi") or vitals.get("bmi"))
        bmi = _compute_bmi(weight_kg, height_cm, raw_bmi)

        systolic = _safe_float(
            vitals.get("blood_pressure_systolic")
            or bio.get("blood_pressure_systolic")
        )
        diastolic = _safe_float(
            vitals.get("blood_pressure_diastolic")
            or bio.get("blood_pressure_diastolic")
        )

        hba1c = _safe_float(labs.get("hba1c") or bio.get("hba1c"))
        func_score = _safe_float(bio.get("functional_limitations_score"))

        # Lipids
        total_chol = _safe_float(labs.get("total_cholesterol"))
        ldl = _safe_float(labs.get("ldl"))
        hdl = _safe_float(labs.get("hdl"))
        triglycerides = _safe_float(labs.get("triglycerides"))

        # Additional vitals
        rhr = _safe_float(vitals.get("resting_heart_rate"))
        resp_rate = _safe_float(vitals.get("respiratory_rate"))
        spo2 = _safe_float(vitals.get("oxygen_saturation"))
        pain = _safe_float(vitals.get("pain_score"))
        vision = vitals.get("vision_acuity")
        hearing = vitals.get("hearing_status")

        # Derived categories
        bmi_cat = "unknown"
        if bmi is not None:
            if bmi < 18.5:
                bmi_cat = "underweight"
            elif bmi < 25:
                bmi_cat = "normal"
            elif bmi < 30:
                bmi_cat = "overweight"
            elif bmi < 35:
                bmi_cat = "obese_class_1"
            elif bmi < 40:
                bmi_cat = "obese_class_2"
            else:
                bmi_cat = "obese_class_3"

        func_cat = "unknown"
        if func_score is not None:
            if func_score < 10:
                func_cat = "none"
            elif func_score < 30:
                func_cat = "mild"
            elif func_score < 60:
                func_cat = "moderate"
            else:
                func_cat = "severe"

        return {
            "bmi": bmi,
            "bmi_category": bmi_cat,
            "weight_kg": weight_kg,
            "height_cm": height_cm,
            "blood_pressure_systolic": systolic,
            "blood_pressure_diastolic": diastolic,
            "bp_category": _bp_category(systolic, diastolic),
            "hba1c": hba1c,
            "hba1c_controlled": hba1c is not None and hba1c < 7.0,
            "total_cholesterol": total_chol,
            "ldl": ldl,
            "hdl": hdl,
            "triglycerides": triglycerides,
            "functional_limitations_score": func_score,
            "functional_category": func_cat,
            "resting_heart_rate": rhr,
            "respiratory_rate": resp_rate,
            "oxygen_saturation": spo2,
            "pain_score": pain,
            "vision_acuity": vision,
            "hearing_status": hearing,
        }

    # ------------------------------------------------------------------ #
    #  Layer 2: Clinical
    # ------------------------------------------------------------------ #

    def _extract_clinical(
        self,
        person: dict[str, Any],
        raw: dict[str, Any],
    ) -> dict[str, Any]:
        """Extract clinical indicators from EHR / claims data.

        Metrics:
            diagnosis_codes, diagnosis_count, chronic_condition_count,
            chronic_conditions, procedure_count, medication_count,
            er_visits_12m, hospitalizations_12m, inpatient_days_12m,
            outpatient_visits_12m, specialist_visits_12m,
            primary_care_visits_12m, readmission_30d_flag,
            last_pcp_visit_days_ago, preventive_care_up_to_date,
            active_medication_classes, polypharmacy_flag
        """
        clinical = raw.get("clinical", {}) or {}
        bio = person.get("dynamic_state", {}).get("bio_state", {}) or {}
        utilization = clinical.get("utilization", {}) or {}
        medications = clinical.get("medications", []) or []

        dx_codes = clinical.get("diagnosis_codes", []) or bio.get("chronic_conditions", []) or []
        if isinstance(dx_codes, str):
            dx_codes = [dx_codes]

        chronic = bio.get("chronic_conditions", []) or clinical.get("chronic_conditions", []) or []
        if isinstance(chronic, str):
            chronic = [chronic]

        procedures = clinical.get("procedures", []) or []
        if isinstance(procedures, str):
            procedures = [procedures]

        er_visits = _safe_int(utilization.get("er_visits_12m") or clinical.get("er_visits_12m"), 0)
        hospitalizations = _safe_int(
            utilization.get("hospitalizations_12m") or clinical.get("hospitalizations_12m"), 0
        )
        inpatient_days = _safe_int(
            utilization.get("inpatient_days_12m") or clinical.get("inpatient_days_12m"), 0
        )
        outpatient = _safe_int(
            utilization.get("outpatient_visits_12m") or clinical.get("outpatient_visits_12m"), 0
        )
        specialist = _safe_int(utilization.get("specialist_visits_12m"), 0)
        pcp_visits = _safe_int(utilization.get("primary_care_visits_12m"), 0)
        readmit_flag = _safe_bool(utilization.get("readmission_30d_flag"))

        last_pcp_days = _safe_int(utilization.get("last_pcp_visit_days_ago"))
        preventive_up_to_date = _safe_bool(utilization.get("preventive_care_up_to_date"))

        if isinstance(medications, list):
            med_count = len(medications)
            med_classes = list({m.get("drug_class", m) if isinstance(m, dict) else str(m) for m in medications})
        else:
            med_count = 0
            med_classes = []

        return {
            "diagnosis_codes": dx_codes,
            "diagnosis_count": len(dx_codes),
            "chronic_condition_count": len(chronic),
            "chronic_conditions": chronic,
            "procedure_count": len(procedures),
            "medication_count": med_count,
            "er_visits_12m": er_visits,
            "hospitalizations_12m": hospitalizations,
            "inpatient_days_12m": inpatient_days,
            "outpatient_visits_12m": outpatient,
            "specialist_visits_12m": specialist,
            "primary_care_visits_12m": pcp_visits,
            "readmission_30d_flag": readmit_flag,
            "last_pcp_visit_days_ago": last_pcp_days,
            "preventive_care_up_to_date": preventive_up_to_date,
            "active_medication_classes": med_classes,
            "polypharmacy_flag": med_count >= 5,
        }

    # ------------------------------------------------------------------ #
    #  Layer 3: Behavioral
    # ------------------------------------------------------------------ #

    def _extract_behavioral(
        self,
        person: dict[str, Any],
        raw: dict[str, Any],
    ) -> dict[str, Any]:
        """Extract behavioral indicators from assessments and clinical data.

        Metrics:
            substance_use_any, substance_use_types, substance_use_severity,
            tobacco_current, alcohol_use_risk_level,
            medication_adherence_score, medication_adherence_category,
            treatment_engagement_score, missed_appointments_12m,
            appointment_no_show_rate, exercise_days_per_week,
            sleep_quality_score, nutrition_quality_score,
            screen_time_hours_daily, gambling_flag
        """
        assessments = raw.get("assessments", {}) or {}
        clinical = raw.get("clinical", {}) or {}
        mental = person.get("dynamic_state", {}).get("mental_state", {}) or {}
        behavioral = assessments.get("behavioral", {}) or {}

        # Substance use
        sud_severity = _safe_float(mental.get("sud_severity") or behavioral.get("sud_severity"))
        substance_types = behavioral.get("substance_use_types", []) or []
        if isinstance(substance_types, str):
            substance_types = [substance_types]
        substance_any = bool(substance_types) or (sud_severity is not None and sud_severity > 0)

        tobacco = _safe_bool(behavioral.get("tobacco_current"))
        alcohol_risk = behavioral.get("alcohol_use_risk_level", "unknown")

        # Medication adherence
        adherence_score = _safe_float(behavioral.get("medication_adherence_score"))
        if adherence_score is not None:
            adherence_score = _clamp(adherence_score, 0.0, 1.0)
        adherence_cat = "unknown"
        if adherence_score is not None:
            if adherence_score >= 0.8:
                adherence_cat = "high"
            elif adherence_score >= 0.5:
                adherence_cat = "moderate"
            else:
                adherence_cat = "low"

        # Treatment engagement
        engagement = _safe_float(behavioral.get("treatment_engagement_score"))
        if engagement is not None:
            engagement = _clamp(engagement, 0.0, 1.0)
        missed_appts = _safe_int(
            behavioral.get("missed_appointments_12m")
            or clinical.get("utilization", {}).get("missed_appointments_12m"),
            0,
        )
        total_appts = _safe_int(behavioral.get("total_appointments_12m"), 0)
        no_show_rate = None
        if total_appts and total_appts > 0:
            no_show_rate = round(missed_appts / total_appts, 4)

        # Lifestyle
        exercise = _safe_float(behavioral.get("exercise_days_per_week"))
        sleep = _safe_float(behavioral.get("sleep_quality_score"))
        nutrition = _safe_float(behavioral.get("nutrition_quality_score"))
        screen_time = _safe_float(behavioral.get("screen_time_hours_daily"))
        gambling = _safe_bool(behavioral.get("gambling_flag"))

        return {
            "substance_use_any": substance_any,
            "substance_use_types": substance_types,
            "substance_use_severity": sud_severity,
            "tobacco_current": tobacco,
            "alcohol_use_risk_level": alcohol_risk,
            "medication_adherence_score": adherence_score,
            "medication_adherence_category": adherence_cat,
            "treatment_engagement_score": engagement,
            "missed_appointments_12m": missed_appts,
            "appointment_no_show_rate": no_show_rate,
            "exercise_days_per_week": exercise,
            "sleep_quality_score": sleep,
            "nutrition_quality_score": nutrition,
            "screen_time_hours_daily": screen_time,
            "gambling_flag": gambling,
        }

    # ------------------------------------------------------------------ #
    #  Layer 4: Economic
    # ------------------------------------------------------------------ #

    def _extract_economic(
        self,
        person: dict[str, Any],
        raw: dict[str, Any],
    ) -> dict[str, Any]:
        """Extract economic indicators from tax, benefits, and employment data.

        Metrics:
            annual_income, monthly_income, income_as_pct_fpl,
            income_volatility_score, income_trend,
            employment_status, employment_duration_months,
            occupation_category, employer_benefits_flag,
            total_assets, total_debts, debt_to_income_ratio,
            net_worth, credit_score_band, bankruptcy_flag,
            public_benefits_income_monthly, tax_liability_annual,
            financial_hardship_index
        """
        economic = raw.get("economic", {}) or {}
        econ_state = person.get("dynamic_state", {}).get("econ_state", {}) or {}

        annual_income = _safe_float(
            economic.get("annual_income") or econ_state.get("current_annual_income")
        )
        monthly_income = round(annual_income / 12.0, 2) if annual_income else None

        # FPL for single person (2024) ~ $15,060
        fpl_single = 15_060.0
        household_size = _safe_int(
            person.get("dynamic_state", {}).get("family_state", {}).get("household_size"),
            1,
        )
        # FPL scales: $15,060 for 1, add ~$5,380 per additional person
        fpl_threshold = fpl_single + (household_size - 1) * 5_380.0
        income_pct_fpl = None
        if annual_income is not None and fpl_threshold > 0:
            income_pct_fpl = round(annual_income / fpl_threshold * 100, 1)

        income_vol = _safe_float(
            economic.get("income_volatility_score")
            or econ_state.get("income_volatility_score")
        )
        income_trend = economic.get("income_trend", "stable")

        emp_status = econ_state.get("employment_status") or economic.get("employment_status")
        emp_duration = _safe_int(economic.get("employment_duration_months"))
        occupation = econ_state.get("occupation_code") or economic.get("occupation_category")
        employer_benefits = _safe_bool(economic.get("employer_benefits_flag"))

        total_assets = _safe_float(econ_state.get("assets_estimate") or economic.get("total_assets"))
        total_debts = _safe_float(econ_state.get("debts_estimate") or economic.get("total_debts"))

        monthly_debt = _safe_float(economic.get("monthly_debt_payments"))
        dti = _debt_to_income(monthly_debt, annual_income)

        net_worth = None
        if total_assets is not None and total_debts is not None:
            net_worth = round(total_assets - total_debts, 2)

        credit_band = economic.get("credit_score_band")
        bankruptcy = _safe_bool(economic.get("bankruptcy_flag"))

        benefits_monthly = _safe_float(economic.get("public_benefits_income_monthly"))
        tax_liability = _safe_float(economic.get("tax_liability_annual"))

        # Financial hardship index: composite of income, debt, assets
        hardship = None
        if annual_income is not None:
            hardship = 0.0
            if income_pct_fpl is not None and income_pct_fpl < 200:
                hardship += (200 - income_pct_fpl) / 200 * 40  # up to 40 pts
            if dti is not None and dti > 0.36:
                hardship += min((dti - 0.36) / 0.64 * 30, 30)  # up to 30 pts
            if total_assets is not None and total_assets < 1000:
                hardship += 20  # 20 pts for near-zero assets
            if bankruptcy:
                hardship += 10
            hardship = _clamp(round(hardship, 1), 0.0, 100.0)

        return {
            "annual_income": annual_income,
            "monthly_income": monthly_income,
            "income_as_pct_fpl": income_pct_fpl,
            "income_volatility_score": income_vol,
            "income_trend": income_trend,
            "employment_status": emp_status,
            "employment_duration_months": emp_duration,
            "occupation_category": occupation,
            "employer_benefits_flag": employer_benefits,
            "total_assets": total_assets,
            "total_debts": total_debts,
            "debt_to_income_ratio": dti,
            "net_worth": net_worth,
            "credit_score_band": credit_band,
            "bankruptcy_flag": bankruptcy,
            "public_benefits_income_monthly": benefits_monthly,
            "tax_liability_annual": tax_liability,
            "financial_hardship_index": hardship,
        }

    # ------------------------------------------------------------------ #
    #  Layer 5: Environmental
    # ------------------------------------------------------------------ #

    def _extract_environmental(
        self,
        person: dict[str, Any],
        raw: dict[str, Any],
    ) -> dict[str, Any]:
        """Extract environmental indicators from census, EPA, and HUD data.

        Metrics:
            adi_national_rank, adi_state_decile, adi_risk_category,
            housing_quality_score, housing_quality_category,
            lead_exposure_risk, lead_risk_category,
            air_quality_index, air_quality_category,
            water_quality_risk, food_desert_flag,
            walkability_score, public_transit_access_score,
            green_space_pct, noise_pollution_level,
            superfund_proximity_flag, census_tract_poverty_rate,
            neighborhood_crime_rate, internet_access_flag
        """
        env = raw.get("environmental", {}) or {}
        housing = person.get("dynamic_state", {}).get("housing_state", {}) or {}

        adi_national = _safe_float(env.get("adi_national_rank"))
        adi_state = _safe_int(env.get("adi_state_decile"))
        adi_cat = "unknown"
        if adi_national is not None:
            if adi_national >= 80:
                adi_cat = "high_disadvantage"
            elif adi_national >= 50:
                adi_cat = "moderate_disadvantage"
            else:
                adi_cat = "low_disadvantage"

        hq_score = _safe_float(
            housing.get("housing_quality_score") or env.get("housing_quality_score")
        )
        hq_cat = "unknown"
        if hq_score is not None:
            if hq_score >= 80:
                hq_cat = "good"
            elif hq_score >= 50:
                hq_cat = "fair"
            elif hq_score >= 25:
                hq_cat = "poor"
            else:
                hq_cat = "very_poor"

        lead_risk = _safe_float(env.get("lead_exposure_risk"))
        lead_cat = "unknown"
        if lead_risk is not None:
            if lead_risk >= 0.7:
                lead_cat = "high"
            elif lead_risk >= 0.3:
                lead_cat = "moderate"
            else:
                lead_cat = "low"

        aqi = _safe_float(env.get("air_quality_index"))
        aqi_cat = "unknown"
        if aqi is not None:
            if aqi <= 50:
                aqi_cat = "good"
            elif aqi <= 100:
                aqi_cat = "moderate"
            elif aqi <= 150:
                aqi_cat = "unhealthy_sensitive"
            elif aqi <= 200:
                aqi_cat = "unhealthy"
            elif aqi <= 300:
                aqi_cat = "very_unhealthy"
            else:
                aqi_cat = "hazardous"

        water_risk = _safe_float(env.get("water_quality_risk"))
        food_desert = _safe_bool(env.get("food_desert_flag"))
        walkability = _safe_float(env.get("walkability_score"))
        transit = _safe_float(env.get("public_transit_access_score"))
        green_space = _safe_float(env.get("green_space_pct"))
        noise = _safe_float(env.get("noise_pollution_level"))
        superfund = _safe_bool(env.get("superfund_proximity_flag"))
        poverty_rate = _safe_float(env.get("census_tract_poverty_rate"))
        crime_rate = _safe_float(env.get("neighborhood_crime_rate"))
        internet = _safe_bool(env.get("internet_access_flag"))

        return {
            "adi_national_rank": adi_national,
            "adi_state_decile": adi_state,
            "adi_risk_category": adi_cat,
            "housing_quality_score": hq_score,
            "housing_quality_category": hq_cat,
            "lead_exposure_risk": lead_risk,
            "lead_risk_category": lead_cat,
            "air_quality_index": aqi,
            "air_quality_category": aqi_cat,
            "water_quality_risk": water_risk,
            "food_desert_flag": food_desert,
            "walkability_score": walkability,
            "public_transit_access_score": transit,
            "green_space_pct": green_space,
            "noise_pollution_level": noise,
            "superfund_proximity_flag": superfund,
            "census_tract_poverty_rate": poverty_rate,
            "neighborhood_crime_rate": crime_rate,
            "internet_access_flag": internet,
        }

    # ------------------------------------------------------------------ #
    #  Layer 6: Social
    # ------------------------------------------------------------------ #

    def _extract_social(
        self,
        person: dict[str, Any],
        raw: dict[str, Any],
    ) -> dict[str, Any]:
        """Extract social determinant metrics from HMIS and case-management data.

        Metrics:
            household_size, dependents_count, dependents_ages,
            marital_status, social_network_size, social_network_category,
            social_isolation_score, social_isolation_category,
            caregiving_burden_score, caregiving_category,
            community_engagement_score, religious_participation_flag,
            language_barrier_flag, primary_language,
            immigration_status, domestic_violence_flag,
            social_support_score, loneliness_score
        """
        social = raw.get("social", {}) or {}
        family = person.get("dynamic_state", {}).get("family_state", {}) or {}

        hh_size = _safe_int(family.get("household_size") or social.get("household_size"), 1)
        dep_ages = family.get("dependents_ages", []) or social.get("dependents_ages", []) or []
        dep_count = len(dep_ages)
        marital = social.get("marital_status")

        network_size = _safe_int(
            family.get("social_network_size") or social.get("social_network_size")
        )
        net_cat = "unknown"
        if network_size is not None:
            if network_size == 0:
                net_cat = "none"
            elif network_size <= 2:
                net_cat = "very_small"
            elif network_size <= 5:
                net_cat = "small"
            elif network_size <= 10:
                net_cat = "moderate"
            else:
                net_cat = "large"

        isolation = _safe_float(
            family.get("social_isolation_score") or social.get("social_isolation_score")
        )
        iso_cat = "unknown"
        if isolation is not None:
            if isolation >= 0.8:
                iso_cat = "severe"
            elif isolation >= 0.5:
                iso_cat = "moderate"
            elif isolation >= 0.2:
                iso_cat = "mild"
            else:
                iso_cat = "none"

        caregiver_burden = _safe_float(
            family.get("caregiving_burden_score") or social.get("caregiving_burden_score")
        )
        care_cat = "unknown"
        if caregiver_burden is not None:
            if caregiver_burden >= 70:
                care_cat = "high"
            elif caregiver_burden >= 40:
                care_cat = "moderate"
            else:
                care_cat = "low"

        community = _safe_float(social.get("community_engagement_score"))
        religious = _safe_bool(social.get("religious_participation_flag"))
        lang_barrier = _safe_bool(social.get("language_barrier_flag"))
        primary_lang = social.get("primary_language", "english")
        immigration = social.get("immigration_status")
        dv_flag = _safe_bool(social.get("domestic_violence_flag"))
        support = _safe_float(social.get("social_support_score"))
        loneliness = _safe_float(social.get("loneliness_score"))

        return {
            "household_size": hh_size,
            "dependents_count": dep_count,
            "dependents_ages": dep_ages,
            "marital_status": marital,
            "social_network_size": network_size,
            "social_network_category": net_cat,
            "social_isolation_score": isolation,
            "social_isolation_category": iso_cat,
            "caregiving_burden_score": caregiver_burden,
            "caregiving_category": care_cat,
            "community_engagement_score": community,
            "religious_participation_flag": religious,
            "language_barrier_flag": lang_barrier,
            "primary_language": primary_lang,
            "immigration_status": immigration,
            "domestic_violence_flag": dv_flag,
            "social_support_score": support,
            "loneliness_score": loneliness,
        }

    # ------------------------------------------------------------------ #
    #  Layer 7: Institutional
    # ------------------------------------------------------------------ #

    def _extract_institutional(
        self,
        person: dict[str, Any],
        raw: dict[str, Any],
    ) -> dict[str, Any]:
        """Extract institutional-interaction metrics from enrollment databases.

        Metrics:
            program_enrollment_count, active_programs, pending_applications,
            benefit_gap_programs, system_touchpoints_12m,
            case_manager_assigned_flag, case_manager_contacts_12m,
            eligibility_redetermination_due_flag,
            days_since_last_system_contact, cross_system_coordination_score,
            referral_count_12m, referral_completion_rate,
            administrative_burden_score, program_churn_count_12m,
            total_annual_benefits_value, benefits_utilization_rate
        """
        inst = raw.get("institutional", {}) or {}
        prog = person.get("dynamic_state", {}).get("program_state", {}) or {}
        enrollment = prog.get("enrollment_snapshot", {}) or {}
        eligibility = prog.get("eligibility_snapshot", {}) or {}

        # Count active enrollments
        active_programs: list[str] = []
        for prog_name, enrolled in enrollment.items():
            if _safe_bool(enrolled):
                active_programs.append(prog_name)
        # Add any from institutional data
        extra_active = inst.get("active_programs", [])
        if isinstance(extra_active, list):
            for p in extra_active:
                if p not in active_programs:
                    active_programs.append(p)
        enrollment_count = len(active_programs)

        # Pending applications
        pending = inst.get("pending_applications", []) or []
        if isinstance(pending, str):
            pending = [pending]

        # Benefit gaps: eligible but not enrolled
        gap_programs: list[str] = []
        for prog_name in eligibility:
            if _safe_bool(eligibility.get(prog_name)) and not _safe_bool(enrollment.get(prog_name)):
                gap_programs.append(prog_name)

        touchpoints = _safe_int(inst.get("system_touchpoints_12m"), 0)
        case_manager = _safe_bool(inst.get("case_manager_assigned_flag"))
        cm_contacts = _safe_int(inst.get("case_manager_contacts_12m"), 0)
        redetermination_due = _safe_bool(inst.get("eligibility_redetermination_due_flag"))
        days_since_contact = _safe_int(inst.get("days_since_last_system_contact"))

        # Cross-system coordination: fraction of active programs with shared data
        coord_score = _safe_float(inst.get("cross_system_coordination_score"))

        referrals = _safe_int(inst.get("referral_count_12m"), 0)
        referral_completed = _safe_int(inst.get("referrals_completed_12m"), 0)
        referral_rate = None
        if referrals > 0:
            referral_rate = round(referral_completed / referrals, 4)

        # Administrative burden: estimate from number of programs and pending apps
        admin_burden = _safe_float(inst.get("administrative_burden_score"))
        if admin_burden is None:
            admin_burden = min(100.0, enrollment_count * 8 + len(pending) * 12 + len(gap_programs) * 5)

        churn = _safe_int(inst.get("program_churn_count_12m"), 0)
        total_benefits = _safe_float(inst.get("total_annual_benefits_value"))
        utilization_rate = _safe_float(inst.get("benefits_utilization_rate"))

        return {
            "program_enrollment_count": enrollment_count,
            "active_programs": active_programs,
            "pending_applications": pending,
            "benefit_gap_programs": gap_programs,
            "system_touchpoints_12m": touchpoints,
            "case_manager_assigned_flag": case_manager,
            "case_manager_contacts_12m": cm_contacts,
            "eligibility_redetermination_due_flag": redetermination_due,
            "days_since_last_system_contact": days_since_contact,
            "cross_system_coordination_score": coord_score,
            "referral_count_12m": referrals,
            "referral_completion_rate": referral_rate,
            "administrative_burden_score": admin_burden,
            "program_churn_count_12m": churn,
            "total_annual_benefits_value": total_benefits,
            "benefits_utilization_rate": utilization_rate,
        }

    # ------------------------------------------------------------------ #
    #  Layer 8: Legal
    # ------------------------------------------------------------------ #

    def _extract_legal(
        self,
        person: dict[str, Any],
        raw: dict[str, Any],
    ) -> dict[str, Any]:
        """Extract legal/justice indicators from court and DOC data.

        Metrics:
            justice_involvement_flag, lifetime_arrests,
            past_12m_arrests, past_12m_jail_days, past_12m_prison_days,
            past_12m_police_contacts, current_incarceration_flag,
            current_supervision_status, supervision_compliance_score,
            active_court_cases, pending_charges_count,
            felony_conviction_flag, misdemeanor_conviction_count,
            sex_offender_registry_flag, protective_order_flag,
            legal_aid_active_flag, reentry_program_flag,
            time_since_last_justice_contact_days
        """
        legal = raw.get("legal", {}) or {}
        justice = person.get("dynamic_state", {}).get("justice_state", {}) or {}

        involvement = _safe_bool(
            justice.get("justice_involvement_flag") or legal.get("justice_involvement_flag")
        )
        lifetime_arrests = _safe_int(legal.get("lifetime_arrests"))
        arrests_12m = _safe_int(legal.get("past_12m_arrests"), 0)
        jail_days = _safe_int(justice.get("past_12m_jail_days") or legal.get("past_12m_jail_days"), 0)
        prison_days = _safe_int(
            justice.get("past_12m_prison_days") or legal.get("past_12m_prison_days"), 0
        )
        police_contacts = _safe_int(
            justice.get("past_12m_police_contacts") or legal.get("past_12m_police_contacts"), 0
        )

        current_incarcerated = jail_days > 300 or prison_days > 300 or _safe_bool(
            legal.get("current_incarceration_flag")
        )

        supervision = (
            justice.get("current_supervision_status")
            or legal.get("current_supervision_status")
        )
        compliance = _safe_float(legal.get("supervision_compliance_score"))

        court_cases = legal.get("active_court_cases", []) or []
        if isinstance(court_cases, int):
            active_cases = court_cases
            court_cases_list: list[Any] = []
        elif isinstance(court_cases, list):
            active_cases = len(court_cases)
            court_cases_list = court_cases
        else:
            active_cases = 0
            court_cases_list = []

        pending = _safe_int(legal.get("pending_charges_count"), 0)
        felony = _safe_bool(legal.get("felony_conviction_flag"))
        misdemeanor = _safe_int(legal.get("misdemeanor_conviction_count"), 0)
        sex_offender = _safe_bool(legal.get("sex_offender_registry_flag"))
        protective_order = _safe_bool(legal.get("protective_order_flag"))
        legal_aid = _safe_bool(legal.get("legal_aid_active_flag"))
        reentry = _safe_bool(legal.get("reentry_program_flag"))
        days_since = _safe_int(legal.get("time_since_last_justice_contact_days"))

        # Auto-set involvement if any indicators present
        if not involvement and (
            arrests_12m > 0 or jail_days > 0 or prison_days > 0
            or police_contacts > 0 or active_cases > 0
            or supervision is not None
        ):
            involvement = True

        return {
            "justice_involvement_flag": involvement,
            "lifetime_arrests": lifetime_arrests,
            "past_12m_arrests": arrests_12m,
            "past_12m_jail_days": jail_days,
            "past_12m_prison_days": prison_days,
            "past_12m_police_contacts": police_contacts,
            "current_incarceration_flag": current_incarcerated,
            "current_supervision_status": supervision,
            "supervision_compliance_score": compliance,
            "active_court_cases": active_cases,
            "court_case_details": court_cases_list,
            "pending_charges_count": pending,
            "felony_conviction_flag": felony,
            "misdemeanor_conviction_count": misdemeanor,
            "sex_offender_registry_flag": sex_offender,
            "protective_order_flag": protective_order,
            "legal_aid_active_flag": legal_aid,
            "reentry_program_flag": reentry,
            "time_since_last_justice_contact_days": days_since,
        }

    # ------------------------------------------------------------------ #
    #  Layer 9: Subjective Wellbeing
    # ------------------------------------------------------------------ #

    def _extract_subjective(
        self,
        person: dict[str, Any],
        raw: dict[str, Any],
    ) -> dict[str, Any]:
        """Extract subjective wellbeing metrics from self-report surveys.

        Metrics:
            self_rated_health, self_rated_health_numeric,
            life_satisfaction, life_satisfaction_category,
            sense_of_purpose_score, autonomy_score,
            hopefulness_score, perceived_stress_score,
            perceived_stress_category, financial_worry_score,
            housing_satisfaction, safety_perception,
            belonging_score, trust_in_institutions_score,
            quality_of_life_composite, happiness_score,
            meaning_in_life_score, future_outlook_score
        """
        subjective = raw.get("subjective", {}) or {}

        # Self-rated health
        srh = subjective.get("self_rated_health")
        srh_numeric = None
        if srh is not None:
            srh_map = {
                "excellent": 5, "very_good": 4, "good": 3, "fair": 2, "poor": 1,
            }
            if isinstance(srh, str):
                srh_numeric = srh_map.get(srh.lower())
            elif isinstance(srh, (int, float)):
                srh_numeric = _clamp(float(srh), 1.0, 5.0)

        # Life satisfaction (Cantril ladder 0-10)
        life_sat = _safe_float(subjective.get("life_satisfaction"))
        if life_sat is not None:
            life_sat = _clamp(life_sat, 0.0, 10.0)
        life_sat_cat = "unknown"
        if life_sat is not None:
            if life_sat >= 7:
                life_sat_cat = "thriving"
            elif life_sat >= 4:
                life_sat_cat = "struggling"
            else:
                life_sat_cat = "suffering"

        purpose = _safe_float(subjective.get("sense_of_purpose_score"))
        if purpose is not None:
            purpose = _clamp(purpose, 0.0, 10.0)

        autonomy = _safe_float(subjective.get("autonomy_score"))
        if autonomy is not None:
            autonomy = _clamp(autonomy, 0.0, 10.0)

        hopefulness = _safe_float(subjective.get("hopefulness_score"))
        if hopefulness is not None:
            hopefulness = _clamp(hopefulness, 0.0, 10.0)

        # Perceived stress (PSS-10: 0-40)
        pss = _safe_float(subjective.get("perceived_stress_score"))
        if pss is not None:
            pss = _clamp(pss, 0.0, 40.0)
        pss_cat = "unknown"
        if pss is not None:
            if pss <= 13:
                pss_cat = "low"
            elif pss <= 26:
                pss_cat = "moderate"
            else:
                pss_cat = "high"

        fin_worry = _safe_float(subjective.get("financial_worry_score"))
        if fin_worry is not None:
            fin_worry = _clamp(fin_worry, 0.0, 10.0)

        housing_sat = _safe_float(subjective.get("housing_satisfaction"))
        if housing_sat is not None:
            housing_sat = _clamp(housing_sat, 0.0, 10.0)

        safety = _safe_float(subjective.get("safety_perception"))
        if safety is not None:
            safety = _clamp(safety, 0.0, 10.0)

        belonging = _safe_float(subjective.get("belonging_score"))
        if belonging is not None:
            belonging = _clamp(belonging, 0.0, 10.0)

        trust_inst = _safe_float(subjective.get("trust_in_institutions_score"))
        if trust_inst is not None:
            trust_inst = _clamp(trust_inst, 0.0, 10.0)

        happiness = _safe_float(subjective.get("happiness_score"))
        if happiness is not None:
            happiness = _clamp(happiness, 0.0, 10.0)

        meaning = _safe_float(subjective.get("meaning_in_life_score"))
        if meaning is not None:
            meaning = _clamp(meaning, 0.0, 10.0)

        future_outlook = _safe_float(subjective.get("future_outlook_score"))
        if future_outlook is not None:
            future_outlook = _clamp(future_outlook, 0.0, 10.0)

        # Quality of life composite: average of available subscales
        qol_components = [
            v for v in [life_sat, purpose, autonomy, hopefulness, happiness, meaning]
            if v is not None
        ]
        qol_composite = None
        if qol_components:
            qol_composite = round(sum(qol_components) / len(qol_components), 2)

        return {
            "self_rated_health": srh,
            "self_rated_health_numeric": srh_numeric,
            "life_satisfaction": life_sat,
            "life_satisfaction_category": life_sat_cat,
            "sense_of_purpose_score": purpose,
            "autonomy_score": autonomy,
            "hopefulness_score": hopefulness,
            "perceived_stress_score": pss,
            "perceived_stress_category": pss_cat,
            "financial_worry_score": fin_worry,
            "housing_satisfaction": housing_sat,
            "safety_perception": safety,
            "belonging_score": belonging,
            "trust_in_institutions_score": trust_inst,
            "quality_of_life_composite": qol_composite,
            "happiness_score": happiness,
            "meaning_in_life_score": meaning,
            "future_outlook_score": future_outlook,
        }
