import shutil
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile
from pandera.errors import SchemaError

from app.core.security import UserDep
from app.db.database import SessionDep
from app.models.datasets import Dataset
from app.utils.validator import churn_schema

router = APIRouter(prefix="/upload")


def store_metadata(
    original_name: str,
    file_path: Path,
    file_id: uuid.UUID,
    user_id: uuid.UUID,
    session: SessionDep,
):
    try:
        row_count = pd.read_csv(file_path).shape[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {e}")

    dataset = Dataset(
        id=file_id,
        user_id=user_id,
        original_name=original_name,
        uploaded_at=datetime.now(),
        row_count=row_count,
    )
    session.add(dataset)
    session.commit()
    session.refresh(dataset)
    return dataset


def store_file(
    file: UploadFile, original_name: str, user_id: uuid.UUID, session: SessionDep
):
    # get to app/ from app/api/routes/upload.py
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
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


@router.post("/")
async def upload_csv(user: UserDep, session: SessionDep, file: UploadFile = File(...)):
    original_name = file.filename
    if not original_name:
        raise HTTPException(status_code=400, detail="Could not read file name")
    if not original_name.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        df = pd.read_csv(
            file.file,
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
            status_code=400,
            detail={
                "message": "Schema validation failed",
                "error": str(e),
                "failure_cases": e.failure_cases,
            },
        )
