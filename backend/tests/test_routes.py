import io
import uuid

import pytest
from sqlmodel import Session

from app.models.datasets_model import Dataset
from app.models.models_model import Model, ModelStatus

CHURN_CSV = (
    "CustomerID,Gender,Age,TenureMonths,ContractType,MonthlyCharges,TotalCharges,"
    "PaymentMethod,InternetService,SupportCalls,Churn\n"
    "1,Male,30,12,One Year,20.5,300.0,Credit Card,DSL,0,No\n"
)


def test_api_root_returns_database_url(client):
    client_instance, _ = client
    response = client_instance.get("/api/v1/")
    assert response.status_code == 200
    assert isinstance(response.json(), str)


def test_protected_route_returns_current_user(client):
    client_instance, user = client
    response = client_instance.get("/api/v1/protected")
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == user.email
    assert body["id"] == str(user.id)


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
    assert "refresh_token=" in response.headers.get("set-cookie", "")


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
    assert response.json().get("active_model") is None


def test_upload_rejects_non_csv_file(client):
    client_instance, _ = client
    response = client_instance.post(
        "/api/v1/datasets/upload",
        files={"file": ("bad.txt", io.BytesIO(b"not csv"), "text/plain")},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Only CSV files are allowed"


def test_upload_csv_valid_returns_201(client):
    client_instance, _ = client
    response = client_instance.post(
        "/api/v1/datasets/upload",
        files={
            "file": (
                "sample.csv",
                io.BytesIO(CHURN_CSV.encode()),
                "text/csv",
            )
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["original_name"] == "sample.csv"
    assert data["row_count"] == 1


def test_get_all_datasets_only_current_user(client, session: Session):
    client_instance, user = client
    session.add(
        Dataset(
            user_id=user.id,
            original_name="mine.csv",
            row_count=1,
            file_path="/tmp/mine.csv",
        )
    )
    session.add(
        Dataset(
            user_id=uuid.uuid4(),
            original_name="theirs.csv",
            row_count=1,
            file_path="/tmp/theirs.csv",
        )
    )
    session.commit()
    response = client_instance.get("/api/v1/datasets/all")
    assert response.status_code == 200
    names = {d["original_name"] for d in response.json()}
    assert names == {"mine.csv"}


def test_get_dataset_by_id_not_found(client):
    client_instance, _ = client
    rid = uuid.uuid4()
    response = client_instance.get(f"/api/v1/datasets/{rid}")
    assert response.status_code == 404


def test_get_dataset_by_id_success(client, session: Session):
    client_instance, user = client
    ds = Dataset(
        user_id=user.id,
        original_name="owned.csv",
        row_count=2,
        file_path="/tmp/owned.csv",
    )
    session.add(ds)
    session.commit()
    session.refresh(ds)
    response = client_instance.get(f"/api/v1/datasets/{ds.id}")
    assert response.status_code == 200
    assert response.json()["original_name"] == "owned.csv"


def test_model_train_returns_202_when_dataset_exists(client, session: Session):
    client_instance, user = client
    ds = Dataset(
        user_id=user.id,
        original_name="d.csv",
        row_count=1,
        file_path="/tmp/d.csv",
    )
    session.add(ds)
    session.commit()
    session.refresh(ds)
    response = client_instance.post(f"/api/v1/model/train/{ds.id}")
    assert response.status_code == 202
    assert "Training started" in response.json().get("message", "")


def test_model_train_returns_404_when_missing(client):
    client_instance, _ = client
    response = client_instance.post(f"/api/v1/model/train/{uuid.uuid4()}")
    assert response.status_code == 404


def test_model_trained_all_empty(client):
    client_instance, _ = client
    response = client_instance.get("/api/v1/model/trained/all")
    assert response.status_code == 200
    assert response.json() == []


def test_model_active_none(client):
    client_instance, _ = client
    response = client_instance.get("/api/v1/model/active")
    assert response.status_code == 200
    assert response.json() is None


def test_model_predict_no_active_model(client):
    client_instance, _ = client
    response = client_instance.post(
        "/api/v1/model/predict",
        files={"file": ("x.csv", io.BytesIO(b"a\n1"), "text/csv")},
    )
    assert response.status_code == 409


def test_model_predict_delegates_to_service(
    client, session: Session, tmp_path, monkeypatch: pytest.MonkeyPatch
):
    client_instance, user = client
    ds_id = uuid.uuid4()
    model = Model(
        name="m_LogisticRegression_v1",
        user_id=user.id,
        dataset_id=ds_id,
        dataset_name="d.csv",
        status=ModelStatus.trained,
        file_path="/tmp/model.joblib",
        accuracy=0.9,
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    user.active_model = model.id
    session.add(user)
    session.commit()

    models_dir = tmp_path / str(user.id) / "models"
    models_dir.mkdir(parents=True)
    (models_dir / f"{model.id}.joblib").write_bytes(b"\x00")

    monkeypatch.setattr("app.api.routes.models.DATA_ROOT", tmp_path)
    monkeypatch.setattr(
        "app.api.routes.models.predict_probabilities",
        lambda *a, **k: [{"ChurnProbability": 0.5}],
    )

    response = client_instance.post(
        "/api/v1/model/predict",
        files={"file": ("x.csv", io.BytesIO(b"a\n1"), "text/csv")},
    )
    assert response.status_code == 200
    assert response.json() == [{"ChurnProbability": 0.5}]


def test_dashboard_summary(client, session: Session):
    client_instance, user = client
    response = client_instance.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["dataset_count"] == 0
    assert data["model_count"] == 0
    assert data["highest_accuracy"] == 0.0


def test_insights_model_metrics_not_found(client):
    client_instance, _ = client
    response = client_instance.get(f"/api/v1/insights/model/metrics/{uuid.uuid4()}")
    assert response.status_code == 404


def test_insights_dataset_metrics_not_found(client):
    client_instance, _ = client
    response = client_instance.get(
        f"/api/v1/insights/dataset/metrics/{uuid.uuid4()}"
    )
    assert response.status_code == 404


def test_insights_dataset_charts_monkeypatched(client, session: Session, monkeypatch):
    client_instance, user = client
    ds = Dataset(
        user_id=user.id,
        original_name="c.csv",
        row_count=1,
        file_path="/tmp/c.csv",
    )
    session.add(ds)
    session.commit()
    session.refresh(ds)
    monkeypatch.setattr(
        "app.api.routes.insights.get_dataset_charts",
        lambda dataset, user_dep: [],
    )
    response = client_instance.get(f"/api/v1/insights/dataset/charts/{ds.id}")
    assert response.status_code == 200
    assert response.json() == []
