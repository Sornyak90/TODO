import pytest
from testcontainers.postgres import PostgresContainer
from fastapi.testclient import TestClient
from src.auth.config import SECRET_KEY  
from datetime import datetime, timedelta, timezone
from jose import jwt
from src.data.config import settings
import json
import random
import string


@pytest.fixture(scope="session")
def pg_container():
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg

@pytest.fixture(scope="session")
def app(pg_container):
    import src.data.config as config
    config.settings = config.Settings(database_url=pg_container.get_connection_url())
    from src.main import app
    from src.data.__init__ import Base, engine
    Base.metadata.create_all(bind=engine)
    yield app

@pytest.fixture
def client(app):
    from fastapi.testclient import TestClient
    return TestClient(app)

# Создаем токены внутри тестов, где доступен client
@pytest.fixture(scope="session")
def auth_token(client):
    response = client.post("/login", data=login_data)
    token_data = response.json()
    return token_data["access_token"]

@pytest.fixture(scope="session")
def expired_token(auth_token):
    payload = jwt.decode(
        auth_token, 
        SECRET_KEY, 
        algorithms=["HS256"],
        options={"verify_signature": False}
    )
    expired_time = datetime.now(timezone.utc) - timedelta(minutes=5)
    payload["exp"] = int(expired_time.timestamp())
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Список некорректных токенов для тестирования авторизации
@pytest.fixture
def token_list(auth_token, expired_token):
    return ["", "saiudghaijyusd", expired_token]


task_data_1 = {
    "name": ''.join(random.choices(string.ascii_letters, k=5)),
    "status": False,
}

task_data_2 = {
    "name": "",
    "status": "",
}

task_data_3 = {
    "name": 333,
    "status": "333",
}

task_name = "Task_To_Update"
task_new = {
    "name": task_name,
    "status": True,
}

task_data_4 = {
        "name": task_name,
        "status": False,
}

login_data = {
        "username": "admin",  
        "password": "admin"   
}