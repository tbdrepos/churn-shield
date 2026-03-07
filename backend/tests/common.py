import io

from fastapi.testclient import TestClient
from sqlmodel import select

from app.core.security import Token
from app.db.database import get_session
from app.models.user import User, UserCreate


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
        response = client.post("/api/v1/auth/register", content=data.model_dump_json())

    else:
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": data.email,
                "password": data.password,
            },
        )
    return Token(**response.json())


def upload_csv(client: TestClient):
    token = get_token(client)
    csv_content = """CustomerID,Gender,Age,TenureMonths,ContractType,MonthlyCharges,TotalCharges,PaymentMethod,InternetService,SupportCalls,Churn\n1001,Male,34,12,Month-to-Month,70.5,845.0,Credit Card,Fiber Optic,3,Yes\n1002,Female,45,36,One Year,55.0,1980.0,Bank Transfer,DSL,1,No\n1003,Male,29,6,Month-to-Month,80.0,480.0,Electronic Check,Fiber Optic,5,Yes\n1004,Female,52,24,Two Year,60.0,1440.0,Mailed Check,DSL,0,No\n1005,Male,40,18,Month-to-Month,75.0,1350.0,Credit Card,Fiber Optic,2,Yes\n1006,Female,31,8,Month-to-Month,65.0,520.0,Bank Transfer,None,1,No\n1007,Male,50,48,Two Year,90.0,4320.0,Credit Card,Fiber Optic,4,No\n1008,Female,27,3,Month-to-Month,85.0,255.0,Electronic Check,Fiber Optic,6,Yes\n1009,Male,36,20,One Year,60.0,1200.0,Bank Transfer,DSL,2,No\n1010,Female,42,15,Month-to-Month,72.0,1080.0,Mailed Check,Fiber Optic,3,Yes\n"""
    file = io.BytesIO(csv_content.encode("utf-8"))

    return client.post(
        "/api/v1/upload",
        headers={"Authorization": f"Bearer {token.access_token}"},
        files={"file": ("test.csv", file, "text/csv")},
    )
