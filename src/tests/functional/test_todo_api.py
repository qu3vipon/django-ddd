from datetime import datetime

import pytest
from schema import Schema, Or

from todo.domain.entity import ToDo
from todo.infra.di_containers import todo_repo

todo_schema = Schema(
    {
        "todo": {
            "id": int,
            "contents": "workout",
            "due_datetime": Or(str, None),
        }
    }
)


class TestTodo:
    def test_get_todo(self, api_client, mocker):
        # given
        todo = ToDo(id=1, contents="workout", due_datetime=datetime(2024, 1, 1))

        # when
        mocker.patch.object(todo_repo, "get_todo_by_id", return_value=todo)
        response = api_client.get("/todos/1")

        # then
        assert response.status_code == 200
        assert todo_schema.validate(response.json())

    def test_get_todo_list(self, api_client):
        response = api_client.get("/todos/")
        assert response.status_code == 200

    def test_post_todos(self, api_client, mocker):
        # given
        todo = ToDo(id=1, contents="workout", due_datetime=datetime(2024, 1, 1))

        # when
        mocker.patch.object(todo_repo, "save", return_value=todo)
        response = api_client.post(path="/todos/", data={"contents": "workout"})

        # then
        assert response.status_code == 201
        assert todo_schema.validate(response.json())

    def test_patch_todos(self, api_client):
        response = api_client.patch("/todos/")
        assert response.status_code == 200

    def test_delete_todos(self, api_client):
        response = api_client.delete("/todos/")
        assert response.status_code == 204

    def test_put_todos(self, api_client):
        response = api_client.put("/todos/")
        assert response.status_code == 405
