from flask import Blueprint, request, jsonify
from app.services.event_service import createEvent, EventAlreadyExistsException

event_bp = Blueprint('event', __name__)

@event_bp.route('/new', methods=['POST'])
def createEventRoute():
    data = request.get_json()
    try:
        event = createEvent(data)
        return jsonify(event), 201
    except EventAlreadyExistsException as e:
        return jsonify({"error": str(e)}), 400