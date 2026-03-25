import os
import shutil
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api import api_v1
from app.core.config import get_settings
from app.db.database import create_db_and_tables, engine

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # During tests we rely on the pytest fixtures to create tables on a
    # dedicated (in-memory) SQLModel engine. Avoid touching the file DB to
    # prevent SQLite locking and cross-test interference.
    if not settings.TESTING:
        create_db_and_tables()
    yield
    engine.dispose()

    # In non-test runs, we clean database + uploaded artifacts on shutdown.
    # In tests, skipping filesystem deletion avoids WinError 32 locks.
    if not settings.TESTING:
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


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # This ensures that even on a crash, a proper JSON response is sent
    # which allows CORSMiddleware to do its job.
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "detail": str(exc)},
    )


# app.mount("/", StaticFiles(directory="static", html=True))
