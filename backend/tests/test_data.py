# tests/test_upload.py
import io
import uuid
from datetime import datetime, timedelta

import jwt
import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings  # contains JWT_SECRET_KEY, JWT_ALGORITHM
from app.db.database import get_session
from app.main import app
from app.models.datasets import Dataset
from app.models.user import User

client = TestClient(app)
settings = get_settings()


@pytest.fixture
def db_session():
    session = next(get_session())
    yield session
    session.rollback()
    session.close()


def create_test_user(db_session):
    user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        hashed_password="fakehashed",  # depends on your model
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def generate_token(user_id: uuid.UUID):
    expire = datetime.now() + timedelta(minutes=30)
    payload = {"sub": str(user_id), "exp": expire}
    token = jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return token


def test_upload_csv_authenticated(db_session, monkeypatch):
    # Override DB session dependency
    app.dependency_overrides[get_session] = lambda: db_session

    # Create a test user
    user = create_test_user(db_session)

    # Generate JWT for that user
    token = generate_token(user.id)

    # Fake CSV file
    csv_content = "col1,col2\n1,2\n3,4\n"
    file = io.BytesIO(csv_content.encode("utf-8"))

    response = client.post(
        "/upload",
        files={"file": ("test.csv", file, "text/csv")},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    # Verify dataset was inserted
    dataset = db_session.query(Dataset).first()
    assert dataset is not None
    assert dataset.user_id == user.id
    assert dataset.original_name == "test.csv"
    assert dataset.row_count == 2
