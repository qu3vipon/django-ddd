from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from todo.domain.entity import ToDo
from todo.domain.exception import ToDoNotFoundException
from todo.infra.di_containers import todo_repo
from user.domain.entity import User
from user.infra.di_containers import user_repo


@pytest.mark.django_db
def test_create_todo():
    # given
    user: User = User.new(email="email", hashed_password="secure-pw")
    user: User = user_repo.save(entity=user)

    due_datetime: datetime = datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC"))
    todo: ToDo = ToDo.new(contents="contents", due_datetime=due_datetime, user=user)

    # when
    todo: ToDo = todo_repo.save(entity=todo)

    # then
    todo_repo.get_todo_of_user(user_id=user.id, todo_id=todo.id)


@pytest.mark.django_db
def test_filter_todos():
    # given
    user: User = User.new(email="email", hashed_password="secure-pw")
    user: User = user_repo.save(entity=user)

    due_datetime: datetime = datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC"))

    todo_1: ToDo = ToDo.new(contents="contents-1", due_datetime=due_datetime, user=user)
    todo_2: ToDo = ToDo.new(contents="contents-2", due_datetime=due_datetime, user=user)

    # when
    todo_1: ToDo = todo_repo.save(entity=todo_1)
    todo_2: ToDo = todo_repo.save(entity=todo_2)

    # then
    ret = todo_repo.get_todos_of_user(user_id=user.id)
    assert ret == [todo_1, todo_2]


@pytest.mark.django_db
def test_delete_todo():
    # given
    user: User = User.new(email="email", hashed_password="secure-pw")
    user: User = user_repo.save(entity=user)

    due_datetime: datetime = datetime(2024, 1, 1, tzinfo=ZoneInfo("UTC"))
    todo: ToDo = ToDo.new(contents="contents", due_datetime=due_datetime, user=user)
    todo: ToDo = todo_repo.save(entity=todo)

    # when
    todo_repo.delete_todo_of_user(user_id=user.id, todo_id=todo.id)

    # then
    with pytest.raises(ToDoNotFoundException):
        todo_repo.get_todo_of_user(user_id=user.id, todo_id=todo.id)
