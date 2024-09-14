from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator

from src.db.settings import settings

engine = create_async_engine(settings.DB_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор асинхронных сессий базы данных.
    """
    async with AsyncSessionLocal() as session:
        yield session
