from flask import Blueprint, request, jsonify
from app.services.auth_service import UserAlreadyExistsException, register_user, login_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user = register_user(data)
        return jsonify(user), 201
    except UserAlreadyExistsException as e:
        return jsonify({"error": str(e)}), 400
    
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        token = login_user(data)
        return jsonify({"token": token}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401