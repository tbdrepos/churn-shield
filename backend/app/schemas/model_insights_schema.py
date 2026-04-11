from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field, model_validator

# Reusable Type Aliases for Readability
UnitInterval = Annotated[float, Field(ge=0, le=1)]
PercentList = list[UnitInterval]

# =========================================================
# BASE CHART TYPES
# =========================================================


class ChartMeta(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ChartData(BaseModel):
    """Base class for all chart data."""

    pass


# =========================================================
# Model Insights
# =========================================================


# =========================================================
# FEATURE IMPORTANCE
# =========================================================


class FeatureImportanceData(ChartData):
    features: list[str]
    importances: list[Annotated[float, Field(ge=0)]]

    @model_validator(mode="after")
    def validate_lengths(self):
        if len(self.features) != len(self.importances):
            raise ValueError("features and importances must have same length")
        return self


class FeatureImportanceChart(BaseModel):
    type: Literal["Feature Importance"] = "Feature Importance"
    data: FeatureImportanceData
    meta: Optional[ChartMeta] = None


# =========================================================
# PREDICTION DISTRIBUTION
# =========================================================


class PredictionDistributionData(ChartData):
    classes: list[str]
    counts: list[int]
    percentages: PercentList

    @model_validator(mode="after")
    def validate_lengths(self):
        if not (len(self.classes) == len(self.counts) == len(self.percentages)):
            raise ValueError("classes, counts, percentages must match length")
        return self


class PredictionDistributionChart(BaseModel):
    type: Literal["Prediction Distribution"] = "Prediction Distribution"
    data: PredictionDistributionData
    meta: Optional[ChartMeta] = None


# =========================================================
# ROC CURVE
# =========================================================


class RocCurveData(ChartData):
    fpr: Annotated[PercentList, Field(min_length=2)]
    tpr: Annotated[PercentList, Field(min_length=2)]
    thresholds: Annotated[list[float], Field(min_length=2)]

    @model_validator(mode="after")
    def validate_lengths(self):
        if not (len(self.fpr) == len(self.tpr) == len(self.thresholds)):
            raise ValueError("fpr, tpr, thresholds must have same length")
        return self


class RocMeta(ChartMeta):
    auc: UnitInterval


class RocCurveChart(BaseModel):
    type: Literal["ROC Curve"] = "ROC Curve"
    data: RocCurveData
    meta: RocMeta


# =========================================================
# CONFUSION MATRIX
# =========================================================


class ConfusionMatrixData(ChartData):
    matrix: list[list[int]]
    normalized_matrix: Optional[list[list[float]]] = None
    labels: list[str]
    predicted_labels: list[str]

    @model_validator(mode="after")
    def validate_matrix(self):
        n = len(self.labels)
        if n == 0:
            raise ValueError("Labels cannot be empty")

        # Verify square matrix against labels length
        for row in self.matrix:
            if len(row) != n:
                raise ValueError(f"Matrix rows must match labels length ({n})")

        if self.normalized_matrix and any(
            len(row) != n for row in self.normalized_matrix
        ):
            raise ValueError("Normalized matrix must match shape")

        return self


class ConfusionMatrixChart(BaseModel):
    type: Literal["Confusion Matrix"] = "Confusion Matrix"
    data: ConfusionMatrixData
    meta: Optional[ChartMeta] = None


# =========================================================
# CALIBRATION CURVE
# =========================================================


class CalibrationCurveData(ChartData):
    mean_predicted_value: PercentList
    fraction_of_positives: PercentList

    @model_validator(mode="after")
    def validate_lengths(self):
        if len(self.mean_predicted_value) != len(self.fraction_of_positives):
            raise ValueError(
                "mean_predicted_value and fraction_of_positives must match"
            )
        return self


class CalibrationCurveChart(BaseModel):
    type: Literal["Calibration Curve"] = "Calibration Curve"
    data: CalibrationCurveData
    meta: Optional[ChartMeta] = None


# =========================================================
# DISCRIMINATED UNION
# =========================================================

ModelChart = Annotated[
    Union[
        FeatureImportanceChart,
        PredictionDistributionChart,
        RocCurveChart,
        ConfusionMatrixChart,
        CalibrationCurveChart,
    ],
    Field(discriminator="type"),
]
