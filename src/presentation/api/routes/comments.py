from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases.comment_use_cases import (
    CreateCommentUseCase,
    UpdateCommentUseCase,
    GetAllCommentsUseCase,
    GetCommentUseCase
)

from src.domain.exceptions import EntityAlreadyExists, EntityNotFound, ValidationError

from src.presentation.api.dependencies import (
    get_create_comment_use_case,
    get_update_comment_use_case,
    get_get_all_comments_use_case,
    get_get_comment_use_case
)
from src.presentation.schemas.comment_schemas import (
    CommentCreateRequest,
    CommentUpdateRequest,
    CommentResponse,
    GetAllCommentsResponse, PaginatedCommentsResponse
)


router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    request: CommentCreateRequest,
    use_case: CreateCommentUseCase = Depends(get_create_comment_use_case),
):
    try:
        comment = await use_case.execute(
            user_id=request.user_id,
            content=request.content,
        )
        return CommentResponse(
            post_id=comment.post_id,
            user_id=comment.user_id,
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
    except EntityAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get("/all", response_model=GetAllCommentsResponse)
async def get_all_comments(
    use_case: GetAllCommentsUseCase = Depends(get_get_all_comments_use_case)
):
    try:
        comments = await use_case.execute()
        return GetAllCommentsResponse(
            comments=[
                CommentResponse(
                    post_id=comment.post_id,
                    user_id=comment.user_id,
                    content=comment.content,
                    created_at=comment.created_at,
                    updated_at=comment.updated_at,
                ) for comment in comments
            ]
        )
    except EntityNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/", response_model=PaginatedCommentsResponse)
async def get_comments_with_pagination(
    page: int = 1,
    limit: int = 10,
    sort: str = "created_at",
    order: str = "desc",
    use_case: GetCommentUseCase = Depends(get_get_comment_use_case)
):
    if page < 1:
        raise HTTPException(status_code=400, detail="page must be >= 1")
    if not (1 <= limit <= 100):
        raise HTTPException(status_code=400, detail="limit must be between 1 and 100")
    try:
        result = await use_case.execute(
            page=page,
            limit=limit,
            sort=sort,
            order=order
        )
        return PaginatedCommentsResponse(
            comments=[
                CommentResponse(
                    post_id=comment.post_id,
                    user_id=comment.user_id,
                    content=comment.content,
                    created_at=comment.created_at,
                    updated_at=comment.updated_at,
                ) for comment in result["comments"]
            ],
            total=result["total"],
            page=page,
            limit=limit,
        )
    except EntityNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{post_id}", response_model=CommentResponse)
async def update_comment(
    post_id: int,
    request: CommentUpdateRequest,
    use_case: UpdateCommentUseCase = Depends(get_update_comment_use_case)
):
    try:
        comment = await use_case.execute(
            post_id=post_id,
            content=request.content,
        )
        return CommentResponse(
            post_id=comment.post_id,
            user_id=comment.user_id,
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
    except EntityNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))