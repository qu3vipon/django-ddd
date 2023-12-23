from django.db import models

from user.infra.database.models import User


class ToDo(models.Model):
    contents = models.CharField(blank=False, max_length=200)
    due_datetime = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")

    class Meta:
        db_table = "todo"
