import uuid

from app.models.metrics_model import Metrics
from app.models.models_model import Model
from app.models.user_model import User


def test_model_metrics_requires_active_model(client):
    client_instance, _ = client
    response = client_instance.get("/api/v1/model/metrics")
    assert response.status_code == 404


def test_model_metrics_returns_metrics_for_active_model(client, session):
    client_instance, user = client
    m_id, d_id = uuid.uuid4(), uuid.uuid4()
    session.add(
        Metrics(
            model_id=m_id,
            dataset_id=d_id,
            accuracy=0.9,
            precision=0.8,
            recall=0.7,
            f1_score=0.75,
            roc_auc=0.85,
        )
    )

    # Update mock user state in DB
    db_user = User(email=user.email, hashed_password="x", active_model=m_id)
    db_user.id = user.id
    session.merge(db_user)
    session.commit()
    user.active_model = m_id

    response = client_instance.get("/api/v1/model/metrics")
    assert response.status_code == 200
    assert response.json()["accuracy"] == 0.9


def test_model_train_calls_service_and_returns_metrics(client, monkeypatch):
    client_instance, _ = client
    d_id = uuid.uuid4()
    fake = Metrics(
        model_id=uuid.uuid4(),
        dataset_id=d_id,
        accuracy=0.91,
        precision=0.8,
        recall=0.8,
        f1_score=0.8,
        roc_auc=0.8,
    )

    monkeypatch.setattr("app.api.routes.ml.train_model", lambda *args, **kwargs: fake)
    response = client_instance.get(f"/api/v1/model/train/{d_id}")
    assert response.status_code == 200
    assert response.json()["f1_score"] == 0.8


def test_predict_returns_service_output(client, session, monkeypatch):
    client_instance, user = client
    model = Model(
        user_id=user.id,
        dataset_id=uuid.uuid4(),
        file_path="placeholder",
        accuracy=0.9,
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    user.active_model = model.id

    expected = [{"ChurnProbability": 0.42}]
    monkeypatch.setattr(
        "app.api.routes.ml.predict_probabilities", lambda *args, **kwargs: expected
    )

    import io

    response = client_instance.post(
        "/api/v1/model/predict",
        files={"file": ("in.csv", io.BytesIO(b"a,b\n1,2"), "text/csv")},
    )
    assert response.status_code == 200
    assert response.json() == expected
