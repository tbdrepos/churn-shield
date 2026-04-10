import uuid
from datetime import datetime, timezone

from sqlmodel import Field as SQLField
from sqlmodel import SQLModel


class Metrics(SQLModel, table=True):
    model_id: uuid.UUID = SQLField(primary_key=True, foreign_key="model.id")
    dataset_id: uuid.UUID = SQLField(foreign_key="dataset.id", index=True)

    generated_at: datetime = SQLField(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )

    accuracy: float = SQLField(ge=0, le=1)
    precision: float = SQLField(ge=0, le=1)
    recall: float = SQLField(ge=0, le=1)
    f1_score: float = SQLField(ge=0, le=1)
    roc_auc: float = SQLField(ge=0, le=1)

    @property
    def timestamp(self) -> datetime:
        return self.generated_at
