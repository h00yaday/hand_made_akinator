from typing import AsyncGenerator
from src.db.session import async_session_maker

async def get_db() -> AsyncGenerator:
    """
    Асинхронный генератор сессий базы данных.
    Позволяет FastAPI автоматически внедрять сессию в эндпоинты.
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            # Сессия закрывается автоматически, но мы подстрахуемся
            await session.close()