import pytest
import json, os, time
from tests.testutils import regNewUser, createNewEvent, delImages

def testNewEvent(client):

    # register a new user in db
    regNewUser(client)

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
    delImages()

def testEditEvent(client):

    # register a new user in db
    regNewUser(client)

    # create a new event in db
    createNewEvent(client)

    # edit the event
    response = client.put(
        "/event/edit",
        json={
            "id": 1,
            "name": "Edited Event",
            "photographer": "Edited User",
            "photographerLink": "editeduser.com",
            "userId": 1,
            "userName": "testuser"
            }
    )

    #assert the event was edited
    assert response.status_code == 200
    info = response.get_json()
    assert info["name"] == "Edited Event"

    # removing the event images folder created:
    delImages()

def testGetEvent(client):

    # register a new user in db
    regNewUser(client)

    # create a new event in db
    createNewEvent(client)

    # get the event
    response = client.get(
        "/event/1",
    )

    #assert the event was retrieved
    assert response.status_code == 200

    # removing the event images folder created:
    delImages()