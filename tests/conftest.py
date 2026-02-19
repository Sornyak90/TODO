import pytest
import sys
from testcontainers.postgres import PostgresContainer
from httpx import ASGITransport, AsyncClient
import random
import string

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

def _async_pg_url(url: str) -> str:
    return url.replace("psycopg2", "asyncpg")

@pytest.fixture
async def app(pg_container):
    import src.config as config
    config.settings = config.Settings(database_url=_async_pg_url(pg_container.get_connection_url()))
    from src.data import Base, engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    from src.main import app as fastapi_app
    yield fastapi_app
    await engine.dispose()

@pytest.fixture
async def client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def auth_token(client, test_data):
    response = await client.post("/login/", data=test_data["login"])
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