""" API """
import json


from .models import User, Room
from flask import jsonify, request, url_for
from . import app, db


@app.route('/')
def test_get():
    return "popravi me :("


@app.route('/register/<string:username>', methods=['POST'])
def register_user(username):
    parms = request.get_json()
    register_room = parms['register_room']
    room_name = parms['room_name']

    if register_room:  # Create new room with new user

        # Create new room with unique id (stored as ObjectID)
        room = Room(room_name=room_name)
        room.save()
        # save ID of newly created room
        created_room_id = room.id

        #  Create new user using name from url parameter. Assign him with room's ID
        user = User(username=username, room=created_room_id)
        user.save()
        # save ID of newly created user
        user_id = user.id

        #  Append created user's id to the list of users.
        room = Room.objects.get(id=created_room_id)
        room.users.append(user_id)
        room.save()

    else:  # add new user to the room (using name from request parameter)
        room = Room.objects.get(room_name=room_name)

        user = User(username=username, room=room.id)
        user.save()

        room.users.append(user.id)
        room.save()

    return 'User je registriran'
