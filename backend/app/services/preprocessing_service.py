from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
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

# models

CLASSIFIER_REGISTRY = {
    "RandomForest": RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_split=20,
        min_samples_leaf=10,
        max_features="sqrt",
        bootstrap=True,
        n_jobs=-1,
        random_state=42,
    ),
    "GradientBoosting": GradientBoostingClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=3,  # via max_depth in base estimators
        subsample=0.8,
        min_samples_split=50,
        min_samples_leaf=20,
        max_features="sqrt",
        random_state=42,
    ),
    "LogisticRegression": LogisticRegression(),
}


def get_pipeline(clf: str = "RandomForest"):
    return Pipeline(
        [
            ("preprocessor", preprocessor),
            ("classifier", CLASSIFIER_REGISTRY[clf]),
        ]
    )
