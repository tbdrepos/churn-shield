import uuid
from pathlib import Path

import joblib
import pandas as pd
from fastapi import HTTPException
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from app.core.config import get_settings
from app.db.database import SessionDep
from app.models.models import Model
from app.models.user import User
from app.services.preprocessing import get_pipeline

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


def train_model(
    session: SessionDep,
    DATA_PATH: Path,
    user_id: str,
    dataset_id: str,
    target: str = "Churn",
):
    # DATA_PATH = app/data/{user_id}
    DATASET_PATH = DATA_PATH / "datasets" / f"{dataset_id}.csv"
    df = pd.read_csv(DATASET_PATH)
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
    store_model(session, model_pipeline, user_id, dataset_id, DATA_PATH)
    # return model metrics
    y_pred = model_pipeline.predict(X_test)
    return {
        "accuracy_score": accuracy_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred, pos_label="Yes"),
        "precision_score": precision_score(y_test, y_pred, pos_label="Yes"),
        "recall_score": recall_score(y_test, y_pred, pos_label="Yes"),
    }
