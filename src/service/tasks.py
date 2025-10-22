from model.tasks import Task
import data.tasks as service


def create(task: Task) -> Task | None:
    return service.create(task)


def get_all():
    return service.get_all()


def get_one(name: str) -> Task | None:
    return service.get_one(name)


def update(task: Task):
    return service.update(task)


def delete(name: str) -> bool | None:
    return service.delete(name)
