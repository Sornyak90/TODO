import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.auth.auth_jwt import get_current_user

class MockUser:
    def __init__(self):
        self.username = "admin"
        self.password = "admin"

@pytest.mark.asyncio
async def test_create_task():
    async def mock_get_current_user():
        return MockUser()
    
    app.dependency_overrides[get_current_user] = mock_get_current_user
    
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as ac:
            response = await ac.post(
                "/tasks/",
                json={
                    "name": "test",
                    "status": False
                }
            )
            
            assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"
            
            response_data = response.json()
            
            assert response_data["name"] == "test"
            assert response_data["status"] is False
            
            if "id" in response_data:
                assert isinstance(response_data["id"], (int, str))
            
    finally:
        app.dependency_overrides.clear()