import loguru
from fastapi import APIRouter, HTTPException, status

from app.core.security import UserDep, update_user
from app.db.database import SessionDep
from app.models.user_model import UserRead, UserSettings, UserUpdate

loguru.logger.add("logs/account.log", rotation="10 MB", level="INFO")

router = APIRouter(prefix="/account")


@router.get("/me")
def get_account_info(user: UserDep, session: SessionDep):
    user_settings = session.get(UserSettings, user.id)
    if not user_settings:
        raise HTTPException(404, detail="User settings not found")
    return {"user_info": UserRead(**user.model_dump()), "settings": user_settings}


@router.patch("/info")
def update_info(user_update: UserUpdate, user: UserDep, session: SessionDep):
    try:
        return update_user(session, user, user_update)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"update failed {Exception}"
        )


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


@router.delete("/delete")
def delete_user(user: UserDep, session: SessionDep):
    session.delete(user)
    session.commit()
    return {"ok": True}
