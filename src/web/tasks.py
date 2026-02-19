from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import (
    HTTPBasic, 
    HTTPBasicCredentials, 
    OAuth2PasswordRequestForm
)
from model.tasks import Task, TaskResponse, User, Filtr
import data.tasks as service
from error import Duplicate, Missing
from typing import Annotated, Tuple
from datetime import timedelta
from auth.fake_db import fake_users
from auth.auth_jwt import create_access_token, get_current_user

router = APIRouter(prefix="/tasks")

@router.post("/", status_code=201)
async def create(task: Task, current_user: User = Depends(get_current_user)) -> TaskResponse | None:
    return await service.create(task)
    
@router.get("/")
async def get_all(filtr: Filtr = 0, offset: int = 0, page_size: int = 5, current_user: User = Depends(get_current_user)) -> list[TaskResponse] | None:
    try:
        if int(filtr.value) > 2:
            raise HTTPException(
                status_code=422,
                detail=[{
                    "loc": ["query", "filtr"],
                    "msg": "Значение filtr должно быть не больше 2",
                    "type": "value_error"
                }]
            )
        return await service.get_all(filtr, offset, page_size)
    except Missing as e:
        raise HTTPException(status_code=422, detail=e.msg)

@router.get("/{name}")
async def get_one(name: str, current_user: User = Depends(get_current_user)) -> TaskResponse | None:
    try:
        result = await service.get_one(name)
        if result is None:
            raise Missing(f"Task '{name}' not found")
        return result
    except Missing as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/")
async def update(task: Task, current_user: User = Depends(get_current_user)) -> Task | None:
    try:
        return await service.update(task)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)

@router.delete("/{name}", status_code=204)
async def delete(name: str, current_user: User = Depends(get_current_user)):
    try:
        result = await service.delete(name)
        if result is False:
            raise Missing(f"Task '{name}' not found")
        return result
    except Missing as e:
        raise HTTPException(status_code=404, detail=str(e))