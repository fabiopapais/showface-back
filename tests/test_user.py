import pytest

def testGetUser(client):

    client.post(
        "/auth/register",
        json={"name": "testuser", "email": "test@test.com", "password": "securepswd"},
    )

    response = client.get(
        "/user/1",
    )

    assert response.status_code == 200