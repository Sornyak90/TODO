# test_auth.py
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends
from auth.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt
from datetime import datetime, timedelta, timezone
from src.auth.auth_jwt import get_current_user
import time
import tzlocal


# Создаем тестовое приложение
app = FastAPI()

# # Импортируем и регистрируем роутер
from src.auth.auth_jwt import router  # замените your_module на имя вашего модуля
app.include_router(router)

client = TestClient(app)

# Тестовые данные
TEST_USER = "admin"
TEST_PASSWORD = "admin"
INVALID_USER = "nonexistent"
INVALID_PASSWORD = "wrongpassword"

# Фикстуры для тестов
@pytest.fixture
def auth_token():
    """Фикстура для получения валидного токена"""
    response = client.post("/login/", data={
        "username": TEST_USER,
        "password": TEST_PASSWORD
    })
    return response.json()["access_token"]

    

@pytest.fixture
def expired_token():
    """Фикстура для создания просроченного токена"""
    expire = datetime.now(timezone.utc) - timedelta(minutes=10)
    to_encode = {
        "sub": TEST_USER,
        "username": TEST_USER,
        "exp": expire
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

class TestAuthentication:
    """Тесты для аутентификации"""
    
    def test_successful_login(self):
        """Тест успешной аутентификации"""
        response = client.post("/login/", data={
            "username": TEST_USER,
            "password": TEST_PASSWORD
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        
        # Проверяем, что токен валиден
        token = data["access_token"]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload.get("username") == TEST_USER
    
    def test_login_invalid_username(self):
        """Тест аутентификации с неверным именем пользователя"""
        response = client.post("/login/", data={
            "username": INVALID_USER,
            "password": TEST_PASSWORD
        })
        
        assert response.status_code == 400
        assert "Invalid credentials" in response.text
    
    def test_login_invalid_password(self):
        """Тест аутентификации с неверным паролем"""
        response = client.post("/login/", data={
            "username": TEST_USER,
            "password": INVALID_PASSWORD
        })
        
        assert response.status_code == 400
        assert "Invalid credentials" in response.text
    
    def test_login_empty_credentials(self):
        """Тест аутентификации с пустыми данными"""
        response = client.post("/login/", data={
            "username": "",
            "password": ""
        })
        
        assert response.status_code == 400
        assert "Invalid credentials" in response.text

class TestTokenValidation:
    """Тесты валидации токенов"""
    
    def test_token_structure(self, auth_token):
        """Тест структуры JWT токена"""
        parts = auth_token.split('.')
        assert len(parts) == 3  # Header.Payload.Signature
        
        # Декодируем payload для проверки содержания
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "username" in payload
        assert "exp" in payload
        assert payload["username"] == TEST_USER
    
    def test_token_expiration(self, auth_token):

        """Тест срока действия токена"""
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp,  tz=timezone.utc)
        
        # Проверяем, что срок действия примерно равен настроенному
        expected_expiry = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        time_diff = abs((exp_datetime.replace(tzinfo=timezone.utc) - expected_expiry).total_seconds())
        
        # Допускаем разницу в 10 секунд из-за времени выполнения
        assert time_diff < 10
    
    def test_expired_token_validation(self, expired_token):
        """Тест валидации просроченного токена"""
        # Пытаемся использовать просроченный токен через зависимость get_current_user
        # Для этого нужно создать endpoint, который использует эту зависимость
        @app.get("/protected")
        async def protected_route(user = Depends(get_current_user)):
            return {"user": user}
        
        response = client.get(
            "/protected",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        
        assert response.status_code == 401
        assert "Could not validate credentials" in response.text
    
    def test_invalid_token_signature(self):
        """Тест с токеном с неверной подписью"""
        # Создаем токен с неправильным секретным ключом
        invalid_token = jwt.encode(
            {"username": TEST_USER, "exp": datetime.now(timezone.utc)  + timedelta(minutes=15)},
            "wrong_secret_key",
            algorithm=ALGORITHM
        )
        
        @app.get("/protected2")
        async def protected_route2(user = Depends(get_current_user)):
            return {"user": user}
        
        response = client.get(
            "/protected2",
            headers={"Authorization": f"Bearer {invalid_token}"}
        )
        
        assert response.status_code == 401
        assert "Could not validate credentials" in response.text
    
    def test_malformed_token(self):
        """Тест с некорректным форматом токена"""
        @app.get("/protected3")
        async def protected_route3(user = Depends(get_current_user)):
            return {"user": user}
        
        response = client.get(
            "/protected3",
            headers={"Authorization": "Bearer malformed.token.here"}
        )
        
        assert response.status_code == 401
        assert "Could not validate credentials" in response.text

class TestOAuth2Flow:
    """Тесты OAuth2 flow"""
    
    def test_oauth2_password_bearer_scheme(self):
        """Тест корректности OAuth2 схемы"""
        response = client.post("/login/", data={
            "username": TEST_USER,
            "password": TEST_PASSWORD
        })
        
        data = response.json()
        assert data["token_type"] == "bearer"
        
        # Проверяем, что токен работает с Authorization header
        token = data["access_token"]
        
        @app.get("/test-protected")
        async def test_protected(user = Depends(get_current_user)):
            return {"user": user}
        
        response = client.get(
            "/test-protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["user"] == TEST_USER
    
    def test_missing_authorization_header(self):
        """Тест запроса без Authorization header"""
        @app.get("/protected4")
        async def protected_route4(user = Depends(get_current_user)):
            return {"user": user}
        
        response = client.get("/protected4")
        
        assert response.status_code == 401
        assert "detail" in response.json()
    
    def test_wrong_auth_scheme(self):
        """Тест с неправильной схемой авторизации"""
        response = client.post("/login/", data={
            "username": TEST_USER,
            "password": TEST_PASSWORD
        })
        
        token = response.json()["access_token"]
        
        @app.get("/protected5")
        async def protected_route5(user = Depends(get_current_user)):
            return {"user": user}
        
        # Используем неправильную схему вместо "Bearer"
        response = client.get(
            "/protected5",
            headers={"Authorization": f"Basic {token}"}
        )
        
        assert response.status_code == 401

class TestMultipleUsers:
    """Тесты для нескольких пользователей"""
    
    def test_different_user_login(self):
        """Тест аутентификации другого пользователя"""
        response = client.post("/login/", data={
            "username": "johndoe",
            "password": "password123"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        
        # Проверяем payload токена
        token = data["access_token"]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload.get("username") == "johndoe"

class TestEdgeCases:
    """Тесты граничных случаев"""
    
    def test_token_without_username(self):
        """Тест токена без username в payload"""
        # Создаем токен без username
        token_without_username = jwt.encode(
            {"exp": datetime.now(timezone.utc)  + timedelta(minutes=15)},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        
        @app.get("/protected6")
        async def protected_route6(user = Depends(get_current_user)):
            return {"user": user}
        
        response = client.get(
            "/protected6",
            headers={"Authorization": f"Bearer {token_without_username}"}
        )
        
        assert response.status_code == 401
        assert "Could not validate credentials" in response.text
    
    def test_token_with_none_username(self):
        """Тест токена с username=None"""
        # Создаем токен с username=None
        token_none_username = jwt.encode(
            {"username": None, "exp": datetime.now(timezone.utc)  + timedelta(minutes=15)},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        
        @app.get("/protected7")
        async def protected_route7(user = Depends(get_current_user)):
            return {"user": user}
        
        response = client.get(
            "/protected7",
            headers={"Authorization": f"Bearer {token_none_username}"}
        )
        
        assert response.status_code == 401
        assert "Could not validate credentials" in response.text

# Дополнительные утилитарные тесты
def test_create_access_token_function():
    """Тест функции create_access_token"""
    from src.auth.auth_jwt import create_access_token  # замените your_module на имя вашего модуля
    
    # Тест с дефолтным expires_delta
    user_data = {"username": "testuser", "email": "test@example.com"}
    token = create_access_token(user_data)
    
    assert isinstance(token, str)
    
    # Декодируем и проверяем
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["username"] == "testuser"
    assert "exp" in payload
    
    # Тест с кастомным expires_delta
    custom_delta = timedelta(minutes=30)
    token2 = create_access_token(user_data, expires_delta=custom_delta)
    payload2 = jwt.decode(token2, SECRET_KEY, algorithms=[ALGORITHM])
    
    # Проверяем, что время истечения примерно корректное
    exp_time = datetime.fromtimestamp(payload2["exp"], tz=timezone.utc)
    expected_time = datetime.now(timezone.utc) + custom_delta
    time_diff = abs((exp_time - expected_time).total_seconds())
    
    assert time_diff < 10