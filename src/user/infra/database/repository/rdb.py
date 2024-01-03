from shared.infra.repository.rdb import RDBRepository

from user.domain.entity import User as UserEntity
from user.domain.exception import UserNotFoundException
from user.infra.database.models import User as UserModel
from user.infra.database.repository.mapper import UserMapper


class UserRDBRepository(RDBRepository):
    def __init__(self, model_mapper: UserMapper):
        self.model_mapper = model_mapper

    def get_user_by_id(self, user_id: int) -> UserEntity:
        try:
            return self.model_mapper.to_entity(instance=UserModel.objects.get(id=user_id))
        except UserModel.DoesNotExist:
            raise UserNotFoundException()

    def get_user_by_email(self, email: str) -> UserEntity:
        try:
            return self.model_mapper.to_entity(instance=UserModel.objects.get(email=email))
        except UserModel.DoesNotExist:
            raise UserNotFoundException()

    @staticmethod
    def delete_user_by_id(user_id: int) -> None:
        try:
            UserModel.objects.get(id=user_id).delete()
        except UserModel.DoesNotExist:
            raise UserNotFoundException()
