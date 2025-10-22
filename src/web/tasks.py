from fastapi import APIRouter, status, HTTPException
from model.tasks import Task
import service.tasks as service


router = APIRouter(prefix="/tasks")


@router.post("/",status_code=status.HTTP_201_CREATED)
def create(task: Task) -> Task | None:
    return service.create(task)


@router.get("/")
def get_all():
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Task | None:
    return service.get_one(name)


@router.patch("/")
def update(task: Task):
    return service.update(task)

@router.delete("/{name}",status_code=status.HTTP_204_NO_CONTENT)
def delete(name: str):
    return service.delete(name)


class TaskConflictException(HTTPException):
    def __init__(self, detail: str = "Task already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )
