import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.main import app
from app.models.user import UserCreate, UserRead


@pytest.fixture
def client():
    return TestClient(app)


def get_settings_override():
    return Settings(database_url="testing_admin@example.com")


app.dependency_overrides[get_settings] = get_settings_override


def test_routing(client):
    response = client.get("/api/v1/")
    assert response.status_code == 200
    data = response.json()
    assert data == "testing_admin@example.com"


def test_create_user(client, capsys):
    data = UserCreate(
        username="doe",
        email="doe@example.com",
        password="doedoe",
    )
    response = client.post("/api/v1/register", content=data.model_dump_json())
    UserRead(**response.json())
