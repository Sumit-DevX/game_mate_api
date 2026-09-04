from fastapi import APIRouter , Depends , HTTPException
from schemas import LoginModel
from crud.users import get_user_by_email

from database import get_db
from sqlalchemy.orm import Session

from utils.security import verify_password , create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(credentials: LoginModel, db : Session = Depends(get_db)):
    user = get_user_by_email(credentials.email,db)

    if verify_password(credentials.password, user.password_hash):
        access_token = create_access_token(user.id)

        return {
            "access_token: " : access_token, 
            "token_type" : "bearer"
            }
    else:
        raise HTTPException(
            status_code=401,
            detail="Incorrect Password"
        )
