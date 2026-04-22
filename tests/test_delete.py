from tests.conftest import *
import json
import uuid

async def test_delete_existing_task_success(client, headers):
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
        headers=headers
    )
    
    # Удаляем созданную задачу
    delete_response = await client.delete(
        f"/tasks/{task_name}",
        headers=headers
    )
    
    # Проверяем успешное удаление (204 No Content)
    assert delete_response.status_code == 204  
    assert delete_response.content == b''      
    assert delete_response.text == ''          
    
    # Проверяем, что задача действительно удалена (404 Not Found)
    get_response = await client.get(
        f"/tasks/{task_name}",
        headers=headers
    )
    assert get_response.status_code == 404  
    
async def test_delete_nonexistent_task(client, headers):
    # Удаление несуществующей задачи -> 404 Not Found
    
    non_existent_name = "NonExistent_Task_12345"
    
    delete_response = await client.delete(
        f"/tasks/{non_existent_name}",
        headers=headers
    )
    assert delete_response.status_code == 404 

async def test_delete_already_deleted_task(client, headers):
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
        headers=headers
    )
    assert create_response.status_code == 201
    
    # Первое удаление -> успех (204)
    delete_response = await client.delete(
        f"/tasks/{task_name}",
        headers=headers
    )
    assert delete_response.status_code == 204  
    
    # Второе удаление той же задачи -> 404 (уже не существует)
    delete_response2 = await client.delete(
        f"/tasks/{task_name}",
        headers=headers
    )
    assert delete_response2.status_code == 404 