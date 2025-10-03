from flask import request, jsonify
from utils.generate_token import verify_token
from functools import wraps

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('auth_token')
        if not token:
            return jsonify({'error': 'Authentication token required'}), 401
        user = verify_token(token)
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401
        request.current_user = user
        return f(*args, **kwargs)
    return decorated_function