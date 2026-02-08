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
def create(task: Task, current_user: User = Depends(get_current_user)) -> Task | None:
    """
    Создать новую задачу.
    
    Параметры:
    task (Task): Задача для создания.
    
    Возвращает:
    Task | None: Созданную задачу или None в случае ошибки.
    
    Исключения:
    HTTPException: Если задача с таким именем уже существует (код статуса 409).
    """    
    return service.create(task)
    
@router.get("/")
def get_all(filtr: Filtr = 0, offset: int = 0, page_size: int = 5, current_user: User = Depends(get_current_user)) -> list[TaskResponse] | None:
    try:
        # Проверяем filtr
        if int(filtr.value) > 2:
            raise HTTPException(
                status_code=422, 
                detail=[{
                    "loc": ["query", "filtr"],
                    "msg": "Значение filtr должно быть не больше 2",
                    "type": "value_error"
                }]
            )
        tasks = service.get_all(filtr,offset, page_size)
        return tasks
    except Missing as e:
        raise HTTPException(status_code=422, detail=e.msg)

@router.get("/{name}")
def get_one(name: str, current_user: User = Depends(get_current_user)) -> TaskResponse | None:
    """
    Получить одну задачу по имени.
    
    Параметры:
    name (str): Имя задачи.
    
    Возвращает:
    Task | None: Запрошенную задачу или None, если задача не найдена.
    
    Исключения:
    HTTPException: Если задача с указанным именем не найдена (код статуса 404).
    """
    try:
        return service.get_one(name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)

@router.patch("/")
def update(task: Task, current_user: User = Depends(get_current_user)) -> Task | None:
    """
    Обновить существующую задачу.
    
    Параметры:
    task (Task): Задача с обновлёнными полями.
    
    Возвращает:
    Task | None: Обновленную задачу или None, если произошла ошибка.
    
    Исключения:
    HTTPException: Если задача с указанным именем не найдена (код статуса 404).
    """
    try:
        return service.update(task)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)

@router.delete("/{name}", status_code=204)
def delete(name: str, current_user: User = Depends(get_current_user)):
    """
    Удалить задачу по её имени.
    
    Параметры:
    name (str): Имя удаляемой задачи.
    
    Возвращает:
    bool: True, если удаление прошло успешно.
    
    Исключения:
    HTTPException: Если задача с указанным именем не найдена (код статуса 404).
    """
    try:
        return service.delete(name)
    except Missing as e:
        raise HTTPException(status_code=404, detail=e.msg)