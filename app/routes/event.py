import json
import threading
from flask import Blueprint, request, jsonify, current_app
from app.services.event_service import createEvent, editEvent, getEventData, EventAlreadyExistsException, EventNotFoundException
from app.services.image_service import saveEventImages, registerImagesOnDatabase, getImages
from app.services.find_service import preGenerateRepresentations

event_bp = Blueprint('event', __name__)

@event_bp.route('/new', methods=['POST'])
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
    
@event_bp.route('/<int:id>', methods=['GET'])
def getEvent(id):
    try:
        event = getEventData(id)
        images_paths = getImages(id)

        # Get pagination parameters from query string
        page = request.args.get('page', default=1, type=int)
        per_page = 30

        # Apply pagination to images
        start = (page - 1) * per_page
        end = min(start + per_page, len(images_paths))
        paginated_images = images_paths[start:end]

        # Include pagination metadata
        event['images'] = paginated_images
        event['pagination'] = {
            "page": page,
            "total": len(images_paths),
            "total_pages": (len(images_paths) + per_page - 1) // per_page
        }

        return jsonify(event), 200
    except EventNotFoundException as e:
        return jsonify({"error": str(e)}), 404