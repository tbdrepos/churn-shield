from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

from app.core.security import UserDep
from app.db.database import SessionDep
from app.services.train import train_model

router = APIRouter(prefix="/model")


@router.get("/train")
def get_model(dataset_id: str, user: UserDep, session: SessionDep):
    user_id = str(user.id)
    # FILE_PATH = f"app/data/{user_id}/datasets/{dataset_id}.csv"
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    FILE_PATH = BASE_DIR / "data" / str(user_id) / "datasets" / f"{dataset_id}.csv"

    df = pd.read_csv(FILE_PATH)
    return train_model(session, df, user_id, dataset_id, FILE_PATH)
