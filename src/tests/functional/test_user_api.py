class TestUser:
    def test_get_user(self, api_client):
        response = api_client.get("/users/me")
        assert response.status_code == 200

    def test_sign_up_user(self, api_client):
        response = api_client.post("/users/")
        assert response.status_code == 201

    def test_log_in_user(self, api_client):
        response = api_client.post("/users/log-in")
        assert response.status_code == 200

    def test_delete_user(self, api_client):
        response = api_client.delete("/users/me")
        assert response.status_code == 204
