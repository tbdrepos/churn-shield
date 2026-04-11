from pathlib import Path

import joblib

from app.core.security import UserDep
from app.models.datasets_model import Dataset
from app.models.models_model import Model
from app.schemas.dataset_insights_schema import DataChart
from app.services.train_service import prepare_data


def get_dataset_charts(dataset: Dataset, user: UserDep):
    return
