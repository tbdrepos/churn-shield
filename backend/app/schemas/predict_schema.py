from typing import Annotated, Literal

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    Gender: str
    Age: int
    TenureMonths: int
    ContractType: str
    MonthlyCharges: float
    TotalCharges: float
    PaymentMethod: str
    InternetService: str
    SupportCalls: int


class FeatureImpact(BaseModel):
    feature: str
    value: str | float | int
    impact_score: float
    impact_label: Literal["Low Risk", "Medium Risk", "High Risk", "Neutral"]
    direction: Literal["increase", "decrease"]


class PredictResponse(BaseModel):
    prediction: Literal["No", "Yes"]
    probability: Annotated[float, Field(ge=0, le=1)]
    feature_impact: list[FeatureImpact]
