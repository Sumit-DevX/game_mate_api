from fastapi import FastAPI , Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import List

from database import User, Game, LFG_Post, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db                                    #get database connection 
    finally:
        db.close()

@app.get("/")
def root():
    return {"message" : "Gamemate API is running"}

class UserModel(BaseModel):

    name : str
    age: int
    email: str
    country: str

class UserResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    email: str
    country: str



@app.post("/users")
def create_user(user : UserModel, db : Session = Depends(get_db)):
    new_user = User(
        name=user.name,
        age=user.age,
        email=user.email,
        country=user.country
    )

    db.add(new_user)
    db.commit()
    return user

@app.get("/users",  response_model=List[UserResponseModel])
def get_users(db : Session = Depends(get_db)):
    users = db.execute(
        select(User)
    ).scalars()

    return users.all()


@app.get("/users/{usr_id}", response_model=UserResponseModel)
def get_user(usr_id : int, db : Session = Depends(get_db)):
    stmt = select(User).where(User.id == usr_id)
    requested_user = db.scalar(stmt)

    if requested_user is None:
        raise HTTPException(
                status_code=404,
                detail="User not found",
                headers={"X-Error": "Unknown user"}
            )

    user = UserResponseModel.model_validate(requested_user)
    return user
        
    
# Games endpoints

class GameModel(BaseModel):
    name: str

class GameResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : int
    name : str

@app.get("/games", response_model=List[GameResponseModel])
def get_games(db : Session = Depends(get_db)):
    games = db.execute(select(Game)).scalars()
    return games.all()

@app.post("/games", response_model=GameResponseModel)
def create_game(game : GameModel, db : Session = Depends(get_db)):
    new_game = Game(
        name = game.name
    )
    db.add(new_game)
    db.commit()
    return GameResponseModel.model_validate(new_game)

@app.get("/games/{game_id}", response_model=GameResponseModel)
def get_game(game_id : int, db : Session = Depends(get_db)):
    stmt = select(Game).where(Game.id == game_id)
    requested_game = db.scalar(stmt)
    if requested_game is None:
        raise HTTPException(
            status_code = 404,
            detail="Game Not Found"
        )
    game = GameResponseModel.model_validate(requested_game)
    return game



@app.post("/user/{usr_id}/games/{game_id}")
def add_user_game(usr_id : int , game_id : int , db : Session = Depends(get_db)):
    user = db.scalar(
        select(User).where(User.id == usr_id)
    )

    game = db.scalar(
        select(Game).where(Game.id == game_id)
    )

    if user is None or game is None:
            raise HTTPException(                            
                status_code=404,
                detail="User or Game Not Found"
            )                                                           # Add games to a user

    for user_game in user.games:
        if user_game.id == game.id:
            raise HTTPException(
                status_code=409,
                detail="User Already Plays This Game"
            )

    user.games.append(game)
    db.commit()
    return {"message" : f"{game.name} is added to {user.name} "}


#LFG Post Endpoints

class LFGPostModel(BaseModel):
    user_id : int
    game_id : int 
    title : str
    players_needed : int
    message: str | None

class LFGPostResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : int
    user_id : int 
    game_id : int
    title : str
    players_needed: int
    message: str | None



@app.post("/lfg",response_model=LFGPostResponseModel)
def create_lfgPost(post : LFGPostModel ,db : Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.id == post.user_id))

    game = db.scalar(select(Game).where(Game.id == post.game_id))

    if user is None or game is None:
        raise HTTPException(
            status_code=404,
            detail="User Or Game Not Found"
        )

    new_lfg_post = LFG_Post(
        user_id = post.user_id,
        game_id = post.game_id,
        title = post.title,
        players_needed = post.players_needed,
        message = post.message
    )

    db.add(new_lfg_post)
    db.commit()

    return LFGPostResponseModel.model_validate(new_lfg_post)

@app.get("/lfg",response_model=List[LFGPostResponseModel])
def get_lfg_posts(db : Session = Depends(get_db), game_id : int = None):
    stmt = select(LFG_Post)

    if game_id is None:
        lfg_posts = db.scalars(stmt)
        return lfg_posts.all()
    else:
        requested_lfg_posts = db.scalars(select(LFG_Post).where(LFG_Post.game_id == game_id))
        return requested_lfg_posts.all()

    
@app.get("/lfg/{post_id}", response_model=LFGPostResponseModel)
def get_lfg_post(post_id : int, db: Session = Depends(get_db)):
    requested_lfg_post = db.scalar(select(LFG_Post).where(LFG_Post.id == post_id))

    if requested_lfg_post is None:
        raise HTTPException(
            status_code = 404,
            detail="Post Not Found"
        )
    else:
        return LFGPostResponseModel.model_validate(requested_lfg_post)
