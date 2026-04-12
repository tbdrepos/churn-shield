import io
import uuid
from datetime import datetime, timezone

from app.models.datasets_model import DatasetStatus


def test_upload_rejects_non_csv_file(client):
    client_instance, _ = client
    response = client_instance.post(
        "/api/v1/datasets/upload",
        files={"file": ("bad.txt", io.BytesIO(b"not csv"), "text/plain")},
    )
    assert response.status_code == 400


def test_upload_csv_success_with_stubs(client, monkeypatch):
    client_instance, user = client

    class FakeDS:
        id, original_name, row_count = uuid.uuid4(), "s.csv", 1
        uploaded_at = datetime.now(timezone.utc)
        status = DatasetStatus.uploaded

    monkeypatch.setattr(
        "app.api.routes.datasets.churn_schema.validate", lambda *_: None
    )
    monkeypatch.setattr("app.api.routes.datasets.store_file", lambda *args: FakeDS())

    csv = "Col1,Col2\nVal1,Val2"
    response = client_instance.post(
        "/api/v1/datasets/upload",
        files={"file": ("s.csv", io.BytesIO(csv.encode()), "text/csv")},
    )
    assert response.status_code == 201
    assert response.json()["original_name"] == "s.csv"
