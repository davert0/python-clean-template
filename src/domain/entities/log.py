from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class LogEntry:
    user_id: int
    action: str
    timestamp: Optional[datetime]