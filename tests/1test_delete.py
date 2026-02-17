from tests.conftest import *
import json

def test_delete_existing_task_success(client, auth_token):
    """
    Тест успешного удаления существующей задачи.
    
    Проверяет:
    1. Что DELETE запрос возвращает 204 No Content (успешное удаление)
    2. Что тело ответа пустое (стандарт для 204)
    3. Что после удаления задача больше не доступна через GET (404)
    
    Использует паттерн Arrange-Act-Assert:
    - Arrange: Создаем задачу для удаления
    - Act: Выполняем DELETE запрос
    - Assert: Проверяем результат удаления и доступность задачи
    """
    task_name = "Task_To_Delete"
    task_data = {"name": task_name, "status": False}
    
    # 1. Создаем задачу для теста
    create_response = client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # 2. Удаляем созданную задачу
    delete_response = client.delete(
        f"/tasks/{task_name}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Проверки ответа на удаление
    assert delete_response.status_code == 204  # Стандартный статус для успешного удаления
    assert delete_response.content == b''      # Тело ответа должно быть пустым (bytes)
    assert delete_response.text == ''          # Текст ответа тоже должен быть пустым
    
    # 3. Проверяем, что задача действительно удалена
    get_response = client.get(
        f"/tasks/{task_name}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert get_response.status_code == 404  # Задача не должна больше существовать
   
def test_delete_unauthorized(client, auth_token):
    """
    Тест ошибок авторизации при удалении задачи.
    
    Проверяет два сценария:
    1. DELETE запрос без заголовка Authorization
    2. DELETE запрос с невалидным токеном
    
    Ожидается, что оба вернут 401 Unauthorized.
    Также проверяется, что задача НЕ удаляется при неудачной авторизации.
    """
    task_name = "Task_To_Delete"
    task_data = {"name": task_name, "status": False}
    
    # Создаем задачу один раз для всех проверок в этом тесте
    create_response = client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Сценарий 1: DELETE без заголовка Authorization
    delete_response = client.delete(f"/tasks/{task_name}")
    assert delete_response.status_code == 401  # Должна быть ошибка авторизации
    
    # Сценарий 2: DELETE с невалидным токеном
    delete_response = client.delete(
        f"/tasks/{task_name}",
        headers={"Authorization": "Bearer invalid_token_123"}
    )
    assert delete_response.status_code == 401  # Тоже должна быть ошибка авторизации
    
    # Важная проверка: задача все еще должна существовать
    # (не должна была быть удалена из-за ошибок авторизации)
    get_response = client.get(
        f"/tasks/{task_name}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert get_response.status_code == 200  # Задача доступна (не удалена)

def test_delete_nonexistent_task(client, auth_token):
    """
    Тест попытки удалить несуществующую задачу.
    
    Проверяет, что API возвращает 404 Not Found при попытке
    удалить задачу, которой не существует в системе.
    """
    non_existent_name = "NonExistent_Task_12345"
    
    delete_response = client.delete(
        f"/tasks/{non_existent_name}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert delete_response.status_code == 404  # Ожидаем 404 (не найдено)

def test_delete_already_deleted_task(client, auth_token):
    """
    Тест попытки удалить уже удаленную задачу.
    
    Проверяет идемпотентность операции DELETE:
    - Первое удаление должно вернуть 204 (успех)
    - Повторное удаление той же задачи должно вернуть 404
    
    Это соответствует RESTful принципам: повторный DELETE
    несуществующего ресурса может возвращать 404.
    """
    # 1. Создаем задачу
    task_name = "Task_Already_Deleted"
    task_data = {"name": task_name, "status": False}
    
    create_response = client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert create_response.status_code == 201  # Успешное создание
    
    # 2. Первое удаление (должно быть успешным)
    delete_response = client.delete(
        f"/tasks/{task_name}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert delete_response.status_code == 204  # Успешное удаление
    
    # 3. Второе удаление той же задачи (должно вернуть 404)
    delete_response2 = client.delete(
        f"/tasks/{task_name}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert delete_response2.status_code == 404  # Задача уже не существует