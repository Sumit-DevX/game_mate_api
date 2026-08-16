from fastapi import FastAPI , Depends
from pydantic import BaseModel
from typing import List

from database import User, SessionLocal
from sqlalchemy.orm import Session

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

