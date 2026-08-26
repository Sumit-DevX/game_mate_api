from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Game

from fastapi import HTTPException

def get_game_by_id(game_id : int , db : Session):
    stmt = select(Game).where(Game.id == game_id)
    requested_game = db.scalar(stmt)

    if requested_game is None:
        raise HTTPException(
            status_code=404,
            detail="Game Not Found"
        )
    else:
        return requested_game