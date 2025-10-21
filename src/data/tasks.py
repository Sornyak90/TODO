from . import curs, IntegrityError
from model.tasks import Task
from error import Duplicate, Missing

curs.execute("""create table if not exists tasks(
                id INT primary key,
                name TEXT
                )""")


def model_to_dict(task: Task) -> dict:
    return task.dict() if task else None


def row_to_model(row: tuple) -> Task:
    id, name = row
    return Task(id=id, name=name)


def create(task: Task):
    qry = """insert into tasks (id, name) values 
            (:id, :name)"""
    params = model_to_dict(task)
    try:
        curs.execute(qry, params)
    except IntegrityError as e:
        raise Duplicate(msg=f"Task {task.id} already exists")
    return get_one(task.id)

def get_one(id: int) -> Task:
    qry = "select * from tasks where id=:id"
    params = {"id": id}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Task {id} not found")
    
