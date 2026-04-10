import uuid
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
from fastapi import HTTPException
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sqlmodel import func, select

from app.core.config import get_settings
from app.db.database import SessionDep
from app.models.datasets_model import Dataset, DatasetStatus
from app.models.metrics_model import ModelMetrics
from app.models.models_model import Model, ModelStatus
from app.models.user_model import User
from app.services.preprocessing_service import get_pipeline
from app.utils.validator import prediction_schema

settings = get_settings()


def generate_model_name(dataset_name: str, model_type: str, model_count: int):
    model_name = f"{dataset_name[:-4]}_{model_type}_v{model_count + 1}"
    return model_name


def prepare_data(dataset_path: Path, target: str):
    df = pd.read_csv(
        dataset_path,
        na_values=[
            " ",
            "#N/A",
            "#N/A N/A",
            "#NA",
            "-1.#IND",
            "-1.#QNAN",
            "-NaN",
            "-nan",
            "1.#IND",
            "1.#QNAN",
            "",
            "N/A",
            "NA",
            "NULL",
            "NaN",
            "n/a",
            "nan",
            "null ",
        ],
        keep_default_na=False,
    )

    if target not in df.columns:
        raise HTTPException(400, f"Target column '{target}' not found")

    try:
        prediction_schema.validate(df)
    except Exception as e:
        raise HTTPException(400, f"Invalid dataset: {str(e)}")

    X = df.drop(target, axis=1)
    y = df[target]

    try:
        return train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=0,
            stratify=y,
        )
    except Exception as e:
        raise HTTPException(400, f"Invalid dataset: {str(e)}")


def train_pipeline(X_train, y_train) -> Pipeline:
    pipeline = get_pipeline()
    pipeline.fit(X_train, y_train)
    return pipeline


def evaluate_model(model: Pipeline, X_test, y_test) -> dict:
    y_pred = model.predict(X_test)
    pos_label = "Yes" if "Yes" in y_test.unique() else y_test.unique()[0]
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred, pos_label=pos_label),
        "precision": precision_score(y_test, y_pred, pos_label=pos_label),
        "recall": recall_score(y_test, y_pred, pos_label=pos_label),
    }

    if hasattr(model, "predict_proba"):
        try:
            y_proba = model.predict_proba(X_test)[:, 1]
            y_encoded = [1 if val == pos_label else 0 for val in y_test]
            metrics["roc_auc"] = roc_auc_score(
                y_encoded,
                y_proba,
            )
        except Exception:
            metrics["roc_auc"] = None

    return metrics


def persist_training_results(
    session: SessionDep,
    model: Pipeline,
    user_uuid: uuid.UUID,
    dataset_uuid: uuid.UUID,
    model_uuid: uuid.UUID,
    data_path: Path,
    metrics: dict,
):

    dataset = session.get(Dataset, dataset_uuid)
    if not dataset:
        raise HTTPException(404, "Dataset not found")

    # save model to disk
    model_path = data_path / "models" / f"{model_uuid}.joblib"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)

    # create model record
    model_query = (
        select(func.count())
        .select_from(Model)
        .where(Model.user_id == user_uuid, Model.dataset_id == dataset_uuid)
    )
    model_count = session.exec(model_query).one()
    model_record = Model(
        id=model_uuid,
        name=generate_model_name(
            dataset.original_name, model.steps[-1][1].__class__.__name__, model_count
        ),
        user_id=user_uuid,
        dataset_id=dataset_uuid,
        dataset_name=dataset.original_name,
        file_path=str(model_path),
        accuracy=metrics["accuracy"],
        status=ModelStatus.training,
    )
    session.add(model_record)
    session.flush()

    # save metrics
    model_metrics = ModelMetrics(
        model_id=model_record.id,
        dataset_id=dataset_uuid,
        **metrics,
    )
    session.add(model_metrics)

    # update user active model
    user = session.get(User, user_uuid)
    if not user:
        raise HTTPException(404, "User not found")

    user.active_model = model_record.id
    session.add(user)

    # update dataset and model status
    dataset.status = DatasetStatus.trained
    model_record.status = ModelStatus.trained
    session.add(dataset)
    session.add(model_record)

    session.commit()

    return model_metrics


def train_model(
    session: SessionDep,
    data_path: Path,
    user_id: str,
    dataset_id: str,
    target: str = "Churn",
) -> ModelMetrics | None:
    try:
        dataset_uuid = uuid.UUID(dataset_id)
    except ValueError:
        raise HTTPException(400, "Invalid dataset id")

    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(400, "Invalid user id")

    dataset = session.get(Dataset, dataset_uuid)
    model_uuid = uuid.uuid4()

    if not dataset:
        raise HTTPException(404, "Dataset not found")

    try:
        # mark as training
        dataset.sqlmodel_update({"status": DatasetStatus.training})
        session.add(dataset)
        session.commit()

        X_train, X_test, y_train, y_test = prepare_data(Path(dataset.file_path), target)

        model = train_pipeline(X_train, y_train)

        metrics_dict = evaluate_model(model, X_test, y_test)

        metrics: ModelMetrics = persist_training_results(
            session,
            model,
            user_uuid,
            dataset_uuid,
            model_uuid,
            data_path,
            metrics_dict,
        )

        return metrics

    except Exception as e:
        session.rollback()

        dataset = session.get(Dataset, dataset_uuid)
        model = session.get(Model, model_uuid)
        if dataset:
            dataset.status = DatasetStatus.failed
            session.add(dataset)

        if model:
            model.status = ModelStatus.failed
            session.add(model)

        session.commit()

        print(f"Training failed: {str(e)}")
        return
