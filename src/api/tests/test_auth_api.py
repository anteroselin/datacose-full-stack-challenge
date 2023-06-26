from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_login():
    response = client.post(
        "/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": "admin", "password": "password"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "access_token" in response_json
    assert "token_type" in response_json
    assert response_json["token_type"] == "bearer"
