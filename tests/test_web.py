import pytest
from httpx import ASGITransport, AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://localhost:8000/login"
        ) as client:
            response = await client.get("/")
            assert response.status_code == 200
            assert response.json() == {"message": "Hello World"}

@pytest.mark.asyncio
async def test_get_all():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://localhost:8000/tasks"
        ) as client:
            response = await client.get("/")
            assert response.status_code == 200
            assert response.json() == {"message": "Hello World"}
