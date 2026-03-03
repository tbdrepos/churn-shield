import io
import uuid

import pytest
from fastapi.testclient import TestClient

from app.core.security import credentials_exception
from app.db.database import get_session
from app.main import app
from app.models.datasets import Dataset
from tests.test_auth import get_token


@pytest.fixture
def client():
    return TestClient(app)


def test_get_user(client, capsys):
    token = get_token(client)

    csv_content = """CustomerID,Gender,Age,TenureMonths,ContractType,MonthlyCharges,TotalCharges,PaymentMethod,InternetService,SupportCalls,Churn\n1001,Male,34,12,Month-to-Month,70.5,845.0,Credit Card,Fiber Optic,3,Yes\n1002,Female,45,36,One Year,55.0,1980.0,Bank Transfer,DSL,1,No\n1003,Male,29,6,Month-to-Month,80.0,480.0,Electronic Check,Fiber Optic,5,Yes\n1004,Female,52,24,Two Year,60.0,1440.0,Mailed Check,DSL,0,No\n1005,Male,40,18,Month-to-Month,75.0,1350.0,Credit Card,Fiber Optic,2,Yes\n1006,Female,31,8,Month-to-Month,65.0,520.0,Bank Transfer,None,1,No\n1007,Male,50,48,Two Year,90.0,4320.0,Credit Card,Fiber Optic,4,No\n1008,Female,27,3,Month-to-Month,85.0,255.0,Electronic Check,Fiber Optic,6,Yes\n1009,Male,36,20,One Year,60.0,1200.0,Bank Transfer,DSL,2,No\n1010,Female,42,15,Month-to-Month,72.0,1080.0,Mailed Check,Fiber Optic,3,Yes\n"""
    file = io.BytesIO(csv_content.encode("utf-8"))

    response = client.post(
        "/api/v1/upload",
        headers={"Authorization": f"Bearer {token.access_token}"},
        files={"file": ("test.csv", file, "text/csv")},
    )
    with capsys.disabled():
        print(response.json())
    """ assert response.status_code == 200
    session = next(get_session())
    try:
        dataset_id = uuid.UUID(response.json()["id"])
    except ValueError:
        raise credentials_exception
    assert dataset_id is not None
    dataset = session.get(Dataset, dataset_id)
    assert dataset is not None
    assert dataset.original_name == "test.csv" """
