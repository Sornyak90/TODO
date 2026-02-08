from fastapi.testclient import TestClient
from main import app
from src.auth.config import SECRET_KEY  
from datetime import datetime, timedelta, timezone
from jose import jwt
import json


client = TestClient(app)

task_data_1 = {
    "name": "Test09",
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

login_data = {
        "username": "admin",  
        "password": "admin"   
}

# Авторизация
auth_response = client.post("/login", data=login_data)
token_data = auth_response.json()
token = token_data["access_token"]

# Просроченная авторизация
payload = jwt.decode(
        token, 
        SECRET_KEY, 
        algorithms=["HS256"],
        options={"verify_signature": False}
)
expired_time = datetime.now(timezone.utc) - timedelta(minutes=5)
payload["exp"] = int(expired_time.timestamp())
expired_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def test_create_successful():

    response = client.post(
        "/tasks/", 
        json=task_data_1,  
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    assert response.json()["name"] == task_data_1["name"]
    assert response.json()["status"] == task_data_1["status"]

def test_error_auth():

    null_token = ""
    error_token = "saiudghaijyusd"

    response1 = client.post(
        "/tasks/", 
        json=task_data_1,  
        headers={"Authorization": f"Bearer {null_token}"}
    )

    response2 = client.post(
        "/tasks/", 
        json=task_data_1,  
        headers={"Authorization": f"Bearer {error_token}"}
    )

    response3 = client.post(
        "/tasks/", 
        json=task_data_1,  
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    assert response1.status_code == 401
    assert response2.status_code == 401
    assert response3.status_code == 401

def test_input_data_validation():

    response1 = client.post(
        "/tasks/", 
        json=task_data_2,  
        headers={"Authorization": f"Bearer {token}"}
    )

    response2 = client.post(
        "/tasks/", 
        json=task_data_3,  
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response1.status_code == 422
    assert response2.status_code == 422

def test_business_logic():
    response = client.post(
    "/tasks/", 
    json=task_data_1,  
    headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 409