import pytest
import sys
from testcontainers.postgres import PostgresContainer
from httpx import ASGITransport, AsyncClient
import random
import string
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from auth.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta, timezone

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
    response = await client.post("/login/", data={"username": "admin",  "password": "admin"})
    assert response.status_code == 200, f"Login failed: {response.text}"
    token_data = response.json()
    return token_data["access_token"]

@pytest.fixture()
def expired_token(auth_token):
    import jwt

    """Создание просроченного токена"""
    payload = jwt.decode(
        auth_token,
        SECRET_KEY,
        algorithms=["HS256"],
        options={"verify_signature": False}
    )
    expired_time = datetime.now(timezone.utc) - timedelta(minutes=5)
    payload["exp"] = int(expired_time.timestamp())
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@pytest.fixture
def token_list1(auth_token):
    return [auth_token, "", "saiudghaijyusd"]

@pytest.fixture
def token_list2(expired_token):
    """Список некорректных токенов"""
    return ["", "saiudghaijyusd", expired_token]
