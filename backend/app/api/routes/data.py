import shutil
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.security import UserDep
from app.db.database import SessionDep
from app.models.datasets import Dataset

router = APIRouter()


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


def store_file(file: UploadFile, user_id: uuid.UUID, session: SessionDep):
    # get to app/ from app/api/routes/upload.py
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    # from there go to app/data/
    UPLOAD_DIR = BASE_DIR / "data"
    # Ensure the directory exists
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    # generate uuid to rename the file
    file_id = uuid.uuid4()
    file_name = f"{file_id}.csv"

    file_path = UPLOAD_DIR / file_name

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    dataset = store_metadata(str(file.filename), file_path, file_id, user_id, session)
    return dataset


@router.post("/upload")
async def upload_csv(user: UserDep, session: SessionDep, file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    dataset = store_file(file, user.id, session)
    return {
        "id": str(dataset.id),
        "original_name": dataset.original_name,
        "row_count": dataset.row_count,
        "uploaded_at": dataset.uploaded_at.isoformat(),
    }
