from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.comment import Comment

class CommentRepository(ABC):
    @abstractmethod
    async def create(self, comment: Comment) -> Optional[Comment]:
        pass

    @abstractmethod
    async def get_by_id(self, post_id: int) -> Optional[Comment]:
        pass

    @abstractmethod
    async def get_all_comments(self) -> List[Comment]:
        pass

    @abstractmethod
    async def get_with_pagination(self,
                                  page: int,
                                  limit: int,
                                  sort: str,
                                  order: str
                                  ) -> List[Comment]:
        pass


    @abstractmethod
    async def update(self, comment: Comment) -> Optional[Comment]:
        pass