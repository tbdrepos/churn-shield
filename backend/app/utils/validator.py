import pandas as pd
from fastapi import UploadFile
from pandera.errors import SchemaError
from pandera.pandas import Check, Column, DataFrameSchema

churn_schema = DataFrameSchema(
    {
        "CustomerID": Column(int, Check.ge(0)),
        "Gender": Column(str, Check.isin(["Male", "Female"])),
        "Age": Column(int, Check.in_range(18, 100)),
        "TenureMonths": Column(int, Check.ge(0)),
        "ContractType": Column(
            str, Check.isin(["Month-to-Month", "One Year", "Two Year"])
        ),
        "MonthlyCharges": Column(float, Check.ge(0)),
        "TotalCharges": Column(float, Check.ge(0)),
        "PaymentMethod": Column(
            str,
            Check.isin(
                ["Credit Card", "Bank Transfer", "Electronic Check", "Mailed Check"]
            ),
        ),
        "InternetService": Column(str, Check.isin(["DSL", "Fiber Optic", "None"])),
        "SupportCalls": Column(int, Check.ge(0)),
        "Churn": Column(str, Check.isin(["Yes", "No"])),
    }
)
