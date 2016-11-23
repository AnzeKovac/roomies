""" API """
import hashlib


from .models import User, Room, Task, Effort
from flask import jsonify, request, url_for, Response, abort
from . import app
from mongoengine.errors import NotUniqueError, DoesNotExist
from collections import defaultdict


def get_document(query):
    """This function gets query object on input and returns document type.
    """
    return query.first()


def error_handler(err_msg, status_code):
    response = jsonify(dict(error=err_msg))
    response.status_code = status_code
    return response


def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def check_password(password, hashed):
    return hash_password(password) == hashed


#authentication
@app.route('/register', methods=['POST'])
def register():
    parms = request.get_json()
    parmsUrl = request.args

    registerRoom = parmsUrl['newRoom']
    username = parms['username']
    password = parms['password']
    room = parms['room']

    if registerRoom == 'true':  # Create new room with new user

        # Create new room with unique id (stored as ObjectID)
        room = Room(name=room['name'])
        try:
            room.save()
        except NotUniqueError:
            return error_handler('There was a conflict. Room name is already taken', 409)

        # save ID of newly created room
        newRoomId = room.id

        #  Create new user. Assign him with to the newly created room
        user = User(username=username, password=hash_password(password), room=room.to_dict())
        user.save()
        # save ID of newly created user
        user_id = user.id

        #  Append created user's id to the list of users.
        room = Room.objects.get(id=newRoomId)
        room.users.append(user_id)
        room.save()

    else:  # add new user to the room roomies.models.DoesNotExist

        try:
            room = Room.objects.get(name=room['name'])
        except DoesNotExist:
            return error_handler('There was a conflict. Room name does not exist', 409)

        existing = User.objects(room__id=room.id)
        existingNames = [name.username for name in existing]

        if username in existingNames:
            return error_handler('There was a conflict. Username for this room is taken', 409)

        user = User(username=username, password=hash_password(password), room=room.to_dict())
        user.save()

        room.users.append(user.id)
        room.save()

    token = User.objects(id=user.id).exclude("password")

    return jsonify(get_document(token).to_dict())


@app.route('/login', methods=['POST'])
def login():
    parms = request.get_json()

    username = parms['username']
    password = parms['password']
    room = parms['room']

    list_users = Room.objects(name=room['name']).only("users").first()
    if not list_users:
        return error_handler("Room is not existent", 401)

    for user_id in list_users.users:
        user = User.objects.get(id=user_id)

        if user.username == username and check_password(password, user.password):
            token = User.objects(id=user.id).exclude("password")
            return jsonify(get_document(token).to_dict())

    return error_handler("Login failed", 401)



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

@app.route('/statistics', methods=['GET'])
def getStatistics():
    params = request.args
    roomId = params['token'] if 'token' in params else None
    if roomId:
        room = Room.objects.get(id=roomId)
        listOfIds = room.users
        print(listOfIds)
        efforts = Effort.objects()
        print(efforts)
        calculations = defaultdict(int)
        if efforts:
            for e in efforts:
                calculations[e.userId] += e.points
            return str(calculations)

#misc
@app.route('/',methods=['GET'])
def returnRoot():
    return "Funny message"
