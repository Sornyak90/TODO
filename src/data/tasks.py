from . import curs, conn, IntegrityError
from model.tasks import Task, TaskResponse
from error import Duplicate, Missing

# Создаем таблицу 'tasks', если она не существует
curs.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    status BOOLEAN DEFAULT FALSE
                )
                """)

def model_to_dict(task: Task) -> dict:
    """
    Преобразует объект модели Task в словарь Python.
    
    Args:
        task (Task): Объект модели Task.
        
    Returns:
        dict: Словарь, представляющий поля модели Task.
    """
    return task.dict() if task else None

def row_to_model(row: tuple) -> TaskResponse:
    """
    Преобразует кортеж SQL-записи в объект модели TaskResponse.
    
    Args:
        row (tuple): Кортеж записей таблицы tasks.
        
    Returns:
        TaskResponse: Экземпляр класса TaskResponse.
    """
    id, name, status = row
    return TaskResponse(id=id, name=name, status=status)

def create(task: Task) -> Task | None:
    """
    Добавляет новую задачу в базу данных.
    
    Args:
        task (Task): Задача для добавления.
        
    Raises:
        Duplicate: Если задача с таким именем уже существует.
        
    Returns:
        Task | None: Новая созданная задача или None, если возникла ошибка.
    """
    qry = """INSERT INTO tasks (name, status) VALUES 
            (:name, :status)"""
    params = model_to_dict(task)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(msg=f"Задача '{task.name}' уже существует.")
    return get_one(task.name)

def get_one(name: str) -> Task | None:
    """
    Получает одну задачу по имени.
    
    Args:
        name (str): Имя задачи.
        
    Raises:
        Missing: Если задача с данным именем не найдена.
        
    Returns:
        Task | None: Найденная задача или None, если произошла ошибка.
    """
    qry = "SELECT * FROM tasks WHERE name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Задача '{name}' не найдена.")

def get_all() -> list[Task]:
    """
    Возвращает список всех задач.
    
    Returns:
        list[Task]: Список объектов Task.
    """
    qry = "SELECT * FROM tasks"
    curs.execute(qry)
    rows = curs.fetchall()
    return [row_to_model(row) for row in rows]

def delete(name: str) -> bool:
    """
    Удаляет задачу по её имени.
    
    Args:
        name (str): Имя удаляемой задачи.
        
    Raises:
        Missing: Если задача с указанным именем не найдена.
        
    Returns:
        bool: Результат операции удаления.
    """
    qry = "DELETE FROM tasks WHERE name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Задача '{name}' не найдена.")
    conn.commit()
    return True

def update(task: Task) -> Task | None:
    """
    Обновляет статус задачи.
    
    Args:
        task (Task): Задача с обновленным статусом.
        
    Raises:
        Missing: Если задача с указанным именем не найдена.
        
    Returns:
        Task | None: Обновленная задача или None, если возникла ошибка.
    """
    qry = """UPDATE tasks SET status = :status WHERE name = :name"""
    params = model_to_dict(task)
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Задача '{task.name}' не найдена.")
    conn.commit()
    return get_one(task.name)