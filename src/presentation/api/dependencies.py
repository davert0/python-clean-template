from src.application.use_cases.user_use_cases import (
    CreateUserUseCase,
    GetUserUseCase,
    GetAllUsersUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
)
from src.application.use_cases.comment_use_cases import (
    CreateCommentUseCase,
    UpdateCommentUseCase,
    GetAllCommentsUseCase,
    GetCommentUseCase
)
from src.application.use_cases.log_use_cases import LogUseCase


from src.application.use_cases.log_use_cases import LogUseCase
from src.infrastructure.database.connection import db_connection
from src.infrastructure.repositories.postgres_user_repository import PostgresUserRepository
from src.infrastructure.repositories.postgres_comment_repository import PostgresCommentRepository
from src.infrastructure.repositories.postgres_log_repository import LogRepositoryImpl


''' User related dependencies '''

def get_user_repository():
    return PostgresUserRepository(db_connection)


def get_create_user_use_case():
    return CreateUserUseCase(get_user_repository())


def get_get_user_use_case():
    return GetUserUseCase(get_user_repository())


def get_get_all_users_use_case():
    return GetAllUsersUseCase(get_user_repository())


def get_update_user_use_case():
    return UpdateUserUseCase(get_user_repository())


def get_delete_user_use_case():
    return DeleteUserUseCase(get_user_repository())


''' Comment related dependencies '''

def get_comment_repository():
    return PostgresCommentRepository(db_connection)


def get_create_comment_use_case():
    return CreateCommentUseCase(get_comment_repository(), get_log_use_case())


def get_get_comment_use_case():
    return GetCommentUseCase(get_comment_repository())


def get_get_all_comments_use_case():
    return GetAllCommentsUseCase(get_comment_repository())


def get_update_comment_use_case():
    return UpdateCommentUseCase(get_comment_repository(), get_log_use_case())


''' Log related dependencies '''

def get_log_repository():
    return LogRepositoryImpl(db_connection)


def get_log_use_case():
    return LogUseCase(get_log_repository())