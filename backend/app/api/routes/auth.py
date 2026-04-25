from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import get_settings
from app.core.security import (
    UserDep,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    get_user,
)
from app.db.database import SessionDep
from app.models.user_model import User, UserCreate, UserSettings

router = APIRouter(prefix="/auth")

settings = get_settings()


@router.post("/register")
def create_user(
    data: UserCreate, remember_me: bool, session: SessionDep
) -> JSONResponse:
    # testing if email is already in use
    other_user = get_user(session=session, email=data.email)
    if other_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="this email address is already registered.",
        )
    # registering to db otherwise
    db_user = User(
        **data.model_dump(exclude={"password"}),
        hashed_password=get_password_hash(data.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    # adding user settings
    user_settings = UserSettings(user_id=db_user.id)
    session.add(user_settings)
    session.commit()
    # jwt token for stateless auth
    user_id = str(db_user.id)
    token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id, remember_me)
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
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    remember_me: bool,
    session: SessionDep,
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
    refresh_token = create_refresh_token(user_id, remember_me)
    response = JSONResponse({"access_token": token, "display_name": user.display_name})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
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


@router.get("/verify")
def verify_token(user: UserDep):
    # UserDep does all the work here
    return {"display_name": user.display_name}
