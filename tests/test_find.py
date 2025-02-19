import pytest
import json, os
from tests.testutils import regNewUser, createNewEvent, delImages

def testFindImages(client):

    regNewUser(client)
    createNewEvent(client)

    with open("tests/files/selfie.png", "rb") as userSelfie:

        eventIdJson = json.dumps({
            "id": 1
        })

        file = (userSelfie, "selfie.png")

        response = client.get(
            "/find/",
            data={"data": eventIdJson, "file": file},
            content_type="multipart/form-data"
        )
    
    assert response.status_code == 200
    assert os.path.isdir("app/static/images/find")
    
    # delete images
    delImages()