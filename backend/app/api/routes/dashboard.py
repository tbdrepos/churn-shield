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

router = APIRouter(prefix="/dashboard")

@router.get('/summary')
def get_summary(user:UserDep, ):