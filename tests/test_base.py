def test_check_health_handler(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "OK"
    }
