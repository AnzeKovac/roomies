"""MongoDB documents"""
from . import db


class Room(db.Document):
    name = db.StringField(required=True, unique=True)
    users = db.ListField(db.ObjectIdField(), default=list)

    def to_dict(self,):
        return {key.replace("_", ""): value for key, value in self.to_mongo().to_dict().items()
                if key is not "users"}


class User(db.Document):
    username = db.StringField(required=True)  # Default is False
    password = db.StringField(required=True)
    room = db.DictField(required=True)
    firstName = db.StringField()
    lastName = db.StringField()

    def to_dict(self):
        return self.to_mongo().to_dict()


class Task(db.Document):
    taskName = db.StringField(required=True)
    additionalDescription = db.StringField(required=True)
    awardPoints = db.IntField(required=True)
    assignedUser = db.DictField()
    status = db.StringField
    room = db.DictField(required=True)

    def to_dict(self):
        return self.to_mongo().to_dict()


class Effort(db.Document):
    taskId = db.ObjectIdField()
    userId = db.ObjectIdField()
    points = db.IntField()
    date = db.DateTimeField()
