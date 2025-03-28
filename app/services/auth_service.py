from app.models import User
from app import db

from app.services.event_service import getEventsByUserId

from flask_jwt_extended import create_access_token

class UserAlreadyExistsException(Exception):
    pass

class UserDoesNotExistException(Exception):
    pass

def registerUser(data):
    # checks existence of email
    if User.query.filter_by(email=data['email']).first():
        raise UserAlreadyExistsException("A user with this email already exists.")

    user = User(name=data['name'], email=data['email'])
    user.setPassword(data['password'])

    db.session.add(user)
    db.session.commit()

    # automatically creating token for register
    token = create_access_token(identity=user.id)

    return { "user": { "id": user.id, "name": user.name, "email": user.email}, "token":token}

def loginUser(data):
    user : User = User.query.filter_by(email=data['email']).first()
    if user and user.checkPassword(data['password']):
        token = create_access_token(identity=user.id)
        return { "user": { "id": user.id, "name": user.name, "email": user.email}, "token":token}
    else:
        raise ValueError("Invalid credentials")

def getUserById(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        raise UserDoesNotExistException("User not found.")
    
    # search for events created by user on events table
    events = getEventsByUserId(id)
    
    userDict = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "events": events
    }

    
    return userDict