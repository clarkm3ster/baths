"""Spend-distribution validation for DOME predictions.

Compares the full statistical distribution of predicted spend against actual
spend, going beyond point-estimate accuracy to verify that the *shape* of the
predicted distribution is realistic.  This matters because Medicaid spend is
extremely right-skewed: the top 5 % of enrollees typically account for ~54 %
of total expenditure.  A model that nails the mean but flattens this tail
would mis-allocate care-management resources.

All statistical computations are implemented with numpy only (no scipy
dependency) so the validation framework stays lightweight.
"""

from __future__ import annotations

import math

import numpy as np
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Pydantic report models
# ---------------------------------------------------------------------------

class DistributionReport(BaseModel):
    """Results of a distributional comparison between predicted and actual spend."""

    ks_statistic: float = Field(
        ...,
        description=(
            "Two-sample Kolmogorov-Smirnov test statistic.  Measures the maximum "
            "vertical distance between the two empirical CDFs.  Smaller is better."
        ),
    )
    ks_p_value: float = Field(
        ...,
        description=(
            "Approximate p-value for the KS test.  Values > 0.05 suggest the two "
            "distributions cannot be distinguished at the 5 % significance level."
        ),
    )
    distributions_match: bool = Field(
        ...,
        description="True when ks_p_value > 0.05 (fail to reject H0 that distributions are equal).",
    )
    predicted_percentiles: dict[str, float] = Field(
        ...,
        description="Key percentiles (p10 .. p99) of the predicted spend distribution.",
    )
    actual_percentiles: dict[str, float] = Field(
        ...,
        description="Key percentiles (p10 .. p99) of the actual spend distribution.",
    )
    percentile_errors: dict[str, float] = Field(
        ...,
        description=(
            "Absolute percentage error at each percentile: "
            "|predicted - actual| / actual * 100."
        ),
    )
    super_utilizer_predicted_share: float = Field(
        ...,
        description="Fraction of total predicted spend attributable to the top 5 % of spenders.",
    )
    super_utilizer_actual_share: float = Field(
        ...,
        description="Fraction of total actual spend attributable to the top 5 % of spenders.",
    )


# ---------------------------------------------------------------------------
# Core validator
# ---------------------------------------------------------------------------

