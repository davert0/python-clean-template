import datetime
from typing import Optional

from src.domain.entities.log import LogEntry
from src.domain.repositories.log_repository import LogRepository

class LogUseCase:
    def __init__(self, log_repository: LogRepository):
        self.log_repository = log_repository

    async def log_action(self, user_id: Optional[int], action: str, timestamp: Optional[str] = None) -> None:
        log = LogEntry(
            user_id=user_id,
            action=action,
            timestamp=timestamp or datetime.datetime.utcnow().isoformat()
        )
        await self.log_repository.create(log)