"""MongoDB documents"""
from . import db


# TODO: What will our models need?

class User(db.Document):
    username = db.StringField(required=True)  # Default is False
    password = db.StringField(required=True)
    room = db.ObjectIdField(required=True)
    firstName = db.StringField()
    lastName = db.StringField()


class Room(db.Document):
    roomName = db.StringField(required=True, unique=True)
    users = db.ListField(db.ObjectIdField(), default=list)


class Task(db.Document):
    taskName = db.StringField(required=True)
    additionalDescription = db.StringField()
    awardPoints = db.IntField()
    assignedUser = db.ObjectIdField
    status = db.StringField
    room = db.ObjectIdField(required=True)
    
class Effort(db.Document):
    taskId = db.ObjectIdField()
    userId = db.ObjectIdField()
    points = db.IntField()
    date = db.DateTimeField()
