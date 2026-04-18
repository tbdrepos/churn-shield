from typing import Annotated, Generic, Literal, Optional, TypeVar, Union

from pydantic import BaseModel, Field, model_validator

# =========================================================
# BASE CHART & SHARED TYPES
# =========================================================
UnitInterval = Annotated[float, Field(ge=0, le=1)]
CorrelationInterval = Annotated[float, Field(ge=-1, le=1)]
""" ChartTypes = Literal[
    "categorical",
    "xy",
    "boxplot",
    "missing_values",
    "target_distribution",
    "correlation_matrix",
    "outliers",
    "feature_distribution",
    "feature_target_relationship",
    "dataset_schema",
]
RenderTypes = Literal["categorical", "xy", "matrix", "boxplot", "table", "composite"] """
CT = TypeVar("CT", bound=str)
RT = TypeVar("RT", bound=str)


class BaseChart(BaseModel, Generic[CT, RT]):
    chart_type: CT
    title: str
    description: Optional[str] = None

    render_type: RT

    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    legend: Optional[list[str]] = None


class CategoricalChart(BaseChart):
    render_type: Literal["categorical"] = "categorical"
    categories: list[str]
    series: list[int] | list[float]

    @model_validator(mode="after")
    def validate_lengths(self):
        if len(self.categories) != len(self.series):
            raise ValueError("categories and series must match length")
        return self


# =========================================================
# 1. MISSING VALUES & 2. TARGET DISTRIBUTION
# =========================================================


class MissingValuesChart(CategoricalChart):
    chart_type: Literal["missing_values"] = "missing_values"
    percentages: list[UnitInterval]


class TargetDistributionChart(CategoricalChart):
    chart_type: Literal["target_distribution"] = "target_distribution"
    percentages: list[UnitInterval]

    @model_validator(mode="after")
    def validate_lengths(self):
        if len(self.categories) != len(self.series) or len(self.series) != len(
            self.percentages
        ):
            raise ValueError("categories, series, and percentages must match length")
        return self


# =========================================================
# 3. CORRELATION MATRIX
# =========================================================


class CorrelationCell(BaseModel):
    x: str  # feature name (column)
    y: CorrelationInterval  # correlation value [-1, 1]


class CorrelationSeries(BaseModel):
    name: str  # feature name (row)
    data: list[CorrelationCell]


class CorrelationMatrixChart(BaseChart):
    chart_type: Literal["correlation_matrix"] = "correlation_matrix"
    render_type: Literal["matrix"] = "matrix"
    series: list[CorrelationSeries]
    labels: list[str]

    @model_validator(mode="after")
    def validate_matrix(self):
        n = len(self.labels)
        if len(self.series) != n or any(len(row.data) != n for row in self.series):
            raise ValueError(
                "Correlation matrix must be square and match labels length"
            )
        return self


# =========================================================
# 4. DATASET SCHEMA & 5. OUTLIERS (DATA MODELS)
# =========================================================


class FeatureSchema(BaseModel):
    name: str
    dtype: str
    missing_count: int
    unique_count: int


class DatasetSchemaChart(BaseChart):
    chart_type: Literal["dataset_schema"] = "dataset_schema"
    render_type: Literal["table"] = "table"
    rows: list[FeatureSchema]


class BoxPlotChart(BaseChart):
    chart_type: Literal["boxplot"] = "boxplot"
    render_type: Literal["boxplot"] = "boxplot"

    series: list[float]  # [lower, q1, median, q3, upper]


class OutliersChart(BaseChart):
    chart_type: Literal["outliers"] = "outliers"
    render_type: Literal["composite"] = "composite"
    charts: list[BoxPlotChart]


# =========================================================
# 6. FEATURE ↔ TARGET & 7. FEATURE DISTRIBUTION
# =========================================================


class FeatureBarChart(CategoricalChart):
    chart_type: Literal["categorical"] = "categorical"


class FeatureDistributionChart(BaseChart):
    chart_type: Literal["feature_distribution"] = "feature_distribution"
    render_type: Literal["composite"] = "composite"
    charts: list[FeatureBarChart]


class XYChart(BaseChart):
    chart_type: Literal["xy"] = "xy"
    render_type: Literal["xy"] = "xy"
    series: list[list[list[float]]]  # [[x1, y1], [x2, y2], ...]


class FeatureTargetRelationshipChart(BaseChart):
    chart_type: Literal["feature_target_relationship"] = "feature_target_relationship"
    render_type: Literal["composite"] = "composite"
    charts: list[XYChart | FeatureBarChart]


# =========================================================
# DISCRIMINATED UNION
# =========================================================


DataChart = Annotated[
    Union[
        MissingValuesChart,
        CorrelationMatrixChart,
        TargetDistributionChart,
        FeatureTargetRelationshipChart,
        FeatureDistributionChart,
        OutliersChart,
        DatasetSchemaChart,
    ],
    Field(discriminator="chart_type"),
]
