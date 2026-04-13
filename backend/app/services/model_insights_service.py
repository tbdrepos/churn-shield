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

loguru.logger.add("logs/model_insights_service.log", rotation="10 MB", level="INFO")
logger = loguru.logger


def safe_list(arr):
    return np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0).tolist()


def get_model_charts(dataset: Dataset, model: Model, user: UserDep) -> list[ModelChart]:
    try:
        _, X_test, _, y_test = prepare_data(Path(dataset.file_path))

        model_pipeline = joblib.load(Path(model.file_path))

        trained_model = model_pipeline.steps[-1][1]

        features_names = model_pipeline[:-1].get_feature_names_out()

        y_pred = model_pipeline.predict(X_test)
        y_pred_labeled = ["Yes" if target == 1 else "No" for target in y_pred]

        probas = model_pipeline.predict_proba(X_test)
        # Defaulting to the positive class for binary
        y_proba = probas[:, 1] if probas.shape[1] == 2 else probas.max(axis=1)
        y_test_labeled = ["Yes" if target == 1 else "No" for target in y_test]

        return [
            build_feature_importance(trained_model, features_names),
            build_prediction_distribution(y_pred_labeled),
            build_confusion_matrix(y_test_labeled, y_pred),
            build_roc_curve(y_test, y_proba),
            build_calibration_curve(y_test, y_proba),
        ]
    except Exception as e:
        logger.exception(e)
        raise


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
    importances = np.nan_to_num(importances)
    indices = np.argsort(importances)[::-1]

    return FeatureImportanceChart(
        data=FeatureImportanceData(
            features=[features_names[i] for i in indices],
            importances=safe_list(importances[indices]),
        ),
    )


def build_prediction_distribution(y_pred) -> ModelChart:
    """
    Extracts prediction distribution.
    """
    classes, counts = np.unique(y_pred, return_counts=True)
    # labeled_classes = ["Yes" if target == 1 else "No" for target in classes]
    total = counts.sum()
    percentages = safe_list(counts / total)

    return PredictionDistributionChart(
        data=PredictionDistributionData(
            classes=safe_list(classes),
            counts=safe_list(counts),
            percentages=percentages,
        ),
    )


def build_roc_curve(y_true, y_proba) -> ModelChart:
    """
    Extracts ROC curve data.
    """
    fpr, tpr, thresholds = roc_curve(y_true, y_proba)

    # 🔧 Remove inf threshold (first element)
    thresholds = thresholds[1:]
    fpr = fpr[1:]
    tpr = tpr[1:]

    auc = roc_auc_score(y_true, y_proba)

    return RocCurveChart(
        data=RocCurveData(
            fpr=safe_list(fpr),
            tpr=safe_list(tpr),
            thresholds=safe_list(thresholds),
        ),
        meta=RocMeta(auc=float(np.nan_to_num(auc))),
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
            matrix=safe_list(cm),
            normalized_matrix=safe_list(normalized),
            labels=safe_list(labels),
            predicted_labels=safe_list(labels),
        ),
    )


def build_calibration_curve(y_true, y_proba) -> ModelChart:
    """
    Extracts calibration curve.
    """

    frac_pos, mean_pred = calibration_curve(y_true, y_proba, n_bins=10)

    frac_pos = np.nan_to_num(frac_pos)
    mean_pred = np.nan_to_num(mean_pred)

    return CalibrationCurveChart(
        data=CalibrationCurveData(
            mean_predicted_value=safe_list(mean_pred),
            fraction_of_positives=safe_list(frac_pos),
        ),
    )
