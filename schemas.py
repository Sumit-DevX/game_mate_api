from pydantic import BaseModel, ConfigDict

class UserModel(BaseModel):

    name : str
    age: int
    email: str
    country: str
    password: str

class UserResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    email: str
    country: str


class GameModel(BaseModel):
    name: str

class GameResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : int
    name : str

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



class JoinRequestModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id : int
    lfg_post_id : int 
    status: str


class JoinRequestUpdateModel(BaseModel):
    status : str

class LoginModel(BaseModel):
    email : str
    password: str

