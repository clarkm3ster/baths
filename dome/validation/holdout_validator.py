"""Holdout-set validation for DOME spend predictions.

Splits a paired set of predictions and actuals into train/test partitions,
then computes standard regression-accuracy metrics and decile-level
calibration diagnostics.  Designed to validate 12-month prospective
spend predictions used in DOME's fiscal engines.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Pydantic report models
# ---------------------------------------------------------------------------

class CalibrationPoint(BaseModel):
    """One row of a decile-calibration table.

    A well-calibrated model will have ``ratio`` near 1.0 for every decile.
    Ratios outside [0.8, 1.2] indicate systematic mis-calibration in that
    risk tier.
    """

    decile: int = Field(..., ge=1, le=10, description="Decile bucket (1 = lowest predicted spend, 10 = highest).")
    predicted_mean: float = Field(..., description="Mean predicted spend in this decile.")
    actual_mean: float = Field(..., description="Mean actual spend in this decile.")
    ratio: float = Field(..., description="predicted_mean / actual_mean.  1.0 is perfectly calibrated.")
    n_in_decile: int = Field(..., ge=0, description="Number of observations in this decile.")
    miscalibrated: bool = Field(
        False,
        description="True when ratio < 0.8 or ratio > 1.2, signaling systematic bias in this tier.",
    )


class ValidationReport(BaseModel):
    """Summary output of a holdout-set validation run.

    Contains point-estimate accuracy metrics (MAE, MAPE, RMSE, R-squared)
    and granular decile-level calibration data.
    """

    mae: float = Field(..., description="Mean Absolute Error across the test set.")
    mape: float = Field(..., description="Mean Absolute Percentage Error (as a fraction, not %).")
    rmse: float = Field(..., description="Root Mean Squared Error across the test set.")
    calibration_by_decile: list[CalibrationPoint] = Field(
        ..., description="Calibration statistics for each predicted-spend decile."
    )
    r_squared: float = Field(..., description="Coefficient of determination (R-squared).")
    n_samples: int = Field(..., ge=0, description="Total number of observations (train + test).")
    n_train: int = Field(..., ge=0, description="Number of observations in the training partition.")
    n_test: int = Field(..., ge=0, description="Number of observations in the test partition.")
    miscalibrated_deciles: list[int] = Field(
        default_factory=list,
        description="Decile numbers where calibration ratio fell outside [0.8, 1.2].",
    )


# ---------------------------------------------------------------------------
# Core validator
# ---------------------------------------------------------------------------

class HoldoutValidator:
    """Validate DOME spend predictions against actual outcomes on a holdout set.

    Parameters
    ----------
    train_fraction : float
        Fraction of data allocated to the training partition.  The remainder
        becomes the test set on which all metrics are computed.  Default 0.80.
    seed : int | None
        Random seed for reproducible train/test splits.
    predicted_field : str
        Key in each prediction dict that holds the predicted 12-month spend.
    actual_field : str
        Key in each actual dict that holds the realised 12-month spend.
    """

    def __init__(
        self,
        train_fraction: float = 0.80,
        seed: int | None = 42,
        predicted_field: str = "predicted_spend",
        actual_field: str = "actual_spend",
    ) -> None:
        if not 0.0 < train_fraction < 1.0:
            raise ValueError(f"train_fraction must be in (0, 1), got {train_fraction}")
        self.train_fraction = train_fraction
        self.seed = seed
        self.predicted_field = predicted_field
        self.actual_field = actual_field

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def validate(
        self,
        predictions: list[dict[str, Any]],
        actuals: list[dict[str, Any]],
    ) -> ValidationReport:
        """Run a full holdout validation.

        Parameters
        ----------
        predictions : list[dict]
            Each dict must contain at least ``self.predicted_field`` with a
            numeric predicted 12-month spend value.
        actuals : list[dict]
            Parallel list (same length, same order) where each dict contains
            ``self.actual_field`` with the realised 12-month spend.

        Returns
        -------
        ValidationReport
            Structured report with accuracy metrics and calibration data.

        Raises
        ------
        ValueError
            If input lists differ in length or are empty.
        """
        if len(predictions) != len(actuals):
            raise ValueError(
                f"predictions ({len(predictions)}) and actuals ({len(actuals)}) must have the same length."
            )
        n_total = len(predictions)
        if n_total == 0:
            raise ValueError("Cannot validate on an empty dataset.")

        # ---- extract numeric arrays ----
        pred_values = np.array(
            [p[self.predicted_field] for p in predictions], dtype=np.float64
        )
        actual_values = np.array(
            [a[self.actual_field] for a in actuals], dtype=np.float64
        )

        # ---- train / test split ----
        rng = np.random.default_rng(self.seed)
        indices = rng.permutation(n_total)
        n_train = int(math.floor(n_total * self.train_fraction))
        n_test = n_total - n_train
        if n_test == 0:
            raise ValueError("Test set is empty — increase data size or decrease train_fraction.")

        test_idx = indices[n_train:]
        pred_test = pred_values[test_idx]
        actual_test = actual_values[test_idx]

        # ---- point metrics ----
        errors = pred_test - actual_test
        abs_errors = np.abs(errors)
        mae = float(np.mean(abs_errors))

        # MAPE — guard against zero actuals
        nonzero_mask = actual_test != 0.0
        if np.any(nonzero_mask):
            mape = float(np.mean(np.abs(errors[nonzero_mask]) / np.abs(actual_test[nonzero_mask])))
        else:
            mape = float("inf")

        rmse = float(np.sqrt(np.mean(errors ** 2)))

        # R-squared
        ss_res = float(np.sum(errors ** 2))
        ss_tot = float(np.sum((actual_test - np.mean(actual_test)) ** 2))
        r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

        # ---- decile calibration ----
        calibration = self._compute_decile_calibration(pred_test, actual_test)
        miscalibrated = [cp.decile for cp in calibration if cp.miscalibrated]

        return ValidationReport(
            mae=mae,
            mape=mape,
            rmse=rmse,
            calibration_by_decile=calibration,
            r_squared=r_squared,
            n_samples=n_total,
            n_train=n_train,
            n_test=n_test,
            miscalibrated_deciles=miscalibrated,
        )

    # ------------------------------------------------------------------
    # Synthetic data generator
    # ------------------------------------------------------------------

    @staticmethod
    def generate_synthetic_validation(
        n: int = 500,
        seed: int = 123,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Create synthetic prediction/actual pairs for testing.

        Generates realistic Medicaid-like spend distributions using a mixture
        of a base lognormal population and a super-utiliser tail:

        * ~90 % of members drawn from LogNormal(mu=8.5, sigma=1.2)
          (median ~$4 900, mean ~$9 900)
        * ~10 % super-utilisers from LogNormal(mu=10.5, sigma=0.8)
          (median ~$36 300, mean ~$53 000)

        Predictions are actuals + noise, with higher noise for
        super-utilisers (harder to predict).

        Parameters
        ----------
        n : int
            Number of synthetic individuals.
        seed : int
            Random seed for reproducibility.

        Returns
        -------
        tuple[list[dict], list[dict]]
            (predictions, actuals) — parallel lists of dicts with keys
            ``predicted_spend`` and ``actual_spend`` respectively, plus
            ``person_id``.
        """
        rng = np.random.default_rng(seed)

        n_super = int(n * 0.10)
        n_base = n - n_super

        # --- actual spend ---
        base_spend = rng.lognormal(mean=8.5, sigma=1.2, size=n_base)
        super_spend = rng.lognormal(mean=10.5, sigma=0.8, size=n_super)
        actual_spend = np.concatenate([base_spend, super_spend])

        # --- predicted spend = actual + heteroscedastic noise ---
        noise_base = rng.normal(loc=0, scale=0.15 * base_spend, size=n_base)
        noise_super = rng.normal(loc=0, scale=0.25 * super_spend, size=n_super)
        pred_spend = np.concatenate([base_spend + noise_base, super_spend + noise_super])
        pred_spend = np.maximum(pred_spend, 0.0)  # spend cannot be negative

        # shuffle so super-utilisers are not grouped at the end
        order = rng.permutation(n)
        actual_spend = actual_spend[order]
        pred_spend = pred_spend[order]

        predictions: list[dict[str, Any]] = []
        actuals: list[dict[str, Any]] = []
        for i in range(n):
            pid = f"SYN-{i:05d}"
            predictions.append({"person_id": pid, "predicted_spend": float(pred_spend[i])})
            actuals.append({"person_id": pid, "actual_spend": float(actual_spend[i])})

        return predictions, actuals

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_decile_calibration(
        predicted: np.ndarray,
        actual: np.ndarray,
    ) -> list[CalibrationPoint]:
        """Bin test-set observations into predicted-spend deciles and compute
        calibration ratios.

        Parameters
        ----------
        predicted, actual : np.ndarray
            Equal-length 1-D arrays of predicted and actual spend for the
            test set.

        Returns
        -------
        list[CalibrationPoint]
            One entry per decile (1-10).
        """
        n = len(predicted)
        # Compute decile assignments (1-10) based on predicted spend rank
        # Use ranking to handle ties gracefully
        order = np.argsort(predicted)
        ranks = np.empty_like(order)
        ranks[order] = np.arange(n)
        # Map rank [0..n-1] to decile [1..10]
        decile_assignments = np.minimum(ranks * 10 // n + 1, 10).astype(int)

        points: list[CalibrationPoint] = []
        for d in range(1, 11):
            mask = decile_assignments == d
            n_in = int(np.sum(mask))
            if n_in == 0:
                points.append(
                    CalibrationPoint(
                        decile=d,
                        predicted_mean=0.0,
                        actual_mean=0.0,
                        ratio=1.0,
                        n_in_decile=0,
                        miscalibrated=False,
                    )
                )
                continue

            p_mean = float(np.mean(predicted[mask]))
            a_mean = float(np.mean(actual[mask]))
            ratio = p_mean / a_mean if a_mean != 0 else float("inf")
            miscalibrated = ratio < 0.8 or ratio > 1.2

            points.append(
                CalibrationPoint(
                    decile=d,
                    predicted_mean=round(p_mean, 2),
                    actual_mean=round(a_mean, 2),
                    ratio=round(ratio, 4),
                    n_in_decile=n_in,
                    miscalibrated=miscalibrated,
                )
            )

        return points
