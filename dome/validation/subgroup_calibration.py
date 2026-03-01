"""Subgroup fairness calibration for DOME spend predictions.

Partitions prediction/actual pairs by a demographic or programmatic grouping
field and checks whether the model is equally accurate across all subgroups.
Disparate calibration ratios can indicate algorithmic bias — for example, a
model that systematically under-predicts costs for one racial group would
produce a lower calibration ratio for that group, leading to under-allocation
of preventive resources.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Pydantic report models
# ---------------------------------------------------------------------------

class GroupCalibration(BaseModel):
    """Accuracy and calibration metrics for a single subgroup."""

    group_value: str = Field(..., description="The value of the grouping field (e.g. 'Black', 'rural').")
    n: int = Field(..., ge=0, description="Number of observations in this subgroup.")
    mae: float = Field(..., description="Mean Absolute Error for this subgroup.")
    mape: float = Field(..., description="Mean Absolute Percentage Error (fraction) for this subgroup.")
    predicted_mean: float = Field(..., description="Mean predicted spend in this subgroup.")
    actual_mean: float = Field(..., description="Mean actual spend in this subgroup.")
    calibration_ratio: float = Field(
        ...,
        description="predicted_mean / actual_mean.  Values near 1.0 indicate good calibration.",
    )


class SubgroupReport(BaseModel):
    """Full subgroup-fairness calibration report.

    The ``fairness_flag`` summarises the worst-case disparity:

    * **green** — max disparity ratio < 1.10 (all groups calibrated similarly)
    * **yellow** — max disparity ratio in [1.10, 1.30) (moderate concern)
    * **red** — max disparity ratio >= 1.30 (significant fairness risk)
    """

    group_field: str = Field(..., description="Name of the field used for subgroup partitioning.")
    overall_mae: float = Field(..., description="MAE across the entire dataset (all groups combined).")
    groups: list[GroupCalibration] = Field(
        ..., description="Per-group calibration metrics."
    )
    max_disparity_ratio: float = Field(
        ...,
        description=(
            "Ratio of the highest to lowest calibration_ratio across groups.  "
            "Values near 1.0 mean all groups are equally well-calibrated."
        ),
    )
    fairness_flag: str = Field(
        ...,
        description="Traffic-light summary: 'green', 'yellow', or 'red'.",
    )


# ---------------------------------------------------------------------------
# Core calibrator
# ---------------------------------------------------------------------------

class SubgroupCalibrator:
    """Check whether DOME predictions are equally calibrated across subgroups.

    Parameters
    ----------
    predicted_field : str
        Key in each prediction dict holding the numeric predicted spend.
    actual_field : str
        Key in each actual dict holding the numeric actual spend.
    min_group_size : int
        Subgroups with fewer than this many members are excluded from the
        disparity calculation (but still reported) because their statistics
        are unreliable.
    """

    def __init__(
        self,
        predicted_field: str = "predicted_spend",
        actual_field: str = "actual_spend",
        min_group_size: int = 10,
    ) -> None:
        self.predicted_field = predicted_field
        self.actual_field = actual_field
        self.min_group_size = min_group_size

    def calibrate(
        self,
        predictions: list[dict[str, Any]],
        actuals: list[dict[str, Any]],
        group_field: str,
    ) -> SubgroupReport:
        """Compute per-subgroup calibration and overall fairness assessment.

        Parameters
        ----------
        predictions : list[dict]
            Each dict must contain ``predicted_field`` and ``group_field``.
        actuals : list[dict]
            Parallel list with ``actual_field`` in each dict.
        group_field : str
            The key whose distinct values define subgroups (e.g. ``"race"``,
            ``"geography"``).

        Returns
        -------
        SubgroupReport
            Structured report including per-group metrics and a fairness flag.

        Raises
        ------
        ValueError
            If lists differ in length, are empty, or ``group_field`` is
            missing from prediction dicts.
        """
        if len(predictions) != len(actuals):
            raise ValueError(
                f"predictions ({len(predictions)}) and actuals ({len(actuals)}) must have the same length."
            )
        if len(predictions) == 0:
            raise ValueError("Cannot calibrate on an empty dataset.")

        # ---- build arrays ----
        pred_arr = np.array(
            [p[self.predicted_field] for p in predictions], dtype=np.float64
        )
        actual_arr = np.array(
            [a[self.actual_field] for a in actuals], dtype=np.float64
        )

        # Extract group labels — try predictions first, then actuals
        group_labels: list[str] = []
        for i, p in enumerate(predictions):
            if group_field in p:
                group_labels.append(str(p[group_field]))
            elif group_field in actuals[i]:
                group_labels.append(str(actuals[i][group_field]))
            else:
                raise ValueError(
                    f"group_field '{group_field}' not found in predictions[{i}] or actuals[{i}]."
                )

        # ---- overall MAE ----
        overall_mae = float(np.mean(np.abs(pred_arr - actual_arr)))

        # ---- per-group metrics ----
        unique_groups = sorted(set(group_labels))
        group_label_arr = np.array(group_labels)

        group_calibrations: list[GroupCalibration] = []
        for gv in unique_groups:
            mask = group_label_arr == gv
            n_group = int(np.sum(mask))
            p_group = pred_arr[mask]
            a_group = actual_arr[mask]

            errors = p_group - a_group
            abs_errors = np.abs(errors)
            group_mae = float(np.mean(abs_errors))

            nonzero = a_group != 0.0
            if np.any(nonzero):
                group_mape = float(
                    np.mean(np.abs(errors[nonzero]) / np.abs(a_group[nonzero]))
                )
            else:
                group_mape = float("inf")

            p_mean = float(np.mean(p_group))
            a_mean = float(np.mean(a_group))
            cal_ratio = p_mean / a_mean if a_mean != 0 else float("inf")

            group_calibrations.append(
                GroupCalibration(
                    group_value=gv,
                    n=n_group,
                    mae=round(group_mae, 2),
                    mape=round(group_mape, 4),
                    predicted_mean=round(p_mean, 2),
                    actual_mean=round(a_mean, 2),
                    calibration_ratio=round(cal_ratio, 4),
                )
            )

        # ---- disparity calculation ----
        # Only include groups with sufficient sample size
        eligible_ratios = [
            gc.calibration_ratio
            for gc in group_calibrations
            if gc.n >= self.min_group_size and np.isfinite(gc.calibration_ratio)
        ]

        if len(eligible_ratios) >= 2:
            max_ratio = max(eligible_ratios)
            min_ratio = min(eligible_ratios)
            disparity = max_ratio / min_ratio if min_ratio > 0 else float("inf")
        elif len(eligible_ratios) == 1:
            disparity = 1.0  # only one group — no disparity computable
        else:
            disparity = float("nan")

        # ---- fairness flag ----
        if np.isnan(disparity) or not np.isfinite(disparity):
            flag = "red"
        elif disparity < 1.10:
            flag = "green"
        elif disparity < 1.30:
            flag = "yellow"
        else:
            flag = "red"

        return SubgroupReport(
            group_field=group_field,
            overall_mae=round(overall_mae, 2),
            groups=group_calibrations,
            max_disparity_ratio=round(disparity, 4),
            fairness_flag=flag,
        )
