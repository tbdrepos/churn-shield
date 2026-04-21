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


def get_shap_values(model, X_train, input_row):
    preprocessor = model.named_steps["preprocessor"]

    X_train_transformed = preprocessor.transform(X_train)
    input_row_transformed = preprocessor.transform(input_row)

    classifier = model.named_steps["classifier"]
    explainer = shap.Explainer(classifier.predict_proba, X_train_transformed)

    shap_values = explainer(input_row_transformed)

    return shap_values


def extract_top_features(shap_values, input_row, feature_names, top_k=5):

    # Handle classification shape
    if len(shap_values.values.shape) == 3:
        values = shap_values.values[0, :, 1]
    else:
        values = shap_values.values[0]

    feature_impact_map = collections.defaultdict(float)

    # Aggregate SHAP values by original feature
    for i, val in enumerate(values):
        original_feature = map_to_original_feature(feature_names[i])
        feature_impact_map[original_feature] += float(val)

    impacts = []

    for feature, impact in feature_impact_map.items():
        value = input_row.iloc[0][feature]

        impacts.append(
            {
                "feature": feature,
                "value": value,
                "impact": impact,
            }
        )

    impacts.sort(key=lambda x: abs(x["impact"]), reverse=True)
    return impacts[:top_k]


def classify_impact(value: float):
    if value > 0.05:
        return "High Risk"
    elif value > 0.01:
        return "Medium Risk"
    elif value < -0.05:
        return "Low Risk"
    else:
        return "Neutral"


def build_feature_impact_response(top_features):
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
    predictRequest: PredictRequest,
    MODEL_PATH: Path,
    DATASET_PATH: Path,
):
    model_pipeline: Pipeline = joblib.load(MODEL_PATH)

    input_row = pd.DataFrame([predictRequest.model_dump()])
    churn_probability = float(model_pipeline.predict_proba(input_row)[0, 1])
    churn_prediction = "Yes" if churn_probability > 0.5 else "No"

    X_train, _, _, _ = prepare_data(DATASET_PATH)
    shap_values = get_shap_values(model_pipeline, X_train, input_row)

    preprocessor = model_pipeline.named_steps["preprocessor"]
    transformed_names = preprocessor.get_feature_names_out()

    top_features = extract_top_features(shap_values, input_row, transformed_names)

    feature_impact = build_feature_impact_response(top_features)
    return PredictResponse(
        prediction=churn_prediction,
        probability=round(churn_probability, 2),
        feature_impact=feature_impact,
    )
