from tests.conftest import *  # Импорт тестовых данных и токенов из модуля

def test_access_with_auth(client,token_list1):
    """
    Тестирование доступа к эндпоинту с разными типами токенов.
    Проверяет корректность работы аутентификации.
    """
    for i in range(len(token_list1)):
        response = client.get(
            "/tasks/", 
            params={
                "filtr": 0,       # Фильтр: все задачи
                "offset": 0,       # Начальная позиция
                "page_size": 5     # Размер страницы
            },
            headers={"Authorization": f"Bearer {token_list1[i]}"}
        )
        
        # Проверки для каждого токена:
        if i == 0: 
            assert response.status_code == 200  # Валидный токен - успешный доступ
        if i == 1: 
            assert response.status_code == 401  # Пустой токен - ошибка аутентификации
        if i == 2: 
            assert response.status_code == 401  # Невалидный токен - ошибка аутентификации

def test_pagination(client, auth_token):
    """
    Тестирование пагинации (разбивки на страницы).
    Проверяет корректность работы параметров offset и page_size.
    """
    # Тест 1: Первая страница (первые 5 задач)
    response = client.get(
        "/tasks/",
        params={
            "filtr": 0,
            "offset": 0,      # Начинаем с первой записи
            "page_size": 5    # Берем 5 записей
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5  # Проверяем, что получили ровно 5 записей
    
    # Тест 2: Вторая страница (следующие 5 задач)
    response = client.get(
        "/tasks/",
        params={
            "filtr": 0,
            "offset": 5,      # Пропускаем первые 5 записей
            "page_size": 5    # Берем следующие 5
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5  # Проверяем, что получили еще 5 записей
    
    # Тест 3: Пустой список при offset >= общего количества задач
    # (Пытаемся получить данные за пределами доступного диапазона)
    response = client.get(
        "/tasks/",
        params={
            "filtr": 0,
            "offset": 2000,   # Очень большое смещение
            "page_size": 5
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # Должен вернуться пустой список
    
    # Тест 4: Отрицательный offset (валидационная ошибка)
    # Проверяем, что API правильно валидирует входные параметры
    response = client.get(
        "/tasks/",
        params={
            "offset": -1,     # Недопустимое значение
            "page_size": 5
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422  # Ожидаем ошибку валидации (422 Unprocessable Entity)
    
    # Тест 5: Отрицательный page_size (валидационная ошибка)
    response = client.get(
        "/tasks/",
        params={
            "offset": 0,
            "page_size": -5   # Недопустимое значение
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422  # Ошибка валидации
    
    # Тест 6: page_size = 0 (валидационная ошибка)
    response = client.get(
        "/tasks/",
        params={
            "offset": 0,
            "page_size": 0    # Недопустимое значение (должно быть > 0)
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422  # Ошибка валидации
    
def test_filter(client, auth_token):
    """
    Тестирование фильтрации задач по статусу.
    Проверяет работу параметра filtr.
    """
    
    # Тест 1: filtr=0 (все задачи без фильтрации)
    # Используем большой page_size, чтобы получить все задачи
    response = client.get(
        "/tasks/",
        params={"filtr": 0, "offset": 0, "page_size": 2000},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    
    # Тест 2: filtr=1 (только активные/невыполненные задачи)
    # В контексте задачи: status=True обычно означает "активная/невыполненная"
    response = client.get(
        "/tasks/",
        params={"filtr": 1, "offset": 0, "page_size": 10},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    datas = response.json()
    # Проверяем, что ВСЕ полученные задачи имеют status=True (активные)
    assert all(data["status"] == True for data in datas)
     
    # Тест 3: filtr=2 (только завершенные задачи)
    # status=False обычно означает "завершенная/выполненная"
    response = client.get(
        "/tasks/",
        params={"filtr": 2, "offset": 0, "page_size": 10},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    datas = response.json()
    # Проверяем, что ВСЕ полученные задачи имеют status=False (завершенные)
    assert all(data["status"] == False for data in datas)
    
    # Тест 4: filtr=999 (несуществующее значение) - валидационная ошибка
    # Проверяем обработку недопустимых значений фильтра
    response = client.get(
        "/tasks/",
        params={"filtr": 999, "offset": 0, "page_size": 10},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422  # Ошибка валидации
    
    # Тест 5: filtr с отрицательным значением
    response = client.get(
        "/tasks/",
        params={"filtr": -1, "offset": 0, "page_size": 10},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 422  # Ошибка валидации
    
    # Тест 6: filtr без значения (используется значение по умолчанию)
    # Проверяем поведение API, когда параметр filtr не указан
    response = client.get(
        "/tasks/",
        params={"offset": 0, "page_size": 10}, 
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    # В зависимости от реализации API:
    # - Может использовать значение по умолчанию (например, filtr=0)
    # - Может вернуть ошибку валидации, если filtr обязателен
    assert response.status_code == 422  # В данном случае ожидается ошибка