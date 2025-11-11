from typing import List, Optional
from model.tasks import Task, UserFullModel
import data.tasks as service


def create(task: Task) -> Task | None:
    """Создает новую задачу и возвращает созданную задачу.

    Args:
        task (Task): Объект задачи для сохранения.

    Returns:
        Optional[Task]: Новая созданная задача или None, если создание невозможно.
    """
    return service.create(task)


def get_all() -> Optional[List[Task]]:
    """Получает список всех существующих задач.

    Returns:
        Optional[List[Task]]: Список всех задач или None, если нет задач.
    """
    return service.get_all()


def get_one(name: str) -> Optional[Task]:
    """Получает отдельную задачу по указанному названию.

    Args:
        name (str): Название задачи.

    Returns:
        Optional[Task]: Найденная задача или None, если задача не найдена.
    """
    return service.get_one(name)


def update(task: Task) -> Optional[Task]:
    """Обновляет существующий объект задачи.

    Args:
        task (Task): Объект задачи с новыми значениями полей.

    Returns:
        Optional[Task]: Обновленная задача или None, если обновление невозможно.
    """
    return service.update(task)


def delete(name: str):
    """Удаляет задачу по указанному названию.

    Args:
        name (str): Название задачи для удаления.

    Returns:
        bool: True, если задача была успешно удалена, иначе False.
    """
    return service.delete(name)

def validate_credentials(username: str, password: str) -> UserFullModel | None:
    for user in users.values():
        if user.username == username and sha256_crypt.verify(
            password, user.password_hash
        ):
            return user
    return None