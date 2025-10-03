from flask import request, jsonify
from functools import wraps
from utils.generate_token import verify_token

def check_password(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        password = request.args.get('password')
        if password != "12345678":
            return jsonify({"error": "sir bhalek"}), 401
        return f(*args, **kwargs)
    return decorated_function



def verify_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({"error": "you don't have a token, try to login"}), 401
        
        user = verify_token(token)
        if not user:
            return jsonify({"error": "your token is invalid, or expired"}), 401
        
        request.current_user = user
        return f(*args, **kwargs)
    
    return decorated_function




