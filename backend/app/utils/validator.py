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
