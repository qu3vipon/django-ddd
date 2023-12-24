import pytest
from user.domain.entity import User
from user.domain.exception import UserNotFoundException
from user.infra.di_containers import user_repo


@pytest.mark.django_db
def test_create_user():
    # given
    user: User = User.new(email="email", hashed_password="secure-pw")

    # when
    user: User = user_repo.save(entity=user)

    # then
    user_repo.get_user_by_id(user_id=user.id)


@pytest.mark.django_db
def test_delete_user():
    # given
    user: User = User.new(email="email", hashed_password="secure-pw")
    user: User = user_repo.save(entity=user)

    # when
    user_repo.delete_user_by_id(user_id=user.id)

    # then
    with pytest.raises(UserNotFoundException):
        user_repo.get_user_by_id(user_id=user.id)
