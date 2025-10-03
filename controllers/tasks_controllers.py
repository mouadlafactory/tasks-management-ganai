from flask import jsonify, request
from bson.objectid import ObjectId
from models import Task
from datetime import datetime

def create_task():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "you didn't send any data in body"}), 400
        
        task = Task.objects.create({
                                    "title": data.get('title'),
                                    "user": data.get('user',"Unknown"),
                                    "description": data.get('description'),
                                    })
        task.save()
        return jsonify({"message": "Task created", "task": data}), 201
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500


def get_all_tasks():
    try:    
        tasks = [{**task, "_id": str(task["_id"])} for task in Task.objects.all()]
        
        return jsonify({"message": "Tasks", "tasks": tasks})
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
    

def get_task(task_id):
    try:
        task = Task.objects.get(id=task_id).first()
        return jsonify({"message": "Task", "task": {**task, "_id": str(task["_id"])}}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
    
def update_task(task_id):
    try:
        data = request.get_json()
        task = Task.objects.get(id=task_id).first()
        task.update(**data)
        task.save()
        return jsonify({"message": "Task updated", "task": {**data, "_id": str(task_id)}}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
    
    
def delete_task(task_id):
    try:
        task = Task.objects.get(id=task_id).first()
        task.delete()
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500

    
    