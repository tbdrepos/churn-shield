import uuid

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    display_name: str | None = None


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: uuid.UUID


class UserUpdate(SQLModel):
    email: str | None = None
    password: str | None = None
    display_name: str | None = None


class UserSettings(SQLModel, table=True):
    user_id: uuid.UUID = Field(primary_key=True, foreign_key="user.id")
    active_model: uuid.UUID | None = Field(foreign_key="model.id", default=None)

    # ML Settings
    preferred_classifier: str = Field(default="RandomForest")
    churn_threshold: float = Field(default=0.5, ge=0.0, le=1.0)

    # SHAP/Explainability settings
    show_top_n_features: int = Field(default=5)
