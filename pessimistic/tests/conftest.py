import pytest
from django.test.client import Client


class APIClient(Client):
    def post(
        self,
        path,
        data=None,
        content_type="application/json",
        follow=False,
        secure=False,
        *,
        headers=None,
        **extra,
    ):
        return super().post(
            path=path,
            data=data,
            content_type=content_type,
            follow=follow,
            secure=secure,
            headers=headers,
            **extra,
        )

    def patch(
        self,
        path,
        data="",
        content_type="application/json",
        follow=False,
        secure=False,
        *,
        headers=None,
        **extra,
    ):
        return super().patch(
            path=path,
            data=data,
            content_type=content_type,
            follow=follow,
            secure=secure,
            headers=headers,
            **extra,
        )


@pytest.fixture(scope="session")
def api_client():
    return APIClient()
