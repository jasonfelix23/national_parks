from flask import Blueprint, request, jsonify
from flask_cors.decorator import cross_origin
from models.user import User
from app import db
from utils.json_response import json_response
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)
user_model = User(db)

@auth_bp.route('/register', methods=["POST"])
def register():
    data = request.json
    username = data['username']
    password = data['password']

    if user_model.find_by_username(username):
        return json_response({'message': 'Username already exists'}, 400)
    
    user_created = user_model.create_user(username, password)
    if user_created:
        user_id = user_created.inserted_id
        expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
        token = jwt.encode({
            'exp': int(expiry_time.timestamp()),
            'iat': datetime.datetime.now(),
            'user_id': str(user_id)
        }, "jason", algorithm='HS256')
        return json_response({'token': token, "expires_at": expiry_time.isoformat()}, 200)
    else:
        return json_response({'message': 'Failed to create user'}, 500)

@auth_bp.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    user = user_model.find_by_username(username)
    if user and user_model.check_password(user, password):
        expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
        token = jwt.encode({
            'exp': int(expiry_time.timestamp()),
            'iat': datetime.datetime.now(),
            'user_id': str(user['_id'])
        }, "jason", algorithm='HS256')
        return json_response({'token': token, "expires_at": expiry_time.isoformat()}, 200)
    
    return json_response({"message": "Invalid Credentials"}, 401)