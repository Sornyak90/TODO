from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import (
    HTTPBasic, 
    HTTPBasicCredentials, 
    OAuth2PasswordRequestForm
)
from model.tasks import Task, TaskResponse, Users, UsersResponse, Status
import data.tasks as service
import data.crud_db as crud_db
from error import Duplicate, Missing
from typing import Annotated, Tuple
from datetime import timedelta
from auth.auth_jwt import create_access_token, get_current_user

router_task = APIRouter(prefix="/tasks")
router_db = APIRouter(prefix="/db")

@router_task.post("/", status_code=201)
async def create(task: Task, current_user: Users = Depends(get_current_user)) -> TaskResponse | None:
    return await service.create(task)
    
@router_task.get("/")
async def get_all(status: Status = 0, offset: int = 0, page_size: int = 5, current_user: Users = Depends(get_current_user)) -> list[TaskResponse] | None:
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

@router_task.get("/{name}")
async def get_one(name: str, current_user: Users = Depends(get_current_user)) -> TaskResponse | None:
    try:
        result = await service.get_one(name)
        if result is None:
            raise Missing(f"Task '{name}' not found")
        return result
    except Missing as e:
        raise HTTPException(status_code=404, detail=str(e))

@router_task.patch("/")
async def update(task: Task, current_user: Users = Depends(get_current_user)) -> TaskResponse | None:
    try:
        return await service.update(task)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)

@router_task.delete("/{name}", status_code=204)
async def delete(name: str, current_user: Users = Depends(get_current_user)):
    try:
        result = await service.delete(name)
        if result is False:
            raise Missing(f"Task '{name}' not found")
        return result
    except Missing as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_db.post("/", status_code=201)
async def create_user(user: Users) -> UsersResponse:
    return await crud_db.create_user(user)

@router_db.get("/{name}")
async def get_user(name: str) -> dict | None:
    return await crud_db.get_user(name)

@router_db.delete("/{name}", status_code=204)
async def delete_user(name: str, current_user: Users = Depends(get_current_user)):
    try:
        result = await crud_db.delete_user(name)
        if result is False:
            raise Missing(f"User '{name}' not found")
        return result
    except Missing as e:
        raise HTTPException(status_code=404, detail=str(e))

@router_db.patch("/{name}")
async def update_user(name: str, password: str, current_user: Users = Depends(get_current_user)) -> bool:
    try:
        return await crud_db.update_user(name, password)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)