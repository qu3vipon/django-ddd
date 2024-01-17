import datetime
from typing import List

from todo.domain.models import ToDo
from user.domain.models import User


def get_todo_of_user(user_id: int, todo_id: int) -> ToDo:
    return ToDo.objects.get_todo_of_user(user_id=user_id, todo_id=todo_id)


def get_todos_of_user(user_id: int) -> List[ToDo]:
    return ToDo.objects.get_todos_of_user(user_id=user_id)


def create_todo(user: User, contents: str, due_datetime: datetime.datetime) -> ToDo:
    return ToDo.objects.new(user=user, contents=contents, due_datetime=due_datetime)


def update_todo(todo: ToDo, contents: str, due_datetime: datetime.datetime) -> ToDo:
    return ToDo.objects.update_values(todo=todo, contents=contents, due_datetime=due_datetime)


def delete_todo_of_user(user_id: int, todo_id: int) -> None:
    return ToDo.objects.delete(user_id=user_id, todo_id=todo_id)
