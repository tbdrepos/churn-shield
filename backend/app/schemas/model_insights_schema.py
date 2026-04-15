from typing import Annotated, Generic, Literal, Optional, TypeVar, Union

from pydantic import BaseModel, Field, model_validator

# =========================================================
# BASE CHART
# =========================================================

# 1. Define a TypeVar that is constrained to strings
T = TypeVar("T", bound=str)


class BaseChart(BaseModel, Generic[T]):
    chart_type: T

    # Core metadata (now first-class)
    title: str
    description: Optional[str] = None

    x_axis: Optional[str] = None
    y_axis: Optional[str] = None

    legend: Optional[list[str]] = None


class CategoricalChart(BaseChart):
    categories: list[str]


# =========================================================
# FEATURE IMPORTANCE
# =========================================================


class FeatureImportanceChart(CategoricalChart):
    chart_type: Literal["feature_importance"] = "feature_importance"

    series: list[float]

    @model_validator(mode="after")
    def validate_lengths(self):
        data_row = self.series
        if len(self.categories) != len(data_row):
            raise ValueError("categories and data must match length")
        return self


# =========================================================
# PREDICTION DISTRIBUTION
# =========================================================


class PredictionDistributionChart(CategoricalChart):
    chart_type: Literal["prediction_distribution"] = "prediction_distribution"

    series: list[int]

    @model_validator(mode="after")
    def validate_lengths(self):
        data_row = self.series
        if len(self.categories) != len(data_row):
            raise ValueError("categories and data must match length")
        return self


# =========================================================
# ROC CURVE (XY SERIES)
# =========================================================


class RocData(BaseModel):
    x: float
    y: float


class RocSeries(BaseModel):
    name: str
    data: list[RocData]  # [[fpr, tpr]]


class RocCurveChart(BaseChart):
    chart_type: Literal["roc_curve"] = "roc_curve"

    series: list[RocSeries]
    auc: float


# =========================================================
# CONFUSION MATRIX
# =========================================================


class ConfusionMatrixData(BaseModel):
    x: str  # x-axis label
    y: float  # probability
    count: int  # count

    @model_validator(mode="after")
    def validate_count(self):
        if self.count < 0:
            raise ValueError("Count must be non-negative")
        return self


class ConfusionMatrixSeries(BaseModel):
    name: str
    data: list[ConfusionMatrixData]


class ConfusionMatrixChart(BaseChart):
    chart_type: Literal["confusion_matrix"] = "confusion_matrix"

    series: list[ConfusionMatrixSeries]
    labels: list[str]  # y-axis labels

    @model_validator(mode="after")
    def validate_matrix(self):
        n = len(self.labels)

        if n == 0:
            raise ValueError("Labels cannot be empty")

        for row in self.series:
            if len(row.data) != n:
                raise ValueError("Matrix must be square")

        return self


# =========================================================
# CALIBRATION CURVE
# =========================================================


class CalibrationSeries(BaseModel):
    name: str
    data: list[list[float]]  # [[pred, true]]


class CalibrationCurveChart(BaseChart):
    chart_type: Literal["calibration_curve"] = "calibration_curve"

    series: list[CalibrationSeries]


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
    Field(discriminator="chart_type"),
]
