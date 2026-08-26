from fastapi import APIRouter, Depends, HTTPException
from crud.games import get_game_by_id

from database import get_db

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select

from models import Game
from schemas import GameModel, GameResponseModel

router = APIRouter(prefix="/games", tags=["Games"])


@router.get("/games", response_model=List[GameResponseModel])
def get_games(db : Session = Depends(get_db)):
    games = db.execute(select(Game)).scalars()
    return games.all()

@router.post("/games", response_model=GameResponseModel)
def create_game(game : GameModel, db : Session = Depends(get_db)):
    new_game = Game(
        name = game.name
    )
    db.add(new_game)
    db.commit()
    return GameResponseModel.model_validate(new_game)

@router.get("/games/{game_id}", response_model=GameResponseModel)
def get_game(game_id : int, db : Session = Depends(get_db)):
    game = get_game_by_id(game_id,db)
    return game


