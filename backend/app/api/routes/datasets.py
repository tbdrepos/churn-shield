import os
import shutil
import uuid

import pandas as pd
from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile, status
from pandera.errors import SchemaError
from sqlmodel import select

from app.core.security import UserDep
from app.db.database import SessionDep
from app.models.datasets_model import Dataset, DatasetRead
from app.models.models_model import Model
from app.services.upload_service import store_file
from app.utils.validator import churn_schema

router = APIRouter(prefix="/datasets")

# remove None from pandas NaN filtering
ALLOWED_NA = [
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


@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=DatasetRead)
async def upload_csv(user: UserDep, session: SessionDep, file: UploadFile = File(...)):
    original_name = file.filename
    if not original_name:
        raise HTTPException(status_code=400, detail="Could not read file name")
    if not original_name.lower().endswith(".csv") or file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        df = pd.read_csv(
            file.file,
            na_values=ALLOWED_NA,
            keep_default_na=False,
        )
        # reset file stream
        file.file.seek(0)
        churn_schema.validate(df)
        dataset = store_file(file, original_name, user.id, session)
        return dataset
    except SchemaError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Schema validation failed {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}",
        )


@router.get("/all", response_model=list[Dataset])
def get_all_datasets(user: UserDep, session: SessionDep):
    query = select(Dataset).where(Dataset.user_id == user.id)
    datasets = session.exec(query).all()
    return datasets


@router.get("/{dataset_id}", response_model=Dataset)
def get_dataset(dataset_id: uuid.UUID, user: UserDep, session: SessionDep):
    # making sure user owns the dataset
    query = select(Dataset).where(Dataset.id == dataset_id, Dataset.user_id == user.id)
    dataset = session.exec(query).first()
    if not dataset:
        raise HTTPException(404, detail="Dataset not found")
    return dataset


@router.delete("/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dataset(
    dataset_id: str,
    user: UserDep,
    session: SessionDep,
    background_tasks: BackgroundTasks,
):
    # 1. Fetching the dataset and verify ownership
    dataset_query = select(Dataset).where(
        Dataset.id == dataset_id, Dataset.user_id == user.id
    )
    dataset = session.exec(dataset_query).first()

    if not dataset:
        raise HTTPException(404, detail="Dataset not found")

    # 2. Identifying associated models for cleanup
    models_query = select(Model).where(
        Model.dataset_id == dataset_id, Model.user_id == user.id
    )
    models = session.exec(models_query).all()

    # 3. Collecting paths for disk cleanup before DB deletion
    paths_to_delete = [dataset.file_path]
    for m in models:
        if hasattr(m, "file_path") and m.file_path:
            paths_to_delete.append(m.file_path)

    # 4. Database Deletion
    try:
        for model in models:
            session.delete(model)
        session.delete(dataset)
        session.commit()
    except Exception:
        session.rollback()
        raise

    # 5. Disk Cleanup
    background_tasks.add_task(cleanup_files, paths_to_delete)


def cleanup_files(paths: list[str]):
    """Helper to remove files from disk safely."""
    for path in paths:
        try:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
        except Exception as e:
            print(f"Error cleaning up {path}: {e}")
