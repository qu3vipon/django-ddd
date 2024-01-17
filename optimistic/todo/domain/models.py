from django.db import models
from todo.domain.managers import ToDoManager
from user.domain.models import User


class ToDo(models.Model):
    contents = models.CharField(blank=False, max_length=200)
    due_datetime = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")

    objects = ToDoManager()

    class Meta:
        db_table = "todo"
