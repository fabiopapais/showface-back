from app.models import Event
from app import db

class EventAlreadyExistsException(Exception):
    pass

class EventNotFoundException(Exception):
    pass

def createEvent(data):
    # checks for existing event name
    if Event.query.filter_by(name=data['name']).first():
        raise EventAlreadyExistsException("An event with this name already exists.")
    
    event = Event(
        name=data['name'],
        photographer=data.get('photographer'), # .get is used in case the key doesn't exist - returns None
        photographerLink=data.get('photographerLink'),
        userId=data['userId'],
        userName=data['userName']
    )

    db.session.add(event)
    db.session.commit()

    # converts event obj into dict for jsonify
    eventDict = {"id": event.id, 
                  "name": event.name, 
                  "photographer": event.photographer, 
                  "photographerLink": event.photographerLink, 
                  "userId": event.userId, 
                  "userName": event.userName}

    return eventDict

def editEvent(data):
    # checks if event exists by the received id
    event = Event.query.filter_by(id=data['id']).first()
    if not event:
        raise EventNotFoundException("Event not found.") # if no event is found with that id, raise exception
    
    # updates to new values
    event.name = data.get('name', event.name)
    event.photographer = data.get('photographer', event.photographer)
    event.photographerLink = data.get('photographerLink', event.photographerLink)

    db.session.commit()

    eventDict = {"id": event.id, 
                  "name": event.name, 
                  "photographer": event.photographer, 
                  "photographerLink": event.photographerLink, 
                  "userId": event.userId, 
                  "userName": event.userName}

    return eventDict