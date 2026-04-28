from model.tasks import Task, TaskResponse, Status
from error import Duplicate, Missing
from . import get_session_engine, Tasks
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from fastapi import HTTPException


async def create(task: Task) -> TaskResponse | None:
    AsyncSessionLocal, _ = get_session_engine()
    try:
        async with AsyncSessionLocal() as session:
            row = Tasks(name=task.name, status=task.status)
            session.add(row)
            await session.commit()
            await session.refresh(row)
            return TaskResponse(id=row.id, name=row.name, status=row.status)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))


async def get_one(name: str) -> TaskResponse | None:
    AsyncSessionLocal, _ = get_session_engine()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Tasks).where(Tasks.name == name))
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return TaskResponse(id=row.id, name=row.name, status=row.status)


async def get_all(status: Status, offset: int, page_size: int) -> list[TaskResponse]:
    AsyncSessionLocal, _ = get_session_engine()
    async with AsyncSessionLocal() as session:
        q = select(Tasks)
        if status == Status.true:
            q = q.where(Tasks.status == True)
        elif status == Status.false:
            q = q.where(Tasks.status == False)
        q = q.offset(offset).limit(page_size)
        result = await session.execute(q)
        rows = result.scalars().all()
        return [TaskResponse(id=r.id, name=r.name, status=r.status) for r in rows]


async def delete(name: str) -> bool:
    AsyncSessionLocal, _ = get_session_engine()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Tasks).where(Tasks.name == name))
        row = result.scalar_one_or_none()
        if row is None:
            return False
        await session.delete(row)
        await session.flush()
        await session.commit()

        return True


async def update(task: Task) -> TaskResponse | None:
    AsyncSessionLocal, _ = get_session_engine()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Tasks).where(Tasks.name == task.name))
        row = result.scalar_one_or_none()
        if row is None:
            raise Missing(f"Задача с именем '{task.name}' не найдена")
        row.status = task.status
        await session.commit()
        await session.refresh(row)
        return TaskResponse(id=row.id, name=row.name, status=row.status)
