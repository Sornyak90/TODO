from fastapi import APIRouter
from sqlalchemy import select

from . import get_session_engine, User


router = APIRouter(prefix="/db")

@router.get("/{name}")
async def get_user(name: str):
    AsyncSessionLocal, _ = get_session_engine()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.name == name))
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return User(id=row.id, name=row.name, password=row.password)

@router.post("/")
async def create_user():
    pass

@router.patch("/")
async def update_user():
    pass

@router.delete("/")
async def delete_user():
    pass