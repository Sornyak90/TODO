from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

from web import tasks
from auth.auth_jwt import router as auth_router
from config import settings
from data import Base, get_session_engine
from data.crud import add_fake_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    session_maker, engine = get_session_engine()
    # Асинхронное создание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    await add_fake_users(session_maker)

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
