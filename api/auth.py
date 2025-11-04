from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Cookie
import jwt
import os
from dotenv import load_dotenv
from pwdlib import PasswordHash

from db import SessionLocal, User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

if SECRET_KEY is None:
    raise RuntimeError("SECRET_KEY environment variable is not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = PasswordHash.recommended()

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(username: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_user(username: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def get_current_user(access_token: str = Cookie(None)):
    print("Access token from cookie:", access_token)

    if access_token is None:
        raise HTTPException(status_code=401, detail="No access token provided")

    username = decode_access_token(access_token)
    user = get_user(username)

    print("Decoded username:", username)
    print("User object:", user)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user
