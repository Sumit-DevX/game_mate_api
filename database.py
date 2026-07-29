from sqlalchemy import create_engine , Column , Integer, String, select
from sqlalchemy import URL
from sqlalchemy import text 
import json

from sqlalchemy.orm import sessionmaker, declarative_base

with open("config.json") as f:
    db_config = json.load(f)


url_object = URL.create(
    "postgresql+psycopg",
    username=db_config["username"],
    password=db_config["password"],
    host=db_config["host"],
    database=db_config["database"]
)

engine = create_engine(url_object)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'gamemate_user'


    id = Column(Integer , primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String,nullable=False)
    country = Column(String, nullable=True)



user1 = User(name="Brutal", age=21, email="exampleabc@gmail.com", country="India")
user2 = User(name="Sujit",age=23, email="sujit4@gmail.com", country="Canada")
user3 = User(name="Swaleha",age=18, email="swaleha4@gmail.com", country="Iran")

session.add_all([user1,user2,user3])
session.commit()

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


Base.metadata.create_all(engine)


game1 = Game(name="Valorant")

session.add(game1)

session.commit()
