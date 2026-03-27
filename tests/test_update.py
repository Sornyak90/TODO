from tests.conftest import *
import uuid

async def test_patch_existing_task_success(client, auth_token):
    unique_id = str(uuid.uuid4())[:8]
    task_name = f"Task_To_Update_{unique_id}"
    task_data = {
        "name": task_name,
        "status": False,
    }
    task_update = {
        "name": task_name,
        "status": True,
    }

    create_response = await client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert create_response.status_code == 201
    original_task = create_response.json()
    task_id = original_task.get("id")
    patch_response = await client.patch(
        "/tasks/",
        json=task_update,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert patch_response.status_code == 200
    updated_task = patch_response.json()

    assert updated_task["status"] == True
    assert updated_task["name"] == task_data["name"]

    get_response = await client.get(
        f"/tasks/{task_update["name"]}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert get_response.status_code == 200
    fetched_task = get_response.json()
    assert fetched_task["status"] == True
    assert fetched_task["id"] == task_id  #  Проверяем что ID не изменился

    delete_response = await client.delete(
        f"/tasks/{task_update["name"]}",  #  Используем имя для удаления
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert delete_response.status_code == 204

async def test_patch_unauthorized(client, auth_token):
    """Ошибки авторизации при обновлении"""
    unique_id = str(uuid.uuid4())[:8]
    task_name = f"Task_To_Update_{unique_id}"
    task_data = {
        "name": task_name,
        "status": False,
    }

    patch_response = await client.patch(
        "/tasks/",
        json=task_data
    )
    assert patch_response.status_code == 401  #  Проверка без токена

    patch_response = await client.patch(
        "/tasks/",
        json=task_data,
        headers={"Authorization": "Bearer invalid_token_123"}
    )
    assert patch_response.status_code == 401  #  Проверка с невалидным токеном


async def test_patch_nonexistent_task(client, auth_token):
    """Попыткprint(patch_response.json())а обновить несуществующую задачу"""
    # 2. Пытаемся обновить несуществующую задачу

    update_data = {
        "name": "NonExistentTask_12345",  #  Указываем имя несуществующей задачи
        "status": True,
        }

    patch_response = await client.patch(
        "/tasks/",
        json=update_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    # 3. Проверяем 404 Not Found
    assert patch_response.status_code == 404  #  Правильный ожидаемый статус

async def test_patch_already_deleted_task(client, auth_token):
    """Попытка обновить уже удаленную задачу"""

    unique_id = str(uuid.uuid4())[:8]
    task_name = f"Task_To_Update_{unique_id}"
    task_data = {
        "name": task_name,
        "status": False,
    }
    create_response = await client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert create_response.status_code == 201

    delete_response = await client.delete(
        f'/tasks/{task_data["name"]}',  # Внешние одинарные, внутренние двойные
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert delete_response.status_code == 204

    patch_response = await client.patch(
        "/tasks/",
        json={"name": task_name, "status": True},  # Явно указываем обновленные данные
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert patch_response.status_code == 404  # Ожидаем 404 после удаления
