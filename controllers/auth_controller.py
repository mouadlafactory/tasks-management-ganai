from flask import jsonify, request
from db.database import user_collection
from datetime import datetime
import bcrypt
from utils.generate_token import generate_token

def logout():
    return jsonify({"message": "Logout successful"}), 200

def register():
    try:    
        data = request.get_json()
        if not data.get('first_name') or not data.get('last_name') or not data.get('email') or not data.get('password'):
            return jsonify({"message": "Create user failed, missing required fields"}), 400
        
        encrypted_password = bcrypt.hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user_collection.insert_one({
            "first_name": data.get('first_name'),
            "last_name": data.get('last_name'),
            "email": data.get('email'),
            "password": encrypted_password,
            "role": data.get('role', "user"),
            "is_active": data.get('is_active', True),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        })
        
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
    
def login():
    try:
        data = request.get_json()
        if not data.get('email') or not data.get('password'):
            return jsonify({"message": "Login failed, missing required fields"}), 400
        
        user = user_collection.find_one({"email": data.get('email')})
        if not user:
            return jsonify({"message": "Login failed, user not found, try to register"}), 401
        
        if not bcrypt.checkpw(data.get('password').encode('utf-8'), user.get('password').encode('utf-8')):
            return jsonify({"message": "Login failed, incorrect password"}), 401
        
        token = generate_token(user)
        
        return jsonify({"message": "Login successful", "token": token}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
    
