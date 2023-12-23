from shared.infra.repository.mapper import ModelMapper

from user.domain.entity import User as UserEntity
from user.infra.database.models import User as UserModel


class UserMapper(ModelMapper):
    model_class = UserModel
    entity_class = UserEntity
