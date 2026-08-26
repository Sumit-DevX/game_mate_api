from database import Base
from sqlalchemy import Column , Integer, String, select, ForeignKey, Table

from sqlalchemy.orm import relationship,declarative_base
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

    lfg_posts = relationship("LFG_Post", back_populates="user")

    join_requests = relationship("Join_Request", back_populates="user")

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    users = relationship("User",secondary=User_Games,back_populates="games")

    lfg_posts = relationship("LFG_Post", back_populates="game")




class LFG_Post(Base):
    __tablename__ = "lfg_posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("gamemate_user.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    title = Column(String, nullable=False)
    players_needed = Column(Integer, nullable=False)
    message = Column(String)

    user = relationship("User", back_populates="lfg_posts")

    game = relationship("Game", back_populates="lfg_posts")

    join_requests = relationship("Join_Request", back_populates="lfg_post")



class Join_Request(Base):
    __tablename__ = "join_requests"

    lfg_post_id = Column(Integer, ForeignKey("lfg_posts.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("gamemate_user.id"), primary_key=True)
    status = Column(String, nullable=False)

    
    lfg_post = relationship("LFG_Post", back_populates="join_requests")

    user = relationship("User", back_populates="join_requests")