import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class Model(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    dataset_id: uuid.UUID = Field(foreign_key="dataset.id", index=True)
    trained_at: datetime = Field(default_factory=datetime.now)
    file_path: str
    accuracy: float

    @property
    def timestamp(self):
        return self.trained_at
