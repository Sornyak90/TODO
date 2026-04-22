from tests.conftest import *

async def test_login_success(client):
    """Тест успешной аутентификации"""
    response = await client.post("/login/", data={
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

async def test_login_invalid_username(client):
    """Тест аутентификации с неверным именем пользователя"""
    response = await client.post("/login/", data={
        "username": INVALID_USER,
        "password": TEST_PASSWORD
    })
    assert response.status_code == 400

async def test_login_invalid_password(client):
    """Тест аутентификации с неверным паролем"""
    response = await client.post("/login/", data={
        "username": TEST_USER,
        "password": INVALID_PASSWORD
    })
    
    assert response.status_code == 400
    assert "Invalid credentials" in response.text
    
async def test_login_empty_credentials(client):
    """Тест аутентификации с пустыми данными"""
    response = await client.post("/login/", data={
        "username": "",
        "password": ""
    })
    
    assert response.status_code == 400
    assert "Invalid credentials" in response.text

async def test_token_expiration(auth_token):

    """Тест срока действия токена"""
    payload = jwt.decode(auth_token, SECRET_KEY, algorithms=[ALGORITHM])
    exp_timestamp = payload["exp"]
    exp_datetime = datetime.fromtimestamp(exp_timestamp,  tz=timezone.utc)
    
    # Проверяем, что срок действия примерно равен настроенному
    expected_expiry = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    time_diff = abs((exp_datetime.replace(tzinfo=timezone.utc) - expected_expiry).total_seconds())
    
    # Допускаем разницу в 10 секунд из-за времени выполнения
    assert time_diff < 10

    