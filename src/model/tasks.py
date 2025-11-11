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

def ErrorMessage(BaseModel):
    detail: str

from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    roles: list[str]


class UserFullModel(UserModel):
    password_hash: str


users: dict[int, UserFullModel] = {
    0: UserFullModel(
        username="admin",
        password_hash="$5$rounds=535000$VmjDekF0Mi38FSlc$KF6JKT1wXEZCw7rB/zK3om/4Bo.Vuf74mLRHQuYiEh0",
        roles=["admin"],
    )
}