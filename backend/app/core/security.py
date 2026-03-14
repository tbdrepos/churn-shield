import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from pydantic import BaseModel
from sqlmodel import select

from app.core.config import get_settings
from app.db.database import SessionDep
from app.models.user import User

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")
password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy_password")


class Token(BaseModel):
    display_name: str | None
    access_token: str


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_password_hash(password: str):
    return password_hash.hash(password)


def get_user(session: SessionDep, email: str) -> User | None:
    request = select(User).where(User.email == email)
    user = session.exec(request).first()
    return user


def authenticate_user(session: SessionDep, email: str, password: str) -> User | None:
    user = get_user(session, email)
    if not user:
        # useless verify to prevent timing attacks
        password_hash.verify(password=password, hash=DUMMY_HASH)
        return None
    if not password_hash.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(
    user_id: str,
    expires_delta: timedelta | None = None,
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    payload = {"exp": expire, "sub": user_id}
    encoded_jwt = jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(user_id: str):
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return create_access_token(user_id, expires_delta)


def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id_str: str | None = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        return user_id_str
    except jwt.exceptions.InvalidTokenError:
        raise credentials_exception


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> User:

    user_id_str = decode_token(token)
    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise credentials_exception

    user = session.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user


UserDep = Annotated[User, Depends(get_current_user)]
