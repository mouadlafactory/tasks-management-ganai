from flask import Blueprint, jsonify, request
from datetime import datetime
from db.database import user_collection
from controllers.auth_controller import register, login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_route():
    return register()

@auth_bp.route('/login', methods=['POST'])
def login_route():
    return login()

