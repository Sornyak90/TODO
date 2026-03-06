from fastapi import FastAPI
import uvicorn
from web import tasks
from auth.auth_jwt import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from data import Base, engine
from contextlib import asynccontextmanager
from config import settings
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(settings)
    # Асинхронное создание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Закрываем соединения при завершении
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # разрешить доступ со всех доменов
    allow_credentials=True,   # разрешить передачу cookies и заголовков аутентификации
    allow_methods=["*"],      # разрешить все методы HTTP
    allow_headers=["*"],      # разрешить все заголовки
)

app.include_router(tasks.router)  # подключаем роутер задач
app.include_router(auth_router) 

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)  # запускаем приложение с автообновлением
