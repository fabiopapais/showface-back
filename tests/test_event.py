import pytest
import json
import os, shutil
import time

def testNewEvent(client):

    client.post(
        "/auth/register",
        json={"name": "testuser", "email": "test@test.com", "password": "securepswd"},
    )

    with open("tests/files/images.zip", "rb") as imageZip:

        eventDataJson = json.dumps({
            "name": "Example Event",
            "photographer": "User",
            "photographerLink": "user.com",
            "userId": 1,
            "userName": "testuser"
        })

        file = (imageZip, "images.zip")

        response = client.post(
            "/event/new",
            data={"data": eventDataJson, "file": file},
            content_type="multipart/form-data"
        )

    # delay so the background task preGenerateRepresentations can finish
    time.sleep(10)

    assert response.status_code == 201
    info = response.get_json()
    assert "id" in info
    assert os.path.isdir("app/static/images/1")

    # removing the event images folder created:
    if os.path.isdir("app/static/images/"):
        shutil.rmtree("app/static/images/")