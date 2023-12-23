from datetime import datetime

from schema import Schema

from todo.domain.entity import ToDo
from todo.infra.di_containers import todo_repo


class TestTodo:
    # Success
    def test_get_todo(self, api_client, mocker):
        # given
        todo = ToDo(id=1, contents="workout", due_datetime=datetime(2024, 1, 1))

        # when
        mocker.patch.object(todo_repo, "get_todo_by_id", return_value=todo)
        response = api_client.get("/todos/1")

        # then
        assert response.status_code == 200
        assert Schema(
            {
                "todo": {
                    "id": 1,
                    "contents": "workout",
                    "due_datetime": str,
                }
            }
        ).validate(response.json())

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
        assert Schema(
            {
                "todo": {
                    "id": 1,
                    "contents": "workout",
                    "due_datetime": str,
                }
            }
        ).validate(response.json())

    def test_patch_todos(self, api_client, mocker):
        # given
        todo = ToDo(id=1, contents="workout", due_datetime=datetime(2024, 1, 1))

        # when
        mocker.patch.object(todo_repo, "get_todo_by_id", return_value=todo)
        mocker.patch.object(todo_repo, "save", return_value=todo)

        response = api_client.patch(path="/todos/1", data={"contents": "read"})

        # then
        assert response.status_code == 200
        assert Schema(
            {
                "todo": {
                    "id": 1,
                    "contents": "read",
                    "due_datetime": str,
                }
            }
        ).validate(response.json())

    def test_delete_todos(self, api_client, mocker):
        # given
        todo = ToDo(id=1, contents="workout", due_datetime=datetime(2024, 1, 1))

        # when
        mocker.patch.object(todo_repo, "delete_todo_by_id", return_value=todo)
        response = api_client.delete("/todos/1")

        # then
        assert response.status_code == 204

    # Fail
    def test_put_todos(self, api_client):
        response = api_client.put("/todos/")
        assert response.status_code == 405
