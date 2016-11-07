""" API """
from .models import User, Room
from flask import jsonify, request
from . import app, db


@app.route('/addTest')
def new_user():
    test = User(username='test123', roomID="neka soba")
    test.save()
    return "dodan je nov user"


@app.route('/getTest')
def test_get():
    return jsonify(User.objects)

@app.route('/uri')
def jaka():
    return MONGODB_URI
