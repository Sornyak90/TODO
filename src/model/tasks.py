from pydantic import BaseModel

# Основная схема задачи для взаимодействия с клиентом
class Task(BaseModel):
    name: str
    status: bool

# Полная схема задачи с уникальным идентификатором
class TaskResponse(Task):
    id: int

# Класс модели запроса на вход в систему
class LoginRequest(BaseModel):
    """
    Модель данных для входа пользователя.
    
    Поля:
    - username (str): Имя пользователя.
    - password (str): Пароль пользователя.
    """
    username: str
    password: str


# Класс модели ответа после успешного входа
class LoginResponse(BaseModel):
    """
    Модель данных для ответа после успешной аутентификации.
    
    Поля:
    - access_token (str): Токен доступа, используемый для последующих запросов.
    - token_type (str): Тип токена, по умолчанию "bearer".
    - username (str): Имя пользователя, вошедшего в систему.
    - password (str): Сообщение о успешном входе ("Login successful").
    """
    access_token: str
    token_type: str = "bearer"
    username: str
    password: str = "Login successful"