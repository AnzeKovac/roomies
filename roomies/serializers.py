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

