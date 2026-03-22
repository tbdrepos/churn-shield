import uuid

from sqlmodel import Field, SQLModel


class Metrics(SQLModel, table=True):
    model_id: uuid.UUID = Field(primary_key=True)
    dataset_id: uuid.UUID = Field(foreign_key="dataset.id")
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
