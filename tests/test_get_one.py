from tests.token_and_data import *
import json


def test_get_existing_task():
    """Успешное получение существующей задачи"""
    task_name = "TestTask_GetOne"
    task_data = {
        "name": task_name,
        "status": False 
    }

    create_response = client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    response = client.get(
        f"/tasks/{task_name}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    task = response.json()
    print(task)
    # assert "id" in task
    # assert "name" in task
    # assert "status" in task
    # assert task["name"] == task_name
    # assert task["status"] == False
    
# def test_get_nonexistent_task():
#     """Попытка получить несуществующую задачу"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     # 2. Пытаемся получить несуществующую задачу
#     non_existent_name = "NonExistentTask_12345"
#     response = client.get(
#         f"/tasks/{non_existent_name}",
#         headers={"Authorization": f"Bearer {token}"}
#     )
    
#     # 3. Проверяем ответ (обычно 404 Not Found)
#     print(f"Ответ для несуществующей задачи: {response.status_code}")
#     assert response.status_code in [404, 400]  # 404 или 400 в зависимости от реализации
    
#     if response.status_code == 404:
#         error_data = response.json()
#         assert "detail" in error_data


# def test_get_task_unauthorized():
#     """Попытка получить задачу без авторизации"""
    
#     # 1. Создаем задачу с авторизацией
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     task_name = "TestTask_NoAuth"
#     task_data = {"name": task_name, "status": False}
    
#     create_response = client.post(
#         "/tasks/",
#         json=task_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert create_response.status_code in [200, 201]
    
#     # 2. Пытаемся получить задачу без токена
#     response = client.get(f"/tasks/{task_name}")
    
#     # 3. Проверяем ошибку авторизации
#     assert response.status_code == 401  # Unauthorized
    
#     # 4. Пытаемся получить задачу с неверным токеном
#     response = client.get(
#         f"/tasks/{task_name}",
#         headers={"Authorization": "Bearer invalid_token_123"}
#     )
#     assert response.status_code == 401


# def test_get_task_with_special_characters():
#     """Получение задачи с особыми символами в имени"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     test_cases = [
#         "Task-With-Dash",
#         "task_with_underscore",
#         "Task.With.Dot",
#         "Task 123",
#         "Task@Special",
#         "ЗадачаНаРусском",  # кириллица
#         "任务",  # китайские иероглифы
#         "タスク",  # японские иероглифы
#     ]
    
#     for task_name in test_cases:
#         # 2. Создаем задачу
#         task_data = {"name": task_name, "status": False}
        
#         try:
#             create_response = client.post(
#                 "/tasks/",
#                 json=task_data,
#                 headers={"Authorization": f"Bearer {token}"}
#             )
            
#             # Если задача успешно создана
#             if create_response.status_code in [200, 201]:
#                 # 3. Получаем задачу
#                 response = client.get(
#                     f"/tasks/{task_name}",
#                     headers={"Authorization": f"Bearer {token}"}
#                 )
                
#                 print(f"Задача '{task_name}': {response.status_code}")
                
#                 if response.status_code == 200:
#                     task = response.json()
#                     assert task["name"] == task_name
#                 elif response.status_code in [404, 400]:
#                     print(f"  Задача не найдена или ошибка валидации")
#                 else:
#                     print(f"  Неожиданный статус: {response.status_code}")
                    
#         except Exception as e:
#             print(f"Ошибка для задачи '{task_name}': {e}")


# def test_get_task_case_sensitivity():
#     """Тестирование чувствительности к регистру"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     # 2. Создаем задачу с определенным регистром
#     task_name = "MyTask_CaseSensitive"
#     task_data = {"name": task_name, "status": False}
    
#     create_response = client.post(
#         "/tasks/",
#         json=task_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert create_response.status_code in [200, 201]
    
#     # 3. Пробуем получить с разным регистром
#     test_variants = [
#         task_name,  # оригинальный регистр
#         task_name.lower(),  # нижний регистр
#         task_name.upper(),  # верхний регистр
#         "mytask_casesensitive",  # полностью нижний
#         "MYTASK_CASESENSITIVE",  # полностью верхний
#     ]
    
#     for variant in test_variants:
#         response = client.get(
#             f"/tasks/{variant}",
#             headers={"Authorization": f"Bearer {token}"}
#         )
        
#         print(f"Запрос '{variant}': {response.status_code}")
        
#         if response.status_code == 200:
#             task = response.json()
#             print(f"  Найдена задача: {task['name']}")


# def test_get_task_response_format():
#     """Проверка формата ответа TaskResponse"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     # 2. Создаем задачу со всеми полями
#     task_name = "FullTask_ResponseTest"
#     task_data = {
#         "name": task_name,
#         "description": "Test description",
#         "status": False,
#         "priority": "high",
#         "due_date": "2024-12-31",
#         # добавьте другие поля если они есть в вашей модели
#     }
    
#     # Фильтруем только существующие поля для создания
#     # (отправляем только обязательные/поддерживаемые поля)
#     create_data = {"name": task_name, "status": False}
#     if "description" in task_data:
#         create_data["description"] = task_data["description"]
    
#     create_response = client.post(
#         "/tasks/",
#         json=create_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert create_response.status_code in [200, 201]
    
#     # 3. Получаем задачу
#     response = client.get(
#         f"/tasks/{task_name}",
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert response.status_code == 200
    
#     # 4. Анализируем структуру ответа
#     task = response.json()
#     print(f"Структура ответа: {list(task.keys())}")
    
#     # Проверяем обязательные поля
#     required_fields = ["id", "name", "status"]
#     for field in required_fields:
#         assert field in task, f"Отсутствует обязательное поле: {field}"
#         print(f"✓ Поле '{field}': {task[field]}")
    
#     # Проверяем типы данных
#     assert isinstance(task["id"], (int, str))
#     assert isinstance(task["name"], str)
#     assert isinstance(task["status"], bool)
    
#     # Проверяем опциональные поля
#     optional_fields = ["description", "created_at", "updated_at", "priority", "due_date"]
#     for field in optional_fields:
#         if field in task:
#             print(f"✓ Опциональное поле '{field}': {task[field]}")


# def test_concurrent_get_requests():
#     """Несколько одновременных запросов к одной задаче"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     # 2. Создаем задачу
#     task_name = "ConcurrentAccessTask"
#     task_data = {"name": task_name, "status": False}
    
#     create_response = client.post(
#         "/tasks/",
#         json=task_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert create_response.status_code in [200, 201]
    
#     # 3. Делаем несколько запросов
#     import concurrent.futures
    
#     def make_request(request_id):
#         response = client.get(
#             f"/tasks/{task_name}",
#             headers={"Authorization": f"Bearer {token}"}
#         )
#         return request_id, response.status_code, response.json() if response.status_code == 200 else None
    
#     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#         futures = [executor.submit(make_request, i) for i in range(5)]
        
#         for future in concurrent.futures.as_completed(futures):
#             request_id, status_code, data = future.result()
#             print(f"Запрос {request_id}: статус {status_code}")
#             assert status_code == 200
#             if data:
#                 assert data["name"] == task_name


# def test_get_task_after_modification():
#     """Получение задачи после её изменения"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     # 2. Создаем задачу
#     task_name = "Task_For_Modification"
#     task_data = {"name": task_name, "status": False, "description": "Original description"}
    
#     create_response = client.post(
#         "/tasks/",
#         json=task_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert create_response.status_code in [200, 201]
    
#     # 3. Получаем задачу (первый раз)
#     response1 = client.get(
#         f"/tasks/{task_name}",
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert response1.status_code == 200
#     task1 = response1.json()
#     assert task1["status"] == False
    
#     # 4. Меняем статус задачи (если есть endpoint для обновления)
#     try:
#         update_data = {"status": True}
#         update_response = client.put(
#             f"/tasks/{task_name}",
#             json=update_data,
#             headers={"Authorization": f"Bearer {token}"}
#         )
        
#         if update_response.status_code == 200:
#             # 5. Получаем задачу снова
#             response2 = client.get(
#                 f"/tasks/{task_name}",
#                 headers={"Authorization": f"Bearer {token}"}
#             )
#             assert response2.status_code == 200
#             task2 = response2.json()
#             assert task2["status"] == True  # Статус должен измениться
#             print(f"Статус изменен с {task1['status']} на {task2['status']}")
#     except:
#         print("Endpoint для обновления не найден, пропускаем тест модификации")


# @pytest.mark.parametrize("task_name, expected_status", [
#     ("ValidTask", 200),
#     ("Task-123", 200),  # с цифрами
#     ("Task_Name", 200),  # с подчеркиванием
#     ("", 404),  # пустое имя - обычно 404 или 422
#     ("   ", 404),  # пробелы
#     ("a" * 100, 200),  # длинное имя
# ])
# def test_get_task_parametrized(task_name, expected_status):
#     """Параметризованный тест для разных имен задач"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     # 2. Создаем задачу только для валидных имен
#     if expected_status == 200 and task_name not in ["", "   "]:
#         task_data = {"name": task_name, "status": False}
#         create_response = client.post(
#             "/tasks/",
#             json=task_data,
#             headers={"Authorization": f"Bearer {token}"}
#         )
#         # Пропускаем если не удалось создать
#         if create_response.status_code not in [200, 201]:
#             pytest.skip(f"Не удалось создать задачу с именем: {task_name}")
    
#     # 3. Пытаемся получить задачу
#     response = client.get(
#         f"/tasks/{task_name}",
#         headers={"Authorization": f"Bearer {token}"}
#     )
    
#     print(f"Имя: '{task_name}' -> статус: {response.status_code}")
    
#     # Проверяем ожидаемый статус
#     # Если 404 ожидается, но получили 422 (валидация) - это тоже нормально
#     if expected_status == 404 and response.status_code == 422:
#         print(f"  Получена ошибка валидации 422 вместо 404")
#     else:
#         assert response.status_code == expected_status


# def test_get_task_integration_with_list():
#     """Интеграционный тест: получение задачи из списка"""
    
#     # 1. Авторизация
#     login_data = {"username": "testuser", "password": "testpass"}
#     auth_response = client.post("/login", data=login_data)
#     token = auth_response.json()["access_token"]
    
#     # 2. Получаем список задач
#     list_response = client.get(
#         "/tasks/",
#         params={"offset": 0, "page_size": 10},
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert list_response.status_code == 200
    
#     tasks = list_response.json()
#     assert isinstance(tasks, list)
    
#     if tasks:
#         # 3. Берем первую задачу из списка
#         first_task = tasks[0]
#         task_name = first_task["name"]
        
#         # 4. Получаем задачу по имени
#         get_response = client.get(
#             f"/tasks/{task_name}",
#             headers={"Authorization": f"Bearer {token}"}
#         )
#         assert get_response.status_code == 200
        
#         # 5. Сравниваем данные
#         detailed_task = get_response.json()
        
#         # Проверяем что данные совпадают
#         assert detailed_task["id"] == first_task["id"]
#         assert detailed_task["name"] == first_task["name"]
#         assert detailed_task["status"] == first_task["status"]
        
#         print(f"✓ Данные задачи '{task_name}' совпадают в списке и при отдельном запросе")