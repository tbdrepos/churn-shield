import uuid
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

from app.core.config import get_settings
from app.db.database import SessionDep
from app.models.metrics import Metrics
from app.models.models import Model
from app.models.user import User
from app.services.preprocessing import get_pipeline
from app.utils.validator import prediction_schema

settings = get_settings()


def store_model(
    session: SessionDep,
    model_pipeline: Pipeline,
    user_id: str,
    dataset_id: str,
    DATA_PATH: Path,
):
    # store model metadata to db
    model_metadata = Model(user_id=uuid.UUID(user_id), dataset_id=uuid.UUID(dataset_id))
    session.add(model_metadata)
    session.commit()
    session.refresh(model_metadata)
    # update user row with new active model
    user_db = session.get(User, uuid.UUID(user_id))
    if not user_db:
        raise HTTPException(status_code=404, detail="user not found")
    user_db.sqlmodel_update({"active_model": model_metadata.id})
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    # store trained model to disk
    MODEL_PATH = DATA_PATH / "models" / f"{str(model_metadata.id)}.joblib"
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)  # make sure the folder exists
    joblib.dump(model_pipeline, MODEL_PATH)
    return model_metadata.id


def train_model(
    session: SessionDep,
    DATA_PATH: Path,
    user_id: str,
    dataset_id: str,
    target: str = "Churn",
):
    # DATA_PATH = app/data/{user_id}
    DATASET_PATH = DATA_PATH / "datasets" / f"{dataset_id}.csv"
    df = pd.read_csv(
        DATASET_PATH,
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
    prediction_schema.validate(df)
    # divide the dataset
    X = df.drop(target, axis=1)
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0, stratify=y
    )
    # train the model
    model_pipeline = get_pipeline()
    model_pipeline.fit(X_train, y_train)
    # store model
    model_id = store_model(session, model_pipeline, user_id, dataset_id, DATA_PATH)
    # store model metrics
    y_pred = model_pipeline.predict(X_test)
    y_proba = model_pipeline.predict_proba(X_test)[:, 1]
    metrics_dict = {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred, pos_label="Yes"),
        "precision": precision_score(y_test, y_pred, pos_label="Yes"),
        "recall": recall_score(y_test, y_pred, pos_label="Yes"),
        "roc_auc": roc_auc_score(
            [1 if val == "Yes" else 0 for val in y_test],
            y_proba,
        ),
    }
    model_metrics = Metrics(
        model_id=model_id, dataset_id=uuid.UUID(dataset_id), **metrics_dict
    )
    session.add(model_metrics)
    session.commit()
    session.refresh(model_metrics)
    return metrics_dict
