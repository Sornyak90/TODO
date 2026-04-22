from tests.conftest import *
import uuid

async def test_patch_existing_task_success(client, headers):
    """Успешное обновление существующей задачи (PATCH)"""
    unique_id = str(uuid.uuid4())[:8]
    task_name = f"Task_To_Update_{unique_id}"
    task_data = {
        "name": task_name,
        "status": False,
    }
    task_update = {
        "name": task_name,
        "status": True,  # Меняем статус с False на True
    }

    # Создаем задачу
    create_response = await client.post(
        "/tasks/",
        json=task_data,
        headers=headers
    )
    assert create_response.status_code == 201
    original_task = create_response.json()
    task_id = original_task.get("id")
    
    # Обновляем задачу
    patch_response = await client.patch(
        "/tasks/",
        json=task_update,
        headers=headers
    )
    assert patch_response.status_code == 200
    updated_task = patch_response.json()

    # Проверяем, что статус обновился
    assert updated_task["status"] == True
    assert updated_task["name"] == task_data["name"]

    # Проверяем через GET, что изменения сохранились
    get_response = await client.get(
        f"/tasks/{task_update["name"]}",
        headers=headers
    )
    assert get_response.status_code == 200
    fetched_task = get_response.json()
    assert fetched_task["status"] == True
    assert fetched_task["id"] == task_id  # ID не должен измениться

    # Очистка: удаляем задачу
    delete_response = await client.delete(
        f"/tasks/{task_update["name"]}",
        headers=headers
    )
    assert delete_response.status_code == 204


async def test_patch_nonexistent_task(client, headers):
    """Попытка обновить несуществующую задачу -> 404"""
    update_data = {
        "name": "NonExistentTask_12345",  # Имя несуществующей задачи
        "status": True,
    }

    patch_response = await client.patch(
        "/tasks/",
        json=update_data,
        headers=headers
    )

    assert patch_response.status_code == 404  # Задача не найдена

async def test_patch_already_deleted_task(client, headers):
    """Попытка обновить уже удаленную задачу -> 404"""
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

    # Удаляем задачу
    delete_response = await client.delete(
        f'/tasks/{task_data["name"]}',
        headers=headers
    )
    assert delete_response.status_code == 204

    # Пытаемся обновить удаленную задачу -> 404
    patch_response = await client.patch(
        "/tasks/",
        json={"name": task_name, "status": True},
        headers=headers
    )
    assert patch_response.status_code == 404  # Задача уже не существует