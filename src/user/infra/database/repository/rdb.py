from shared.infra.repository.rdb import RDBRepository

from user.domain.entity import User
from user.domain.exception import UserNotFoundException
from user.infra.database.repository.mapper import UserMapper


class UserRDBRepository(RDBRepository):
    def __int__(self, model_mapper: UserMapper):
        self.model_mapper = model_mapper

    def get_user_by_id(self, user_id: int) -> User:
        try:
            return self._get_by_pk(pk=user_id)
        except self.model_mapper.model_class.DoesNotExist:
            raise UserNotFoundException()

    def get_user_by_email(self, email: str) -> User:
        try:
            return self._get_by(email=email)
        except self.model_mapper.model_class.DoesNotExist:
            raise UserNotFoundException()

    def delete_user_by_id(self, user_id: int) -> None:
        try:
            self._delete(pk=user_id)
        except self.model_mapper.model_class.DoesNotExist:
            raise UserNotFoundException()
