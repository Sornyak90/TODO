from model.tasks import Task
import data.tasks as service


def create(task: Task) -> Task | None:
    return service.create(task)


# def get_all() -> list(Task):
#     return None


def get_one(id) -> Task | None:
    return service.get_one(id)


# def update(task: Task) -> Task:
#     return task


# def replace(task: Task) -> Task:
#     return task


# def delete(id) -> bool | None:
#     return None
