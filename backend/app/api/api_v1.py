# includes the routes in api/v1


from fastapi import APIRouter

from app.api.routes import auth, datasets, ml
from app.core.config import SettingsDep
from app.core.security import UserDep

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(ml.router)
router.include_router(datasets.router)


@router.get("/")
def test(settings: SettingsDep):
    return settings.DATABASE_URL


@router.get("/protected")
def get_user(user: UserDep):
    return user
