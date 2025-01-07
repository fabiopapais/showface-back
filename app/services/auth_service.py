from app.models import User
from app import db
from flask_jwt_extended import create_access_token

def register_user(data):
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return {"id": user.id, "username": user.username}

def login_user(data):
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return token
    raise ValueError("Invalid credentials")