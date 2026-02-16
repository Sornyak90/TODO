from tests.conftest import *  # Импорт тестовых данных и токенов из модуля

def test_create_successful(client, auth_token, test_data):
    
    response = client.post(
        "/tasks/", 
        json=test_data["task_valid"],  
        headers={"Authorization": f"Bearer {auth_token}"}  
    )

    assert response.status_code == 201
    assert response.json()["name"] == test_data["task_valid"]["name"]
    assert response.json()["status"] == test_data["task_valid"]["status"]

def test_error_auth(client, token_list2, test_data):
    """
    Тест ошибок авторизации.
    Проверяет обработку различных некорректных токенов.
    """
    # Перебираем все некорректные токены из списка
    for i in range(len(token_list2)):
        response = client.post(
            "/tasks/", 
            json=test_data["task_valid"],  # Используем валидные данные задачи
            headers={"Authorization": f"Bearer {token_list2[i]}"}  # Некорректный токен
        )

        # Для каждого типа некорректного токена ожидаем статус 401 (Unauthorized)
        if i == 0: 
            assert response.status_code == 401  # Пустой токен
        if i == 1: 
            assert response.status_code == 401  # Неверный/случайный токен
        if i == 2: 
            assert response.status_code == 401  # Просроченный токен

def test_input_data_validation(client, auth_token, test_data):
    """
    Тест валидации входных данных.
    Проверяет обработку некорректных данных задачи.
    """
    # Перебираем тестовые данные с ошибками валидации
    for i in range(len(test_data["task_invalid_list"])):
        response = client.post(
            "/tasks/", 
            json=test_data["task_invalid_list"][i],  # Некорректные данные задачи
            headers={"Authorization": f"Bearer {auth_token}"}  # Валидный токен
        )

        # Ожидаем статус 422 (Unprocessable Entity) - ошибка валидации данных
        if i == 0: 
            assert response.status_code == 422  # Первый набор некорректных данных
        if i == 1: 
            assert response.status_code == 422  # Второй набор некорректных данных

def test_business_logic(client, auth_token, test_data):
    """
    Тест бизнес-логики.
    Проверяет обработку конфликтных ситуаций (например, дублирование задач).
    """
    # Пытаемся создать задачу с данными, которые должны вызвать конфликт
    # (например, задача с таким именем уже существует)
    response = client.post(
        "/tasks/", 
        json=test_data["task_valid"],  # Данные, которые могут вызвать конфликт
        headers={"Authorization": f"Bearer {auth_token}"}  # Валидный токен
    )
    
    # Ожидаем статус 409 (Conflict) - конфликт данных/состояния
    # Например: задача с таким именем уже существует
    assert response.status_code == 409