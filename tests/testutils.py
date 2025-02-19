import json
import time
import os, shutil

#USEFUL FUNCTIONS FOR TESTING WILL BE HERE AND IMPORTED TO OTHER FILES FROM HERE

def regNewUser(client):
    client.post(
        "/auth/register",
        json={"name": "testuser", "email": "test@test.com", "password": "securepswd"},
    )

def createNewEvent(client):
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

        client.post(
            "/event/new",
            data={"data": eventDataJson, "file": file},
            content_type="multipart/form-data"
        )

    # delay so the background task preGenerateRepresentations can finish
    time.sleep(10)

def delImages():
    if os.path.isdir("app/static/images/"):
        shutil.rmtree("app/static/images/")