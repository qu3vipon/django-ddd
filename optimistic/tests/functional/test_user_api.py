import pytest
from schema import Schema
from user.domain.models import User


class TestUser:
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxfQ.NCNw2ZWj2UMA7kZXnKg2Bg7eObEUUXysJzGzRK4b6Ps"
    }

    @pytest.mark.django_db
    def test_sign_up_user(self, api_client):
        # given
        User(id=1, email="email", password="hashed")

        # when
        response = api_client.post("/api/users/", data={"email": "email", "password": "plain"})

        # then
        assert response.status_code == 201
        assert Schema(
            {
                "results": {
                    "user": {
                        "id": 1,
                        "email": "email",
                    }
                }
            }
        ).is_valid(response.json())

    @pytest.mark.django_db
    def test_log_in_user(self, api_client):
        # given
        User.objects.create(email="email", password="$2b$12$H89akv/AxCmqoSGJmcwS6eBqMD0Nlz1BTHHOso60dvnERYgzzOMuy")

        # when
        response = api_client.post("/api/users/log-in", data={"email": "email", "password": "plain"})

        # then
        assert response.status_code == 200
        assert Schema({"results": {"token": str}}).is_valid(response.json())

    @pytest.mark.django_db
    def test_delete_user(self, api_client):
        # given
        User.objects.create(email="email", password="$2b$12$H89akv/AxCmqoSGJmcwS6eBqMD0Nlz1BTHHOso60dvnERYgzzOMuy")

        # when
        response = api_client.delete("/api/users/me", headers=self.headers)

        # then
        assert response.status_code == 204
