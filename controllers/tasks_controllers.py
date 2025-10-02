from flask import jsonify, request
from bson.objectid import ObjectId
from db.database import task_collection
from datetime import datetime

def create_task():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "you didn't send any data in body"}), 400
        
        task_collection.insert_one({
                                    "title": data.get('title'),
                                    "user": data.get('user',"Unknown"),
                                    "description": data.get('description'),
                                    "created_at": datetime.now(),
                                    "updated_at": datetime.now(),
                                    "completed_at": datetime.now(),
                                    "status": "pending",
                                    "priority": "medium"
                                    })
        return jsonify({"message": "Task created", "task": data}), 201
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500


def get_all_tasks():
    try:    
        tasks = [{**task, "_id": str(task["_id"])} for task in task_collection.find()]
        
        return jsonify({"message": "Tasks", "tasks": tasks})
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
    

def get_task(task_id):
    try:
        task = task_collection.find_one({"_id": ObjectId(task_id)})
        return jsonify({"message": "Task", "task": {**task, "_id": str(task["_id"])}}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
    
def update_task(task_id):
    try:
        data = request.get_json()
        task_collection.update_one({"_id": ObjectId(task_id)}, {"$set": data})
        return jsonify({"message": "Task updated", "task": {**data, "_id": str(task_id)}}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
    
    
def delete_task(task_id):
    try:
        task_collection.delete_one({"_id": ObjectId(task_id)})
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500

    
    