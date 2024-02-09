from shared.presentation.rest.containers import auth_service

from user.application.command import UserCommand
from user.application.query import UserQuery
from user.infra.database.repository.rdb import UserRDBRepository

user_repo = UserRDBRepository()

user_query = UserQuery(user_repo=user_repo)

user_command = UserCommand(
    auth_service=auth_service,
    user_repo=user_repo,
)
