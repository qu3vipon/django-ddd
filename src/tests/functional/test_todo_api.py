from datetime import datetime

from schema import Schema

from todo.domain.entity import ToDo
from todo.infra.di_containers import todo_command, todo_query
from user.domain.entity import User
from user.infra.di_containers import user_query


class TestTodo:
    # payload(user_id: 1)
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxfQ.VXxfcKEMlBdcasrjitwvAuZxzjCg2kWMPTwLd2E3Ofk"}

    # Success
    def test_get_todo(self, api_client, mocker):
        # given
        user: User = User(id=1, email="email", password="secure-pw")
        todo = ToDo(id=1, contents="workout", due_datetime=datetime(2024, 1, 1), user=user)

        # when
        get_todo_of_user = mocker.patch.object(todo_query, "get_todo_of_user", return_value=todo)
        response = api_client.get("/todos/1", headers=self.headers)

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

        get_todo_of_user.assert_called_once_with(user_id=1, todo_id=1)

    def test_get_todo_list(self, api_client, mocker):
        # given
        user: User = User(id=1, email="email", password="secure-pw")
        todo = ToDo(id=1, contents="workout", due_datetime=datetime(2024, 1, 1), user=user)

        # when
        mocker.patch.object(todo_query, "get_todos_of_user", return_value=[todo])
        response = api_client.get("/todos/", headers=self.headers)

        # then
        assert response.status_code == 200
        assert Schema(
            {
                "todos": [
                    {
                        "id": 1,
                        "contents": "workout",
                        "due_datetime": str,
                    }
                ]
            }
        ).validate(response.json())

    def test_post_todos(self, api_client, mocker):
        # given
        user: User = User(id=1, email="email", password="secure-pw")
        todo = ToDo(id=1, contents="workout", due_datetime=datetime(2024, 1, 1), user=user)

        # when
        get_user = mocker.patch.object(user_query, "get_user", return_value=user)
        create_todo = mocker.patch.object(todo_command, "create_todo", return_value=todo)

        response = api_client.post(
            path="/todos/",
            data={"contents": "workout", "due_datetime": "2024-01-01T00:00:00"},
            headers=self.headers,
        )
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

        get_user.assert_called_once_with(user_id=1)
        create_todo.assert_called_once_with(user=user, contents="workout", due_datetime=datetime(2024, 1, 1))

    def test_patch_todos(self, api_client, mocker):
        before_update, after_update = "workout", "read"

        # given
        user: User = User(id=1, email="email", password="secure-pw")
        todo = ToDo(id=1, contents=before_update, due_datetime=datetime(2024, 1, 1), user=user)
        todo_updated = ToDo(id=1, contents=after_update, due_datetime=datetime(2024, 1, 1), user=user)

        # when
        get_todo_of_user = mocker.patch.object(todo_query, "get_todo_of_user", return_value=todo)
        update_todo = mocker.patch.object(todo_command, "update_todo", return_value=todo_updated)

        response = api_client.patch(path="/todos/1", data={"contents": after_update}, headers=self.headers)

        # then
        assert response.status_code == 200
        assert Schema(
            {
                "todo": {
                    "id": 1,
                    "contents": after_update,
                    "due_datetime": str,
                }
            }
        ).validate(response.json())

        get_todo_of_user.assert_called_once_with(user_id=1, todo_id=1)
        update_todo.assert_called_once_with(todo=todo, contents=after_update, due_datetime=None)

    def test_delete_todos(self, api_client, mocker):
        # given
        user: User = User(id=1, email="email", password="secure-pw")
        todo = ToDo(id=1, contents="workout", due_datetime=datetime(2024, 1, 1), user=user)

        # when
        delete_todo_of_user = mocker.patch.object(todo_command, "delete_todo_of_user", return_value=todo)
        response = api_client.delete("/todos/1", headers=self.headers)

        # then
        assert response.status_code == 204
        delete_todo_of_user.assert_called_once_with(user_id=1, todo_id=1)

    # Fail
    def test_put_todos(self, api_client):
        response = api_client.put("/todos/")
        assert response.status_code == 405
