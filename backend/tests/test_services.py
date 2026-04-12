import io
import uuid
from types import SimpleNamespace

import joblib
import pandas as pd
import pytest
from fastapi import UploadFile
from sqlmodel import Session

from app.models.metrics_model import DatasetMetrics
from app.models.user_model import User
from app.services.dashboard_service import get_kpi, get_recent_activity
from app.services.prediction_service import predict_probabilities
from app.services.preprocessing_service import get_pipeline
from app.services.train_service import generate_model_name, prepare_data
from app.services.upload_service import calculate_dataset_metrics, store_metadata
from app.utils.validator import read_churn_df

CHURN_CSV = (
    "CustomerID,Gender,Age,TenureMonths,ContractType,MonthlyCharges,TotalCharges,"
    "PaymentMethod,InternetService,SupportCalls,Churn\n"
    "1,Male,30,12,One Year,20.5,300.0,Credit Card,DSL,0,No\n"
    "2,Female,45,24,Two Year,80.0,1500.0,Bank Transfer,Fiber Optic,2,Yes\n"
)

_CHURN_H = (
    "CustomerID,Gender,Age,TenureMonths,ContractType,MonthlyCharges,TotalCharges,"
    "PaymentMethod,InternetService,SupportCalls,Churn"
)
CHURN_MULTI = _CHURN_H + "\n" + "\n".join(
    f"{i},Male,30,12,One Year,20.5,300.0,Credit Card,DSL,0,{'No' if i < 4 else 'Yes'}"
    for i in range(8)
)


def test_calculate_dataset_metrics_churn_yes_no():
    df = pd.read_csv(io.StringIO(CHURN_CSV))
    did = uuid.uuid4()
    m = calculate_dataset_metrics(did, df)
    assert isinstance(m, DatasetMetrics)
    assert m.dataset_id == did
    assert m.row_count == 2
    assert m.churn_rate == pytest.approx(0.5)
    assert m.avg_tenure == pytest.approx(18.0)


def test_calculate_dataset_metrics_missing_target_raises():
    df = pd.read_csv(io.StringIO("CustomerID\n1\n"))
    with pytest.raises(ValueError, match="Target column"):
        calculate_dataset_metrics(uuid.uuid4(), df, target_col="Churn")


def test_generate_model_name():
    assert generate_model_name("data.csv", "LogisticRegression", 0) == "data_LogisticRegression_v1"
    assert generate_model_name("data.csv", "LogisticRegression", 2) == "data_LogisticRegression_v3"


def test_get_pipeline_fit_and_predict():
    df = pd.read_csv(io.StringIO(CHURN_CSV))
    X = df.drop(columns=["Churn"])
    y = df["Churn"]
    pipe = get_pipeline()
    pipe.fit(X, y)
    preds = pipe.predict(X)
    assert len(preds) == 2


def test_prepare_data_writes_and_splits(tmp_path):
    path = tmp_path / "train.csv"
    path.write_text(CHURN_MULTI, encoding="utf-8")
    X_train, X_test, y_train, y_test = prepare_data(path, target="Churn")
    assert len(X_train) + len(X_test) == 8
    assert "Churn" not in X_train.columns


def test_read_churn_df_roundtrip(tmp_path):
    path = tmp_path / "f.csv"
    path.write_text(CHURN_CSV, encoding="utf-8")
    df = read_churn_df(path)
    assert df.shape[0] == 2
    assert "Churn" in df.columns


def test_get_kpi_empty(session: Session):
    uid = uuid.uuid4()
    u = User(
        id=uid,
        email="kpi@example.com",
        hashed_password="x",
        display_name="K",
        active_model=None,
    )
    session.add(u)
    session.commit()
    user_like = SimpleNamespace(id=uid, active_model=None)
    kpi = get_kpi(user_like, session)
    assert kpi.dataset_count == 0
    assert kpi.model_count == 0
    assert kpi.highest_accuracy == 0.0


def test_get_recent_activity_empty(session: Session):
    uid = uuid.uuid4()
    u = User(
        id=uid,
        email="act@example.com",
        hashed_password="x",
        active_model=None,
    )
    session.add(u)
    session.commit()
    user_like = SimpleNamespace(id=uid, active_model=None)
    assert get_recent_activity(user_like, session) == []


def test_store_metadata_persists_dataset_and_metrics(tmp_path, session: Session):
    uid = uuid.uuid4()
    u = User(
        id=uid,
        email="up@example.com",
        hashed_password="x",
        active_model=None,
    )
    session.add(u)
    session.commit()

    csv_path = tmp_path / "u.csv"
    csv_path.write_text(CHURN_CSV, encoding="utf-8")
    fid = uuid.uuid4()
    ds = store_metadata("u.csv", csv_path, fid, uid, session)
    assert ds.original_name == "u.csv"
    assert ds.row_count == 2
    assert ds.user_id == uid


def test_predict_probabilities_with_trained_pipeline(tmp_path, session: Session):
    df = pd.read_csv(io.StringIO(CHURN_CSV))
    X = df.drop(columns=["Churn"])
    y = df["Churn"]
    pipe = get_pipeline()
    pipe.fit(X, y)
    model_path = tmp_path / "m.joblib"
    joblib.dump(pipe, model_path)

    pred_csv = io.BytesIO(CHURN_CSV.encode())
    uf = UploadFile(filename="p.csv", file=pred_csv)
    out = predict_probabilities(uf, model_path, session)
    assert isinstance(out, list)
    assert len(out) == 2
    assert "ChurnProbability" in out[0]
