import os
import asyncpg
import logging
from typing import Optional

from src.infrastructure.config import settings

logger = logging.getLogger(__name__)


class DatabaseConnection:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self.dsn = os.getenv('DATABASE_URL')
    
    async def connect(self):
        if not self.pool:
            try:
                logger.info("Попытка подключения к БД")
                self.pool = await asyncpg.create_pool(
                    host=settings.database_host,
                    port=settings.database_port,
                    database=settings.database_name,
                    user=settings.database_user,
                    password=settings.database_password,
                    min_size=1,
                    max_size=20,
                    timeout=30.0,
                    command_timeout=60.0,
                )
                logger.info("Подключение к БД успешно установлено")
            except (ConnectionError, OSError, Exception) as e:
                logger.error(f"Ошибка подключения к БД: {e}")
    
    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.pool = None
    
    async def execute(self, query: str, *args):
        async with self.pool.acquire(timeout=10.0) as connection:
            return await connection.execute(query, *args)
    
    async def fetch(self, query: str, *args):
        async with self.pool.acquire(timeout=10.0) as connection:
            return await connection.fetch(query, *args)
    
    async def fetchrow(self, query: str, *args):
        async with self.pool.acquire(timeout=10.0) as connection:
            return await connection.fetchrow(query, *args)


db_connection = DatabaseConnection()

