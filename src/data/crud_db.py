from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from . import get_session_engine, User
from model.tasks import Users, UsersResponse

async def get_user(username: str) -> dict:
    AsyncSessionLocal, _ = get_session_engine()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.username == username))
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return {
            "id": row.id,
            "username": row.username,
            "password": row.password
        }

async def create_user(user: Users) -> UsersResponse:
    AsyncSessionLocal, _ = get_session_engine()
    try:
        async with AsyncSessionLocal() as session:
            row = User(username=user.username, password=user.password)
            session.add(row)
            await session.commit()
            await session.refresh(row)
            return UsersResponse(id=row.id, username=row.username, password=row.password)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))

async def update_user(username: str, password: str) -> bool:
    AsyncSessionLocal, _ = get_session_engine()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.username == username))
        row = result.scalar_one_or_none()
        if row is None:
            return False
        row.password = password
        await session.commit()

        return True

async def delete_user(username: str) -> bool:
    AsyncSessionLocal, _ = get_session_engine()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.username == username))
        row = result.scalar_one_or_none()
        if row is None:
            return False
        await session.delete(row)
        await session.flush()
        await session.commit()

        return True