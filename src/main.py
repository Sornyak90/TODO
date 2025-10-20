from fastapi import FastAPI
import uvicorn
from web import tasks

app = FastAPI()

app.include_router(tasks.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
