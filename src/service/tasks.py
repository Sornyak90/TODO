from typing import List, Optional
from model.tasks import Task, TaskResponse, Filtr
import data.tasks as data_tasks


async def create(task: Task) -> TaskResponse | None:
    return await data_tasks.create(task)


async def get_all(filtr: Filtr, offset: int, page_size: int) -> Optional[List[TaskResponse]]:
    return await data_tasks.get_all(filtr, offset, page_size)


async def get_one(name: str) -> Optional[TaskResponse]:
    return await data_tasks.get_one(name)


async def update(task: Task) -> Optional[TaskResponse]:
    return await data_tasks.update(task)


async def delete(name: str) -> bool:
    return await data_tasks.delete(name)
