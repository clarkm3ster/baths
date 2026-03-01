"""DOME Validation Framework.

Provides holdout-set validation, subgroup fairness calibration,
spend-distribution analysis, and bias/surveillance auditing for
THE DOME's predictive models.
"""

from dome.validation.holdout_validator import (
    CalibrationPoint,
    HoldoutValidator,
    ValidationReport,
)
from dome.validation.subgroup_calibration import (
    GroupCalibration,
    SubgroupCalibrator,
    SubgroupReport,
)
from dome.validation.spend_distribution import (
    DistributionReport,
    SpendDistributionValidator,
)
from dome.validation.bias_audit import (
    BiasAuditor,
    BiasCheck,
    BiasReport,
)

__all__ = [
    # holdout
    "CalibrationPoint",
    "HoldoutValidator",
    "ValidationReport",
    # subgroup
    "GroupCalibration",
    "SubgroupCalibrator",
    "SubgroupReport",
    # distribution
    "DistributionReport",
    "SpendDistributionValidator",
    # bias
    "BiasAuditor",
    "BiasCheck",
    "BiasReport",
]
