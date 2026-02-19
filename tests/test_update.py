from tests.conftest import *


async def test_patch_existing_task_success(client, auth_token, test_data):
    create_response = await client.post(
        "/tasks/",
        json=test_data["task_for_update"],
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert create_response.status_code == 201
    original_task = create_response.json()
    task_id = original_task.get("id")
    patch_response = await client.patch(
        "/tasks/",
        json=test_data["task_updated"],
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert patch_response.status_code == 200
    updated_task = patch_response.json()
    
    assert updated_task["status"] == True  
    assert updated_task["name"] == test_data["task_for_update"]["name"]  
    
    get_response = await client.get(
        f"/tasks/{test_data["task_for_update"]["name"]}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert get_response.status_code == 200
    fetched_task = get_response.json()
    assert fetched_task["status"] == True
    assert fetched_task["id"] == task_id  #  Проверяем что ID не изменился

# async def test_patch_unauthorized(client, auth_token, test_data):
#     """Ошибки авторизации при обновлении"""
    
#     patch_response = await client.patch(
#         "/tasks/",
#         json=test_data["task_for_update"] 
#     )
#     assert patch_response.status_code == 401  #  Проверка без токена
    
#     patch_response = await client.patch(
#         "/tasks/",
#         json=test_data["task_for_update"],
#         headers={"Authorization": "Bearer invalid_token_123"}
#     )
#     assert patch_response.status_code == 401  #  Проверка с невалидным токеном
    

# async def test_patch_nonexistent_task(client, auth_token):
#     """Попытка обновить несуществующую задачу"""
#     # 2. Пытаемся обновить несуществующую задачу
    
#     update_data = {
#         "name": "NonExistentTask_12345",  #  Указываем имя несуществующей задачи
#         "status": True,
#         }
    
#     patch_response = await client.patch(
#         "/tasks/",
#         json=update_data,
#         headers={"Authorization": f"Bearer {auth_token}"}
#     )
    
#     # 3. Проверяем 404 Not Found
#     assert patch_response.status_code == 404  #  Правильный ожидаемый статус

async def test_patch_already_deleted_task(client, auth_token, test_data):
    """Попытка обновить уже удаленную задачу"""
    
    delete_response = await client.delete(
        f"/tasks/{test_data["task_for_update"]["name"]}",  #  Используем имя для удаления
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert delete_response.status_code == 204
    
    patch_response = await client.patch(
        "/tasks/",
        json=test_data["task_for_update"], 
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert patch_response.status_code == 404  #  Ожидаем 404 после удаления