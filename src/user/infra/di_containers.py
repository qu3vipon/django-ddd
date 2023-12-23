from user.infra.database.repository.mapper import UserMapper
from user.infra.database.repository.rdb import UserRDBRepository

user_repo = UserRDBRepository(
    model_mapper=UserMapper(),
)
