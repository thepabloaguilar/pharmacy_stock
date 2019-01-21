import datetime
import jwt

from functools import wraps
from flask import abort, request
from passlib.context import CryptContext


_pwd_context = CryptContext(
            schemes=['pbkdf2_sha256'])


# Make the password's encryptation
def encrypt_password(password):
    return _pwd_context.encrypt(password)


# Verify if password is equal to generated Hash
def check_encrypted_password(password, hashed):
    return _pwd_context.verify(password, hashed)


# Create a JWT Token with 1 hour of expiration time
def generate_auth_token(user):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow(),
            'sub': {
                'user_id': user['_id'],
                'username': user['username'],
                'is_admin': user['is_admin']
            }
        }
        token = jwt.encode(payload, 'CRIPTOGRAFY_KEY', algorithm='HS256')
        return token.decode()
    except Exception as e:
        return e


# Verify token auth and return its payload
def decode_auth_token(token):
    try:
        payload = jwt.decode(token, 'CRIPTOGRAFY_KEY')
        return payload['sub']
    except jwt.ExpiredSignatureError:
        abort(401, 'Token is invalid or expired')
    except jwt.InvalidSignatureError:
        abort(401, 'Token is invalid or expired')
    except jwt.exceptions.DecodeError:
        abort(401, 'Token is invalid or expired')


# Decorator to verify token sent in request HEADER
def auth_token_required(only_admin=False):
    def validation(func):
        @wraps(func)
        def decorated(_self, *args, **kwargs):
            token = request.headers.get('Token', None)

            if not token:
                abort(403, 'Token is not in request HEADER')
            
            user_info = decode_auth_token(token)
            if only_admin and not user_info['is_admin']:
                abort(403, 'Only admin can access')
            
            _self.user_info = user_info
            return func(_self, *args, **kwargs)
        return decorated
    return validation
