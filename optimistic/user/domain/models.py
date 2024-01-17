from __future__ import annotations

from django.db import models
from user.domain.managers import UserManager


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200, blank=False, null=False)

    objects = UserManager()

    class Meta:
        app_label = "user"
        db_table = "user"
