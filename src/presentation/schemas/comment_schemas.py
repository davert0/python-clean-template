from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class CommentCreateRequest(BaseModel):
    user_id: int
    content: str


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    post_id : int
    user_id: int
    content: str
    created_at: datetime
    updated_at: datetime


class GetAllCommentsResponse(BaseModel):
    comments: list[CommentResponse]


class PaginatedCommentsResponse(BaseModel):
    comments: list[CommentResponse]
    total: int
    page: int
    limit: int


class CommentUpdateRequest(BaseModel):
    content: Optional[str] = None