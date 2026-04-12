import uuid

from app.models.datasets_model import Dataset
from app.models.metrics_model import ModelMetrics
from app.models.models_model import Model, ModelStatus


def test_insights_model_metrics_not_found(client):
    client_instance, _ = client
    response = client_instance.get(f"/api/v1/insights/model/metrics/{uuid.uuid4()}")
    assert response.status_code == 404


def test_insights_model_metrics_success(client, session):
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

    model = Model(
        name="m_LogisticRegression_v1",
        user_id=user.id,
        dataset_id=ds.id,
        dataset_name=ds.original_name,
        status=ModelStatus.trained,
        file_path="/tmp/m.joblib",
        accuracy=0.88,
    )
    session.add(model)
    session.commit()
    session.refresh(model)

    session.add(
        ModelMetrics(
            model_id=model.id,
            dataset_id=ds.id,
            accuracy=0.9,
            precision=0.85,
            recall=0.8,
            f1_score=0.82,
            roc_auc=0.91,
        )
    )
    session.commit()

    response = client_instance.get(f"/api/v1/insights/model/metrics/{model.id}")
    assert response.status_code == 200
    body = response.json()
    assert body["accuracy"] == 0.9
    assert body["model_id"] == str(model.id)


def test_model_trained_for_dataset_empty(client, session):
    client_instance, user = client
    ds = Dataset(
        user_id=user.id,
        original_name="e.csv",
        row_count=1,
        file_path="/tmp/e.csv",
    )
    session.add(ds)
    session.commit()
    session.refresh(ds)
    response = client_instance.get(f"/api/v1/model/trained/{ds.id}")
    assert response.status_code == 200
    assert response.json() == []


def test_model_delete_not_found(client):
    client_instance, _ = client
    response = client_instance.delete(f"/api/v1/model/{uuid.uuid4()}")
    assert response.status_code == 404
