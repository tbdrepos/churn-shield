from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field, model_validator

# =========================================================
# SHARED TYPES
# =========================================================

UnitInterval = Annotated[float, Field(ge=0, le=1)]
PercentList = list[UnitInterval]


class ChartMeta(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ChartData(BaseModel):
    pass


# =========================================================
# DATA INSIGHTS
# =========================================================


# =========================================================
# 1. MISSING VALUES
# =========================================================


class MissingValuesData(ChartData):
    features: list[str]
    missing_counts: list[int]
    missing_percentages: PercentList

    @model_validator(mode="after")
    def validate_lengths(self):
        if not (
            len(self.features)
            == len(self.missing_counts)
            == len(self.missing_percentages)
        ):
            raise ValueError("All lists must have the same length")
        return self


class MissingValuesChart(BaseModel):
    type: Literal["Missing Values"] = "Missing Values"
    data: MissingValuesData
    meta: Optional[ChartMeta] = None


# =========================================================
# 2. TARGET DISTRIBUTION
# =========================================================


class TargetDistributionData(ChartData):
    classes: list[str]
    counts: list[int]
    percentages: PercentList

    @model_validator(mode="after")
    def validate_lengths(self):
        if not (len(self.classes) == len(self.counts) == len(self.percentages)):
            raise ValueError("classes, counts, percentages must match length")
        return self


class TargetDistributionChart(BaseModel):
    type: Literal["Target Distribution"] = "Target Distribution"
    data: TargetDistributionData
    meta: Optional[ChartMeta] = None


# =========================================================
# 3. CORRELATION MATRIX
# =========================================================


class CorrelationMatrixData(ChartData):
    features: list[str]
    matrix: list[list[float]]

    @model_validator(mode="after")
    def validate_matrix(self):
        n = len(self.features)

        if n == 0:
            raise ValueError("features cannot be empty")

        if any(len(row) != n for row in self.matrix):
            raise ValueError("Matrix must be square and match features length")

        # Optional: enforce correlation bounds [-1, 1]
        for row in self.matrix:
            for val in row:
                if val < -1 or val > 1:
                    raise ValueError("Correlation values must be between -1 and 1")

        return self


class CorrelationMatrixChart(BaseModel):
    type: Literal["Correlation Matrix"] = "Correlation Matrix"
    data: CorrelationMatrixData
    meta: Optional[ChartMeta] = None


# =========================================================
# 4. DATASET SCHEMA (STRUCTURE INSIGHT)
# =========================================================


class FeatureSchema(BaseModel):
    name: str
    dtype: str
    missing_count: int
    unique_count: int


class DatasetSchemaData(ChartData):
    features: list[FeatureSchema]


class DatasetSchemaChart(BaseModel):
    type: Literal["Schema"] = "Schema"
    data: DatasetSchemaData
    meta: Optional[ChartMeta] = None


# =========================================================
# 5. OUTLIERS
# =========================================================


class OutlierStats(BaseModel):
    feature: str
    lower_bound: float
    upper_bound: float
    outlier_count: int
    outlier_percentage: UnitInterval


class OutliersData(ChartData):
    features: list[OutlierStats]


class OutliersChart(BaseModel):
    type: Literal["Outliers"] = "Outliers"
    data: OutliersData
    meta: Optional[ChartMeta] = None


# =========================================================
# 6. FEATURE ↔ TARGET RELATIONSHIP
# =========================================================


class FeatureTargetRelationshipData(ChartData):
    feature: str
    bins_or_categories: list[str]
    target_rate: PercentList  # e.g. churn rate per bin/category

    @model_validator(mode="after")
    def validate_lengths(self):
        if len(self.bins_or_categories) != len(self.target_rate):
            raise ValueError("bins/categories and target_rate must match")
        return self


class FeatureTargetRelationshipChart(BaseModel):
    type: Literal["Feature Target Relationship"] = "Feature Target Relationship"
    data: FeatureTargetRelationshipData
    meta: Optional[ChartMeta] = None


# =========================================================
# 7. FEATURE DISTRIBUTION
# =========================================================


class FeatureDistributionData(ChartData):
    feature: str
    bins: list[float]
    counts: list[int]

    @model_validator(mode="after")
    def validate_lengths(self):
        if len(self.bins) != len(self.counts):
            raise ValueError("bins and counts must match length")
        return self


class FeatureDistributionChart(BaseModel):
    type: Literal["Feature Distribution"] = "Feature Distribution"
    data: FeatureDistributionData
    meta: Optional[ChartMeta] = None


# =========================================================
# UNION (DATA INSIGHTS)
# =========================================================

DataChart = Annotated[
    Union[
        FeatureDistributionChart,
        MissingValuesChart,
        TargetDistributionChart,
        CorrelationMatrixChart,
        DatasetSchemaChart,
        OutliersChart,
        FeatureTargetRelationshipChart,
    ],
    Field(discriminator="type"),
]
