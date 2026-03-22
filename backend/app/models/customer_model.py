from datetime import datetime

from sqlmodel import Field, SQLModel


class CustomerBase(SQLModel):
    tenure: int
    monthly_charges: float


class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    churn_probability: float | None = None
    created_at: datetime = Field(default_factory=datetime.now)


class CustomerRead(CustomerBase):
    id: int
    churn_probability: float | None
