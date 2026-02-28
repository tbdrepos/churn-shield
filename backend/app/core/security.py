from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from pwdlib import PasswordHash
from pydantic import BaseModel
from sqlmodel import select

from app.core.dependencies import SessionDep, oauth2_scheme, settings
from app.models.user import User

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy_password")


class Token(BaseModel):
    access_token: str
    token_type: str


def get_password_hash(password: str):
    return password_hash.hash(password)


def get_user(session: SessionDep, username: str) -> User | None:
    request = select(User).where(User.username == username)
    user = session.exec(request).first()
    return user


def authenticate_user(session: SessionDep, username: str, password: str) -> User | None:
    user = get_user(session, username)
    if not user:
        # useless verify to prevent timing attacks that enumerate existing usernames
        password_hash.verify(password=password, hash=DUMMY_HASH)
        return None
    if not password_hash.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire, "sub": data["username"]})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


async def get_current_user(
    session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.jwt_key, algorithms=[settings.jwt_algorithm]
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.exceptions.InvalidTokenError:
        raise credentials_exception
    user = get_user(session, username)
    if user is None:
        raise credentials_exception
    return user
