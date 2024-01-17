from datetime import datetime

import pytest
from schema import Schema
from todo.domain.models import ToDo
from user.domain.models import User

# from todo.domain.entity import ToDo
# from todo.presentation.rest.containers import todo_command, todo_query
# from user.domain.entity import User
# from user.presentation.rest.containers import user_query


class TestTodo:
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxfQ.NCNw2ZWj2UMA7kZXnKg2Bg7eObEUUXysJzGzRK4b6Ps"
    }

    @pytest.mark.django_db
    def test_get_todo(self, api_client):
        # given
        user = User.objects.create(
            email="email", password="$2b$12$H89akv/AxCmqoSGJmcwS6eBqMD0Nlz1BTHHOso60dvnERYgzzOMuy"
        )
        ToDo.objects.create(id=1, contents="workout", due_datetime=datetime(2024, 1, 1), user=user)

        # when
        response = api_client.get("/api/todos/1", headers=self.headers)

        # then
        assert response.status_code == 200
        assert Schema(
            {
                "results": {
                    "todo": {
                        "id": 1,
                        "contents": "workout",
                        "due_datetime": str,
                    }
                }
            }
        ).validate(response.json())

    @pytest.mark.django_db
    def test_get_todo_list(self, api_client):
        # given
        user = User.objects.create(
            email="email", password="$2b$12$H89akv/AxCmqoSGJmcwS6eBqMD0Nlz1BTHHOso60dvnERYgzzOMuy"
        )
        ToDo.objects.create(id=1, contents="workout", due_datetime=datetime(2024, 1, 1), user=user)
        ToDo.objects.create(id=2, contents="read", due_datetime=datetime(2024, 1, 1), user=user)

        # when
        response = api_client.get("/api/todos/", headers=self.headers)

        # then
        assert response.status_code == 200
        assert Schema(
            {
                "results": {
                    "todos": [
                        {
                            "id": int,
                            "contents": str,
                            "due_datetime": str,
                        }
                    ]
                }
            }
        ).validate(response.json())

    @pytest.mark.django_db
    def test_post_todos(self, api_client):
        # given
        User.objects.create(email="email", password="$2b$12$H89akv/AxCmqoSGJmcwS6eBqMD0Nlz1BTHHOso60dvnERYgzzOMuy")

        # when
        response = api_client.post(
            path="/api/todos/",
            data={"contents": "workout", "due_datetime": "2024-01-01T00:00:00"},
            headers=self.headers,
        )
        # then
        assert response.status_code == 201
        assert Schema(
            {
                "results": {
                    "todo": {
                        "id": 1,
                        "contents": "workout",
                        "due_datetime": str,
                    }
                }
            }
        ).validate(response.json())

    @pytest.mark.django_db
    def test_patch_todos(self, api_client):
        # given
        user = User.objects.create(
            email="email", password="$2b$12$H89akv/AxCmqoSGJmcwS6eBqMD0Nlz1BTHHOso60dvnERYgzzOMuy"
        )
        ToDo.objects.create(id=1, contents="workout", due_datetime=datetime(2024, 1, 1), user=user)

        # when
        response = api_client.patch(path="/api/todos/1", data={"contents": "read"}, headers=self.headers)

        # then
        assert response.status_code == 200
        assert Schema(
            {
                "results": {
                    "todo": {
                        "id": 1,
                        "contents": "read",
                        "due_datetime": None,
                    }
                }
            }
        ).validate(response.json())

    @pytest.mark.django_db
    def test_delete_todos(self, api_client):
        # given
        user = User.objects.create(
            email="email", password="$2b$12$H89akv/AxCmqoSGJmcwS6eBqMD0Nlz1BTHHOso60dvnERYgzzOMuy"
        )
        ToDo.objects.create(id=1, contents="workout", due_datetime=datetime(2024, 1, 1), user=user)

        # when
        response = api_client.delete("/api/todos/1", headers=self.headers)

        # then
        assert response.status_code == 204
