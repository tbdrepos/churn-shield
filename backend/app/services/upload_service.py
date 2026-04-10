import shutil
import uuid
from pathlib import Path

import pandas as pd
from fastapi import HTTPException, UploadFile

from app.db.database import SessionDep
from app.models.datasets_model import Dataset
from app.models.metrics_model import DatasetMetrics


def calculate_dataset_metrics(
    dataset_id: uuid.UUID,
    df: pd.DataFrame,
    target_col="churn",
    user_id_col="CustomerID",
) -> DatasetMetrics:
    """
    Calculates metrics for the DatasetMetrics SQLModel from a pandas DataFrame.
    """
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in CSV.")

    target_series = pd.to_numeric(df[target_col], errors="coerce")
    churn_rate = float(target_series.mean()) if not target_series.empty else 0.0

    avg_tenure = float(df["tenure"].mean()) if "tenure" in df.columns else 0.0

    rev_col = "MonthlyCharges" if "MonthlyCharges" in df.columns else None
    avg_revenue = (
        float(df[rev_col].mean()) if rev_col and rev_col in df.columns else 0.0
    )

    missing_rows = int(df.isnull().any(axis=1).sum())

    duplicate_users = (
        int(df[user_id_col].duplicated().sum()) if user_id_col in df.columns else 0
    )

    total_cells = df.size
    null_value_ratio = (
        (df.isnull().sum().sum() / total_cells) if total_cells > 0 else 0.0
    )

    return DatasetMetrics(
        dataset_id=dataset_id,
        row_count=df.shape[0],
        column_count=df.shape[1],
        missing_rows=missing_rows,
        null_value_ratio=null_value_ratio,
        duplicate_rows=duplicate_users,
        churn_rate=churn_rate,
        avg_tenure=avg_tenure,
        avg_monthly_revenue_per_user=avg_revenue,
    )


def store_metadata(
    original_name: str,
    file_path: Path,
    file_id: uuid.UUID,
    user_id: uuid.UUID,
    session: SessionDep,
):
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            raise ValueError("The uploaded CSV file is empty.")
        datasetMetrics: DatasetMetrics = calculate_dataset_metrics(file_id, df)
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=400, detail=f"Data Validation Error: {str(e)}")

    dataset = Dataset(
        id=file_id,
        user_id=user_id,
        original_name=original_name,
        row_count=datasetMetrics.row_count,
        file_path=str(file_path),
    )
    session.add(dataset)
    session.add(datasetMetrics)
    session.commit()
    session.refresh(dataset)
    return dataset


def store_file(
    file: UploadFile, original_name: str, user_id: uuid.UUID, session: SessionDep
):
    # get to app/ from app/api/routes/datasets.py
    BASE_DIR = Path(__file__).resolve().parent.parent
    # from there go to app/data/
    UPLOAD_DIR = BASE_DIR / "data" / str(user_id) / "datasets"
    # Ensure the directory exists
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    # generate uuid to rename the file
    file_id = uuid.uuid4()
    file_name = f"{file_id}.csv"

    file_path = UPLOAD_DIR / file_name
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    dataset = store_metadata(original_name, file_path, file_id, user_id, session)
    return dataset
