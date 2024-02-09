from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        app_label = "user"
        db_table = "user"
