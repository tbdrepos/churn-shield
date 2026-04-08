import logging
import uuid

from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError  # Added for specific DB error handling
from sqlmodel import col, func, select

from app.core.security import UserDep
from app.db.database import SessionDep
from app.models.datasets_model import Dataset
from app.models.models_model import Model

# Initialize logging
logger = logging.getLogger(__name__)


class Kpi(BaseModel):
    dataset_count: int
    model_count: int
    highest_accuracy: float
    active_model: str | None


def get_kpi(user: UserDep, session: SessionDep):
    try:
        # 1. Get Dataset Count
        dataset_query = (
            select(func.count()).select_from(Dataset).where(Dataset.user_id == user.id)
        )
        dataset_count = session.exec(dataset_query).one()

        # 2. Get Model Count
        model_query = (
            select(func.count()).select_from(Model).where(Model.user_id == user.id)
        )
        model_count = session.exec(model_query).one()

        # 3. Get Highest Accuracy
        accuracy_query = select(func.max(Model.accuracy)).where(
            Model.user_id == user.id
        )
        highest_accuracy = session.exec(accuracy_query).first() or 0.0

        # 4. Get Active model name
        active_model_name = "None"
        if user.active_model:
            model = session.get(Model, user.active_model)
            if model:
                active_model_name = model.name

        return Kpi(
            dataset_count=dataset_count,
            model_count=model_count,
            highest_accuracy=highest_accuracy,
            active_model=active_model_name,
        )

    except SQLAlchemyError as e:
        logger.error(
            f"Database error while fetching dashboard summary for user {user.id}: {e}"
        )
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_dashboard_summary: {e}")
        raise


def get_recent_models(user: UserDep, session: SessionDep):
    try:
        query = (
            select(Model)
            .where(Model.user_id == user.id)
            .order_by(col(Model.trained_at).desc())
            .limit(5)
        )
        return session.exec(query).all()
    except SQLAlchemyError as e:
        logger.error(
            f"Database error while fetching recent models for user {user.id}: {e}"
        )
        raise


def get_recent_datasets(user: UserDep, session: SessionDep):
    try:
        query = (
            select(Dataset)
            .where(Dataset.user_id == user.id)
            .order_by(col(Dataset.uploaded_at).desc())
            .limit(5)
        )
        return session.exec(query).all()
    except SQLAlchemyError as e:
        logger.error(
            f"Database error while fetching recent datasets for user {user.id}: {e}"
        )
        raise


def get_recent_activity(user: UserDep, session: SessionDep):
    recent_models = list(get_recent_models(user, session))
    recent_datasets = list(get_recent_datasets(user, session))

    activity: list[Dataset | Model] = sorted(
        recent_models + recent_datasets,
        key=lambda x: x.timestamp,
        reverse=True,
    )

    activity_log: list[str] = []

    for act in activity[:5]:
        if isinstance(act, Dataset):
            activity_log.append(f"Dataset '{act.original_name}' uploaded.")
        else:
            activity_log.append(
                f"Model '{act.id}' trained with {act.accuracy} accuracy."
            )

    return activity_log
