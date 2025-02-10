from flask import Blueprint, request, jsonify
from app.services.auth_service import UserAlreadyExistsException, registerUser, loginUser

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user = registerUser(data)
        return jsonify(user), 201
    except UserAlreadyExistsException as e:
        return jsonify({"error": str(e)}), 400
    
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        token = loginUser(data)
        return jsonify(token), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401