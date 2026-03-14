from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, status

from app.core.security import UserDep
from app.db.database import SessionDep
from app.models.metrics import Metrics
from app.models.models import Model
from app.services.prediction import predict_probabilities
from app.services.train import train_model

router = APIRouter(prefix="/model")


@router.get("/train")
def model_training(dataset_id: str, user: UserDep, session: SessionDep):
    user_id = str(user.id)
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    # path for the user's data folder
    DATA_PATH = BASE_DIR / "data" / str(user_id)
    return train_model(session, DATA_PATH, user_id, dataset_id)


@router.get("/train/metrics")
def get_training_metrics(user: UserDep, session: SessionDep):
    active_model_id = user.active_model
    if not active_model_id:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="User doesn't have a trained model set"
        )
    return session.get(Metrics, active_model_id)


@router.post("/predict")
def get_prediction(file: UploadFile, user: UserDep, session: SessionDep):
    active_model = session.get(Model, user.active_model)
    if not active_model:
        raise HTTPException(
            409,
            "No trained model available. Train a model before requesting predictions.",
        )
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    FILE_PATH = (
        BASE_DIR / "data" / str(user.id) / "models" / f"{str(active_model.id)}.joblib"
    )
    return predict_probabilities(file, FILE_PATH, session)
