from app.services.auth_service import getUserById, UserDoesNotExistException

from flask import Blueprint, request, jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('/<int:id>', methods=['GET'])
def getUser(id):
    try:
        userData = getUserById(id)
        return jsonify(userData), 200
    except UserDoesNotExistException as e:
        return jsonify({"error": str(e)}), 404
