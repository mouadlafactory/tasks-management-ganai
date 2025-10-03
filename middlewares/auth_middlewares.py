from flask import request, jsonify
from utils.generate_token import verify_token
from functools import wraps

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({'error': 'Authentication token required'}), 401
        user = verify_token(token)
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401
        request.current_user = user
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = getattr(request, 'current_user', None)
        if not user:
            return jsonify({'error': 'User not authenticated'}), 401
        if user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403

        return f(*args, **kwargs)
    return decorated_function