import json
import threading
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.event_service import createEvent, editEvent, getEventData, EventAlreadyExistsException, EventNotFoundException
from app.services.image_service import saveEventImages, registerImagesOnDatabase, getImages
from app.services.find_service import preGenerateRepresentations

event_bp = Blueprint('event', __name__)

@event_bp.route('/new', methods=['POST'])
@jwt_required()
def createEventRoute():
    json_data = request.form.to_dict()
    
    # TEMP CODE FOR TESTING - if form is received as a dict with '{data: '{json_data}'}' instead of just '{json_data}'
    # happens when running tests, grabs the data from the 'data' key and converts it to a dict through json.loads
    # TODO: FIND AN ALTERNATIVE
    if len(json_data) == 1: 
        json_data = json_data['data']
        json_data = json.loads(json_data)

    files = request.files.get('file')
    event = None

    try:
        # verify if jwt token identity belonging to the user is the same as the userId in the event data
        jwtIdentity = get_jwt_identity()
        if jwtIdentity != str(json_data['userId']):
            return jsonify({"error": "Unauthorized user"}), 401

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
@jwt_required()
def editEventRoute():
    data = request.get_json()

    jwtIdentity = get_jwt_identity()
    if jwtIdentity != str(data['userId']):
        return jsonify({"error": "Unauthorized user"}), 401
    
    try:
        event = editEvent(data)
        return jsonify(event), 200
    except EventNotFoundException as e:
        return jsonify({"error": str(e)}), 400
    except EventAlreadyExistsException as e:
        return jsonify({"error": str(e)}), 400
    
@event_bp.route('/<int:id>', methods=['GET'])
def getEvent(id):
    try:
        event = getEventData(id)
        images_paths = getImages(id)
        event['images'] = images_paths

        return jsonify(event), 200
    except EventNotFoundException as e:
        return jsonify({"error": str(e)}), 404