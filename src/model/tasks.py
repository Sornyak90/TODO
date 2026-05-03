from pydantic import BaseModel
from enum import StrEnum

# Основная схема задачи для взаимодействия с клиентом
class Task(BaseModel):
    name: str
    status: bool

class Status(StrEnum):
   default = "0"
   true = "1"
   false = "2"

# Полная схема задачи с уникальным идентификатором
class TaskResponse(Task):
    id: int

class Users(BaseModel):
    username: str
    password: str

class UsersResponse(Users):
    id: int