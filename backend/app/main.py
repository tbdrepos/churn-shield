import os
import shutil
from contextlib import asynccontextmanager

import loguru
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api import api_v1
from app.core.config import get_settings
from app.db.database import create_db_and_tables, engine

settings = get_settings()

loguru.logger.add(
    "logs/app.log",
    format="{time} {level} {message}",
    level="INFO",
    rotation="1 MB",
    compression="zip",
)
logger = loguru.logger


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

        # delete uploaded data
        DATA_PATH = "app/data"
        if os.path.exists(DATA_PATH):
            shutil.rmtree(DATA_PATH)
            print(f"Shutting down: {DATA_PATH} deleted")
        # recreate empty data folder
        os.mkdir(DATA_PATH)


app = FastAPI(lifespan=lifespan)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # This ensures that even on a crash, a proper JSON response is sent
    # which allows CORSMiddleware to do its job.
    logger.exception(f"Unhandled error {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "detail": str(exc)},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.exception(f"Unhandled error {str(exc.detail)}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


app.include_router(api_v1.router)

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):

    try:
        response = await call_next(request)

    except Exception as exc:
        logger.exception(f"Unhandled error {str(exc)}")
        response = JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
        )

    origin = request.headers.get("origin")

    if origin in origins:
        response.headers["Access-Control-Allow-Origin"] = origin

    response.headers["Access-Control-Allow-Credentials"] = "true"

    return response


# app.mount("/", StaticFiles(directory="static", html=True))
