import json
import threading
from flask import Blueprint, request, jsonify, current_app
from app.services.event_service import createEvent, editEvent, getEventData, EventAlreadyExistsException, EventNotFoundException
from app.services.image_service import saveEventImages, registerImagesOnDatabase, getImages
from app.services.find_service import preGenerateRepresentations

event_bp = Blueprint('event', __name__)

@event_bp.route('/new', methods=['POST'])
def createEventRoute():
    data = request.form.get('data')  # 'data' is the key sent in the request
    json_data = json.loads(data)  # Parse the JSON string into a Python dictionary
    files = request.files.get('file')
    event = None

    try:
        event = createEvent(json_data) # creates event data on events database
        savedImagesPaths = saveEventImages(files, event['id']) # saves images to the images folder
        registerImagesOnDatabase(event['id'], event['userId'], savedImagesPaths) # saves image data to the images database
        event['images'] = savedImagesPaths

        # Capture the Flask app context before starting the thread
        app_context = current_app.app_context()
        def background_task():
            with app_context:  # Ensure the thread has Flask's application context
                preGenerateRepresentations(event['id'], event['images'])
        threading.Thread(target=background_task, daemon=True).start()  # daemon=True ensures cleanup

        return jsonify(event), 201
    except EventAlreadyExistsException as e:
        return jsonify({"error": str(e)}), 400
    
@event_bp.route('/edit', methods=['PUT'])
def editEventRoute():
    data = request.get_json()
    try:
        event = editEvent(data)
        return jsonify(event), 200
    except EventNotFoundException as e:
        return jsonify({"error": str(e)}), 400
    except EventAlreadyExistsException as e:
        return jsonify({"error": str(e)}), 400
    
@event_bp.route('/', methods=['GET'])
def getEvent():
    data = request.get_json()
    try:
        event = getEventData(data)
        images_paths = getImages(event['id'])
        event['images'] = images_paths

        return jsonify(event), 200
    except EventNotFoundException as e:
        return jsonify({"error": str(e)}), 404