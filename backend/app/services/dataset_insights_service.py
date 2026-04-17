from pathlib import Path

import numpy as np
import pandas as pd

from app.core.security import UserDep
from app.models.datasets_model import Dataset
from app.schemas.dataset_insights_schema import (
    BoxPlotChart,
    CategoricalChart,
    CorrelationCell,
    CorrelationMatrixChart,
    CorrelationSeries,
    DataChart,
    DatasetSchemaChart,
    FeatureDistributionChart,
    FeatureSchema,
    FeatureTargetRelationshipChart,
    MissingValuesChart,
    OutliersChart,
    TargetDistributionChart,
    XYChart,
)
from app.utils.validator import read_churn_df


def get_dataset_charts(dataset: Dataset, user: UserDep) -> list[DataChart]:
    df = read_churn_df(Path(dataset.file_path))
    target_column = "Churn"

    # Core Dataset Insights
    dataset_charts: list[DataChart] = [
        build_schema(df),
        build_missing_values(df),
        build_target_distribution(df, target_column),
        build_correlation_matrix(df),
        build_outliers(df),
        build_feature_distributions(df),
        build_feature_target_relationships(df, target_column),
    ]

    return dataset_charts


def build_missing_values(df: pd.DataFrame) -> MissingValuesChart:
    missing_counts = df.isnull().sum()
    return MissingValuesChart(
        chart_type="missing_values",
        render_type="categorical",
        title="Missing Values per Feature",
        description="Count and percentage of null values found in each column.",
        x_axis="Features",
        y_axis="Missing Count",
        categories=missing_counts.index.tolist(),
        series=missing_counts.tolist(),
        percentages=df.isnull().mean().tolist(),
    )


def build_target_distribution(
    df: pd.DataFrame, target_column: str
) -> TargetDistributionChart:
    counts = df[target_column].value_counts(dropna=False)
    percentages = df[target_column].value_counts(normalize=True)

    return TargetDistributionChart(
        chart_type="target_distribution",
        render_type="categorical",
        title="Target Class Distribution",
        description=f"Balance of classes within the {target_column} column.",
        categories=counts.index.astype(str).tolist(),
        series=counts.tolist(),
        percentages=percentages.tolist(),
    )


def build_correlation_matrix(df: pd.DataFrame) -> CorrelationMatrixChart:
    numeric_df = df.drop("CustomerID", axis=1).select_dtypes(include=[np.number])
    corr = numeric_df.corr().fillna(0)
    cols = corr.columns.tolist()

    series_list = []
    for i, row_name in enumerate(cols):
        row_cells = [
            CorrelationCell(x=col_name, y=float(corr.iloc[i, j]))  # type: ignore
            for j, col_name in enumerate(cols)
        ]
        series_list.append(CorrelationSeries(name=row_name, data=row_cells))

    return CorrelationMatrixChart(
        chart_type="correlation_matrix",
        render_type="matrix",
        title="Feature Correlation Matrix",
        description="Pearson correlation coefficients between numeric features.",
        labels=cols,
        series=series_list,
    )


def build_schema(df: pd.DataFrame) -> DatasetSchemaChart:
    feature_list = [
        FeatureSchema(
            name=col,
            dtype=str(df[col].dtype),
            missing_count=int(df[col].isnull().sum()),
            unique_count=int(df[col].nunique()),
        )
        for col in df.columns
    ]
    return DatasetSchemaChart(
        chart_type="dataset_schema",
        render_type="table",
        title="Dataset Structural Schema",
        description="High-level overview of data types and uniqueness.",
        rows=feature_list,
    )


def build_outliers(df: pd.DataFrame) -> OutliersChart:
    numeric_df = df.select_dtypes(include=[np.number])
    outlier_results = []

    for col in numeric_df.columns:
        series = numeric_df[col].dropna()
        if len(series) < 5:
            continue

        q1, q3 = np.percentile(series, [25, 75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr

        mask = (series < lower) | (series > upper)
        count = int(mask.sum())

        outlier_results.append(
            BoxPlotChart(
                chart_type="boxplot",
                render_type="boxplot",
                title=col,
                series=[
                    float(lower),
                    float(q1),
                    float(series.median()),
                    float(q3),
                    float(upper),
                ],
            )
        )

    return OutliersChart(
        chart_type="outliers",
        render_type="composite",
        title="Numeric Outlier Detection",
        description="Features containing values outside 1.5x the Interquartile Range (IQR).",
        charts=outlier_results,
    )


def build_feature_target_relationships(
    df: pd.DataFrame, target_column: str
) -> DataChart:
    charts = []
    working_df = df.copy()

    # Ensure target is numeric (0/1) for averaging
    if not pd.api.types.is_numeric_dtype(working_df[target_column]):
        working_df[target_column] = (
            working_df[target_column]
            .astype(str)
            .str.lower()
            .isin(["yes", "true", "1"])
            .astype(int)
        )

    cols = [c for c in df.columns if c != target_column]
    for col in cols:
        series = working_df[[col, target_column]].dropna()
        if series.empty:
            continue

        # Bin numeric, group categorical
        if pd.api.types.is_numeric_dtype(series[col]):
            try:
                series["bin"] = pd.qcut(series[col], q=10, duplicates="drop")
                grouped = series.groupby("bin")[target_column].mean()
            except ValueError:
                continue
        else:
            grouped = series.groupby(col)[target_column].mean()

        charts.append(
            XYChart(
                chart_type="xy",
                render_type="categorical",
                title=f"Relationship: {col} vs {target_column}",
                x_axis=col,
                y_axis=f"Avg {target_column} Rate",
                series=grouped.values.astype(float).tolist(),
            )
        )
    return FeatureTargetRelationshipChart(
        chart_type="feature_target_relationship",
        render_type="composite",
        title="Feature Target Relationship",
        description="Relationship between numeric features and target variable.",
        charts=charts,
    )


def build_feature_distributions(df: pd.DataFrame) -> DataChart:
    charts = []
    for col in df.columns:
        series = df[col].dropna()
        if series.empty:
            continue

        if pd.api.types.is_numeric_dtype(series):
            counts, edges = np.histogram(series, bins=10)
            labels = [
                f"{edges[i]:.2f}-{edges[i + 1]:.2f}" for i in range(len(edges) - 1)
            ]
        else:
            vc = series.value_counts().head(10)
            labels, counts = vc.index.astype(str).tolist(), vc.values.tolist()

        charts.append(
            CategoricalChart(
                chart_type="feature_distribution",
                render_type="categorical",
                title=f"Distribution of {col}",
                x_axis=col,
                y_axis="Frequency",
                categories=labels,
                series=[int(c) for c in counts],
            )
        )
    return FeatureDistributionChart(
        chart_type="feature_distribution",
        render_type="composite",
        title="Feature Distributions",
        description="Distribution of numeric and categorical features.",
        charts=charts,
    )
