import pytest
from django.test.client import Client


@pytest.fixture(scope="session")
def api_client():
    return Client()
