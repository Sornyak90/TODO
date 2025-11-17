from pydantic import BaseModel

# Основная схема задачи для взаимодействия с клиентом
class Task(BaseModel):
    name: str
    status: bool

# Полная схема задачи с уникальным идентификатором
class TaskResponse(Task):
    id: int

class User(BaseModel):
    username: str
    password: str