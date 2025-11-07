from model.tasks import Task, TaskResponse
from error import Duplicate, Missing
from . import Session, User


def create(task: Task) -> Task | None:
    # """
    # Добавляет новую задачу в базу данных.
    
    # Args:
    #     task (Task): Задача для добавления.
        
    # Raises:
    #     Duplicate: Если задача с таким именем уже существует.
        
    # Returns:
    #     Task | None: Новая созданная задача или None, если возникла ошибка.
    # """
    with Session() as session:
        task = User(name=task.name, status=task.status)
        print(task.id)
        session.add(task)
        session.commit()
    return None

def get_one(name: str) -> Task | None:
    # """
    # Получает одну задачу по имени.
    
    # Args:
    #     name (str): Имя задачи.
        
    # Raises:
    #     Missing: Если задача с данным именем не найдена.
        
    # Returns:
    #     Task | None: Найденная задача или None, если произошла ошибка.
    # """
    with Session() as session:
        task = session.query(User).filter_by(name=name).first()
        return task
    

def get_all() -> list[Task]:
    # """
    # Возвращает список всех задач.
    
    # Returns:
    #     list[Task]: Список объектов Task.
    # """
    with Session() as session:
        tasks = session.query(User).all()
        return tasks
    

def delete(name: str):
    # """
    # Удаляет задачу по её имени.
    
    # Args:
    #     name (str): Имя удаляемой задачи.
        
    # Raises:
    #     Missing: Если задача с указанным именем не найдена.
        
    # Returns:
    #     bool: Результат операции удаления.
    # """
     with Session() as session:
        task_to_delete = session.query(User).filter_by(name=name).first()
        
        if task_to_delete:
            session.delete(task_to_delete)
            session.commit()
            return True
        else:
            return False
    

def update(task: Task) -> Task | None:
    # """
    # Обновляет статус задачи.
    
    # Args:
    #     task (Task): Задача с обновленным статусом.
        
    # Raises:
    #     Missing: Если задача с указанным именем не найдена.
        
    # Returns:
    #     Task | None: Обновленная задача или None, если возникла ошибка.
    # """
    with Session.begin() as session:
        update_task = session.query(User).filter_by(name=task.name).first()
    
        if update_task:
            update_task.status = task.status
            
            session.commit()
            return update_task
        else:
            return None
