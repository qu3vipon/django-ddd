import pytest
from schema import Schema


class TestTodo:

    def test_get_todos(self, api_client):
        response = api_client.get("/todos/")
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_post_todos(self, api_client):
        response = api_client.post(path="/todos/", data={"contents": "workout"})
        assert response.status_code == 201
        schema = Schema(
            {
                "todo": {
                    "id": int,
                    "contents": "workout",
                    "due_datetime": None,
                }
            }
        )
        assert schema.validate(response.json())

    def test_patch_todos(self, api_client):
        response = api_client.patch("/todos/")
        assert response.status_code == 200

    def test_delete_todos(self, api_client):
        response = api_client.delete("/todos/")
        assert response.status_code == 204

    def test_put_todos(self, api_client):
        response = api_client.put("/todos/")
        assert response.status_code == 405
