from flask import Blueprint, render_template, redirect, url_for
from functools import wraps
from flask import request, jsonify
from utils.generate_token import verify_token

web_bp = Blueprint('web', __name__)


def auth_required(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from cookie
        if request.cookies.get('auth_token'):
            user = verify_token(request.cookies.get('auth_token'))
            if user:
                request.current_user = user
            return f(*args, **kwargs)
        else:
            return redirect(url_for('web.login'))
    
    return decorated_function

@web_bp.route('/')
@auth_required
def index():
    return render_template('task_crud.html')

@web_bp.route('/login')
def login():
    return render_template('login.html')



