from schema import Schema

from user.domain.entity import User
from user.infra.di_containers import user_command


class TestUser:
    # payload(user_id: 1)
    jwt_token: str = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxfQ.VXxfcKEMlBdcasrjitwvAuZxzjCg2kWMPTwLd2E3Ofk"

    def test_sign_up_user(self, api_client, mocker):
        # given
        user = User(id=1, email="email", password="hashed")
        sign_up_user = mocker.patch.object(user_command, "sign_up_user", return_value=user)

        # when
        response = api_client.post("/users/", data={"email": "email", "password": "plain"})

        # then
        sign_up_user.assert_called_once_with(email="email", plain_password="plain")
        assert response.status_code == 201
        assert Schema(
            {
                "user": {
                    "id": 1,
                    "email": "email",
                }
            }
        ).is_valid(response.json())

    def test_log_in_user(self, api_client, mocker):
        # given
        log_in_user = mocker.patch.object(user_command, "log_in_user", return_value="jwt_token")

        # when
        response = api_client.post("/users/log-in", data={"email": "email", "password": "plain"})

        # then
        log_in_user.assert_called_once_with(email="email", plain_password="plain")
        assert response.status_code == 200
        assert Schema(
            {
                "token": str
            }
        ).is_valid(response.json())

    def test_delete_user(self, api_client, mocker):
        # given
        delete_user = mocker.patch.object(user_command, "delete_user_by_id", return_value=None)

        # when
        response = api_client.delete("/users/me", headers={"Authorization": self.jwt_token})

        # then
        assert response.status_code == 204
        delete_user.assert_called_once_with(user_id=1)
