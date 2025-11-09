from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy import URL, create_engine, text, Column, Integer,String, Boolean
from .config import settings
from model.tasks import TaskResponse 

# Настройка подключения к базе данных PostgreSQL
engine = create_engine(
    url=settings.DATABASE_URI,
    echo=False
)


Base = declarative_base()
Session = sessionmaker(bind=engine)

# Определение модели таблицы задач
class User(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    status = Column(Boolean)

# Создание таблицы в базе данных
Base.metadata.create_all(engine)