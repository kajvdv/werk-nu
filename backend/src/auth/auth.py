from datetime import timedelta, datetime, timezone
import os

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from .config import settings

SECRET_KEY_ACCESS = settings.secret_key_access
SECRET_KEY_REFRESH = settings.secret_key_refresh
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

password_hash = PasswordHash.recommended()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    if not expires_delta:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_ACCESS, algorithm=ALGORITHM)
    return encoded_jwt


# def create_refresh_token():
#     expires_delta = timedelta(days=1)
#     expire = datetime.now(timezone.utc) + expires_delta
#     to_encode = {
#         "sub": "demo@demo.com",
#         "exp": expire
#     }
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY_REFRESH, algorithm=ALGORITHM)
#     return encoded_jwt


def decode_token(token, type="access"):
    if type == "refresh":
        secret = SECRET_KEY_REFRESH
    else:
        secret = SECRET_KEY_ACCESS
    try:
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise Exception("Invalid token")
    return payload
    
def hash_password(password: str):
   return password_hash.hash(password) 

def authenticate_user(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)