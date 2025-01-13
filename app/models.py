from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    photographer = db.Column(db.String(150), nullable=True)
    photographerLink = db.Column(db.String(150), nullable=True)
    
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    userName = db.Column(db.String(150), nullable=False)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    link = db.Column(db.String(150), nullable=False)
    
    eventId = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)