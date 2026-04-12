import uuid

from fastapi import (
    APIRouter,
    HTTPException,
    status,
)
from sqlmodel import select

from app.core.security import UserDep
from app.db.database import SessionDep
from app.models.datasets_model import Dataset
from app.models.metrics_model import DatasetMetrics, ModelMetrics
from app.models.models_model import Model
from app.schemas.dataset_insights_schema import DataChart
from app.schemas.model_insights_schema import ModelChart
from app.services.dataset_insights_service import get_dataset_charts
from app.services.model_insights_service import get_model_charts

router = APIRouter(prefix="/insights")


@router.get("/model/metrics/{model_id}", response_model=ModelMetrics)
def read_model_metrics(model_id: uuid.UUID, user: UserDep, session: SessionDep):
    # Verifying the model belongs to the user
    query = select(Model).where(Model.id == model_id, Model.user_id == user.id)
    model = session.exec(query).first()

    if not model:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Model not found or access denied"
        )

    metrics = session.get(ModelMetrics, model_id)
    return metrics


@router.get("/dataset/metrics/{dataset_id}", response_model=DatasetMetrics)
def read_dataset_metrics(dataset_id: uuid.UUID, user: UserDep, session: SessionDep):
    # Verifying the model belongs to the user
    query = select(Dataset).where(Dataset.id == dataset_id, Dataset.user_id == user.id)
    model = session.exec(query).first()

    if not model:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Dataset not found or access denied"
        )

    datasetMetrics = session.get(DatasetMetrics, dataset_id)
    return datasetMetrics


@router.get("/model/charts/{model_id}", response_model=list[ModelChart])
def read_model_charts(model_id: uuid.UUID, user: UserDep, session: SessionDep):
    # Verifying the model belongs to the user
    query = select(Model).where(Model.id == model_id, Model.user_id == user.id)
    model = session.exec(query).first()

    if not model:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Model not found or access denied"
        )

    query = select(Dataset).where(
        Dataset.id == model.dataset_id,
        Dataset.user_id == user.id,
    )
    dataset = session.exec(query).first()

    if not dataset:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Dataset not found or access denied"
        )

    return get_model_charts(dataset, model, user)


@router.get("/dataset/charts/{dataset_id}", response_model=list[DataChart])
def read_dataset_charts(dataset_id: uuid.UUID, user: UserDep, session: SessionDep):
    # Verifying the dataset belongs to the user
    query = select(Dataset).where(Dataset.id == dataset_id, Dataset.user_id == user.id)
    dataset = session.exec(query).first()

    if not dataset:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Dataset not found or access denied"
        )

    return get_dataset_charts(dataset, user)
