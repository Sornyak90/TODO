from fastapi import APIRouter, HTTPException
from model.tasks import Task
import service.tasks as service
from error import Duplicate, Missing


router = APIRouter(prefix="/tasks")


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
    try:
        return service.create(task)
    except Duplicate as e:
        raise HTTPException(status_code=409, detail=e.msg)


@router.get("/")
def get_all() -> list[Task] | None:
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