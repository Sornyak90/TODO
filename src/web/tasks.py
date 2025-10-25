from fastapi import APIRouter, HTTPException
from model.tasks import Task
import service.tasks as service
from error import Duplicate, Missing


router = APIRouter(prefix="/tasks")


@router.post("/", status_code=201)
def create(task: Task) -> Task | None:
    try:
        return service.create(task)
    except Duplicate as e:
        raise HTTPException(status_code=409, detail=e.msg)


@router.get("/")
def get_all():
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Task | None:
    try:
        return service.get_one(name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.patch("/")
def update(task: Task):
    try:
        return service.update(task)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.delete("/{name}", status_code=204)
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)
