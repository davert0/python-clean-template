import datetime
from typing import List, Optional
from src.domain.entities.comment import Comment
from src.domain.exceptions import EntityNotFound, CommentNotFound
from src.domain.repositories.comment_repository import CommentRepository
from src.application.use_cases.log_use_cases import LogUseCase

class CreateCommentUseCase:
    def __init__(self, comment_repository: CommentRepository, log_use_case: LogUseCase):
        self.comment_repository = comment_repository
        self.log_use_case = log_use_case

    async def execute(self, user_id: int, content: str) -> Comment:
        comment = Comment(post_id=None, user_id=user_id, content=content)
        result = await self.comment_repository.create(comment)

        if result:
            await self.log_use_case.log_action(user_id=user_id, action="create_comment",
                                               timestamp=datetime.datetime.utcnow().isoformat())
        return result

class GetCommentUseCase:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    async def execute(self,
                      page: int = 1,
                      limit: int = 10,
                      sort: str = "created_at",
                      order: str = "desc",
                      ) -> list[Comment]:
        result = await self.comment_repository.get_with_pagination(
            page=page,
            limit=limit,
            sort=sort,
            order=order)
        if not result or not result.get("comments"):
            raise CommentNotFound(f"Comment not found")
        return result

class GetAllCommentsUseCase:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    async def execute(self) -> List[Comment]:
        comments = await self.comment_repository.get_all_comments()
        return comments

class UpdateCommentUseCase:
    def __init__(self, comment_repository: CommentRepository, log_use_case: LogUseCase):
        self.comment_repository = comment_repository
        self.log_use_case = log_use_case

    async def execute(self, post_id: int, content: Optional[str] = None) -> Comment:
        existing_comment = await self.comment_repository.get_by_id(post_id=post_id)
        if not existing_comment:
            raise EntityNotFound(f"Entity not found")

        if content:
            existing_comment.content = content
            await self.log_use_case.log_action(user_id=existing_comment.user_id, action="update_comment",
                                               timestamp=datetime.datetime.utcnow().isoformat())

        updated_comment = await self.comment_repository.update(existing_comment)
        if not updated_comment:
            raise EntityNotFound(f"Entity not found")
        return updated_comment