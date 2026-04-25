import collections
from pathlib import Path

import joblib
import pandas as pd
import shap
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from app.schemas.predict_schema import FeatureImpact, PredictRequest, PredictResponse
from app.utils.formatter import map_to_original_feature
from app.utils.validator import read_churn_df

# Assuming you have a schema for settings
# from app.schemas.settings_schema import UserSettings


def prepare_data(dataset_path: Path, target: str = "Churn"):
    df = read_churn_df(dataset_path)

    X = df.drop(target, axis=1)
    y = df[target].map({"Yes": 1, "No": 0})

    return train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=0,
        stratify=y,
    )


def get_shap_values(model: Pipeline, X_train: pd.DataFrame, input_row: pd.DataFrame):
    preprocessor = model.named_steps["preprocessor"]

    X_train_transformed = preprocessor.transform(X_train)
    input_row_transformed = preprocessor.transform(input_row)

    classifier = model.named_steps["classifier"]

    # SHAP Explainer using the transformed background data
    explainer = shap.Explainer(classifier.predict_proba, X_train_transformed)
    shap_values = explainer(input_row_transformed)

    return shap_values


def extract_top_features(shap_values, input_row, feature_names, top_k: int):
    """
    Refactored to use dynamic top_k
    """
    # Handle classification shape (n_samples, n_features, n_classes)
    if len(shap_values.values.shape) == 3:
        # We focus on the 'Churn = Yes' class (index 1)
        values = shap_values.values[0, :, 1]
    else:
        values = shap_values.values[0]

    feature_impact_map = collections.defaultdict(float)

    # Aggregate SHAP values back to original feature names
    for i, val in enumerate(values):
        original_feature = map_to_original_feature(feature_names[i])
        feature_impact_map[original_feature] += float(val)

    impacts = []
    for feature, impact in feature_impact_map.items():
        # Get the value from the original input row for display
        value = input_row.iloc[0][feature]

        impacts.append(
            {
                "feature": feature,
                "value": value,
                "impact": impact,
            }
        )

    # Sort by absolute magnitude to find most influential features
    impacts.sort(key=lambda x: abs(x["impact"]), reverse=True)
    return impacts[:top_k]


def classify_impact(value: float):
    # Thresholds for labeling can also eventually be moved to settings if needed
    if value > 0.05:
        return "High Risk"
    elif value > 0.01:
        return "Medium Risk"
    elif value < -0.05:
        return "Low Risk"
    else:
        return "Neutral"


def build_feature_impact_response(top_features) -> list[FeatureImpact]:
    result: list[FeatureImpact] = []

    for feature in top_features:
        result.append(
            FeatureImpact(
                feature=feature["feature"],
                value=feature["value"],
                impact_score=feature["impact"],
                impact_label=classify_impact(feature["impact"]),
                direction="increase" if feature["impact"] > 0 else "decrease",
            )
        )

    return result


def predict_probabilities(
    predict_request: PredictRequest,
    model_path: Path,
    dataset_path: Path,
    churn_threshold: float = 0.5,  # Defaulted to 0.5 if not provided
    show_top_n_features: int = 5,  # Defaulted to 5 if not provided
) -> PredictResponse:
    """
    Main entry point for prediction.
    Now respects user-defined threshold and feature count.
    """
    model_pipeline: Pipeline = joblib.load(model_path)

    # Convert incoming request to DataFrame
    input_row = pd.DataFrame([predict_request.model_dump()])

    # Calculate Probabilities
    # [0, 1] is the probability of class 1 (Churn=Yes)
    churn_probability = float(model_pipeline.predict_proba(input_row)[0, 1])

    # APPLY DYNAMIC THRESHOLD
    churn_prediction = "Yes" if churn_probability >= churn_threshold else "No"

    # Explainability Logic
    X_train, _, _, _ = prepare_data(dataset_path)
    shap_values = get_shap_values(model_pipeline, X_train, input_row)

    preprocessor = model_pipeline.named_steps["preprocessor"]
    transformed_names = preprocessor.get_feature_names_out()

    # APPLY DYNAMIC TOP_N
    top_features = extract_top_features(
        shap_values, input_row, transformed_names, top_k=show_top_n_features
    )

    feature_impact = build_feature_impact_response(top_features)

    return PredictResponse(
        prediction=churn_prediction,
        probability=round(churn_probability, 2),
        feature_impact=feature_impact,
    )
