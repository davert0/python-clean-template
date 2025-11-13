from typing import Optional
from src.domain.entities.log import LogEntry
from src.domain.repositories.log_repository import LogRepository
from src.infrastructure.database.connection import DatabaseConnection

class LogRepositoryImpl(LogRepository):
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    async def create(self, log: LogEntry) -> Optional[LogEntry]:
        row = await self.db_connection.fetchrow(
            """
            INSERT INTO logs (user_id, action)
            VALUES ($1, $2)
            RETURNING user_id, action, timestamp
            """,
            log.user_id,
            log.action,
        )
        if row:
            return LogEntry(
                user_id=row["user_id"],
                action=row["action"],
                timestamp=row["timestamp"]
            )
        return None