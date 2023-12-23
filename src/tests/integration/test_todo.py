from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from todo.domain.entity import ToDo
from todo.domain.exception import ToDoNotFoundException
from todo.infra.di_containers import todo_repo


@pytest.mark.django_db
def test_create_todo():
    # given
    due_datetime: datetime = datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC"))
    todo: ToDo = ToDo.new(contents="contents", due_datetime=due_datetime)

    # when
    todo: ToDo = todo_repo.save(entity=todo)

    # then
    todo_repo.get_todo_by_id(todo_id=todo.id)


@pytest.mark.django_db
def test_delete_todo():
    # given
    due_datetime: datetime = datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC"))
    todo: ToDo = ToDo.new(contents="contents", due_datetime=due_datetime)
    todo: ToDo = todo_repo.save(entity=todo)

    # when
    todo_repo.delete_todo_by_id(todo_id=todo.id)

    # then
    with pytest.raises(ToDoNotFoundException):
        todo_repo.get_todo_by_id(todo.id)
