import uuid

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile
from pandera.errors import SchemaError
from sqlmodel import select

from app.core.security import UserDep
from app.db.database import SessionDep
from app.models.datasets_model import Dataset
from app.services.upload_service import store_file
from app.utils.validator import churn_schema

router = APIRouter(prefix="/datasets")


@router.post("/upload")
async def upload_csv(user: UserDep, session: SessionDep, file: UploadFile = File(...)):
    original_name = file.filename
    if not original_name:
        raise HTTPException(status_code=400, detail="Could not read file name")
    if not original_name.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        # remove None from pandas NaN filtering
        allowed_na = [
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
        ]
        df = pd.read_csv(
            file.file,
            na_values=allowed_na,
            keep_default_na=False,
        )
        # reset file stream
        file.file.seek(0)
        churn_schema.validate(df)
        dataset = store_file(file, original_name, user.id, session)
        return {
            "id": str(dataset.id),
            "original_name": dataset.original_name,
            "row_count": dataset.row_count,
            "uploaded_at": dataset.uploaded_at.isoformat(),
        }
    except SchemaError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Schema validation failed",
                "error": str(e),
                "failure_cases": e.failure_cases,
            },
        )


@router.get("/{dataset_id}", response_model=Dataset)
def get_dataset(dataset_id: str, user: UserDep, session: SessionDep):
    try:
        validated_id = uuid.UUID(dataset_id)
    except ValueError:
        raise HTTPException(400, detail="Invalid dataset id")
    dataset = session.get(Dataset, validated_id)
    if not dataset:
        raise HTTPException(404, detail="Dataset not found")
    return dataset


@router.get("/all", response_model=list[Dataset])
def get_all_datasets(user: UserDep, session: SessionDep):
    query = select(Dataset).where(Dataset.user_id == user.id)
    datasets = session.exec(query).all()
    return datasets
