from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from config import settings



def get_session_engine():
    # Используем асинхронный движок
    engine = create_async_engine(
        url=settings.database_url.replace('postgresql://', 'postgresql+asyncpg://'),
        echo=False
    )
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    ), engine

Base = declarative_base()

# Модель User
class User(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    status = Column(Boolean)

class fake_db(Base):
    __tablename__ = 'fake_db'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    password = Column(String)
