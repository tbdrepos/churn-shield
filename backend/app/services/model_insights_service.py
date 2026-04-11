from pathlib import Path

import joblib
import numpy as np
from sklearn.calibration import calibration_curve
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve

from app.core.security import UserDep
from app.models.datasets_model import Dataset
from app.models.models_model import Model
from app.schemas.model_insights_schema import (
    CalibrationCurveChart,
    CalibrationCurveData,
    ConfusionMatrixChart,
    ConfusionMatrixData,
    FeatureImportanceChart,
    FeatureImportanceData,
    ModelChart,
    PredictionDistributionChart,
    PredictionDistributionData,
    RocCurveChart,
    RocCurveData,
    RocMeta,
)
from app.services.train_service import prepare_data


def get_model_charts(dataset: Dataset, model: Model, user: UserDep) -> list[ModelChart]:
    _, X_test, _, y_test = prepare_data(Path(dataset.file_path))

    model_pipeline = joblib.load(Path(model.file_path))

    trained_model = model_pipeline.steps[-1][1]

    # Fallback for feature names
    if hasattr(trained_model, "feature_names_in_"):
        features_names = trained_model.feature_names_in_
    elif hasattr(X_test, "columns"):
        features_names = X_test.columns.tolist()
    else:
        features_names = [f"feature_{i}" for i in range(X_test.shape[1])]

    y_pred = model_pipeline.predict(X_test)

    probas = model_pipeline.predict_proba(X_test)
    # Defaulting to the positive class for binary
    y_proba = probas[:, 1] if probas.shape[1] == 2 else probas.max(axis=1)

    return [
        build_feature_importance(trained_model, features_names),
        build_prediction_distribution(y_pred),
        build_confusion_matrix(y_test, y_pred),
        build_roc_curve(y_test, y_proba),
        build_calibration_curve(y_test, y_proba),
    ]


def build_feature_importance(model, features_names) -> ModelChart:
    """
    Extracts feature importance from ANY fitted scikit-learn model.
    """
    # 1. Check for Tree-based importance (MDI)
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_

    # 2. Check for Linear coefficients
    elif hasattr(model, "coef_"):
        # For multiclass, average absolute coefficients across classes
        if model.coef_.ndim > 1:
            importances = np.mean(np.abs(model.coef_), axis=0)
        else:
            importances = np.abs(model.coef_)

    # 3. Raise error if no importance found
    else:
        raise ValueError(
            "Cannot determine feature importance for model type: %s" % type(model)
        )
    indices = np.argsort(importances)[::-1]
    return FeatureImportanceChart(
        data=FeatureImportanceData(
            features=[features_names[i] for i in indices],
            importances=importances[indices].tolist(),
        ),
    )


def build_prediction_distribution(y_pred) -> ModelChart:
    """
    Extracts prediction distribution.
    """
    classes, counts = np.unique(y_pred, return_counts=True)
    total = counts.sum()
    percentages = (counts / total).tolist()

    return PredictionDistributionChart(
        data=PredictionDistributionData(
            classes=classes.tolist(),
            counts=counts.tolist(),
            percentages=percentages,
        ),
    )


def build_roc_curve(y_true, y_proba) -> ModelChart:
    """
    Extracts ROC curve data.
    """

    fpr, tpr, thresholds = roc_curve(y_true, y_proba)
    auc = roc_auc_score(y_true, y_proba)

    return RocCurveChart(
        data=RocCurveData(
            fpr=fpr.tolist(), tpr=tpr.tolist(), thresholds=thresholds.tolist()
        ),
        meta=RocMeta(auc=float(auc)),
    )


def build_confusion_matrix(y_true, y_pred) -> ModelChart:
    """
    Extracts confusion matrix.
    """

    labels = np.unique(y_true)

    cm = confusion_matrix(y_true, y_pred, labels=labels)

    with np.errstate(divide="ignore", invalid="ignore"):
        normalized = cm / cm.sum(axis=1, keepdims=True)
        normalized = np.nan_to_num(normalized)  # Convert NaNs to 0

    return ConfusionMatrixChart(
        data=ConfusionMatrixData(
            matrix=cm.tolist(),
            normalized_matrix=normalized.tolist(),
            labels=labels.tolist(),
            predicted_labels=labels.tolist(),
        ),
    )


def build_calibration_curve(y_true, y_proba) -> ModelChart:
    """
    Extracts calibration curve.
    """

    frac_pos, mean_pred = calibration_curve(y_true, y_proba, n_bins=10)

    return CalibrationCurveChart(
        data=CalibrationCurveData(
            mean_predicted_value=mean_pred.tolist(),
            fraction_of_positives=frac_pos.tolist(),
        ),
    )
