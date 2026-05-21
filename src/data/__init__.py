from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Identity
from config import settings


def get_session_engine():
    # Используем асинхронный движок
    engine = create_async_engine(
        url=settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
        echo=False,
    )
    return async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    ), engine


Base = declarative_base()


# Модель Tasks
class Tasks(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    status: Mapped[bool] = mapped_column()


class User(Base):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column()
