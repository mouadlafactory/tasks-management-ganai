from flask import jsonify, request, make_response 
from models import User
from utils.generate_token import generate_token

def logout():
    return jsonify({"message": "Logout successful"}), 200

def register():
    try:    
        data = request.get_json()
        required_fields = ['username', 'email', 'name', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"message": "Create user failed, missing required fields"}), 400
        
        # Check if user already exists
        existing_user = User.objects(email=data.get('email')).first()
        if existing_user:
            return jsonify({"error": "User with this email already exists"}), 400
            
        existing_username = User.objects(username=data.get('username')).first()
        if existing_username:
            return jsonify({"error": "Username already taken"}), 400
        
        # Create user with keyword arguments
        user = User(
            username=data.get('username'),
            email=data.get('email'),
            name=data.get('name')
        )
        user.set_password(data.get('password'))
        user.save()
        
        print("i am here")
        user_created = {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "name": user.name
        }
        return jsonify({"message": "User registered successfully","user": user_created}), 201
    except Exception as e:
        print("i am here 2")
        return jsonify({"error": str(e)}), 500
    
    
def login():
    try:
        data = request.get_json()
        print(data)
        required_fields = ['email', 'password']  # 'email' can be email or username
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": "Login failed, missing required fields"}), 400

        email_field = data.get('email')
        
        # Try to find user by email first, then by username
        user = User.objects(email=email_field).first()
    
        if not user:
            return jsonify({"error": "Login failed, user not found"}), 401
        
        if not user.check_password(data.get('password')):
            return jsonify({"error": "Login failed, incorrect password"}), 401
        
        token = generate_token(user)
        # Create response
        response = make_response(jsonify({
            'message': 'Login successful',
            'user': {
                'id': str(user.id),
                'email': user.email,
                'name': user.name,
                'username': user.username
            },
            'token': token
        }), 200)
        
        # Set JWT token in HTTP-only cookie
        response.set_cookie(
            'token',
            token,
            max_age=1000 * 60 * 60 * 24 * 30, # 30 days
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        
        return response
        
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
    

def get_current_user(): 
    user = getattr(request, 'current_user', None)
    if not user:
        return jsonify({"error": "User not authenticated"}), 401
    
    user_data = {
        "id": str(user.id),
        "email": user.email,
    }
    return jsonify({"user": user_data}), 200
    
    