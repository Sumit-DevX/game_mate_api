from fastapi import FastAPI , Depends
from pydantic import BaseModel, ConfigDict
from typing import List

from database import User, SessionLocal
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



