from abc import ABC, abstractmethod
from src.domain.entities.log import LogEntry

class LogRepository(ABC):

    @abstractmethod
    async def create(self, log: LogEntry):
        pass

