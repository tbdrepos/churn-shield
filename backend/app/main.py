import os
import shutil
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import api_v1
from app.core.config import get_settings
from app.db.database import create_db_and_tables, engine

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    # clean database after reload for testing
    engine.dispose()
    DB_FILE = settings.DATABASE_NAME
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Shutting down: {DB_FILE} deleted")
    DATA_PATH = "app/data"
    # delete uploaded data
    if os.path.exists(DATA_PATH):
        shutil.rmtree(DATA_PATH)
        print(f"Shutting down: {DATA_PATH} deleted")
    # recreate empty data folder
    os.mkdir(DATA_PATH)


app = FastAPI(lifespan=lifespan)

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(api_v1.router)

# app.mount("/", StaticFiles(directory="static", html=True))
