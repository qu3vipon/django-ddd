import pytest

from user.domain.entity import User
from user.infra.di_containers import user_repo


@pytest.mark.django_db
def test_create_user():
    # given
    user: User = User.new(email="email", password="secure-pw")

    # when
    user: User = user_repo.save(entity=user)

    # then
    user_repo.get_user_by_id(user_id=user.id)
