from fastapi import APIRouter, HTTPException

from app.core.security import (
    UserDep,
)
from app.db.database import SessionDep
from app.models.user_model import UserRead, UserSettings

router = APIRouter(prefix="/account")


@router.get("/me")
def get_account_info(user: UserDep, session: SessionDep):
    user_settings = session.get(UserSettings, user.id)
    if not user_settings:
        raise HTTPException(404, detail="User settings not found")

    return {"user_info": UserRead(**user.model_dump()), "settings": user_settings}


@router.patch("/settings")
def update_settings(user_settings: UserSettings, user: UserDep, session: SessionDep):
    db_settings = session.get(UserSettings, user.id)
    if not db_settings:
        raise HTTPException(404, detail="User settings not found")
    settings_data = user_settings.model_dump(exclude_unset=True)
    db_settings.sqlmodel_update(settings_data)
    session.add(db_settings)
    session.commit()
    session.refresh(db_settings)
    return db_settings
