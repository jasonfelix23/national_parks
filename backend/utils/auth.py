from functools import wraps
from flask import request, jsonify
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
        
        print(token)

        if not token:
            return jsonify({'message': 'Missing Authorization Header'}), 401
        
        try:
            payload = jwt.decode(token, "jason", algorithms=['HS256'])
            print("Decoded payload:", payload)
            current_user = payload['user_id']
        except ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except DecodeError:
            return jsonify({"message": "Token is invalid"}), 401
        except Exception as e:
            print("Error decoding token:", str(e))
            return jsonify({"message": "Token is invalid"}), 401
        
        return f(current_user, *args, **kwargs)

    return decorated