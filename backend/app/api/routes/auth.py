from fastapi import APIRouter, HTTPException

from app.db.database import SessionDep
from app.models.user import User, UserCreate, UserRead

router = APIRouter()


@router.post("/register", response_model=UserRead)
def create_user(data: UserCreate, session: SessionDep):
    db_user = User.model_validate(data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"user:{user_id} not found")
    return user
