class TestTodo:
    def test_get_todos(self, api_client):
        response = api_client.get("/todos/")
        assert response.status_code == 200

    def test_post_todos(self, api_client):
        response = api_client.post(path="/todos/", data={"todo": "workout"})
        assert response.status_code == 201

    def test_patch_todos(self, api_client):
        response = api_client.patch("/todos/")
        assert response.status_code == 200

    def test_delete_todos(self, api_client):
        response = api_client.delete("/todos/")
        assert response.status_code == 204

    def test_put_todos(self, api_client):
        response = api_client.put("/todos/")
        assert response.status_code == 405
