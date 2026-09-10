from pwdlib import PasswordHash
from pydantic import validate_call
from fastapi import Depends, HTTPException

from datetime import datetime , timedelta , timezone

import jwt

import os
from dotenv import load_dotenv

from fastapi.security import OAuth2PasswordBearer

from database import get_db
from crud.users import get_user_by_id
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import User


load_dotenv()

JWT_SECRET = os.environ["JWT_SECRET_KEY"]
ALGORITHM = os.environ["JWT_ALGORITHM"]

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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


def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id = int(decoded["sub"])

        stmt = select(User).where(User.id == user_id)
        user = db.scalar(stmt)

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized"
            )
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has Expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
