from flask import Blueprint, render_template, redirect, url_for
from functools import wraps
from flask import request, jsonify
from utils.generate_token import verify_token

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
def index():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('web.login'))
        
    user = verify_token(token)
    if not user:
        return redirect(url_for('web.login'))
        

    return render_template('task_crud.html')

@web_bp.route('/login')
def login():
    return render_template('login_v2.html')



