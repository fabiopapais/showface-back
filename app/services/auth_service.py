from app.models import User
from app import db
from flask_jwt_extended import create_access_token

class UserAlreadyExistsException(Exception):
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

    return {user:{ "id": user.id, "name": user.name, "email": user.email}, "token":token}

def loginUser(data):
    user : User = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return {user:{ "id": user.id, "name": user.name, "email": user.email}, "token":token}
    else:
        raise ValueError("Invalid credentials")