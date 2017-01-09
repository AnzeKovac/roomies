def serialize_task(task):
    return {
        'id': task.id,
        'taskName': task.taskName,
        'additionalDescription': task.additionalDescription,
        'awardPoints': int(task.awardPoints),
        'assignedUser':task.assignedUser,
        'status':str(task.status),
    }

def serialize_room(room):
    return{
        'id': room.id,
        'name':room.name
    }

def serialize_effort(effort):
    return{
    'id':effort.id,
    'userId':effort.userId,
    'taskId':effort.taskId,
    'roomId':effort.roomId,
    'points':effort.points,
    'date':effort.date,
    'userName':effort.userName

    }
