from shared.infra.repository.mapper import ModelMapperInterface

from user.domain.entity import User as UserEntity
from user.infra.database.models import User as UserModel


class UserMapper(ModelMapperInterface):
    def to_entity(self, instance: UserModel) -> UserEntity:
        return UserEntity(
            id=instance.id,
            email=instance.email,
            password=instance.password,
        )

    def to_instance(self, entity: UserEntity) -> UserModel:
        return UserModel(
            id=entity.id,
            email=entity.email,
            password=entity.password,
        )
