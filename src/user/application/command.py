from shared.domain.exception import NotAuthorizedException
from shared.infra.authentication import AuthenticationService

from user.domain.entity import User
from user.domain.exception import UserNotFoundException
from user.infra.database.repository.rdb import UserRDBRepository


class UserCommand:
    def __init__(
        self,
        auth_service: AuthenticationService,
        user_repo: UserRDBRepository,
    ):
        self.auth_service = auth_service
        self.user_repo = user_repo

    def sign_up_user(self, email: str, plain_password: str) -> User:
        hashed_password: str = self.auth_service.hash_password(plain_password=plain_password)
        user: User = User.new(email=email, hashed_password=hashed_password)
        return self.user_repo.save(entity=user)

    def log_in_user(self, email: str, plain_password: str) -> str:
        try:
            user: User = self.user_repo.get_user_by_email(email=email)
        except UserNotFoundException:
            raise NotAuthorizedException()

        if not self.auth_service.verify_password(plain_password=plain_password, hashed_password=user.password):
            raise NotAuthorizedException()

        return self.auth_service.create_jwt(user=user)

    def delete_user_by_id(self, user_id: int) -> None:
        self.user_repo.delete_user_by_id(user_id=user_id)
