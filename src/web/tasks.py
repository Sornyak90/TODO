from fastapi import APIRouter
from model.tasks import Task
import data.tasks as tasks


router = APIRouter(prefix="/tasks")


@router.post("/")
def create(task: Task) -> Task:
    return service.create(task)


@router.get("/")
def get_all() -> list(Task):
    return service.get_all


@router.get("/{id}")
def get_one(id) -> Task | None:
    return service.get_one


@router.patch("/")
def update(task: Task) -> Task:
    return service.update(task)


@router.put("/")
def replace(task: Task) -> Task:
    return service.replace(task)


@router.delete("/{id}")
def delete(id) -> bool:
    return None
