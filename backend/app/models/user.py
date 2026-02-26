from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str
    email: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # TODO: change this to hashed_password after implementing security.py
    password: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
