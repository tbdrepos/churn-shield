from pathlib import Path

import numpy as np
import pandas as pd

from app.core.security import UserDep
from app.models.datasets_model import Dataset
from app.models.models_model import Model
from app.schemas.dataset_insights_schema import (
    ChartMeta,
    CorrelationMatrixChart,
    CorrelationMatrixData,
    DataChart,
    DatasetSchemaChart,
    DatasetSchemaData,
    FeatureDistributionChart,
    FeatureDistributionData,
    FeatureSchema,
    FeatureTargetRelationshipChart,
    FeatureTargetRelationshipData,
    MissingValuesChart,
    MissingValuesData,
    OutliersChart,
    OutliersData,
    OutlierStats,
    TargetDistributionChart,
    TargetDistributionData,
)
from app.services.train_service import prepare_data
from app.utils.validator import read_churn_df


def get_dataset_charts(dataset: Dataset, user: UserDep) -> list[DataChart]:
    df = read_churn_df(Path(dataset.file_path))
    target_column = "Churn"
    dataset_charts: list[DataChart] = [
        build_missing_values(df),
        build_target_distribution(df, target_column),
        build_correlation_matrix(df),
    ]

    dataset_charts.extend(
        build_feature_target_relationships(df, target_column, max_bins=10)
    )
    return dataset_charts


def build_missing_values(df: pd.DataFrame) -> MissingValuesChart:
    missing_counts = df.isnull().sum()
    missing_values_data: MissingValuesData = MissingValuesData(
        features=missing_counts.index.tolist(),
        missing_counts=missing_counts.tolist(),
        missing_percentages=df.isnull().mean().tolist(),
    )
    return MissingValuesChart(type="Missing Values", data=missing_values_data)


def build_target_distribution(
    df: pd.DataFrame, target_column: str
) -> TargetDistributionChart:
    counts = df[target_column].value_counts(dropna=False)
    target_distribution_data: TargetDistributionData = TargetDistributionData(
        classes=counts.index.astype(str).tolist(),
        counts=counts.tolist(),
        percentages=df[target_column].value_counts(normalize=True).tolist(),
    )
    return TargetDistributionChart(
        type="Target Distribution", data=target_distribution_data
    )


def build_correlation_matrix(df: pd.DataFrame) -> CorrelationMatrixChart:
    numeric_df = df.select_dtypes(include=[np.number])
    correlation_matrix_data: CorrelationMatrixData = CorrelationMatrixData(
        features=numeric_df.columns.tolist(),
        matrix=numeric_df.corr().values.tolist(),
    )
    return CorrelationMatrixChart(
        type="Correlation Matrix", data=correlation_matrix_data
    )


def build_schema(df: pd.DataFrame) -> DatasetSchemaChart:
    features: list[FeatureSchema] = []

    for col in df.columns:
        series = df[col]

        features.append(
            FeatureSchema(
                name=col,
                dtype=str(series.dtype),
                missing_count=int(series.isnull().sum()),
                unique_count=int(series.nunique(dropna=True)),
            )
        )

    dataset_schema_data: DatasetSchemaData = DatasetSchemaData(
        features=features,
    )
    return DatasetSchemaChart(type="Schema", data=dataset_schema_data)


