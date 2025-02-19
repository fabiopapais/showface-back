import pytest
from tests.testutils import regNewUser

def test_register(client):
    response = client.post(
        "/auth/register",
        json={"name": "testuser", "email": "test@test.com", "password": "securepswd"},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert "token" in data

def test_login(client):

    regNewUser(client)

    response = client.post(
        "/auth/login",
        json={"name": "testuser", "email": "test@test.com", "password": "securepswd"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data