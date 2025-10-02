from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

def generate_token(user):
    """Generate JWT token for user"""
    payload = {
        'user_id': str(user["_id"]),
        'email': user["email"],
    }
    
    return jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm='HS256')
