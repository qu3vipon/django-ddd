from shared.exception import NotAuthorizedException
from shared.presentation.rest.containers import auth_service
from user.domain.models import User


def sign_up_user(email: str, plain_password: str) -> User:
    hashed_password: str = auth_service.hash_password(plain_password=plain_password)
    return User.objects.new(email=email, password=hashed_password)


def delete_user_by_id(user_id: int) -> None:
    User.objects.delete(user_id=user_id)


def log_in_user(email: str, plain_password: str) -> str:
    user: User = User.objects.get_user_by_email(email=email)

    if not auth_service.verify_password(plain_password=plain_password, hashed_password=user.password):
        raise NotAuthorizedException()

    return auth_service.create_jwt(user=user)


def get_user(user_id: int) -> User:
    return User.objects.get_user_by_id(user_id=user_id)
