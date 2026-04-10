from fastapi import APIRouter

from app.core.security import UserDep
from app.db.database import SessionDep
from app.models.datasets_model import Dataset
from app.models.models_model import Model
from app.schemas.dashboard_schema import Kpi
from app.services.dashboard_service import (
    get_kpi,
    get_recent_activity,
    get_recent_datasets,
    get_recent_models,
)

router = APIRouter(prefix="/dashboard")


@router.get("/summary", response_model=Kpi)
def read_kpi_summary(user: UserDep, session: SessionDep):
    """Retrieve top-level KPI metrics for the dashboard."""
    return get_kpi(user, session)


@router.get("/summary/activity", response_model=list[str])
def read_recent_activity(user: UserDep, session: SessionDep):
    """Retrieve the latest mixed activity (Models and Datasets)."""
    return get_recent_activity(user, session)


@router.get("/summary/datasets", response_model=list[Dataset])
def read_recent_datasets(user: UserDep, session: SessionDep):
    """Retrieve the most recently uploaded datasets."""
    return get_recent_datasets(user, session)


@router.get("/summary/models", response_model=list[Model])
def read_recent_models(user: UserDep, session: SessionDep):
    """Retrieve the most recently trained models."""
    return get_recent_models(user, session)
