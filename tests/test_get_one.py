from tests.token_and_data import *
import json

# Импортируются тестовые данные: токены и тестовые данные для БД
# token - предположительно валидный токен для тестов

def test_get_existing_task():
    """
    Тест успешного получения существующей задачи.
    
    Проверяет:
    1. Что эндпоинт возвращает 200 OK для существующей задачи
    2. Что возвращаемый JSON содержит обязательные поля
    3. Что данные задачи соответствуют ожидаемым
    4. Что статус задачи правильный (в данном случае False - завершенная)
    """
    task_name = "TestTask_GetOne"  # Имя тестовой задачи, которая должна существовать в БД
    
    # Отправляем GET запрос для получения конкретной задачи по имени
    response = client.get(
        f"/tasks/{task_name}",  # URL: /tasks/TestTask_GetOne
        headers={"Authorization": f"Bearer {token}"}  # С валидным токеном
    )
    
    # Проверка 1: Статус код должен быть 200 (успех)
    assert response.status_code == 200
    
    # Парсим JSON ответ
    task = response.json()
    
    # Проверка 2: В ответе должны быть все обязательные поля задачи
    assert "id" in task          # ID задачи (уникальный идентификатор)
    assert "name" in task        # Имя задачи (должно совпадать с запрошенным)
    assert "status" in task      # Статус задачи (True/False)
    
    # Проверка 3: Имя задачи должно совпадать с запрошенным
    assert task["name"] == task_name
    
    # Проверка 4: Статус должен быть False (предположительно "завершено")
    # В контексте задачи: True = активная, False = завершенная
    assert task["status"] == False


def test_get_nonexistent_task():
    """
    Тест попытки получения несуществующей задачи.
    
    Проверяет:
    1. Что API возвращает 404 Not Found для несуществующей задачи
    2. Корректность обработки отсутствующих записей
    """
    non_existent_name = "NonExistentTask_12345"  # Случайное имя, которого точно нет в БД
    
    response = client.get(
        f"/tasks/{non_existent_name}",  # Запрос несуществующей задачи
        headers={"Authorization": f"Bearer {token}"}  # С валидным токеном
    )
    
    # Проверка: должен вернуться 404 (не найдено)
    assert response.status_code == 404
    # Можно также проверить тело ответа:
    # error_detail = response.json()
    # assert "detail" in error_detail
    # assert "not found" in error_detail["detail"].lower()


def test_get_task_unauthorized():
    """
    Тест доступа к задаче без авторизации или с невалидным токеном.
    
    Проверяет два сценария:
    1. Запрос без заголовка Authorization
    2. Запрос с невалидным/истекшим токеном
    
    Оба должны возвращать 401 Unauthorized
    """
    task_name = "TestTask_GetOne"  # Существующая задача
    
    # Сценарий 1: Полный запрос без заголовка Authorization
    response = client.get(f"/tasks/{task_name}")
    # Проверка: должен вернуться 401 (не авторизован)
    assert response.status_code == 401
    
    # Сценарий 2: Запрос с невалидным токеном
    response = client.get(
        f"/tasks/{task_name}",
        headers={"Authorization": "Bearer invalid_token_123"}  # Заведомо неверный токен
    )
    # Проверка: тоже должен вернуться 401
    assert response.status_code == 401
    