from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

def generate_token(user):
    """Generate JWT token for user"""
    payload = {
        'user_id': str(user["id"]),
        'email': user["email"],
    }
    
    return jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm='HS256')


def verify_token(token):
    """Verify JWT token and return user"""
    return jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=['HS256'])