import pytest
import json

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

        data = {
            "data": eventDataJson,
            "file": (imageZip, "imagens.zip")
        }

        response = client.post(
            "/event/new",
            data=data,
            content_type="multipart/form-data"
        )
    
    #TODO: COMPLETAR TESTE



    