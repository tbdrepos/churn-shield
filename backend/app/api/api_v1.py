# includes the routes in api/v1
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.routes import auth
from app.core.config import Settings
from app.core.dependencies import get_settings

router = APIRouter()

router.include_router(auth.router)


@router.get("/")
def test(settings: Annotated[Settings, Depends(get_settings)]):
    return settings.database_url
