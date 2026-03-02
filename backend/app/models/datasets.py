import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class Dataset(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    original_name: str = Field(index=True)
    uploaded_at: datetime
    row_count: int
