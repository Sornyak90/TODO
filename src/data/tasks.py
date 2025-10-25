from . import curs, conn, IntegrityError
from model.tasks import Task, TaskResponse
from error import Duplicate, Missing

curs.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    status BOOLEAN DEFAULT FALSE
                )
                """)


def model_to_dict(task: Task) -> dict:
    return task.dict() if task else None


def row_to_model(row: tuple) -> TaskResponse:
    id, name, status = row
    return TaskResponse(id=id, name=name, status=status)


def create(task: Task):
    qry = """insert into tasks (name, status) values 
            (:name, :status)"""
    params = model_to_dict(task)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(msg=f"Explorer {task.name} already exists")
    return get_one(task.name)


def get_one(name: str) -> Task:
    qry = "select * from tasks where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Explorer {name} not found")


def get_all() -> list[Task]:
    qry = "select * from tasks"
    curs.execute(qry)
    rows = curs.fetchall()
    return [row_to_model(row) for row in rows]


def delete(name: str):
    qry = "delete from tasks where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Task {name} not found")
    else:
        curs.fetchone()
        conn.commit()
    return True


def update(task: Task):
    qry = """update tasks set status = :status where name = :name"""
    params = model_to_dict(task)
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Task {task.name} not found")
