from tests.token_and_data import *
import json

def test_patch_existing_task_success():
    """Успешное частичное обновление существующей задачи"""
    
    task_name = task_data_1["name"]
    
    create_response = client.post(
        "/tasks/",
        json=task_data_1,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_response.status_code == 201
    original_task = create_response.json()
    task_id = original_task.get("id")
    
    update_data = {"status": True}
    patch_response = client.patch(
        f"/tasks/{task_name}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert patch_response.status_code == 200
    updated_task = patch_response.json()
    
    assert updated_task["status"] == True  
    assert updated_task["name"] == task_name 
    
    get_response = client.get(
        f"/tasks/{task_name}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 200
    fetched_task = get_response.json()
    assert fetched_task["status"] == True

# def test_patch_partial_update_multiple_fields():
#     """Частичное обновление нескольких полей"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     # 2. Создаем задачу
#     task_name = "Task_Multi_Update"
#     task_data = {
#         "name": task_name,
#         "description": "Old description",
#         "status": False,
#         "priority": "low"
#     }
    
#     create_response = client.post(
#         "/tasks/",
#         json=task_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert create_response.status_code in [200, 201]
    
#     # 3. Обновляем несколько полей
#     update_data = {
#         "status": True,
#         "description": "Updated description",
#         "priority": "high"
#     }
    
#     patch_response = client.patch(
#         f"/tasks/{task_name}",
#         json=update_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
    
#     assert patch_response.status_code == 200
#     updated_task = patch_response.json()
    
#     # Проверяем обновления
#     assert updated_task["status"] == True
#     assert updated_task["description"] == "Updated description"
#     assert updated_task.get("priority") == "high"
#     assert updated_task["name"] == task_name  # Без изменений
    
#     print(f"✓ Обновлено несколько полей: статус, описание, приоритет")


# def test_patch_unauthorized():
#     """Ошибки авторизации при обновлении"""
    
#     # 1. Авторизация и создание задачи
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     task_name = "Task_Unauthorized_Update"
#     task_data = {"name": task_name, "status": False}
    
#     create_response = client.post(
#         "/tasks/",
#         json=task_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert create_response.status_code in [200, 201]
#     original_status = create_response.json()["status"]
    
#     # 2. Пытаемся обновить без токена
#     update_data = {"status": True}
#     patch_response = client.patch(
#         f"/tasks/{task_name}",
#         json=update_data
#     )
#     assert patch_response.status_code == 401  # Unauthorized
#     print(f"✓ Без токена: {patch_response.status_code}")
    
#     # 3. Пытаемся обновить с невалидным токеном
#     patch_response = client.patch(
#         f"/tasks/{task_name}",
#         json=update_data,
#         headers={"Authorization": "Bearer invalid_token_123"}
#     )
#     assert patch_response.status_code == 401
#     print(f"✓ С невалидным токеном: {patch_response.status_code}")
    
#     # 4. Проверяем что задача НЕ обновлена
#     get_response = client.get(
#         f"/tasks/{task_name}",
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert get_response.status_code == 200
#     task = get_response.json()
#     assert task["status"] == original_status  # Статус не изменился
#     print(f"✓ Задача не обновлена после неудачных попыток")


# def test_patch_nonexistent_task():
#     """Попытка обновить несуществующую задачу"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     # 2. Пытаемся обновить несуществующую задачу
#     non_existent_name = "NonExistent_Task_Update"
#     update_data = {"status": True}
    
#     patch_response = client.patch(
#         f"/tasks/{non_existent_name}",
#         json=update_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
    
#     # 3. Проверяем 404 Not Found
#     assert patch_response.status_code == 404
#     print(f"✓ Несуществующая задача: {patch_response.status_code}")
    
#     # Проверяем структуру ошибки
#     error_data = patch_response.json()
#     assert "detail" in error_data
#     print(f"  Сообщение: {error_data['detail']}")


# def test_patch_already_deleted_task():
#     """Попытка обновить уже удаленную задачу"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     # 2. Создаем и удаляем задачу
#     task_name = "Task_Deleted_Update"
#     task_data = {"name": task_name, "status": False}
    
#     create_response = client.post(
#         "/tasks/",
#         json=task_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert create_response.status_code in [200, 201]
    
#     # Удаляем задачу
#     delete_response = client.delete(
#         f"/tasks/{task_name}",
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert delete_response.status_code == 204
    
#     # 3. Пытаемся обновить удаленную задачу
#     update_data = {"status": True}
#     patch_response = client.patch(
#         f"/tasks/{task_name}",
#         json=update_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
    
#     # 4. Проверяем 404 Not Found
#     assert patch_response.status_code == 404
#     print(f"✓ Уже удаленная задача: {patch_response.status_code}")


# def test_patch_with_different_users():
#     """Попытка обновить задачу другого пользователя"""
    
#     # 1. Создаем двух пользователей
#     users = [
#         {"username": "user1_patch", "password": "pass1"},
#         {"username": "user2_patch", "password": "pass2"}
#     ]
    
#     tokens = []
#     for user in users:
#         auth_response = client.post("/login", data=user)
#         assert auth_response.status_code == 200
#         tokens.append(auth_response.json()["access_token"])
    
#     user1_token, user2_token = tokens
    
#     # 2. User1 создает задачу
#     task_name = "User1_Task_Patch"
#     task_data = {"name": task_name, "status": False}
    
#     create_response = client.post(
#         "/tasks/",
#         json=task_data,
#         headers={"Authorization": f"Bearer {user1_token}"}
#     )
#     assert create_response.status_code in [200, 201]
#     original_task = create_response.json()
    
#     # 3. User2 пытается обновить задачу user1
#     update_data = {"status": True}
#     patch_response = client.patch(
#         f"/tasks/{task_name}",
#         json=update_data,
#         headers={"Authorization": f"Bearer {user2_token}"}
#     )
    
#     # Ожидаем 404 (безопасность) или 403 (Forbidden)
#     assert patch_response.status_code in [404, 403]
#     print(f"✓ Задача другого пользователя: {patch_response.status_code}")
    
#     # 4. Проверяем что задача user1 НЕ обновлена
#     get_response = client.get(
#         f"/tasks/{task_name}",
#         headers={"Authorization": f"Bearer {user1_token}"}
#     )
#     assert get_response.status_code == 200
#     task = get_response.json()
#     assert task["status"] == original_task["status"]  # Статус не изменился
#     print(f"✓ Задача user1 не обновлена user2")


# def test_patch_validation_errors():
#     """Валидация входных данных при обновлении"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     # 2. Создаем задачу
#     task_name = "Task_Validation_Test"
#     task_data = {"name": task_name, "status": False}
    
#     create_response = client.post(
#         "/tasks/",
#         json=task_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert create_response.status_code in [200, 201]
    
#     test_cases = [
#         # (update_data, description, expected_status)
#         ({"status": "invalid_bool"}, "Невалидный boolean", 422),
#         ({"priority": "invalid_priority"}, "Невалидный приоритет", 422),
#         ({"due_date": "not-a-date"}, "Невалидная дата", 422),
#         ({"name": ""}, "Пустое имя", 422),  # если name можно обновлять
#         ({"name": "   "}, "Имя из пробелов", 422),
#         ({"extra_field": "value"}, "Несуществующее поле", 422),  # или игнорируется (200)
#         ({}, "Пустой объект обновления", 200),  # может быть 200 или 422
#     ]
    
#     for update_data, description, expected_status in test_cases:
#         print(f"\nТестируем: {description}")
        
#         patch_response = client.patch(
#             f"/tasks/{task_name}",
#             json=update_data,
#             headers={"Authorization": f"Bearer {token}"}
#         )
        
#         print(f"  PATCH статус: {patch_response.status_code}")
        
#         # Проверяем ожидаемый статус
#         if expected_status == 422:
#             # Для 422 проверяем структуру ошибки
#             assert patch_response.status_code == 422
#             error_data = patch_response.json()
#             assert "detail" in error_data
#             print(f"  Ошибка: {error_data['detail'][0].get('msg', '')}")
#         else:
#             # Для 200 проверяем успешный ответ
#             assert patch_response.status_code == 200
    
#     # 3. Проверяем что исходная задача не испорчена
#     get_response = client.get(
#         f"/tasks/{task_name}",
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert get_response.status_code == 200
#     task = get_response.json()
#     assert task["name"] == task_name
#     print(f"✓ Исходная задача не испорчена невалидными обновлениями")


# def test_patch_immutable_fields():
#     """Попытка изменить неизменяемые поля"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     # 2. Создаем задачу
#     task_name = "Task_Immutable_Test"
#     task_data = {
#         "name": task_name,
#         "status": False,
#         "description": "Original"
#     }
    
#     create_response = client.post(
#         "/tasks/",
#         json=task_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert create_response.status_code in [200, 201]
#     original_task = create_response.json()
#     original_id = original_task.get("id")
#     original_created_at = original_task.get("created_at")
    
#     # 3. Пытаемся изменить неизменяемые поля
#     update_data = {
#         "id": 99999,  # Обычно неизменяемо
#         "created_at": "2020-01-01",  # Обычно неизменяемо
#         "user_id": "hacked",  # Обычно неизменяемо
#         "status": True  # Изменяемое поле для контроля
#     }
    
#     patch_response = client.patch(
#         f"/tasks/{task_name}",
#         json=update_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
    
#     print(f"✓ Обновление с неизменяемыми полями: {patch_response.status_code}")
    
#     # Может быть 200 (игнорируются) или 422 (ошибка)
#     if patch_response.status_code == 200:
#         updated_task = patch_response.json()
        
#         # Проверяем что неизменяемые поля остались прежними
#         assert updated_task.get("id") == original_id
#         if original_created_at:
#             assert updated_task.get("created_at") == original_created_at
        
#         # Проверяем что изменяемое поле обновилось
#         assert updated_task["status"] == True
        
#         print(f"  Неизменяемые поля игнорируются, статус обновлен")
#     elif patch_response.status_code == 422:
#         print(f"  Неизменяемые поля вызывают ошибку валидации")


# def test_patch_empty_update():
#     """Обновление без изменений (пустой объект)"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     # 2. Создаем задачу
#     task_name = "Task_Empty_Update"
#     task_data = {"name": task_name, "status": False}
    
#     create_response = client.post(
#         "/tasks/",
#         json=task_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert create_response.status_code in [200, 201]
#     original_task = create_response.json()
    
#     # 3. Отправляем пустой объект обновления
#     patch_response = client.patch(
#         f"/tasks/{task_name}",
#         json={},  # Пустой объект
#         headers={"Authorization": f"Bearer {token}"}
#     )
    
#     # Может быть 200 (успешно, ничего не меняем) или 422 (ошибка валидации)
#     print(f"✓ Пустое обновление: {patch_response.status_code}")
    
#     if patch_response.status_code == 200:
#         updated_task = patch_response.json()
#         # Задача должна остаться неизменной
#         assert updated_task["name"] == original_task["name"]
#         assert updated_task["status"] == original_task["status"]
#         print(f"  Задача осталась без изменений")
#     elif patch_response.status_code == 422:
#         error_data = patch_response.json()
#         print(f"  Ошибка: {error_data['detail'][0].get('msg', '')}")


# def test_patch_concurrent_updates():
#     """Конкурентные обновления одной задачи"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     import concurrent.futures
#     import time
    
#     # 2. Создаем задачу
#     task_name = "Concurrent_Patch_Task"
#     task_data = {"name": task_name, "status": False, "counter": 0}
    
#     create_response = client.post(
#         "/tasks/",
#         json=task_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert create_response.status_code in [200, 201]
    
#     # 3. Функция для конкурентного обновления
#     def update_task(thread_id):
#         """Обновляет задачу с задержкой"""
#         time.sleep(0.1 * thread_id)  # Разные задержки для создания гонки
        
#         update_data = {
#             "status": True,
#             "description": f"Updated by thread {thread_id}"
#         }
        
#         response = client.patch(
#             f"/tasks/{task_name}",
#             json=update_data,
#             headers={"Authorization": f"Bearer {token}"}
#         )
#         return thread_id, response.status_code, response.json() if response.status_code == 200 else None
    
#     # 4. Запускаем несколько одновременных обновлений
#     with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#         futures = [executor.submit(update_task, i) for i in range(3)]
        
#         results = []
#         for future in concurrent.futures.as_completed(futures):
#             thread_id, status, data = future.result()
#             results.append((thread_id, status))
#             print(f"  Поток {thread_id}: статус {status}")
            
#             if data:
#                 print(f"    Описание: {data.get('description')}")
        
#         # Все должны быть успешными или хотя бы один
#         success_count = sum(1 for _, status in results if status == 200)
#         assert success_count > 0
#         print(f"✓ Успешных обновлений: {success_count}/{len(results)}")


# def test_patch_with_invalid_json():
#     """Обновление с невалидным JSON"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     # 2. Создаем задачу
#     task_name = "Task_Invalid_JSON"
#     task_data = {"name": task_name, "status": False}
    
#     create_response = client.post(
#         "/tasks/",
#         json=task_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert create_response.status_code in [200, 201]
    
#     # 3. Пытаемся отправить невалидный JSON
#     # Используем raw данные вместо json параметра
#     headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
#     invalid_json = '{"status": true,}'  # Лишняя запятая
    
#     patch_response = client.patch(
#         f"/tasks/{task_name}",
#         data=invalid_json,
#         headers=headers
#     )
    
#     # Должна быть ошибка 422 или 400
#     assert patch_response.status_code in [422, 400]
#     print(f"✓ Невалидный JSON: {patch_response.status_code}")


# @pytest.mark.parametrize("test_case", [
#     {
#         "description": "Обновление только статуса",
#         "update_data": {"status": True},
#         "expected_status": 200,
#         "should_change": ["status"]
#     },
#     {
#         "description": "Обновление описания",
#         "update_data": {"description": "New description"},
#         "expected_status": 200,
#         "should_change": ["description"]
#     },
#     {
#         "description": "Невалидный статус",
#         "update_data": {"status": "not_a_boolean"},
#         "expected_status": 422,
#         "should_change": []
#     },
#     {
#         "description": "Пустое обновление",
#         "update_data": {},
#         "expected_status": 200,  # или 422
#         "should_change": []
#     },
#     {
#         "description": "Обновление несуществующим полем",
#         "update_data": {"nonexistent": "value"},
#         "expected_status": 422,  # или 200 если игнорируется
#         "should_change": []
#     },
# ])
# def test_patch_parametrized(test_case):
#     """Параметризованные тесты обновления"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     # 2. Создаем задачу
#     task_name = f"Task_Param_{hash(str(test_case)) % 1000}"
#     task_data = {
#         "name": task_name,
#         "status": False,
#         "description": "Original",
#         "priority": "low"
#     }
    
#     create_response = client.post(
#         "/tasks/",
#         json=task_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     if create_response.status_code not in [200, 201]:
#         pytest.skip(f"Не удалось создать задачу: {create_response.status_code}")
    
#     original_task = create_response.json()
    
#     # 3. Обновляем задачу
#     update_data = test_case["update_data"]
#     expected_status = test_case["expected_status"]
    
#     patch_response = client.patch(
#         f"/tasks/{task_name}",
#         json=update_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
    
#     print(f"\n{test_case['description']}")
#     print(f"  Статус: {patch_response.status_code} (ожидалось {expected_status})")
    
#     # Для 422 проверяем ошибку
#     if expected_status == 422:
#         assert patch_response.status_code == 422
#         error_data = patch_response.json()
#         assert "detail" in error_data
#     else:
#         # Для 200 проверяем обновления
#         assert patch_response.status_code == 200
#         updated_task = patch_response.json()
        
#         # Проверяем какие поля должны были измениться
#         for field in test_case["should_change"]:
#             if field in update_data:
#                 assert updated_task[field] == update_data[field]
#                 print(f"  ✓ Поле '{field}' обновлено: {update_data[field]}")
        
#         # Проверяем что остальные поля не изменились
#         for field in ["name", "status", "description", "priority"]:
#             if field not in test_case["should_change"] and field in original_task:
#                 assert updated_task.get(field) == original_task.get(field)