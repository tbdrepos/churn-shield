from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import (
    Token,
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_user,
)
from app.db.database import SessionDep
from app.models.user import User, UserCreate

router = APIRouter(prefix="/auth")


@router.post("/register")
def create_user(data: UserCreate, session: SessionDep) -> Token:
    db_user = User(
        **data.model_dump(),
        hashed_password=get_password_hash(data.password),
    )
    # testing if email is already in use
    other_user = get_user(session=session, email=db_user.email)
    if other_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="this email address is already registered.",
        )
    # registering to db otherwise
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    # jwt token for stateless auth
    token = create_access_token(
        db_user.model_dump(exclude={"hashed_password", "email"})
    )
    return Token(access_token=token, token_type="bearer")


@router.post("/login")
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user.model_dump(exclude={"hashed_password", "email"}))
    return Token(access_token=token, token_type="bearer")
