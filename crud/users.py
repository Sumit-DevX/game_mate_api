from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User

from fastapi import HTTPException

def get_user_by_id(usr_id : int, db : Session):
    stmt = select(User).where(User.id == usr_id)
    requested_user = db.scalar(stmt)

    if requested_user is None:
        raise HTTPException(
                status_code=404,
                detail="User not found",
            )
    else:
        return requested_user