import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

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


app = FastAPI(lifespan=lifespan)
app.include_router(api_v1.router, prefix="/api/v1")
