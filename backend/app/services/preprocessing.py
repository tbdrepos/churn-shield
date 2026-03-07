from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Selectors
categorical_selector = make_column_selector(dtype_include=("object", "category"))  # type: ignore
numeric_selector = make_column_selector(dtype_include=("number",))  # type: ignore

# Preprocessor with imputers
preprocessor = ColumnTransformer(
    [
        (
            "cat",
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("encoder", OneHotEncoder(handle_unknown="ignore", drop="first")),
                ]
            ),
            categorical_selector,
        ),
        (
            "num",
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            ),
            numeric_selector,
        ),
    ],
    verbose_feature_names_out=False,
)


def get_pipeline():
    return Pipeline(
        [
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression()),
        ]
    )
