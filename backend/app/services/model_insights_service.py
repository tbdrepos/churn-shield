from pathlib import Path

import joblib
import loguru
import numpy as np
from sklearn.calibration import calibration_curve
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve

from app.core.security import UserDep
from app.models.datasets_model import Dataset
from app.models.models_model import Model
from app.schemas.model_insights_schema import (
    CalibrationCurveChart,
    CalibrationSeries,
    ConfusionMatrixChart,
    ConfusionMatrixData,
    ConfusionMatrixSeries,
    FeatureImportanceChart,
    FeatureImportanceSeries,
    ModelChart,
    PredictionDistributionChart,
    RocCurveChart,
    RocData,
    RocSeries,
)
from app.services.train_service import prepare_data

loguru.logger.add("logs/model_insights_service.log", rotation="10 MB", level="INFO")
logger = loguru.logger


def safe_list(arr):
    """Ensures numpy arrays are JSON serializable and handle NaNs."""
    return np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0).tolist()


def get_model_charts(dataset: Dataset, model: Model, user: UserDep) -> list[ModelChart]:
    try:
        _, X_test, _, y_test = prepare_data(Path(dataset.file_path))
        model_pipeline = joblib.load(Path(model.file_path))
        trained_model = model_pipeline.steps[-1][1]
        features_names = model_pipeline[:-1].get_feature_names_out()

        y_pred = model_pipeline.predict(X_test)

        probs = model_pipeline.predict_proba(X_test)
        # Defaulting to the positive class for binary
        y_prob = probs[:, 1] if probs.shape[1] == 2 else probs.max(axis=1)

        return [
            build_feature_importance(trained_model, features_names),
            build_prediction_distribution(y_pred),
            build_confusion_matrix(y_test, y_pred),
            build_roc_curve(y_test, y_prob),
            build_calibration_curve(y_test, y_prob),
        ]
    except Exception as e:
        logger.exception(e)
        raise


def build_feature_importance(model, features_names) -> FeatureImportanceChart:
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = (
            np.mean(np.abs(model.coef_), axis=0)
            if model.coef_.ndim > 1
            else np.abs(model.coef_)
        )
    else:
        raise ValueError(f"Cannot determine importance for model type: {type(model)}")

    indices = np.argsort(importances)[::-1]

    return FeatureImportanceChart(
        title="Feature Importance",
        description="Relative importance of features based on model weights or impurity reduction.",
        x_axis="Importance Score",
        y_axis="Features",
        categories=[str(features_names[i]) for i in indices][:5],
        series=[
            FeatureImportanceSeries(
                name="Importance", data=(safe_list(importances[indices])[:5])
            )
        ],
    )


def build_prediction_distribution(y_pred) -> PredictionDistributionChart:
    classes, counts = np.unique(y_pred, return_counts=True)
    # Ensure classes are strings for the categories field
    str_classes = ["Churned" if c == 1 else "Not Churned" for c in classes]

    return PredictionDistributionChart(
        title="Prediction Distribution",
        description="Frequency of each class predicted by the model.",
        x_axis="Class",
        y_axis="Count",
        categories=str_classes,
        series=[int(c) for c in counts],
    )


def build_roc_curve(y_true, y_prob) -> RocCurveChart:
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    auc_score = float(roc_auc_score(y_true, y_prob))

    # Constructing list of RocData objects
    roc_points = [RocData(x=float(f), y=float(t)) for f, t in zip(fpr, tpr)]

    return RocCurveChart(
        title="ROC Curve",
        description="Trade-off between True Positive Rate and False Positive Rate.",
        x_axis="False Positive Rate",
        y_axis="True Positive Rate",
        auc=auc_score,
        series=[RocSeries(name="Model Performance", data=roc_points)],
    )


def build_confusion_matrix(y_true, y_pred) -> ConfusionMatrixChart:
    # Map numeric labels 1->"Churned", 0->"Not churned"
    label_map = {1: "Churned", 0: "Not churned"}
    labels = [0, 1]  # ensure consistent ordering: 0 then 1
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    with np.errstate(divide="ignore", invalid="ignore"):
        normalized = cm / cm.sum(axis=1, keepdims=True)
        normalized = np.nan_to_num(normalized)

    series_list = []
    str_labels = [label_map[l] for l in labels]

    for i, label in enumerate(str_labels):
        row_data = []
        for j, pred_label in enumerate(str_labels):
            row_data.append(
                ConfusionMatrixData(
                    x=pred_label, y=float(normalized[i][j]), count=int(cm[i][j])
                )
            )
        series_list.append(ConfusionMatrixSeries(name=label, data=row_data))

    return ConfusionMatrixChart(
        title="Confusion Matrix",
        description="Actual vs. Predicted class comparison.",
        labels=str_labels,
        series=series_list,
    )


def build_calibration_curve(y_true, y_prob) -> CalibrationCurveChart:
    frac_pos, mean_pred = calibration_curve(y_true, y_prob, n_bins=10)

    # Schema expects list[list[float]] in format [[pred, true], ...]
    combined_data = [
        [float(pred), float(true)] for pred, true in zip(mean_pred, frac_pos)
    ]

    return CalibrationCurveChart(
        title="Calibration Curve",
        description="Reliability diagram comparing predicted probabilities to actual outcomes.",
        x_axis="Mean Predicted Probability",
        y_axis="Fraction of Positives",
        series=[CalibrationSeries(name="Model Calibration", data=combined_data)],
    )
