import jwt
import datetime
from functools import wraps
from flask import request, jsonify
import hashlib
import os
import json

SECRET_KEY = os.environ.get('SECRET_KEY')
USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file)

users = load_users()

def create_user(username, password):
    if username in users:
        return False
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    users[username] = hashed_password
    save_users(users)
    return True

def authenticate(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if username in users and users[username] == hashed_password:
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        return token
    return None

def validate_token(token):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
            if validate_token(token):
                return f(*args, **kwargs)
        return jsonify({'error': 'Invalid token'}), 403
    return decorated

# Вспомогательная функция для тестирования
def delete_all_users():
    users = {}
    save_users(users)
    print("All users have been deleted.")