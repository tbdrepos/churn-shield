import uuid
from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class DatasetStatus(str, Enum):
    uploaded = "uploaded"
    training = "training"
    trained = "trained"
    failed = "failed"


class DatasetBase(SQLModel):
    original_name: str = Field(index=True)
    uploaded_at: datetime
    row_count: int
    status: DatasetStatus = Field(default=DatasetStatus.uploaded)


class DatasetRead(DatasetBase):
    pass


class Dataset(DatasetBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
