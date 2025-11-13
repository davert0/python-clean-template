from typing import Optional, Any, Coroutine

from src.domain.entities.comment import Comment
from src.domain.repositories.comment_repository import CommentRepository
from src.infrastructure.database.connection import DatabaseConnection

class PostgresCommentRepository(CommentRepository):
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def _map_row_to_comment(self, row) -> Comment | None:
        if not row:
            return None
        return Comment(
            post_id=row['post_id'],
            user_id=row['user_id'],
            content=row['content'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )

    async def create(self, comment: Comment) -> Comment:
        row = await self.db.fetchrow(
            """
            insert into comments (user_id, content)
            values ($1, $2)
            returning post_id, user_id, content, created_at, updated_at
            """,
            comment.user_id, comment.content
        )
        return self._map_row_to_comment(row)

    async def get_by_id(self, post_id: int) -> Optional[Comment]:
        row = await self.db.fetchrow(
            """
            select post_id, user_id, content, created_at, updated_at
            from comments
            where post_id = $1
            """,
            post_id
        )
        return self._map_row_to_comment(row)

    async def get_all_comments(self) -> list[Comment]:
        rows = await self.db.fetch(
            """
            select post_id, user_id, content, created_at, updated_at
            from comments
            """
        )
        return [self._map_row_to_comment(row) for row in rows]

    async def update(self, comment: Comment) -> Optional[Comment]:
        row = await self.db.fetchrow(
            """
            update comments
            set content = $1, updated_at = current_timestamp
            where post_id = $2
            returning post_id, user_id, content, created_at, updated_at
            """,
            comment.content, comment.post_id
        )
        return self._map_row_to_comment(row)

    async def get_with_pagination(self,
                               page: int = 1,
                               limit: int = 10,
                               sort: str = "created_at",
                               order: str = "desc"
                               ) -> dict[str, list[Comment | None] | int | Any]:
        offset = (page - 1) * limit

        if sort not in {"created_at", "updated_at"}:
            sort = "created_at"
        if order.lower() not in {"asc", "desc"}:
            order = "desc"

        query = f"""
            SELECT post_id, user_id, content, created_at, updated_at
            FROM comments
            ORDER BY {sort} {order}
            LIMIT $1 offset $2
        """
        rows = await self.db.fetch(
            query,
            limit, offset
        )

        total_row = await self.db.fetchrow("SELECT COUNT(*) AS total FROM comments")
        total = total_row["total"] if total_row else 0

        comments = [self._map_row_to_comment(row) for row in rows]

        return {
            "comments": comments, "total": total,
            "page": page, "limit": limit
        }