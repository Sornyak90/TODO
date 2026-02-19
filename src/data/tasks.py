from model.tasks import Task, TaskResponse, Filtr
from error import Duplicate, Missing
from . import AsyncSessionLocal, User
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from fastapi import HTTPException


async def create(task: Task) -> TaskResponse | None:
    try:
        async with AsyncSessionLocal() as session:
            row = User(name=task.name, status=task.status)
            session.add(row)
            await session.commit()
            await session.refresh(row)
            return TaskResponse(id=row.id, name=row.name, status=row.status)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))


async def get_one(name: str) -> TaskResponse | None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.name == name))
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return TaskResponse(id=row.id, name=row.name, status=row.status)


async def get_all(filtr: Filtr, offset: int, page_size: int) -> list[TaskResponse]:
    async with AsyncSessionLocal() as session:
        q = select(User)
        if filtr == Filtr.true:
            q = q.where(User.status == True)
        elif filtr == Filtr.false:
            q = q.where(User.status == False)
        q = q.offset(offset).limit(page_size)
        result = await session.execute(q)
        rows = result.scalars().all()
        return [TaskResponse(id=r.id, name=r.name, status=r.status) for r in rows]


async def delete(name: str) -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.name == name))
        row = result.scalar_one_or_none()
        if row is None:
            return False
        session.delete(row)
        await session.commit()
        return True


async def update(task: Task) -> TaskResponse | None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.name == task.name))
        row = result.scalar_one_or_none()
        if row is None:
            raise Missing(f"Задача с именем '{task.name}' не найдена")
        row.status = task.status
        await session.commit()
        await session.refresh(row)
        return TaskResponse(id=row.id, name=row.name, status=row.status)
