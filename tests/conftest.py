import pytest
from testcontainers.postgres import PostgresContainer
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone
from jose import jwt
import random
import string
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from src.data import Base

@pytest.fixture(scope="session")
def test_data():
    """Единая фикстура со всеми тестовыми данными"""
    
    # Данные для логина
    login_data = {
        "username": "admin",  
        "password": "admin"   
    }
    
    # Валидные данные задач
    task_valid = {
        "name": ''.join(random.choices(string.ascii_letters, k=5)),
        "status": False,
    }
    
    # Невалидные данные задач
    task_invalid_1 = {
        "name": "",
        "status": "",
    }
    
    task_invalid_2 = {
        "name": 333,
        "status": "333",
    }
    
    # Данные для обновления
    task_name = "Task_To_Update"
    task_for_update = {
        "name": task_name,
        "status": False,
    }
    
    task_updated = {
        "name": task_name,
        "status": True,
    }
    
    return {
        "login": login_data,
        "task_valid": task_valid,
        "task_invalid_list": [task_invalid_1, task_invalid_2],
        "task_for_update": task_for_update,
        "task_updated": task_updated,
        "task_name": task_name
    }

# === ФИКСТУРЫ ===
@pytest.fixture(scope="session")
def pg_container():
    """Фикстура для PostgreSQL контейнера"""
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg

@pytest.fixture(scope="session")
def app(pg_container):
    """Фикстура для приложения"""
    import src.config as config
    # Создаем URL для asyncpg
    sync_url = pg_container.get_connection_url()
    async_url = sync_url.replace('postgresql://', 'postgresql+asyncpg://')
    
    # Обновляем настройки
    config.settings = config.Settings(database_url=async_url)
    
    # Создаем таблицы асинхронно
    async def init_db():
        from src.data import engine
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    asyncio.run(init_db())
    
    from src.main import app
    yield app

@pytest.fixture(scope="session")
def client(app):
    """Фикстура для тестового клиента"""
    return TestClient(app)

@pytest.fixture(scope="session")
def auth_token(client,test_data):
    """Получение токена авторизации"""
    response = client.post("/login", data=test_data["login"])
    assert response.status_code == 200, f"Login failed: {response.text}"
    token_data = response.json()
    return token_data["access_token"]

# @pytest.fixture(scope="session")
# def expired_token(auth_token):
#     """Создание просроченного токена"""
#     payload = jwt.decode(
#         auth_token, 
#         SECRET_KEY, 
#         algorithms=["HS256"],
#         options={"verify_signature": False}
#     )
#     expired_time = datetime.now(timezone.utc) - timedelta(minutes=5)
#     payload["exp"] = int(expired_time.timestamp())
#     return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@pytest.fixture
def token_list1(auth_token):
    return [auth_token, "", "saiudghaijyusd"]

@pytest.fixture
def token_list2(expired_token):
    """Список некорректных токенов"""
    return ["", "saiudghaijyusd", expired_token]