from pathlib import Path

import joblib
import pandas as pd
from fastapi import UploadFile
from sklearn.pipeline import Pipeline

from app.db.database import SessionDep


def predict_probabilities(file: UploadFile, FILE_PATH: Path, session: SessionDep):
    df = pd.read_csv(file.file)
    model_pipeline: Pipeline = joblib.load(FILE_PATH)
    positive_probas = model_pipeline.predict_proba(df)[:, 1]
    df["ChurnProbability"] = positive_probas
    return df.to_dict(orient="records")
