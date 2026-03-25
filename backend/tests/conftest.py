import os
import uuid
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

# Ensure Settings are populated before app imports read them.
os.environ.setdefault("TESTING", "true")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret")
os.environ.setdefault("JWT_ALGORITHM", "HS256")

from app.core.security import get_current_user, get_password_hash
from app.db.database import get_session
from app.main import app
from app.models.user_model import User


@pytest.fixture(scope="session", name="test_engine")
def test_engine_fixture() -> Generator:
    # Use a static pool so the in-memory SQLite database persists across
    # connections for the whole test session.
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    # No explicit drop_all: in-memory SQLite disappears when the engine is
    # disposed, and dropping triggers SQLAlchemy foreign-key cycle warnings.


@pytest.fixture(name="session")
def session_fixture(test_engine) -> Generator[Session, None, None]:
    with Session(test_engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    mock_user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        hashed_password=get_password_hash("password"),
        display_name="Test User",
        active_model=None,
    )

    # Overriding dependencies to bypass real DB and JWT logic
    def get_session_override():
        yield session

    def get_current_user_override():
        return mock_user

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override

    with TestClient(app) as client:
        yield client, mock_user

    # Clean up after the test
    app.dependency_overrides.clear()
