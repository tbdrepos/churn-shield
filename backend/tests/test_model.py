import io

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
    assert response.json()["accuracy"] > 0
    with capsys.disabled():
        print(response.json())


def test_predict(client, capsys):
    token = get_token(client)
    csv_content = """CustomerID,Gender,Age,TenureMonths,ContractType,MonthlyCharges,TotalCharges,PaymentMethod,InternetService,SupportCalls\n1001,Male,34,12,Month-to-Month,70.5,845.0,Credit Card,Fiber Optic,3\n1002,Female,45,36,One Year,55.0,1980.0,Bank Transfer,DSL,1\n"""
    file = io.BytesIO(csv_content.encode("utf-8"))
    response = client.post(
        "/api/v1/model/predict",
        headers={"Authorization": f"Bearer {token.access_token}"},
        files={"file": ("predict.csv", file, "text/csv")},
    )
