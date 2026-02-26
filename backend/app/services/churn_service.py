import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

### loading data ###
dataset_source = "kaggle-datasets"
dataset_name = "Heart_Disease_Prediction"
response_name = "Heart Disease"  # binary classification
df = pd.read_csv(f"{dataset_source}/{dataset_name}.csv")
# test if dataset has nan values
if df.isna().any().any():
    df.dropna(inplace=True)

X = df.drop(response_name, axis=1)
y = df[response_name]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

### preprocessing ###
categorical_selector = make_column_selector(dtype_include=["object", "category"])
numeric_selector = make_column_selector(dtype_include=["number"])

preprocessor = ColumnTransformer(
    [
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore", drop="first"),
            categorical_selector,
        ),
        ("num", StandardScaler(), numeric_selector),
    ],
    verbose_feature_names_out=False,
)
model_pipeline = Pipeline(
    [
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression()),
    ]
)

### model fit  ###
model_pipeline.fit(X_train, y_train)
accuracy = model_pipeline.score(X_test, y_test)
