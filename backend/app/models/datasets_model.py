import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


class DatasetStatus(str, Enum):
    uploaded = "uploaded"
    training = "training"
    trained = "trained"
    failed = "failed"


class DatasetBase(SQLModel):
    original_name: str = Field(index=True)
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    row_count: int
    status: DatasetStatus = Field(default=DatasetStatus.uploaded)

    @property
    def timestamp(self):
        return self.uploaded_at


class DatasetRead(DatasetBase):
    id: uuid.UUID


class Dataset(DatasetBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    file_path: str
