"""Bias and surveillance audit for DOME predictions.

Implements six concrete bias checks designed for human-services spend
prediction, with special attention to Medicaid / justice-system contexts:

1. **Prediction error by race** — MAE should not vary > 20 % across groups.
2. **Prediction error by income quintile** — MAE should not vary > 25 %.
3. **Prediction error by geography** — MAE (urban vs rural) should not vary > 15 %.
4. **Hypervisibility bias** — correlation between number of system touchpoints
   and predicted risk score should be < 0.3 (more data should not
   mechanically inflate risk).
5. **Surveillance bias** — justice-involved individuals should not have
   systematically higher predicted costs after controlling for actual health
   status.  Evaluated via residual analysis.
6. **Data density bias** — prediction accuracy should not degrade for people
   with sparse records (few data fields populated).

Each check produces a structured ``BiasCheck`` with a pass/fail verdict, a
numeric score, and a plain-language explanation.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Pydantic report models
# ---------------------------------------------------------------------------

class BiasCheck(BaseModel):
    """Result of a single bias audit check."""

    check_name: str = Field(..., description="Human-readable name of the check.")
    passed: bool = Field(..., description="True if the check met its acceptance criterion.")
    score: float = Field(
        ...,
        description="Numeric score specific to each check (e.g. disparity ratio, correlation).",
    )
    details: str = Field(..., description="Plain-language explanation of the result.")


class BiasReport(BaseModel):
    """Aggregate bias-audit report across all checks.

    ``overall_assessment`` is one of:

    * **pass** — all checks passed.
    * **concern** — one or two checks failed with moderate scores.
    * **fail** — three or more checks failed, or any single check failed
      with a severe score.
    """

    overall_assessment: str = Field(
        ..., description="Overall verdict: 'pass', 'concern', or 'fail'."
    )
    checks: list[BiasCheck] = Field(..., description="Individual check results.")
    recommendations: list[str] = Field(
        default_factory=list,
        description="Actionable recommendations based on failed checks.",
    )


# ---------------------------------------------------------------------------
# Core auditor
# ---------------------------------------------------------------------------

class BiasAuditor:
    """Run a structured bias audit on DOME spend predictions.

    Parameters
    ----------
    predicted_field : str
        Key in each prediction dict for the predicted 12-month spend.
    actual_field : str
        Key in each prediction dict (or metadata) for the actual spend.
    risk_score_field : str
        Key in each prediction dict for the predicted risk score (0-1 scale
        or similar continuous score).  Used by the hypervisibility check.
    race_field : str
        Key in metadata for the individual's race/ethnicity.
    income_quintile_field : str
        Key in metadata for income quintile (1-5).
    geography_field : str
        Key in metadata for geography type ('urban' or 'rural').
    n_data_points_field : str
        Key in metadata for the count of system touchpoints / data records.
    justice_involved_field : str
        Key in metadata for justice-involvement flag (bool or 0/1).
    health_status_field : str
        Key in metadata for an independent health-status index (e.g. CRG
        weight, HCC risk score) used to control for morbidity in the
        surveillance-bias check.
    data_completeness_field : str
        Key in metadata for a 0-1 data-completeness fraction.
    """

    def __init__(
        self,
        predicted_field: str = "predicted_spend",
        actual_field: str = "actual_spend",
        risk_score_field: str = "risk_score",
        race_field: str = "race",
        income_quintile_field: str = "income_quintile",
        geography_field: str = "geography",
        n_data_points_field: str = "n_data_points",
        justice_involved_field: str = "justice_involved",
        health_status_field: str = "health_status_score",
        data_completeness_field: str = "data_completeness",
    ) -> None:
        self.predicted_field = predicted_field
        self.actual_field = actual_field
        self.risk_score_field = risk_score_field
        self.race_field = race_field
        self.income_quintile_field = income_quintile_field
        self.geography_field = geography_field
        self.n_data_points_field = n_data_points_field
        self.justice_involved_field = justice_involved_field
        self.health_status_field = health_status_field
        self.data_completeness_field = data_completeness_field

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def audit(
        self,
        predictions: list[dict[str, Any]],
        metadata: list[dict[str, Any]],
    ) -> BiasReport:
        """Execute all six bias checks and compile an aggregate report.

        Parameters
        ----------
        predictions : list[dict]
            Each dict contains at least ``predicted_field`` and ``actual_field``.
            May also contain ``risk_score_field``.
        metadata : list[dict]
            Parallel list with demographic and administrative fields
            needed by the individual checks.

        Returns
        -------
        BiasReport
            Structured report with individual check results and recommendations.

        Raises
        ------
        ValueError
            If inputs differ in length or are empty.
        """
        if len(predictions) != len(metadata):
            raise ValueError(
                f"predictions ({len(predictions)}) and metadata ({len(metadata)}) "
                "must have the same length."
            )
        if len(predictions) == 0:
            raise ValueError("Cannot audit an empty dataset.")

        # Pre-extract common arrays
        pred = np.array([p[self.predicted_field] for p in predictions], dtype=np.float64)
        actual = np.array([p[self.actual_field] for p in predictions], dtype=np.float64)
        errors = np.abs(pred - actual)

        checks: list[BiasCheck] = []
        recommendations: list[str] = []

        # 1) Race
        check = self._check_error_by_group(
            errors=errors,
            metadata=metadata,
            group_field=self.race_field,
            check_name="Prediction error by race",
            max_variation=0.20,
        )
        checks.append(check)
        if not check.passed:
            recommendations.append(
                f"MAE varies by {check.score:.1%} across racial groups (threshold 20 %).  "
                "Investigate whether training data under-represents high-cost conditions "
                "in the disadvantaged group, or whether proxy variables encode racial bias."
            )

        # 2) Income quintile
        check = self._check_error_by_group(
            errors=errors,
            metadata=metadata,
            group_field=self.income_quintile_field,
            check_name="Prediction error by income quintile",
            max_variation=0.25,
        )
        checks.append(check)
        if not check.passed:
            recommendations.append(
                f"MAE varies by {check.score:.1%} across income quintiles (threshold 25 %).  "
                "Low-income individuals may have sparser or more fragmented data.  "
                "Consider imputation strategies or income-stratified model training."
            )

        # 3) Geography
        check = self._check_error_by_group(
            errors=errors,
            metadata=metadata,
            group_field=self.geography_field,
            check_name="Prediction error by geography (urban/rural)",
            max_variation=0.15,
        )
        checks.append(check)
        if not check.passed:
            recommendations.append(
                f"MAE varies by {check.score:.1%} between urban and rural populations "
                "(threshold 15 %).  Rural residents may have different utilisation "
                "patterns and provider availability.  Consider geographic interaction terms."
            )

        # 4) Hypervisibility bias
        check = self._check_hypervisibility(predictions, metadata)
        checks.append(check)
        if not check.passed:
            recommendations.append(
                f"Correlation between system touchpoints and risk score is {check.score:.3f} "
                "(threshold 0.30).  The model may be conflating data volume with true risk.  "
                "Consider normalising features by data density or adding a data-volume control."
            )

        # 5) Surveillance bias
        check = self._check_surveillance_bias(pred, actual, metadata)
        checks.append(check)
        if not check.passed:
            recommendations.append(
                f"Justice-involved individuals show mean residual of ${check.score:,.0f} "
                "above non-justice-involved, after controlling for health status.  "
                "The model may be using justice-system contact as a proxy for cost, "
                "amplifying existing disparities.  Consider removing justice-related "
                "features or applying a fairness constraint."
            )

        # 6) Data density bias
        check = self._check_data_density_bias(errors, metadata)
        checks.append(check)
        if not check.passed:
            recommendations.append(
                f"Prediction accuracy degrades by {check.score:.1%} for individuals with "
                "sparse data (below-median completeness) vs dense data.  Sparse-data "
                "individuals may receive less accurate risk stratification.  Consider "
                "ensemble methods that handle missing data, or flagging low-confidence "
                "predictions for manual review."
            )

        # ---- overall assessment ----
        n_failed = sum(1 for c in checks if not c.passed)
        # Severe failure: any single check with extreme score
        severe = any(
            (not c.passed and c.score > 0.50 and c.check_name.startswith("Prediction error"))
            or (not c.passed and c.check_name == "Hypervisibility bias" and c.score > 0.5)
            for c in checks
        )

        if n_failed == 0:
            overall = "pass"
        elif n_failed <= 2 and not severe:
            overall = "concern"
        else:
            overall = "fail"

        return BiasReport(
            overall_assessment=overall,
            checks=checks,
            recommendations=recommendations,
        )

    # ------------------------------------------------------------------
    # Synthetic data generator
    # ------------------------------------------------------------------

    @staticmethod
    def generate_synthetic_audit_data(
        n: int = 500,
        seed: int = 42,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Generate synthetic prediction + metadata for bias-audit testing.

        Injects *known* biases so that audit checks can be validated:

        * **Race bias**: predictions for ``"Black"`` group are systematically
          5 % higher than actuals (over-prediction).
        * **Hypervisibility**: risk_score is positively correlated with
          n_data_points (r ~ 0.35).
        * **Surveillance bias**: justice-involved individuals get an extra
          $2 000 added to their predicted spend, unrelated to health status.
        * **Data density bias**: individuals with low data_completeness get
          30 % more noise in predictions.

        Parameters
        ----------
        n : int
            Number of synthetic records.
        seed : int
            Random seed.

        Returns
        -------
        tuple[list[dict], list[dict]]
            (predictions, metadata) — parallel lists.
        """
        rng = np.random.default_rng(seed)

        # --- Demographics ---
        races = rng.choice(
            ["White", "Black", "Hispanic", "Asian", "Other"],
            size=n,
            p=[0.40, 0.25, 0.20, 0.10, 0.05],
        )
        income_quintiles = rng.choice([1, 2, 3, 4, 5], size=n, p=[0.30, 0.25, 0.20, 0.15, 0.10])
        geographies = rng.choice(["urban", "rural"], size=n, p=[0.65, 0.35])
        justice_involved = rng.choice([False, True], size=n, p=[0.85, 0.15])

        # Health status score: independent of justice involvement (by design)
        health_status = rng.beta(a=2, b=5, size=n)  # skewed low, range [0, 1]

        # Data completeness: correlated with income
        base_completeness = 0.3 + 0.12 * income_quintiles + rng.normal(0, 0.1, size=n)
        data_completeness = np.clip(base_completeness, 0.1, 1.0)

        # System touchpoints: correlated with justice involvement and health status
        n_data_points = (
            rng.poisson(lam=8, size=n)
            + (justice_involved.astype(int) * rng.poisson(lam=5, size=n))
            + (health_status * 10).astype(int)
        )
        n_data_points = np.maximum(n_data_points, 1)

        # --- Actual spend (driven by health status + noise) ---
        log_spend = 7.5 + 3.0 * health_status + rng.normal(0, 0.8, size=n)
        actual_spend = np.exp(log_spend)

        # --- Predicted spend (with injected biases) ---
        # Base prediction: actual + noise scaled by data completeness
        noise_scale = np.where(data_completeness < 0.5, 0.25, 0.12)  # data density bias
        pred_noise = rng.normal(0, 1, size=n) * noise_scale * actual_spend
        predicted_spend = actual_spend + pred_noise

        # Inject race bias: over-predict for Black individuals
        race_mask_black = races == "Black"
        predicted_spend[race_mask_black] *= 1.05

        # Inject surveillance bias: justice-involved get $2000 added
        predicted_spend[justice_involved] += 2000.0

        predicted_spend = np.maximum(predicted_spend, 0.0)

        # --- Risk score: correlated with health status AND n_data_points (hypervisibility) ---
        risk_score = (
            0.5 * health_status
            + 0.02 * n_data_points / np.max(n_data_points)
            + rng.normal(0, 0.08, size=n)
        )
        risk_score = np.clip(risk_score, 0.0, 1.0)

        # --- Assemble output ---
        predictions: list[dict[str, Any]] = []
        metadata_list: list[dict[str, Any]] = []

        for i in range(n):
            predictions.append({
                "person_id": f"AUDIT-{i:05d}",
                "predicted_spend": float(predicted_spend[i]),
                "actual_spend": float(actual_spend[i]),
                "risk_score": float(risk_score[i]),
            })
            metadata_list.append({
                "person_id": f"AUDIT-{i:05d}",
                "race": str(races[i]),
                "income_quintile": int(income_quintiles[i]),
                "geography": str(geographies[i]),
                "n_data_points": int(n_data_points[i]),
                "justice_involved": bool(justice_involved[i]),
                "health_status_score": float(health_status[i]),
                "data_completeness": float(data_completeness[i]),
            })

        return predictions, metadata_list

    # ------------------------------------------------------------------
    # Individual bias checks
    # ------------------------------------------------------------------

    def _check_error_by_group(
        self,
        errors: np.ndarray,
        metadata: list[dict[str, Any]],
        group_field: str,
        check_name: str,
        max_variation: float,
    ) -> BiasCheck:
        """Check whether MAE varies beyond a threshold across groups.

        Parameters
        ----------
        errors : np.ndarray
            Absolute prediction errors for every individual.
        metadata : list[dict]
            Each dict must contain ``group_field``.
        group_field : str
            The metadata key to group by.
        check_name : str
            Human-readable name for the check.
        max_variation : float
            Maximum allowable relative variation (max_mae - min_mae) / min_mae.

        Returns
        -------
        BiasCheck
        """
        # Extract group labels
        labels = np.array([str(m.get(group_field, "unknown")) for m in metadata])
        unique_groups = np.unique(labels)

        if len(unique_groups) < 2:
            return BiasCheck(
                check_name=check_name,
                passed=True,
                score=0.0,
                details=f"Only one group found for '{group_field}' — no disparity possible.",
            )

        group_maes: dict[str, float] = {}
        group_counts: dict[str, int] = {}
        for g in unique_groups:
            mask = labels == g
            n_g = int(np.sum(mask))
            if n_g < 5:
                continue  # skip tiny groups
            group_maes[g] = float(np.mean(errors[mask]))
            group_counts[g] = n_g

        if len(group_maes) < 2:
            return BiasCheck(
                check_name=check_name,
                passed=True,
                score=0.0,
                details=f"Insufficient group sizes for '{group_field}' — cannot assess disparity.",
            )

        mae_values = list(group_maes.values())
        min_mae = min(mae_values)
        max_mae = max(mae_values)
        variation = (max_mae - min_mae) / min_mae if min_mae > 0 else float("inf")

        worst_group = max(group_maes, key=group_maes.get)  # type: ignore[arg-type]
        best_group = min(group_maes, key=group_maes.get)  # type: ignore[arg-type]

        passed = variation <= max_variation

        details = (
            f"MAE ranges from ${min_mae:,.0f} ({best_group}, n={group_counts[best_group]}) "
            f"to ${max_mae:,.0f} ({worst_group}, n={group_counts[worst_group]}). "
            f"Relative variation: {variation:.1%} (threshold: {max_variation:.0%}). "
            f"{'PASS' if passed else 'FAIL'}."
        )

        return BiasCheck(
            check_name=check_name,
            passed=passed,
            score=round(variation, 4),
            details=details,
        )

    def _check_hypervisibility(
        self,
        predictions: list[dict[str, Any]],
        metadata: list[dict[str, Any]],
    ) -> BiasCheck:
        """Check for hypervisibility bias: correlation(n_data_points, risk_score).

        A model exhibiting hypervisibility bias will assign higher risk scores
        to individuals simply because they have more system interactions
        (more jail bookings, more ER visits logged, etc.), regardless of
        underlying health need.

        Parameters
        ----------
        predictions : list[dict]
            Must contain ``risk_score_field``.
        metadata : list[dict]
            Must contain ``n_data_points_field``.

        Returns
        -------
        BiasCheck
        """
        risk_scores = np.array(
            [p.get(self.risk_score_field, 0.0) for p in predictions], dtype=np.float64
        )
        n_data_pts = np.array(
            [m.get(self.n_data_points_field, 0) for m in metadata], dtype=np.float64
        )

        correlation = self._pearson_r(n_data_pts, risk_scores)
        passed = abs(correlation) < 0.30

        details = (
            f"Pearson correlation between system touchpoints and risk score: "
            f"r = {correlation:.4f} (threshold: |r| < 0.30). "
            f"{'PASS — risk scoring is not unduly driven by data volume.' if passed else 'FAIL — risk scores may reflect surveillance intensity, not genuine need.'}"
        )

        return BiasCheck(
            check_name="Hypervisibility bias",
            passed=passed,
            score=round(abs(correlation), 4),
            details=details,
        )

    def _check_surveillance_bias(
        self,
        pred: np.ndarray,
        actual: np.ndarray,
        metadata: list[dict[str, Any]],
    ) -> BiasCheck:
        """Check for surveillance bias against justice-involved individuals.

        Method: Compute the residual (predicted - actual) for each person.
        Regress residuals on health_status_score to control for morbidity.
        Then compare mean *adjusted* residuals for justice-involved vs not.
        If justice-involved individuals have significantly higher adjusted
        residuals, the model is over-predicting their costs beyond what
        health status explains.

        Parameters
        ----------
        pred, actual : np.ndarray
            Predicted and actual spend arrays.
        metadata : list[dict]
            Must contain ``justice_involved_field`` and ``health_status_field``.

        Returns
        -------
        BiasCheck
        """
        residuals = pred - actual

        justice = np.array(
            [bool(m.get(self.justice_involved_field, False)) for m in metadata]
        )
        health = np.array(
            [m.get(self.health_status_field, 0.0) for m in metadata], dtype=np.float64
        )

        n_justice = int(np.sum(justice))
        n_non_justice = int(np.sum(~justice))

        if n_justice < 5 or n_non_justice < 5:
            return BiasCheck(
                check_name="Surveillance bias (justice involvement)",
                passed=True,
                score=0.0,
                details="Insufficient justice-involved or non-involved individuals to assess.",
            )

        # Simple linear regression: residual ~ beta_0 + beta_1 * health_status
        # Then compare residuals of justice vs non-justice after removing
        # the health-status effect.
        adjusted_residuals = self._adjust_for_covariate(residuals, health)

        mean_resid_justice = float(np.mean(adjusted_residuals[justice]))
        mean_resid_non = float(np.mean(adjusted_residuals[~justice]))
        diff = mean_resid_justice - mean_resid_non

        # Threshold: adjusted residual difference should be < $1000
        # (i.e., the model does not systematically over-predict by more
        # than $1000 for justice-involved after controlling for health)
        threshold = 1000.0
        passed = abs(diff) < threshold

        details = (
            f"Mean adjusted residual (predicted - actual, controlling for health status): "
            f"justice-involved = ${mean_resid_justice:,.0f} (n={n_justice}), "
            f"non-justice = ${mean_resid_non:,.0f} (n={n_non_justice}). "
            f"Difference = ${diff:,.0f} (threshold: ${threshold:,.0f}). "
            f"{'PASS' if passed else 'FAIL — model may over-predict costs for justice-involved individuals beyond health-status differences.'}."
        )

        return BiasCheck(
            check_name="Surveillance bias (justice involvement)",
            passed=passed,
            score=round(abs(diff), 2),
            details=details,
        )

    def _check_data_density_bias(
        self,
        errors: np.ndarray,
        metadata: list[dict[str, Any]],
    ) -> BiasCheck:
        """Check whether prediction accuracy degrades for sparse-data individuals.

        Splits the population at the median data-completeness value and
        compares MAE between the sparse and dense halves.

        Parameters
        ----------
        errors : np.ndarray
            Absolute prediction errors.
        metadata : list[dict]
            Must contain ``data_completeness_field``.

        Returns
        -------
        BiasCheck
        """
        completeness = np.array(
            [m.get(self.data_completeness_field, 0.5) for m in metadata], dtype=np.float64
        )
        median_c = float(np.median(completeness))

        sparse_mask = completeness <= median_c
        dense_mask = completeness > median_c

        n_sparse = int(np.sum(sparse_mask))
        n_dense = int(np.sum(dense_mask))

        if n_sparse < 5 or n_dense < 5:
            return BiasCheck(
                check_name="Data density bias",
                passed=True,
                score=0.0,
                details="Insufficient split between sparse and dense data to assess.",
            )

        mae_sparse = float(np.mean(errors[sparse_mask]))
        mae_dense = float(np.mean(errors[dense_mask]))

        # Relative degradation: how much worse is MAE for sparse vs dense
        degradation = (mae_sparse - mae_dense) / mae_dense if mae_dense > 0 else float("inf")

        # Threshold: sparse-data MAE should not exceed dense-data MAE by > 30 %
        threshold = 0.30
        passed = degradation <= threshold

        details = (
            f"MAE for sparse-data individuals (completeness <= {median_c:.2f}): "
            f"${mae_sparse:,.0f} (n={n_sparse}). "
            f"MAE for dense-data individuals (completeness > {median_c:.2f}): "
            f"${mae_dense:,.0f} (n={n_dense}). "
            f"Relative degradation: {degradation:.1%} (threshold: {threshold:.0%}). "
            f"{'PASS' if passed else 'FAIL — predictions are significantly less accurate for data-sparse individuals.'}."
        )

        return BiasCheck(
            check_name="Data density bias",
            passed=passed,
            score=round(degradation, 4),
            details=details,
        )

    # ------------------------------------------------------------------
    # Statistical helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _pearson_r(x: np.ndarray, y: np.ndarray) -> float:
        """Compute the Pearson correlation coefficient between two arrays.

        Parameters
        ----------
        x, y : np.ndarray
            1-D arrays of equal length.

        Returns
        -------
        float
            Correlation coefficient in [-1, 1].  Returns 0.0 if either
            array has zero variance.
        """
        if len(x) < 2:
            return 0.0

        x_mean = np.mean(x)
        y_mean = np.mean(y)
        x_dev = x - x_mean
        y_dev = y - y_mean

        numerator = float(np.sum(x_dev * y_dev))
        denominator = math.sqrt(float(np.sum(x_dev ** 2)) * float(np.sum(y_dev ** 2)))

        if denominator == 0:
            return 0.0
        return numerator / denominator

    @staticmethod
    def _adjust_for_covariate(
        response: np.ndarray,
        covariate: np.ndarray,
    ) -> np.ndarray:
        """Remove the linear effect of a covariate from a response variable.

        Fits OLS: response = beta_0 + beta_1 * covariate, then returns
        the residuals.  This is the simplest approach to "controlling for"
        the covariate.

        Parameters
        ----------
        response : np.ndarray
            The variable to adjust (e.g. prediction residuals).
        covariate : np.ndarray
            The confound to partial out (e.g. health status).

        Returns
        -------
        np.ndarray
            Adjusted residuals (response minus the linear fit).
        """
        n = len(response)
        if n < 2:
            return response.copy()

        # Design matrix [1, covariate]
        X = np.column_stack([np.ones(n), covariate])

        # OLS: beta = (X'X)^{-1} X'y
        XtX = X.T @ X
        Xty = X.T @ response

        # Solve via numpy (handles near-singularity gracefully)
        try:
            beta = np.linalg.solve(XtX, Xty)
        except np.linalg.LinAlgError:
            # Singular matrix — covariate has no variance
            return response - np.mean(response)

        fitted = X @ beta
        return response - fitted