class SpendDistributionValidator:
    """Compare predicted vs actual spend distributions.

    Parameters
    ----------
    significance_level : float
        P-value threshold for the KS test.  Default 0.05.
    super_utilizer_top_pct : float
        Percentile cutoff that defines super-utilisers.  Default 0.05
        (top 5 %).
    """

    PERCENTILE_KEYS: list[str] = ["p10", "p25", "p50", "p75", "p90", "p95", "p99"]
    PERCENTILE_VALUES: list[float] = [10, 25, 50, 75, 90, 95, 99]

    def __init__(
        self,
        significance_level: float = 0.05,
        super_utilizer_top_pct: float = 0.05,
    ) -> None:
        self.significance_level = significance_level
        self.super_utilizer_top_pct = super_utilizer_top_pct

    def validate(
        self,
        predicted_distribution: list[float],
        actual_distribution: list[float],
    ) -> DistributionReport:
        """Run a full distributional comparison.

        Parameters
        ----------
        predicted_distribution : list[float]
            Predicted spend values (one per person).
        actual_distribution : list[float]
            Actual spend values (one per person).  Does not need to be the
            same length as ``predicted_distribution`` — they are treated as
            independent samples from two distributions.

        Returns
        -------
        DistributionReport
            Structured comparison report.

        Raises
        ------
        ValueError
            If either input is empty.
        """
        if len(predicted_distribution) == 0 or len(actual_distribution) == 0:
            raise ValueError("Both predicted and actual distributions must be non-empty.")

        pred = np.asarray(predicted_distribution, dtype=np.float64)
        actual = np.asarray(actual_distribution, dtype=np.float64)

        # ---- KS test (pure numpy) ----
        ks_stat, ks_p = self._two_sample_ks(pred, actual)

        # ---- percentiles ----
        pred_pcts = self._compute_percentiles(pred)
        actual_pcts = self._compute_percentiles(actual)
        pct_errors = self._percentile_errors(pred_pcts, actual_pcts)

        # ---- super-utiliser concentration ----
        su_pred = self._super_utilizer_share(pred)
        su_actual = self._super_utilizer_share(actual)

        return DistributionReport(
            ks_statistic=round(ks_stat, 6),
            ks_p_value=round(ks_p, 6),
            distributions_match=ks_p > self.significance_level,
            predicted_percentiles=pred_pcts,
            actual_percentiles=actual_pcts,
            percentile_errors=pct_errors,
            super_utilizer_predicted_share=round(su_pred, 4),
            super_utilizer_actual_share=round(su_actual, 4),
        )

    # ------------------------------------------------------------------
    # Internal: two-sample Kolmogorov-Smirnov test
    # ------------------------------------------------------------------

    @staticmethod
    def _two_sample_ks(
        sample_a: np.ndarray,
        sample_b: np.ndarray,
    ) -> tuple[float, float]:
        """Two-sample KS test implemented from first principles with numpy.

        Computes the KS statistic D_n,m as the supremum of the absolute
        difference between the two empirical CDFs, then approximates the
        p-value using the Kolmogorov-Smirnov asymptotic distribution.

        Parameters
        ----------
        sample_a, sample_b : np.ndarray
            Two 1-D arrays of observed values.

        Returns
        -------
        tuple[float, float]
            (ks_statistic, approximate_p_value)
        """
        n_a = len(sample_a)
        n_b = len(sample_b)

        # Combine and sort all unique values
        combined = np.sort(np.concatenate([sample_a, sample_b]))

        # Empirical CDFs at each point
        cdf_a = np.searchsorted(np.sort(sample_a), combined, side="right") / n_a
        cdf_b = np.searchsorted(np.sort(sample_b), combined, side="right") / n_b

        d_stat = float(np.max(np.abs(cdf_a - cdf_b)))

        # Effective sample size for asymptotic approximation
        n_eff = math.sqrt(n_a * n_b / (n_a + n_b))
        lam = (n_eff + 0.12 + 0.11 / n_eff) * d_stat

        # Asymptotic survival function (Kolmogorov distribution)
        # P(D > d) ~ 2 * sum_{k=1}^{inf} (-1)^{k-1} * exp(-2 k^2 lambda^2)
        p_value = SpendDistributionValidator._kolmogorov_survival(lam)

        return d_stat, max(0.0, min(1.0, p_value))

    @staticmethod
    def _kolmogorov_survival(lam: float) -> float:
        """Compute the Kolmogorov survival function Q(lambda).

        Uses the convergent series:
            Q(lam) = 2 * sum_{k=1}^{inf} (-1)^{k-1} exp(-2 k^2 lam^2)

        The series converges rapidly for lam > 0.  For very small lam,
        returns 1.0 (cannot reject).

        Parameters
        ----------
        lam : float
            The scaled KS statistic (d * sqrt(n_eff)).

        Returns
        -------
        float
            Approximate p-value in [0, 1].
        """
        if lam <= 0:
            return 1.0
        if lam > 4.0:
            # For very large lambda, p-value is essentially zero
            return 0.0

        total = 0.0
        for k in range(1, 201):
            term = (-1) ** (k - 1) * math.exp(-2.0 * k * k * lam * lam)
            total += term
            # Early termination when terms become negligible
            if abs(term) < 1e-15:
                break

        return max(0.0, min(1.0, 2.0 * total))

    # ------------------------------------------------------------------
    # Internal: percentiles
    # ------------------------------------------------------------------

    def _compute_percentiles(self, data: np.ndarray) -> dict[str, float]:
        """Compute standard percentiles for a distribution.

        Parameters
        ----------
        data : np.ndarray
            1-D array of spend values.

        Returns
        -------
        dict[str, float]
            Keys like 'p10', 'p25', ..., 'p99' mapping to the corresponding
            percentile values.
        """
        result: dict[str, float] = {}
        for key, pct in zip(self.PERCENTILE_KEYS, self.PERCENTILE_VALUES, strict=True):
            result[key] = round(float(np.percentile(data, pct)), 2)
        return result

    @staticmethod
    def _percentile_errors(
        pred_pcts: dict[str, float],
        actual_pcts: dict[str, float],
    ) -> dict[str, float]:
        """Compute absolute percentage error at each percentile.

        Parameters
        ----------
        pred_pcts, actual_pcts : dict[str, float]
            Percentile dictionaries with matching keys.

        Returns
        -------
        dict[str, float]
            Absolute percentage error for each percentile key.
        """
        errors: dict[str, float] = {}
        for key in pred_pcts:
            p = pred_pcts[key]
            a = actual_pcts[key]
            if a != 0:
                errors[key] = round(abs(p - a) / abs(a) * 100.0, 2)
            else:
                errors[key] = float("inf") if p != 0 else 0.0
        return errors

    # ------------------------------------------------------------------
    # Internal: super-utiliser share
    # ------------------------------------------------------------------

    def _super_utilizer_share(self, distribution: np.ndarray) -> float:
        """Compute the fraction of total spend from the top N % of spenders.

        Parameters
        ----------
        distribution : np.ndarray
            1-D array of spend values.

        Returns
        -------
        float
            Fraction of total spend from the top ``super_utilizer_top_pct``
            of spenders.  For US Medicaid, this is typically ~0.54 for the
            top 5 %.
        """
        total = float(np.sum(distribution))
        if total == 0:
            return 0.0

        sorted_desc = np.sort(distribution)[::-1]
        n_top = max(1, int(math.ceil(len(distribution) * self.super_utilizer_top_pct)))
        top_spend = float(np.sum(sorted_desc[:n_top]))

        return top_spend / total
