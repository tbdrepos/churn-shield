import os
import shutil
import uuid

import pandas as pd
from fastapi import (
    APIRouter,
    BackgroundTasks,
    File,
    HTTPException,
    Response,
    UploadFile,
    status,
)
from loguru import logger
from pandera.errors import SchemaError
from sqlmodel import select

from app.core.security import UserDep
from app.db.database import SessionDep
from app.models.datasets_model import Dataset, DatasetRead
from app.models.metrics_model import Metrics
from app.models.models_model import Model
from app.services.insights_service import *
from app.utils.validator import churn_schema

router = APIRouter(prefix="/insights")


@router.get("/metrics/active", response_model=Metrics)
def get_active_metrics(user: UserDep, session: SessionDep):
    if not user.active_model:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No active model set")

    # Ensure the model actually exists and belongs to the user
    metrics = session.get(Metrics, user.active_model)
    if not metrics:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Metrics not found")

    return metrics


@router.get("/metrics/{model_id}", response_model=Metrics)
def get_specific_metrics(model_id: uuid.UUID, user: UserDep, session: SessionDep):
    # Verifying the model belongs to the user
    query = select(Model).where(Model.id == model_id, Model.user_id == user.id)
    model = session.exec(query).first()

    if not model:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Model not found or access denied"
        )

    metrics = session.get(Metrics, model_id)
    return metrics
