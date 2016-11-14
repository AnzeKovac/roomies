""" API """
import json


from .models import User, Room, Task
from flask import jsonify, request, url_for
from . import app, db


@app.route('/')
def test_get():
    return "popravi me :("

#authentication
@app.route('/register/<string:username>', methods=['POST'])
def register_user(username):
    parms = request.get_json()
    register_room = parms['registerRoom']
    room_name = parms['roomName']

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
    #let's program in engleski, shall we ?
    return 'User je registriran' 


#add new task
@app.route('/task/add', methods=['POST'])
def addNewTas():
        task = Task()
        parameters = request.get_json()

        taskName = parameters['taskName']
        additionalDescription = parameters['additionalDescription'] if 'additionalDescription' in parameters else ''
        awardPoints = parameters['awardPoints'] if 'awardPoints' in parameters else 0
        assignedUser =  parameters['userId'] if 'usedId' in parameters else ''
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
@app.route('/task/<string:taskId>',methods=['GET','DELETE','PUT'])
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
@app.route('/tasks/',methods=['GET'])
def getAllTasks():
    params = request.get_json()
    room==params['token'] if 'token' in params else ''
    return jsonify(Task.objects(room=room))
        
    