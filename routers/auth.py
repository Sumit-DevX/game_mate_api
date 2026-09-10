from fastapi import APIRouter , Depends , HTTPException


from crud.users import get_user_by_email

from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select

from utils.security import verify_password , create_access_token , oauth2_scheme , get_current_user

from fastapi.security import OAuth2PasswordRequestForm
from models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == form.username))

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    if verify_password(form.password, user.password_hash):
        access_token = create_access_token(user.id)

        return {
            "access_token" : access_token, 
            "token_type" : "bearer"
            }
    else:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

@router.get("/test_auth")
def test_auth(current_user : User = Depends(get_current_user)):
    return {
        "message" : "You are authenticated",
        "User id" : current_user.id,
        "User name" : current_user.name
    }