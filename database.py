from sqlalchemy import create_engine , Column , Integer, String, select, ForeignKey, Table
from sqlalchemy import URL
from sqlalchemy import text 
import json

from sqlalchemy.orm import sessionmaker, declarative_base, relationship

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

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base = declarative_base()

User_Games = Table(
    'user_games',
    Base.metadata,
    Column("user_id", Integer, ForeignKey("gamemate_user.id"), primary_key=True),
    Column("game_id", Integer, ForeignKey("games.id"), primary_key=True)
)

class User(Base):
    __tablename__ = 'gamemate_user'


    id = Column(Integer , primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String,nullable=False)
    country = Column(String, nullable=True)


    games = relationship("Game",secondary=User_Games,back_populates="users")



# user1 = User(name="Brutal", age=21, email="exampleabc@gmail.com", country="India")
# user2 = User(name="Sujit",age=23, email="sujit4@gmail.com", country="Canada")
# user3 = User(name="Swaleha",age=18, email="swaleha4@gmail.com", country="Iran")

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    users = relationship("User",secondary=User_Games,back_populates="games")




# Base.metadata.create_all(engine)
array = []

usr_stmt = select(User)
result = session.execute(usr_stmt)

users = result.scalars()

for user in users:
    print(f"{user.name}\t{user.age}\t{user.email}\t{user.country}")

