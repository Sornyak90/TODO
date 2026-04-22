import pytest
import sys
from testcontainers.postgres import PostgresContainer
from httpx import ASGITransport, AsyncClient
import random
import string
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings
from datetime import datetime, timedelta, timezone
import jwt

# Использование настроек
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Тестовые данные
TEST_USER = "admin"
TEST_PASSWORD = "admin"
INVALID_USER = "nonexistent"
INVALID_PASSWORD = "wrongpassword"

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
    import config
    url = pg_container.get_connection_url()
    config.settings = config.Settings(database_url=_async_pg_url(url))
    from data import Base
    from main import app as fastapi_app

    engine = create_async_engine(config.settings.database_url)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Передай engine/session в приложение или сервисы, если нужно

    yield fastapi_app

    await engine.dispose()

@pytest.fixture
async def client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def auth_token(client):
    response = await client.post("/login/", data={"username": TEST_USER,  "password": TEST_PASSWORD})
    token_data = response.json()
    return token_data["access_token"]

@pytest.fixture()
def expired_token(auth_token):

    """Создание просроченного токена"""
    payload = jwt.decode(
        auth_token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
        options={"verify_signature": False}
    )
    expired_time = datetime.now(timezone.utc) - timedelta(minutes=5)
    payload["exp"] = int(expired_time.timestamp())
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@pytest.fixture
def headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}

@pytest.fixture
def headers_invlid():
    return {"Authorization": "Bearer invalid_token"}

@pytest.fixture
def headers_expired_token(expired_token):
    return {"Authorization": f"Bearer {expired_token}"}

@pytest.fixture
def pagination_params():
    """Фикстура с параметрами пагинации для разных тестов"""
    return {
        "first_page": {"status": 0, "offset": 0, "page_size": 5},
        "second_page": {"status": 0, "offset": 5, "page_size": 5},
        "large_offset": {"status": 0, "offset": 2000, "page_size": 5},
        "negative_offset": {"status": 0, "offset": -1, "page_size": 5},
        "negative_page_size": {"status": 0, "offset": 0, "page_size": -5},
        "zero_page_size": {"status": 0, "offset": 0, "page_size": 0},
        "status_1": {"status": 1, "offset": 0, "page_size": 10},
        "status_2": {"status": 2, "offset": 0, "page_size": 10}
    }
