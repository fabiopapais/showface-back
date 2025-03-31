from app.models import Event, User
from app import db

class EventAlreadyExistsException(Exception):
    pass

class EventNotFoundException(Exception):
    pass

def createEvent(data):
    # checks for existing event name
    print(data['name'])
    if Event.query.filter_by(name=data['name']).first():
        raise EventAlreadyExistsException("An event with this name already exists.")

    user = User.query.filter_by(id=data['userId']).first()
    if not user:
        raise EventNotFoundException("User not found.")

    event = Event(
        name=data['name'],
        photographer=data.get('photographer'), # .get is used in case the key doesn't exist - returns None
        photographerLink=data.get('photographerLink'),
        userId=data['userId'],
        userName=user.name,
        processed=False
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
    
    # TODO: Authenticate with JWT 

    # checks if Event name already exists
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

def getEventData(id):
    event = Event.query.filter_by(id=id).first()
    if not event:
        raise EventNotFoundException("Event not found.")
    
    eventDict = {"id": event.id, 
                  "name": event.name, 
                  "photographer": event.photographer, 
                  "photographerLink": event.photographerLink, 
                  "userId": event.userId, 
                  "userName": event.userName,
                  "processed": event.processed}

    return eventDict

def getEventsByUserId(userId):
    events = Event.query.filter_by(userId=userId).all()
    eventDicts = []
    for event in events:
        eventDict = {"id": event.id, 
                      "name": event.name, 
                      "photographer": event.photographer, 
                      "photographerLink": event.photographerLink, 
                      "userId": event.userId, 
                      "userName": event.userName}
        eventDicts.append(eventDict)

    return eventDicts