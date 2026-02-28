# includes the routes in api/v1


from fastapi import APIRouter

from app.api.routes import auth
from app.core.dependencies import settings

router = APIRouter()

router.include_router(auth.router)


@router.get("/")
def test():
    return settings.database_url
