from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import SessionDep
from app.core.security import (
    Token,
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from app.models.user import User, UserCreate, UserRead

router = APIRouter()


@router.post("/register", response_model=UserRead)
def create_user(data: UserCreate, session: SessionDep) -> Token:
    db_user = User(
        **data.model_dump(),
        hashed_password=get_password_hash(data.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    token = create_access_token(
        db_user.model_dump(exclude={"hashed_password", "email"})
    )
    return Token(access_token=token, token_type="bearer")


@router.get("/login")
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user.model_dump(exclude={"hashed_password", "email"}))
    return Token(access_token=token, token_type="bearer")
