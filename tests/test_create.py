from tests.token_and_data import *  # Импорт тестовых данных и токенов из модуля
import json

# Список некорректных токенов для тестирования авторизации:
# - пустая строка, неверный токен, просроченный токен
token_list = ["", "saiudghaijyusd", expired_token]

# Список тестовых данных с некорректными/невалидными задачами
_tasks = [task_data_2, task_data_3]

def test_create_successful():
    """
    Тест успешного создания задачи.
    Проверяет корректную работу endpoint при валидных данных и токене.
    """
    # Отправляем POST-запрос на создание задачи с валидными данными и токеном
    response = client.post(
        "/tasks/", 
        json=task_data_1,  # Валидные данные задачи
        headers={"Authorization": f"Bearer {token}"}  # Валидный токен
    )
    
    # Ожидаем статус 201 (Created) - успешное создание ресурса
    assert response.status_code == 201
    # Проверяем, что имя задачи в ответе соответствует отправленному
    assert response.json()["name"] == task_data_1["name"]
    # Проверяем, что статус задачи в ответе соответствует отправленному
    assert response.json()["status"] == task_data_1["status"]

def test_error_auth():
    """
    Тест ошибок авторизации.
    Проверяет обработку различных некорректных токенов.
    """
    # Перебираем все некорректные токены из списка
    for i in range(len(token_list)):
        response = client.post(
            "/tasks/", 
            json=task_data_1,  # Используем валидные данные задачи
            headers={"Authorization": f"Bearer {token_list[i]}"}  # Некорректный токен
        )

        # Для каждого типа некорректного токена ожидаем статус 401 (Unauthorized)
        if i == 0: 
            assert response.status_code == 401  # Пустой токен
        if i == 1: 
            assert response.status_code == 401  # Неверный/случайный токен
        if i == 2: 
            assert response.status_code == 401  # Просроченный токен

def test_input_data_validation():
    """
    Тест валидации входных данных.
    Проверяет обработку некорректных данных задачи.
    """
    # Перебираем тестовые данные с ошибками валидации
    for i in range(len(_tasks)):
        response = client.post(
            "/tasks/", 
            json=_tasks[i],  # Некорректные данные задачи
            headers={"Authorization": f"Bearer {token}"}  # Валидный токен
        )

        # Ожидаем статус 422 (Unprocessable Entity) - ошибка валидации данных
        if i == 0: 
            assert response.status_code == 422  # Первый набор некорректных данных
        if i == 1: 
            assert response.status_code == 422  # Второй набор некорректных данных

def test_business_logic():
    """
    Тест бизнес-логики.
    Проверяет обработку конфликтных ситуаций (например, дублирование задач).
    """
    # Пытаемся создать задачу с данными, которые должны вызвать конфликт
    # (например, задача с таким именем уже существует)
    response = client.post(
        "/tasks/", 
        json=task_data_1,  # Данные, которые могут вызвать конфликт
        headers={"Authorization": f"Bearer {token}"}  # Валидный токен
    )
    
    # Ожидаем статус 409 (Conflict) - конфликт данных/состояния
    # Например: задача с таким именем уже существует
    assert response.status_code == 409