""" API """
import hashlib


from .models import User, Room, Task
from flask import jsonify, request, url_for, Response, abort
from . import app
from mongoengine.errors import NotUniqueError
#from werkzeug.security import generate_password_hash, check_password_hash


def register_err(err_msg, status_code):
    response = jsonify(dict(error=err_msg))
    response.status_code = status_code
    return response


def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def check_password(hashed, password):
    return hash_password(hashed) == password


#authentication
@app.route('/register', methods=['POST'])
def register_user():
    parms = request.get_json()

    registerRoom = parms['registerRoom']
    username = parms['username']
    password = parms['password']
    roomName = parms['roomName']

    if registerRoom:  # Create new room with new user

        # Create new room with unique id (stored as ObjectID)
        room = Room(roomName=roomName)
        try:
            room.save()
        except NotUniqueError:
            return register_err('There was a conflict. Room name is already taken', 409)

        # save ID of newly created room
        newRoomId = room.id

        #  Create new user. Assign him with to the newly created room
        user = User(username=username, password=hash_password(password), room=newRoomId)
        user.save()
        # save ID of newly created user
        user_id = user.id

        #  Append created user's id to the list of users.
        room = Room.objects.get(id=newRoomId)
        room.users.append(user_id)
        room.save()

    else:  # add new user to the room (using name from request parameter)
        room = Room.objects.get(roomName=roomName)

        existing = User.objects(room=room.id)
        existingNames = [name.username for name in existing]

        if username in existingNames:
            return register_err('There was a conflict. Username for this room is taken', 409)

        user = User(username=username, password=hash_password(password), room=room.id)
        user.save()

        room.users.append(user.id)
        room.save()

    return jsonify(dict(token=str(room.id)))


#add new task
@app.route('/task/add', methods=['POST'])
def addNewTas():
        task = Task()
        parameters = request.get_json()

        taskName = parameters['taskName']
        additionalDescription = parameters['additionalDescription'] if 'additionalDescription' in parameters else ''
        awardPoints = parameters['awardPoints'] if 'awardPoints' in parameters else 0
        assignedUser = parameters['userId'] if 'usedId' in parameters else ''
        room = parameters['room'] if 'room' in parameters else ''

        task.taskName = taskName if taskName else ''
        task.additionalDescription = additionalDescription
        task.awardPoints = awardPoints
        task.assignedUser = assignedUser
        task.status = 'new'
        task.room = room
        #if user send notification ?
        task.save()
        return jsonify(task)
        
        
#task get,update,delete
@app.route('/task/<string:taskId>', methods=['GET', 'DELETE', 'PUT'])
def completeTask(taskId):
    if request.method == 'GET':
        return jsonify(Task.objects.get(id=taskId))
    elif request.method == 'PUT':
        params = request.get_json()
        task = Task.objects.get(id=taskId)
        task.taskName = params['taskName'] if 'taskName' in params else task.TaskName
        task.additionalDescription = params['additionalDescription'] if 'additionalDescription' in params else task.additionalDescription
        task.awardPoints = params['awardPoints'] if 'awardPoints' in params else task.awardPoints
        task.assignedUser = params['userId'] if 'userId' in params else task.assignedUser
        task.room = params['room'] if 'room' in params else task.room
        task.status = params['status'] if 'status' in params else task.status
        task.save()
        return 'Update OK'
    elif request.method == 'DELETE':
        task = Task.objects.get(id=taskId)
        task.delete()
        return 'Delete OK'


#get all tasks
@app.route('/tasks/', methods=['GET'])
def getAllTasks():
    #params = request.get_json()
    #room==params['token'] if 'token' in params else ''
    return jsonify(Task.objects())
