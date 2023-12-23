def test_health_check(api_client):
    response = api_client.get("/health-check/")
    assert response.status_code == 200
