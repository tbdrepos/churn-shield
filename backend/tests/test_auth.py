import pytest
from fastapi.testclient import TestClient
from sqlmodel import select

from app.core.config import Settings, get_settings
from app.core.security import Token
from app.db.database import get_session
from app.main import app
from app.models.user import User, UserCreate


@pytest.fixture
def client():
    return TestClient(app)


def get_settings_override():
    return Settings(DATABASE_URL="testing_admin@example.com")


def get_token(client: TestClient):
    data = UserCreate(
        display_name="doe",
        email="doe@example.com",
        password="doedoe",
    )
    session = next(get_session())
    query = select(User).where(User.email == data.email)
    query_result = session.exec(query).first()
    if query_result is None:
        response = client.post("/api/v1/register", content=data.model_dump_json())

    else:
        response = client.post(
            "/api/v1/login",
            data={
                "username": data.email,
                "password": data.password,
            },
        )
    return Token(**response.json())


def test_routing(client):
    get_settings.cache_clear()
    app.dependency_overrides[get_settings] = get_settings_override
    response = client.get("/api/v1/")
    assert response.status_code == 200
    data = response.json()
    assert data == "testing_admin@example.com"


def test_get_user(client: TestClient, capsys):

    token = get_token(client)
    response = client.get(
        "/api/v1/protected", headers={"Authorization": f"Bearer {token.access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "doe@example.com"
