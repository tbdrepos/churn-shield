import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.main import app
from tests.common import get_token


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


def test_get_user(client: TestClient, capsys):

    token = get_token(client)
    response = client.get(
        "/api/v1/protected", headers={"Authorization": f"Bearer {token.access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "doe@example.com"
