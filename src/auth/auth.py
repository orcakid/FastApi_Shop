from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt


load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")

password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def get_hash_pwd(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_pwd: str, hash_pwd: str) -> bool:
    return password_context.verify(plain_pwd, hash_pwd)


def create_access_token(subject: Union[str, Any], expire_delta: int = None) -> str:
    if expire_delta is not None:
        expire_delta = datetime.utcnow() + timedelta(expire_delta)
    else:
        expire_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {'exp': expire_delta, 'sub': str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + timedelta(expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {'exp': expires_delta, 'sub': str(subject)}
    encoded_jwt_refresh = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt_refresh