"""MongoDB documents"""
from . import db


# TODO: What will our models need?

class User(db.Document):
    username = db.StringField(required=True)
    firstname = db.StringField()
    lastname = db.StringField()
    roomID = db.StringField(required=True)


class Room(db.Document):
    title = db.StringField(required=True)
