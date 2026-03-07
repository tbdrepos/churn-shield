import io
import uuid

import pytest
from fastapi.testclient import TestClient

from app.db.database import get_session
from app.main import app
from app.models.datasets import Dataset
from tests.common import upload_csv


@pytest.fixture
def client():
    return TestClient(app)


def test_get_user(client, capsys):
    response = upload_csv(client)

    assert response.status_code == 200
    session = next(get_session())
    dataset_id = uuid.UUID(response.json()["id"])
    assert dataset_id is not None
    dataset = session.get(Dataset, dataset_id)
    assert dataset is not None
    assert dataset.original_name == "test.csv"
