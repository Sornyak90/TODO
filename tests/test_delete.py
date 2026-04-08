from tests.conftest import *
import json
import uuid

async def test_delete_existing_task_success(client, auth_token):
    # Успешное удаление существующей задачи
    
    unique_id = str(uuid.uuid4())[:8]
    task_name = f"Task_To_Update_{unique_id}"
    task_data = {
        "name": task_name,
        "status": False,
    }
    
    # Создаем задачу для последующего удаления
    create_response = await client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Удаляем созданную задачу
    delete_response = await client.delete(
        f"/tasks/{task_name}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Проверяем успешное удаление (204 No Content)
    assert delete_response.status_code == 204  
    assert delete_response.content == b''      
    assert delete_response.text == ''          
    
    # Проверяем, что задача действительно удалена (404 Not Found)
    get_response = await client.get(
        f"/tasks/{task_name}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert get_response.status_code == 404  
   
async def test_delete_unauthorized(client, auth_token):
    # Проверка удаления без авторизации или с неверным токеном
    
    unique_id = str(uuid.uuid4())[:8]
    task_name = f"Task_To_Update_{unique_id}"
    task_data = {
        "name": task_name,
        "status": False,
    }
    
    # Создаем задачу
    create_response = await client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Попытка удаления без токена -> 401 Unauthorized
    delete_response = await client.delete(f"/tasks/{task_name}")
    assert delete_response.status_code == 401 
    
    # Попытка удаления с неверным токеном -> 401 Unauthorized
    delete_response = await client.delete(
        f"/tasks/{task_name}",
        headers={"Authorization": "Bearer invalid_token_123"}
    )
    assert delete_response.status_code == 401 
    
    # Проверяем, что задача не была удалена (существует)
    get_response = await client.get(
        f"/tasks/{task_name}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert get_response.status_code == 200  

async def test_delete_nonexistent_task(client, auth_token):
    # Удаление несуществующей задачи -> 404 Not Found
    
    non_existent_name = "NonExistent_Task_12345"
    
    delete_response = await client.delete(
        f"/tasks/{non_existent_name}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert delete_response.status_code == 404 

async def test_delete_already_deleted_task(client, auth_token):
    # Повторное удаление уже удаленной задачи -> 404 Not Found
    
    unique_id = str(uuid.uuid4())[:8]
    task_name = f"Task_To_Update_{unique_id}"
    task_data = {
        "name": task_name,
        "status": False,
    }
    
    # Создаем задачу
    create_response = await client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert create_response.status_code == 201
    
    # Первое удаление -> успех (204)
    delete_response = await client.delete(
        f"/tasks/{task_name}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert delete_response.status_code == 204  
    
    # Второе удаление той же задачи -> 404 (уже не существует)
    delete_response2 = await client.delete(
        f"/tasks/{task_name}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert delete_response2.status_code == 404 