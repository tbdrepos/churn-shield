import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app
from tests.common import get_token, upload_csv


@pytest.fixture
def client():
    return TestClient(app)


def test_model_train(client, capsys):
    upload_response = upload_csv(client)
    dataset_id = upload_response.json()["id"]
    token = get_token(client)
    response = client.get(
        "/api/v1/model/train",
        headers={"Authorization": f"Bearer {token.access_token}"},
        params={"dataset_id": dataset_id},
    )
    assert response.json()["accuracy_score"] > 0
