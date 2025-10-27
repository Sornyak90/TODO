from fastapi import FastAPI
import uvicorn
from web import tasks
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # разрешить доступ со всех доменов
    allow_credentials=True,   # разрешить передачу cookies и заголовков аутентификации
    allow_methods=["*"],      # разрешить все методы HTTP
    allow_headers=["*"],      # разрешить все заголовки
)

app.include_router(tasks.router)  # подключаем роутер задач

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)  # запускаем приложение с автообновлением
