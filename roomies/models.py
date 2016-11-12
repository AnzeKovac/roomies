"""MongoDB documents"""
from . import db


# TODO: What will our models need?

class User(db.Document):
    username = db.StringField(required=True)  # Default is False
    room = db.ObjectIdField(required=True)
    first_name = db.StringField()
    last_name = db.StringField()


class Room(db.Document):
    room_name = db.StringField(required=True)
    users = db.ListField(db.ObjectIdField(), default=list)

