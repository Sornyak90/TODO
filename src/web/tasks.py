from fastapi import APIRouter
from model.tasks import Task
import service.tasks as service


router = APIRouter(prefix="/tasks")


@router.post("/")
def create(task: Task) -> Task | None:
    return service.create(task)


# @router.get("/")
# def get_all():
#     return service.get_all


@router.get("/{id}")
def get_one(id) -> Task | None:
    return service.get_one(id)


# @router.patch("/")
# def update(task: Task) -> Task:
#     return service.update(task)


# @router.put("/")
# def replace(task: Task) -> Task:
#     return service.replace(task)


# @router.delete("/{id}")
# def delete(id) -> bool:
#     return None
