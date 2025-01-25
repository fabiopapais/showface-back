import json
from flask import Blueprint, request, jsonify
from app.services.event_service import getEventData, EventNotFoundException
from app.services.image_service import getImages
from app.services.find_service import findImagesOnEvent

find_bp = Blueprint('find', __name__)

@find_bp.route('/', methods=['GET'])
def getEvent():
    data = json.loads(request.form.get('data'))
    files = request.files.get('file')
    try:
        event = getEventData(data)
        images_paths = getImages(event['id'])

        # get paths for each event image
        event_image_paths = []
        for image in images_paths:
            event_image_paths.append(image['link'])

        # return matching images paths
        matching_images = findImagesOnEvent(event_image_paths, files)

        return jsonify(matching_images), 200
    except EventNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400