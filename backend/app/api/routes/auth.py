from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    get_user,
)
from app.db.database import SessionDep
from app.models.user import User, UserCreate

router = APIRouter(prefix="/auth")


@router.post("/register")
def create_user(data: UserCreate, session: SessionDep) -> JSONResponse:
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
    user_id = str(db_user.id)
    token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    response = JSONResponse(
        {"access_token": token, "display_name": db_user.display_name}
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return response


@router.post("/login")
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> JSONResponse:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = str(user.id)
    token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    response = JSONResponse({"access_token": token, "display_name": user.display_name})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return response


@router.post("/refresh")
def refresh_token(request: Request):

    refresh_token = request.cookies.get("refresh_token")

    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token in request cookie",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = decode_token(refresh_token)

    new_access_token = create_access_token(user_id)

    return {"access_token": new_access_token}
