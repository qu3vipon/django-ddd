from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from todo.domain.entity import ToDo
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
