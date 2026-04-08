from tests.conftest import *  # Импорт тестовых данных и токенов из модуля
import uuid

async def test_access_with_auth(client, auth_token):
    """Тест авторизации для эндпоинта получения списка задач"""
    
    # Сценарий 1: Запрос с валидным токеном -> 200 OK
    response = await client.get(
            "/tasks/", 
            params={
                "filtr": 0,       # Фильтр: 0 = все задачи
                "offset": 0,      # Смещение для пагинации
                "page_size": 5    # Количество задач на странице
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
    assert response.status_code == 200 

    # Сценарий 2: Запрос без токена -> 401 Unauthorized
    response = await client.get(
            "/tasks/", 
            params={
                "filtr": 0,       
                "offset": 0,    
                "page_size": 5     
            }
        )
    assert response.status_code == 401  
    
    # Сценарий 3: Запрос с неверным токеном -> 401 Unauthorized
    response = await client.get(
            "/tasks/", 
            params={
                "filtr": 0,      
                "offset": 0,       
                "page_size": 5     
            },
            headers={"Authorization": "Bearer invalid_token"}
        )
    assert response.status_code == 401  
        

async def test_pagination(client, auth_token):
    """Тест пагинации (offset и page_size) для списка задач"""
   
    # Создаем 100 тестовых задач
    for i in range(100):  
        unique_id = str(uuid.uuid4())[:8]
        task_name = f"Task_Pagination_{unique_id}"
        task_data = {
            "name": task_name,
            "status": False,
        }

        response = await client.post(
            "/tasks/", 
            json=task_data,  
            headers={"Authorization": f"Bearer {auth_token}"}  
        )
    
    # Тест 1: Первая страница (offset=0, page_size=5) -> 5 задач
    response = await client.get(
        "/tasks/",
        params={
            "filtr": 0,
            "offset": 0,      
            "page_size": 5    
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5  
    
    # Тест 2: Вторая страница (offset=5, page_size=5) -> следующие 5 задач
    response = await client.get(
        "/tasks/",
        params={
            "filtr": 0,
            "offset": 5,      
            "page_size": 5    
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5  
    
    # Тест 3: Смещение больше количества задач (offset=2000) -> пустой список
    response = await client.get(
        "/tasks/",
        params={
            "filtr": 0,
            "offset": 2000,  
            "page_size": 5
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  
    
    # Тест 4: Отрицательный offset -> 422 Validation Error
    response = await client.get(
        "/tasks/",
        params={
            "offset": -1,     
            "page_size": 5
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422  
    
    # Тест 5: Отрицательный page_size -> 422
    response = await client.get(
        "/tasks/",
        params={
            "offset": 0,
            "page_size": -5  
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422  
    
    # Тест 6: Нулевой page_size -> 422
    response = await client.get(
        "/tasks/",
        params={
            "offset": 0,
            "page_size": 0   
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422  
    
async def test_filter(client, auth_token):
    """Тест фильтрации задач по статусу (filtr параметр)"""
   
    # Создаем 100 тестовых задач (все со статусом False)
    for i in range(100):  
        unique_id = str(uuid.uuid4())[:8]
        task_name = f"Task_Filter_{unique_id}"
        task_data = {
            "name": task_name,
            "status": False,
        }

        response = await client.post(
            "/tasks/", 
            json=task_data,  
            headers={"Authorization": f"Bearer {auth_token}"}  
        )
    
    # Тест 1: filtr=0 (все задачи) -> успешный ответ
    response = await client.get(
        "/tasks/",
        params={"filtr": 0, "offset": 0, "page_size": 2000},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    
    # Тест 2: filtr=1 (только активные задачи, status=True) -> все задачи должны иметь status=True
    response = await client.get(
        "/tasks/",
        params={"filtr": 1, "offset": 0, "page_size": 10},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    datas = response.json()
    # Проверяем, что все возвращенные задачи имеют статус True
    assert all(data["status"] == True for data in datas)
     
    # Тест 3: filtr=2 (только завершенные задачи, status=False) -> все задачи должны иметь status=False
    response = await client.get(
        "/tasks/",
        params={"filtr": 2, "offset": 0, "page_size": 10},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    datas = response.json()
    # Проверяем, что все возвращенные задачи имеют статус False
    assert all(data["status"] == False for data in datas)
    
    # Тест 4: Невалидный filtr (999) -> 422 Validation Error
    response = await client.get(
        "/tasks/",
        params={"filtr": 999, "offset": 0, "page_size": 10},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422  
    
    # Тест 5: Отрицательный filtr -> 422
    response = await client.get(
        "/tasks/",
        params={"filtr": -1, "offset": 0, "page_size": 10},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422 
    
    # Тест 6: Отсутствие обязательного параметра filtr -> 422
    response = await client.get(
        "/tasks/",
        params={"offset": 0, "page_size": 10},  # filtr не указан
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422