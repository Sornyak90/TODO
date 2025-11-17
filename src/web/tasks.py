from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from model.tasks import Task, TaskResponse, User
import service.tasks as service
from error import Duplicate, Missing
from auth.auth_jwt import authenticate_user, get_current_user
from typing import Annotated
from datetime import timedelta
from auth.config import ACCESS_TOKEN_EXPIRE_MINUTES
from auth.auth_jwt import create_access_token, authenticate_user


router = APIRouter(prefix="/tasks")


@router.post("/login")
def login(user: User) -> bool:
    if authenticated_user := authenticate_user(user.username, user.password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        print(authenticated_user)
        access_token = create_access_token(
        data={"sub": authenticated_user.username}, expires_delta=access_token_expires
    )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return read_users_me


@router.get("/users/me/")
def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):    
    return current_user


@router.post("/", status_code=201)
def create(task: Task) -> Task | None:
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
def get_all() -> list[TaskResponse] | None:
    """
    Получить список всех задач.
    
    Возвращает:
    list[Task] | None: Список всех задач или None, если задач нет.
    """
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Task | None:
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
def update(task: Task) -> Task | None:
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
def delete(name: str):
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