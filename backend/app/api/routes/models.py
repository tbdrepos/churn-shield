import uuid
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, HTTPException, UploadFile, status
from sqlmodel import select

from app.core.security import UserDep
from app.db.database import SessionDep
from app.models.datasets_model import Dataset
from app.models.models_model import Model
from app.services.prediction_service import predict_probabilities
from app.services.train_service import train_model

router = APIRouter(prefix="/models")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_ROOT = BASE_DIR / "data"


@router.post("/train/{dataset_id}", status_code=status.HTTP_202_ACCEPTED)
def model_training(
    dataset_id: uuid.UUID,
    user: UserDep,
    session: SessionDep,
    background_tasks: BackgroundTasks,
):
    query = select(Dataset).where(Dataset.id == dataset_id, Dataset.user_id == user.id)
    dataset = session.exec(query).first()

    if not dataset:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Dataset not found")

    user_id_str = str(user.id)
    user_data_path = DATA_ROOT / user_id_str

    background_tasks.add_task(
        train_model, session, user_data_path, user_id_str, str(dataset_id)
    )

    return {"message": "Training started in the background"}


@router.get("/trained/all", response_model=list[Model])
def get_all_models(user: UserDep, session: SessionDep):
    query = select(Model).where(Model.user_id == user.id)
    models = session.exec(query).all()
    return models


@router.get("/trained/{dataset_id}", response_model=list[Model])
def get_dataset_models(dataset_id: uuid.UUID, user: UserDep, session: SessionDep):
    query = select(Model).where(
        Model.user_id == user.id, Model.dataset_id == dataset_id
    )
    models = session.exec(query).all()
    return models


@router.get("/active")
def get_active_model(user: UserDep, session: SessionDep) -> Model | None:
    if not user.active_model:
        return None
    return session.get(Model, user.active_model)


@router.delete("/{model_id}")
def delete_model(model_id: uuid.UUID, user: UserDep, session: SessionDep):
    # Verifying the model belongs to the user
    query = select(Model).where(Model.id == model_id, Model.user_id == user.id)
    model = session.exec(query).first()

    if not model:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Model not found or access denied"
        )

    session.delete(model)
    session.commit()
    return {"ok": True}


@router.post("/predict")
async def get_prediction(file: UploadFile, user: UserDep, session: SessionDep):
    if not user.active_model:
        raise HTTPException(409, detail="No active model set for predictions.")

    active_model = session.get(Model, user.active_model)

    if not active_model or active_model.user_id != user.id:
        raise HTTPException(404, detail="Active model not found")

    file_path = DATA_ROOT / str(user.id) / "models" / f"{active_model.id}.joblib"

    if not file_path.exists():
        raise HTTPException(404, detail="Model file missing from storage")

    return predict_probabilities(file, file_path, session)
