from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Comment:
    post_id: Optional[int]
    user_id: Optional[int]
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None