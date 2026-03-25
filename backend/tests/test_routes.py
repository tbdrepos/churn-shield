"""import io
import uuid

from app.models.metrics_model import Metrics
from app.models.models_model import Model
from app.models.user_model import User


def test_api_root_returns_database_url(client):
    client_instance, _ = client
    response = client_instance.get("/api/v1/")

    assert response.status_code == 200
    assert isinstance(response.json(), str)


def test_protected_route_returns_current_user(client):
    client_instance, user = client
    response = client_instance.get("/api/v1/protected")

    assert response.status_code == 200
    assert response.json()["email"] == user.email


def test_register_user_success(client):
    client_instance, _ = client
    payload = {
        "email": "register@example.com",
        "password": "StrongPass123!",
        "display_name": "Registered User",
    }
    response = client_instance.post(
        "/api/v1/auth/register?remember_me=false", json=payload
    )

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["display_name"] == "Registered User"
    assert "refresh_token=" in response.headers["set-cookie"]


def test_register_user_duplicate_email_returns_409(client):
    client_instance, _ = client
    payload = {
        "email": "dupe@example.com",
        "password": "StrongPass123!",
        "display_name": "First",
    }
    first = client_instance.post(
        "/api/v1/auth/register?remember_me=false", json=payload
    )
    second = client_instance.post(
        "/api/v1/auth/register?remember_me=true", json=payload
    )

    assert first.status_code == 200
    assert second.status_code == 409


def test_login_user_success(client):
    client_instance, _ = client
    register_payload = {
        "email": "login@example.com",
        "password": "StrongPass123!",
        "display_name": "Login User",
    }
    client_instance.post(
        "/api/v1/auth/register?remember_me=false", json=register_payload
    )

    login_response = client_instance.post(
        "/api/v1/auth/login?remember_me=false",
        data={"username": "login@example.com", "password": "StrongPass123!"},
    )

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_login_user_invalid_credentials_returns_401(client):
    client_instance, _ = client
    response = client_instance.post(
        "/api/v1/auth/login?remember_me=false",
        data={"username": "missing@example.com", "password": "wrong"},
    )

    assert response.status_code == 401


def test_refresh_requires_cookie(client):
    client_instance, _ = client
    response = client_instance.post("/api/v1/auth/refresh")

    assert response.status_code == 401
    assert response.json()["detail"] == "No refresh token in request cookie"


def test_refresh_with_cookie_returns_access_token(client):
    client_instance, _ = client
    register_payload = {
        "email": "refresh@example.com",
        "password": "StrongPass123!",
        "display_name": "Refresh User",
    }
    register_response = client_instance.post(
        "/api/v1/auth/register?remember_me=true",
        json=register_payload,
    )
    set_cookie = register_response.headers["set-cookie"].split(";", 1)[0]
    cookie_value = set_cookie.split("=", 1)[1]

    client_instance.cookies.set("refresh_token", cookie_value)
    response = client_instance.post("/api/v1/auth/refresh")

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_verify_returns_current_user_fields(client):
    client_instance, user = client
    response = client_instance.get("/api/v1/auth/verify")

    assert response.status_code == 200
    assert response.json()["display_name"] == user.display_name
    assert response.json()["active_model"] is None


def test_upload_rejects_non_csv_file(client):
    client_instance, _ = client
    response = client_instance.post(
        "/api/v1/datasets/upload",
        files={"file": ("bad.txt", io.BytesIO(b"not csv"), "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only CSV files are allowed"


def test_upload_csv_success_with_stubs(client, monkeypatch):
    client_instance, user = client

    class FakeDataset:
        id = uuid.uuid4()
        original_name = "sample.csv"
        row_count = 1

        @staticmethod
        def uploaded_at():
            # never called; replaced right below
            return None

    from datetime import datetime, timezone

    FakeDataset.uploaded_at = datetime.now(timezone.utc)

    monkeypatch.setattr(
        "app.api.routes.datasets.churn_schema.validate", lambda *_: None
    )
    monkeypatch.setattr(
        "app.api.routes.datasets.store_file",
        lambda file, original_name, user_id, session: FakeDataset(),
    )

    csv_content = (
        "CustomerID,Gender,Age,TenureMonths,ContractType,MonthlyCharges,TotalCharges,"
        "PaymentMethod,InternetService,SupportCalls,Churn\n"
        "1,Male,30,12,One Year,20.5,300.0,Credit Card,DSL,0,No\n"
    )
    response = client_instance.post(
        "/api/v1/datasets/upload",
        files={"file": ("sample.csv", io.BytesIO(csv_content.encode()), "text/csv")},
    )

    assert response.status_code == 200
    assert response.json()["original_name"] == "sample.csv"


def test_model_metrics_requires_active_model(client):
    client_instance, _ = client
    response = client_instance.get("/api/v1/model/metrics")

    assert response.status_code == 404
    assert "trained model" in response.json()["detail"]


def test_model_metrics_returns_metrics_for_active_model(client, session):
    client_instance, user = client
    model_id = uuid.uuid4()
    dataset_id = uuid.uuid4()

    session.add(
        Metrics(
            model_id=model_id,
            dataset_id=dataset_id,
            accuracy=0.9,
            precision=0.8,
            recall=0.7,
            f1_score=0.75,
            roc_auc=0.85,
        )
    )
    db_user = User(email=user.email, hashed_password="x", active_model=model_id)
    db_user.id = user.id
    session.merge(db_user)
    session.commit()
    user.active_model = model_id

    response = client_instance.get("/api/v1/model/metrics")

    assert response.status_code == 200
    assert response.json()["accuracy"] == 0.9


def test_model_train_calls_service_and_returns_metrics(client, monkeypatch):
    client_instance, _ = client
    dataset_id = uuid.uuid4()

    fake_metrics = Metrics(
        model_id=uuid.uuid4(),
        dataset_id=dataset_id,
        accuracy=0.91,
        precision=0.82,
        recall=0.79,
        f1_score=0.8,
        roc_auc=0.88,
    )

    monkeypatch.setattr(
        "app.api.routes.ml.train_model", lambda *args, **kwargs: fake_metrics
    )

    response = client_instance.get(f"/api/v1/model/train/{dataset_id}")

    assert response.status_code == 200
    assert response.json()["f1_score"] == 0.8


def test_predict_requires_existing_model(client):
    client_instance, _ = client
    response = client_instance.post(
        "/api/v1/model/predict",
        files={"file": ("input.csv", io.BytesIO(b"a,b\n1,2"), "text/csv")},
    )

    assert response.status_code == 409


def test_predict_returns_service_output(client, session, monkeypatch):
    client_instance, user = client
    model = Model(user_id=user.id, dataset_id=uuid.uuid4())
    session.add(model)
    session.commit()
    session.refresh(model)
    user.active_model = model.id

    expected = [{"ChurnProbability": 0.42}]
    monkeypatch.setattr(
        "app.api.routes.ml.predict_probabilities", lambda *args, **kwargs: expected
    )

    response = client_instance.post(
        "/api/v1/model/predict",
        files={"file": ("input.csv", io.BytesIO(b"a,b\n1,2"), "text/csv")},
    )

    assert response.status_code == 200
    assert response.json() == expected
"""
