from fastapi import APIRouter,Depends, HTTPException

from crud.users import get_user_by_id
from crud.games import get_game_by_id

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db

from models import User
from schemas import UserResponseModel, UserModel

from utils.security import generate_hash

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("",response_model=UserResponseModel)
def create_user(user : UserModel, db : Session = Depends(get_db)):

    pwd_hash = generate_hash(user.password)
    new_user = User(
        name=user.name,
        age=user.age,
        email=user.email,
        country=user.country,
        password_hash=pwd_hash
    )

    db.add(new_user)
    db.commit()
    return UserResponseModel.model_validate(new_user)

@router.get("",  response_model=List[UserResponseModel])
def get_users(db : Session = Depends(get_db)):
    users = db.execute(
        select(User)
    ).scalars()

    return users.all()


@router.get("/{usr_id}", response_model=UserResponseModel)
def get_user(usr_id : int, db : Session = Depends(get_db)):
    requested_user = get_user_by_id(usr_id,db)

    return UserResponseModel.model_validate(requested_user)


@router.post("/{usr_id}/games/{game_id}")
def add_user_game(usr_id : int , game_id : int , db : Session = Depends(get_db)):
    user = get_user_by_id(usr_id,db)

    game = get_game_by_id(game_id,db)                                                    # Add games to a user

    for user_game in user.games:
        if user_game.id == game.id:
            raise HTTPException(
                status_code=409,
                detail="User Already Plays This Game"
            )

    user.games.append(game)
    db.commit()
    return {"message" : f"{game.name} is added to {user.name} "}
