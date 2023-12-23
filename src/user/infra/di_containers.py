from shared.infra.di_containers import auth_service
from user.application.command import UserCommand
from user.application.query import UserQuery
from user.infra.database.repository.mapper import UserMapper
from user.infra.database.repository.rdb import UserRDBRepository

user_repo = UserRDBRepository(
    model_mapper=UserMapper(),
)

user_query = UserQuery(
    user_repo=user_repo,
)

user_command = UserCommand(
    auth_service=auth_service,
    user_repo=user_repo,
)
