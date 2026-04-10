import uuid
from datetime import datetime, timezone

from sqlmodel import Field as SQLField
from sqlmodel import SQLModel


class ModelMetrics(SQLModel, table=True):
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


class DatasetMetrics(SQLModel, table=True):
    dataset_id: uuid.UUID = SQLField(primary_key=True, foreign_key="dataset.id")

    generated_at: datetime = SQLField(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )

    # --- Basic Stats ---
    row_count: int = SQLField(ge=0)
    column_count: int = SQLField(ge=0)

    # --- Quality Checks ---
    missing_rows: int = SQLField(ge=0)  # Rows with at least one NULL
    null_value_ratio: float = SQLField(default=0.0, ge=0, le=1)
    duplicate_rows: int = SQLField(default=0, ge=0)

    # --- Churn Specifics ---
    churn_rate: float = SQLField(ge=0, le=1)
    avg_tenure: float = SQLField(default=0.0)
    avg_monthly_revenue_per_user: float = SQLField(nullable=True)

    @property
    def timestamp(self) -> datetime:
        return self.generated_at
