from fastapi.testclient import TestClient
from main import app
from src.auth.config import SECRET_KEY  
from datetime import datetime, timedelta, timezone
from jose import jwt
import json
import random
import string

client = TestClient(app)



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