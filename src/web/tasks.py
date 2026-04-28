from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import (
    HTTPBasic, 
    HTTPBasicCredentials, 
    OAuth2PasswordRequestForm
)
from model.tasks import Task, TaskResponse, Tasks, Status
import data.tasks as service
from error import Duplicate, Missing
from typing import Annotated, Tuple
from datetime import timedelta
from auth.auth_jwt import create_access_token, get_current_user

router = APIRouter(prefix="/tasks")

@router.post("/", status_code=201)
async def create(task: Task, current_user: Tasks = Depends(get_current_user)) -> TaskResponse | None:
    return await service.create(task)
    
@router.get("/")
async def get_all(status: Status = 0, offset: int = 0, page_size: int = 5, current_user: Tasks = Depends(get_current_user)) -> list[TaskResponse] | None:
    try:
        if int(status.value) > 2:
            raise HTTPException(
                status_code=422,
                detail=[{
                    "loc": ["query", "status"],
                    "msg": "Значение status должно быть не больше 2",
                    "type": "value_error"
                }]
            )
         # Проверка offset
        if offset < 0:
            raise HTTPException(
                status_code=422,
                detail=[{
                    "loc": ["query", "offset"],
                    "msg": "Значение offset не может быть отрицательным",
                    "type": "value_error"
                }]
            )
        
        # Проверка page_size
        if page_size <= 0:
            raise HTTPException(
                status_code=422,
                detail=[{
                    "loc": ["query", "page_size"],
                    "msg": "Значение page_size должно быть больше 0",
                    "type": "value_error"
                }]
            )
            
        return await service.get_all(status, offset, page_size)
    except Missing as e:
        raise HTTPException(status_code=422, detail=e.msg)

@router.get("/{name}")
async def get_one(name: str, current_user: Tasks = Depends(get_current_user)) -> TaskResponse | None:
    try:
        result = await service.get_one(name)
        if result is None:
            raise Missing(f"Task '{name}' not found")
        return result
    except Missing as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/")
async def update(task: Task, current_user: Tasks = Depends(get_current_user)) -> TaskResponse | None:
    try:
        return await service.update(task)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)


@router.delete("/{name}", status_code=204)
async def delete(name: str, current_user: Tasks = Depends(get_current_user)):
    try:
        result = await service.delete(name)
        if result is False:
            raise Missing(f"Task '{name}' not found")
        return result
    except Missing as e:
        raise HTTPException(status_code=404, detail=str(e))