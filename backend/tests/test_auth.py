import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.core.security import Token
from app.main import app
from app.models.user import UserCreate


@pytest.fixture
def client():
    return TestClient(app)


def get_settings_override():
    return Settings(DATABASE_URL="testing_admin@example.com")


def test_routing(client):
    get_settings.cache_clear()
    app.dependency_overrides[get_settings] = get_settings_override
    response = client.get("/api/v1/")
    assert response.status_code == 200
    data = response.json()
    assert data == "testing_admin@example.com"


def test_create_user(client, capsys):
    data = UserCreate(
        display_name="doe",
        email="doe@example.com",
        password="doedoe",
    )
    response = client.post("/api/v1/register", content=data.model_dump_json())
    Token(**response.json())
