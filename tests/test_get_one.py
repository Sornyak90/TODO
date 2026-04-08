from tests.conftest import *
import json
import uuid


async def test_get_existing_task(client, auth_token):
    """Тест успешного получения существующей задачи"""
    
    unique_id = str(uuid.uuid4())[:8]
    task_name = f"Task_To_Get_{unique_id}"  # Уникальное имя задачи
    task_data = {
        "name": task_name,
        "status": False,
    }

    # Создаем задачу перед получением
    response = await client.post(
            "/tasks/", 
            json=task_data, 
            headers={"Authorization": f"Bearer {auth_token}"}  
        )
    
    # GET запрос существующей задачи
    response = await client.get(
        f"/tasks/{task_name}",  
        headers={"Authorization": f"Bearer {auth_token}"} 
    )
    
    # Проверка успешного статуса
    assert response.status_code == 200
    
    # Получаем JSON ответа
    task = response.json()
    
    # Проверка наличия обязательных полей
    assert "id" in task        # ID задачи
    assert "name" in task      # Имя задачи
    assert "status" in task    # Статус задачи
    
    # Проверка соответствия имени
    assert task["name"] == task_name
    
    # Проверка статуса (False = завершена)
    assert task["status"] == False

async def test_get_nonexistent_task(client, auth_token):
    """Тест получения несуществующей задачи -> 404"""
    
    non_existent_name = "NonExistentTask_12345"  # Заведомо несуществующее имя
    
    response = await client.get(
        f"/tasks/{non_existent_name}", 
        headers={"Authorization": f"Bearer {auth_token}"}  
    )
    
    # Должен вернуться 404 Not Found
    assert response.status_code == 404
    
async def test_get_task_unauthorized(client, auth_token):
    """Тест доступа к задаче без авторизации -> 401"""
    
    unique_id = str(uuid.uuid4())[:8]
    task_name = f"Task_To_Get_{unique_id}"
    task_data = {
        "name": task_name,
        "status": False,
    }

    # Создаем задачу для теста
    response = await client.post(
        "/tasks/", 
        json=task_data,  
        headers={"Authorization": f"Bearer {auth_token}"}  
    )

    # Сценарий 1: GET запрос без токена
    response = await client.get(f"/tasks/{task_name}")
    assert response.status_code == 401  # Не авторизован
    
    # Сценарий 2: GET запрос с неверным токеном
    response = await client.get(
        f"/tasks/{task_name}",
        headers={"Authorization": "Bearer invalid_token_123"}  
    )
    assert response.status_code == 401  # Не авторизован