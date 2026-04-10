from app.core.security import UserDep
from app.models.datasets_model import Dataset
from app.models.models_model import Model
from app.schemas.insights_schema import DataChart, ModelChart


def get_model_charts(model: Model, user: UserDep):
    return


def get_dataset_charts(dataset: Dataset, user: UserDep):
    return
