import json
from flask import Blueprint, request, jsonify
from app.services.event_service import getEventData, EventNotFoundException
from app.services.image_service import getImages

find_bp = Blueprint('find', __name__)

@find_bp.route('/', methods=['GET'])
def getEvent():
    data = json.loads(request.form.get('data'))
    files = request.files.get('file')
    try:
        event = getEventData(data)
        images_paths = getImages(event['id'])

        # TODO: filter images_paths based on face verification and return images_paths

        return jsonify(event), 200
    except EventNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400