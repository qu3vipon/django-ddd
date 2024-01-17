from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from user.domain.models import User


class UserManager(models.Manager):
    def new(self, email: str, password: str) -> "User":
        return self.create(email=email, password=password)

    def delete(self, user_id: int) -> None:
        return self.get(id=user_id).delete()

    def get_user_by_id(self, user_id: int) -> "User":
        return self.get(id=user_id)

    def get_user_by_email(self, email: str) -> "User":
        return self.get(email=email)
