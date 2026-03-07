import uuid

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    display_name: str | None = None
    active_model: uuid.UUID | None = Field(foreign_key="model.id", default=None)


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
    active_model: uuid.UUID | None = Field(foreign_key="model.id", default=None)
