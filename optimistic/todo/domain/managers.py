import datetime
from typing import TYPE_CHECKING, List

from django.db import models

if TYPE_CHECKING:
    from todo.domain.models import ToDo
    from user.domain.models import User


class ToDoManager(models.Manager):
    def new(self, user: "User", contents: str, due_datetime: datetime.datetime):
        return self.create(user=user, contents=contents, due_datetime=due_datetime)

    def get_todo_of_user(self, user_id: int, todo_id: int) -> "ToDo":
        return self.get(id=todo_id, user_id=user_id)

    def get_todos_of_user(self, user_id: int) -> List["ToDo"]:
        return self.filter(user_id=user_id)

    def update_values(self, todo: "ToDo", contents: str, due_datetime: datetime.datetime) -> "ToDo":
        todo.contents = contents
        todo.due_datetime = due_datetime
        todo.save()
        return self.get(id=todo.id)

    def delete(self, todo_id: int, user_id: int) -> None:
        return self.get(id=todo_id, user_id=user_id).delete()
