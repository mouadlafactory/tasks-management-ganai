from flask import jsonify, request
from bson.objectid import ObjectId
from models import Task
from datetime import datetime

def create_task():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "you didn't send any data in body"}), 400
        
        task = Task(
            title=data.get('title'),
            user=data.get('user',"Unknown"),
            description=data.get('description'),
        )
        task.save()
        return jsonify({"message": "Task created", "task": data}), 201
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500


def get_all_tasks():
    try:    
        user = getattr(request, 'current_user', None)
        if not user:
            return jsonify({"message": "User not authenticated"}), 401
        
        print("user: 🛑🛑🛑🛑🛑🛑🛑🛑 user data 🛑🛑🛑🛑🛑🛑🛑🛑 ", user)
        
        tasks = Task.objects()
        print("list: ", tasks)
        
        # Convert MongoEngine objects to dictionaries
        task_list = []
        for task in tasks:
            task_dict = {
                "id": str(task.id),
                "_id": str(task.id),  # For compatibility
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None
            }
            task_list.append(task_dict)
        
        return jsonify({"message": "Tasks", "tasks": task_list})
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
    
def get_task(task_id):
    try:
        task = Task.objects(id=task_id).first()
        if not task:
            return jsonify({"message": "Task not found"}), 404
            
        task_dict = {
            "id": str(task.id),
            "_id": str(task.id),
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None
        }
        
        return jsonify({"message": "Task", "task": task_dict}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
    
def update_task(task_id):
    try:
        data = request.get_json()
        task = Task.objects(id=task_id).first()
        
        if not task:
            return jsonify({"message": "Task not found"}), 404
        
        # Update fields if provided
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        if 'priority' in data:
            task.priority = data['priority']
        if 'user' in data:
            task.user = data['user']
            
        # Update timestamp
        task.updated_at = datetime.utcnow()
        task.save()
        
        # Return updated task
        task_dict = {
            "id": str(task.id),
            "_id": str(task.id),
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None
        }
        
        return jsonify({"message": "Task updated", "task": task_dict}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
    
def delete_task(task_id):
    try:
        task = Task.objects(id=task_id).first()
        
        if not task:
            return jsonify({"message": "Task not found"}), 404
            
        task.delete()
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500

    
    