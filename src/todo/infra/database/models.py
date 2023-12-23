from django.db import models


class ToDo(models.Model):
    contents = models.CharField(blank=False, max_length=200)
    due_datetime = models.DateTimeField(null=True)