def build_outliers(df: pd.DataFrame) -> OutliersChart:
    numeric_df = df.select_dtypes(include=[np.number])
    outlier_results: list[OutlierStats] = []

    total_rows = len(df)

    for col in numeric_df.columns:
        series = numeric_df[col].dropna()

        if len(series) < 5:
            continue  # skip small samples

        q1 = np.percentile(series, 25)
        q3 = np.percentile(series, 75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        # mask to catch outliers
        mask = (series < lower) | (series > upper)
        count = int(mask.sum())
        percentage = count / total_rows if total_rows > 0 else 0

        outlier_results.append(
            OutlierStats(
                feature=col,
                lower_bound=float(lower),
                upper_bound=float(upper),
                outlier_count=int(count),
                outlier_percentage=float(percentage),
            )
        )
    outliers_data: OutliersData = OutliersData(
        features=outlier_results,
    )
    return OutliersChart(type="Outliers", data=outliers_data)


def build_feature_target_relationships(
    df: pd.DataFrame,
    target_column: str,
    max_bins: int = 10,
) -> list[DataChart]:
    charts: list[DataChart] = []

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    # Ensuring target is numeric for .mean() to work
    working_df = df.copy()
    if not pd.api.types.is_numeric_dtype(working_df[target_column]):
        # mask to catch 'yes'/'true'/'1'
        truthy_mask = (
            working_df[target_column].astype(str).str.lower().isin(["yes", "true", "1"])
        )
        # convert 'yes'/'true'/'1' as 1, others as 0
        working_df[target_column] = (truthy_mask).astype(int)

    # Remove target_column from features
    if target_column in numeric_cols:
        numeric_cols.remove(target_column)
    if target_column in categorical_cols:
        categorical_cols.remove(target_column)

    # -------------------------
    # NUMERIC FEATURES (BINNING)
    # -------------------------
    for col in numeric_cols:
        series = working_df[[col, target_column]].dropna()

        if series.empty:
            continue

        try:
            series["bin"] = pd.qcut(series[col], q=max_bins, duplicates="drop")
        except ValueError:
            continue  # not enough unique values

        grouped = series.groupby("bin")[target_column].mean()

        charts.append(
            FeatureTargetRelationshipChart(
                data=FeatureTargetRelationshipData(
                    feature=col,
                    bins_or_categories=grouped.index.astype(str).tolist(),
                    target_rate=grouped.values.astype(float).tolist(),
                ),
                meta=ChartMeta(title=f"{col} vs churn"),
            )
        )

    # -------------------------
    # CATEGORICAL FEATURES
    # -------------------------
    for col in categorical_cols:
        series = working_df[[col, target_column]].dropna()

        if series.empty:
            continue

        grouped = series.groupby(col)[target_column].mean()

        charts.append(
            FeatureTargetRelationshipChart(
                data=FeatureTargetRelationshipData(
                    feature=col,
                    bins_or_categories=grouped.index.astype(str).tolist(),
                    target_rate=grouped.values.astype(float).tolist(),
                ),
                meta=ChartMeta(title=f"{col} vs churn"),
            )
        )
    return charts


def build_feature_distributions(
    df: pd.DataFrame,
    max_bins: int = 10,
    top_k: int = 5,
) -> list[DataChart]:
    charts: list[DataChart] = []

    for col in df.columns:
        series = df[col].dropna()

        if series.empty:
            continue

        # -------------------------
        # NUMERIC FEATURES
        # -------------------------
        if pd.api.types.is_numeric_dtype(series):
            try:
                counts, bin_edges = np.histogram(series, bins=max_bins)

                labels = [
                    f"{round(bin_edges[i], 2)} - {round(bin_edges[i + 1], 2)}"
                    for i in range(len(bin_edges) - 1)
                ]

                charts.append(
                    FeatureDistributionChart(
                        data=FeatureDistributionData(
                            feature=col,
                            bins_or_categories=labels,
                            counts=counts.tolist(),
                        ),
                        meta=ChartMeta(title=f"{col} distribution"),
                    )
                )

            except Exception:
                continue

        # -------------------------
        # CATEGORICAL FEATURES
        # -------------------------
        else:
            value_counts = series.value_counts().head(top_k)

            charts.append(
                FeatureDistributionChart(
                    data=FeatureDistributionData(
                        feature=col,
                        bins_or_categories=value_counts.index.astype(str).tolist(),
                        counts=value_counts.values.astype(int).tolist(),
                    ),
                    meta=ChartMeta(title=f"{col} distribution"),
                )
            )

    return charts
