from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import os
import json
from dotenv import load_dotenv
from pathlib import Path

from web import tasks
from auth.auth_jwt import router as auth_router
from config import settings
from data import Base, get_session_engine
from data.crud import add_fake_users


@asynccontextmanager
async def lifespan(app: FastAPI):

    session_maker, engine = get_session_engine()

    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    fake_users_str = os.getenv("FAKE_USERS")
    fake_users = json.loads(fake_users_str)

    # Асинхронное создание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    await add_fake_users(session_maker, fake_users)

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

app.include_router(tasks.router_task)  # подключаем роутер задач
app.include_router(auth_router)
app.include_router(tasks.router_db)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)  # запускаем приложение с автообновлением
