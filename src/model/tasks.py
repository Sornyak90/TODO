from pydantic import BaseModel


class Task(BaseModel):
    name: str
    status: bool


class TaskResponse(Task):
    id: int
