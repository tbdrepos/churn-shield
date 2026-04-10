from pydantic import BaseModel


class Kpi(BaseModel):
    dataset_count: int
    model_count: int
    highest_accuracy: float
    active_model: str | None
