from tests.conftest import *  
import uuid

async def test_create_successful(client, auth_token):
    """Тест успешного создания задачи (201 Created)"""
    unique_id = str(uuid.uuid4())[:8]
    task_name = f"Task_Create_{unique_id}"  # Уникальное имя задачи
    task_data = {
        "name": task_name,
        "status": False,
    }

    response = await client.post(
        "/tasks/", 
        json=task_data,  
        headers={"Authorization": f"Bearer {auth_token}"}  
    )

    # Проверка успешного создания
    assert response.status_code == 201
    assert response.json()["name"] == task_data["name"]
    assert response.json()["status"] == task_data["status"]

async def test_error_auth(client, expired_token):
    """Тест ошибок авторизации при создании задачи (401)"""
    
    unique_id = str(uuid.uuid4())[:8]
    task_name = f"Task_Create_{unique_id}"
    task_data = {
        "name": task_name,
        "status": False,
    }

    # Сценарий 1: Запрос без токена -> 401
    patch_response = await client.post(
        "/tasks/",
        json=task_data
    )
    assert patch_response.status_code == 401  

    # Сценарий 2: Запрос с неверным токеном -> 401
    patch_response = await client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": "Bearer invalid_token_123"}
    )
    assert patch_response.status_code == 401  

    # Сценарий 3: Запрос с просроченным токеном -> 401
    response = await client.post(
        "/tasks/", 
        json=task_data,  
        headers={"Authorization": f"Bearer {expired_token}"}  
    )
    assert response.status_code == 401  

async def test_input_data_validation(client, auth_token):
    """Тест валидации входных данных (422)"""
    
    # Тест 1: Пустые значения name и status -> 422
    response = await client.post(
        "/tasks/",
        json={"name": "", "status": ""},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422  

    # Тест 2: Неверные типы данных (name и status - строки, а нужны str и bool) -> 422
    response = await client.post(
        "/tasks/",
        json={"name": "333", "status": "333"},  # status должен быть boolean
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422  

async def test_business_logic(client, auth_token):
    """Тест бизнес-логики: создание дубликата задачи -> 409 Conflict"""
    
    unique_id = str(uuid.uuid4())[:8]
    task_name = f"Task_Duplicate_{unique_id}"
    task_data = {
        "name": task_name,
        "status": False,
    }

    # Первое создание задачи -> успех (201)
    response = await client.post(
        "/tasks/", 
        json=task_data,  
        headers={"Authorization": f"Bearer {auth_token}"}  
    )
    assert response.status_code == 201

    # Второе создание задачи с тем же именем -> 409 Conflict (дубликат)
    response = await client.post(
        "/tasks/", 
        json=task_data,  
        headers={"Authorization": f"Bearer {auth_token}"} 
    )
    assert response.status_code == 409  # Конфликт: задача с таким именем уже существует