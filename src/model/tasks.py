from pydantic import BaseModel
from enum import Enum

# Основная схема задачи для взаимодействия с клиентом
class Task(BaseModel):
    name: str
    status: bool

class Filtr(Enum):
   default = 0
   true = 1
   false = 2

# Полная схема задачи с уникальным идентификатором
class TaskResponse(Task):
    id: int

class User(BaseModel):
    username: str
    password: str