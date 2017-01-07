def serialize_task(task):
    return {
        'id': task.id,
        'taskName': str(task.taskName),
        'additionalDescription': str(task.additionalDescription),
        'awardPoints': int(task.awardPoints),
        'assignedUser':task.assignedUser,
        'status':str(task.status),
    }

def serialize_room(room):
    return{
        'id': room.id,
        'name':str(room.name)
    }

def serialize_effort(effort):
    return{
    'id':effort.id,
    'userId':effort.userId,
    'taskId':effort.taskId,
    'points':effort.points,
    'date':effort.date
    }
