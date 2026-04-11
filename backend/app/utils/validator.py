from pathlib import Path
from typing import Any

import pandas as pd
from pandera.pandas import Check, Column, DataFrameSchema

churn_schema = DataFrameSchema(
    {
        "CustomerID": Column(int, Check.ge(0)),
        "Gender": Column(str, Check.isin(["Male", "Female"]), nullable=True),
        "Age": Column(int, Check.in_range(18, 100), nullable=True),
        "TenureMonths": Column(int, Check.ge(0), nullable=True),
        "ContractType": Column(
            str, Check.isin(["Month-to-Month", "One Year", "Two Year"]), nullable=True
        ),
        "MonthlyCharges": Column(float, Check.ge(0), nullable=True),
        "TotalCharges": Column(float, Check.ge(0), nullable=True),
        "PaymentMethod": Column(
            str,
            Check.isin(
                ["Credit Card", "Bank Transfer", "Electronic Check", "Mailed Check"]
            ),
            nullable=True,
        ),
        "InternetService": Column(
            str, Check.isin(["DSL", "Fiber Optic", "None"]), nullable=True
        ),
        "SupportCalls": Column(int, Check.ge(0), nullable=True),
        "Churn": Column(str, Check.isin(["Yes", "No"])),
    }
)

prediction_schema = churn_schema = DataFrameSchema(
    {
        "CustomerID": Column(int, Check.ge(0)),
        "Gender": Column(str, Check.isin(["Male", "Female"]), nullable=True),
        "Age": Column(int, Check.in_range(18, 100), nullable=True),
        "TenureMonths": Column(int, Check.ge(0), nullable=True),
        "ContractType": Column(
            str, Check.isin(["Month-to-Month", "One Year", "Two Year"]), nullable=True
        ),
        "MonthlyCharges": Column(float, Check.ge(0), nullable=True),
        "TotalCharges": Column(float, Check.ge(0), nullable=True),
        "PaymentMethod": Column(
            str,
            Check.isin(
                ["Credit Card", "Bank Transfer", "Electronic Check", "Mailed Check"]
            ),
            nullable=True,
        ),
        "InternetService": Column(
            str, Check.isin(["DSL", "Fiber Optic", "None"]), nullable=True
        ),
        "SupportCalls": Column(int, Check.ge(0), nullable=True),
    }
)


def validate_equal_lengths(*lists: list[Any]) -> None:
    """Helper to ensure multiple lists share the same length."""
    if not lists:
        return
    iterator = iter(lists)
    length = len(next(iterator))
    if not all(len(l) == length for l in iterator):
        raise ValueError("All data arrays must have the same length")


def read_churn_df(dataset_path: Path):
    df = pd.read_csv(
        dataset_path,
        na_values=[
            " ",
            "#N/A",
            "#N/A N/A",
            "#NA",
            "-1.#IND",
            "-1.#QNAN",
            "-NaN",
            "-nan",
            "1.#IND",
            "1.#QNAN",
            "",
            "N/A",
            "NA",
            "NULL",
            "NaN",
            "n/a",
            "nan",
            "null ",
        ],
        keep_default_na=False,
    )

    return df
