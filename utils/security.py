from pwdlib import PasswordHash
from pydantic import validate_call

from datetime import datetime , timedelta , timezone

import jwt

import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.environ["JWT_SECRET_KEY"]
ALGORITHM = os.environ["JWT_ALGORITHM"]

password_hash = PasswordHash.recommended()

@validate_call
def generate_hash(password : str) -> str:

    hashed_password = password_hash.hash(password)

    return hashed_password

@validate_call
def verify_password(password : str , hashed_password : str) -> bool:
    

    try:
        return password_hash.verify(password, hashed_password)
    except Exception: 
        return False


@validate_call
def create_access_token(user_id: int) -> str:
    payload = {
        "sub" : str(user_id),
        "exp" : datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    token = jwt.encode(payload , JWT_SECRET, algorithm=ALGORITHM)
    return token