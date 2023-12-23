from datetime import datetime

from schema import Schema

from todo.domain.entity import ToDo
from todo.infra.di_containers import todo_command, todo_query
from user.domain.entity import User


class TestTodo:
    jwt_token: str = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxfQ.VXxfcKEMlBdcasrjitwvAuZxzjCg2kWMPTwLd2E3Ofk"

    # Success
    def test_get_todo(self, api_client, mocker):
        # given
        user: User = User(id=1, email="email", password="secure-pw")
        todo = ToDo(id=1, contents="workout", due_datetime=datetime(2024, 1, 1), user=user)

        # when
        mocker.patch.object(todo_query, "get_todo_by_id", return_value=todo)
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
        response = api_client.get("/todos/", headers={"Authorization": self.jwt_token})
        assert response.status_code == 200

    def test_post_todos(self, api_client, mocker):
        # given
        user: User = User(id=1, email="email", password="secure-pw")
        todo = ToDo(id=1, contents="workout", due_datetime=datetime(2024, 1, 1), user=user)

        # when
        mocker.patch.object(todo_command, "create_todo", return_value=todo)
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
        before, after = "workout", "read"

        # given
        user: User = User(id=1, email="email", password="secure-pw")
        todo = ToDo(id=1, contents=before, due_datetime=datetime(2024, 1, 1), user=user)
        todo_updated = ToDo(id=1, contents=after, due_datetime=datetime(2024, 1, 1), user=user)

        # when
        mocker.patch.object(todo_query, "get_todo_by_id", return_value=todo)
        mocker.patch.object(todo_command, "update_todo", return_value=todo_updated)

        response = api_client.patch(path="/todos/1", data={"contents": after})

        # then
        assert response.status_code == 200
        assert Schema(
            {
                "todo": {
                    "id": 1,
                    "contents": after,
                    "due_datetime": str,
                }
            }
        ).validate(response.json())

    def test_delete_todos(self, api_client, mocker):
        # given
        user: User = User(id=1, email="email", password="secure-pw")
        todo = ToDo(id=1, contents="workout", due_datetime=datetime(2024, 1, 1), user=user)

        # when
        mocker.patch.object(todo_command, "delete_todo_by_id", return_value=todo)
        response = api_client.delete("/todos/1")

        # then
        assert response.status_code == 204

    # Fail
    def test_put_todos(self, api_client):
        response = api_client.put("/todos/")
        assert response.status_code == 405
