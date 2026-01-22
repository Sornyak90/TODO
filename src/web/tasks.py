from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import (
    HTTPBasic, 
    HTTPBasicCredentials, 
    OAuth2PasswordRequestForm
)
from model.tasks import Task, TaskResponse, User, Filtr
import service.tasks as service
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
def get_all(filtr: Filtr, current_user: User = Depends(get_current_user)) -> list[TaskResponse] | None:
    """
    Получить список всех задач.
    
    Возвращает:
    list[Task] | None: Список всех задач или None, если задач нет.
    """
    return service.get_all(filtr)

@router.get("/{page}")
def get_pages(filtr: Filtr, page: int, current_user: User = Depends(get_current_user)) -> Tuple[list[TaskResponse], int] | None:
    """
    Получить список всех задач.
    
    Возвращает:
    list[Task] | None: Список всех задач или None, если задач нет.
    """
    tasks, pages = service.get_pages(filtr, page)
    return tasks, pages

@router.get("/{name}")
def get_one(name: str, current_user: User = Depends(get_current_user)) -> Task | None:
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