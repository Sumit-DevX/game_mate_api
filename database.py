from sqlalchemy import create_engine , URL 
import json

from sqlalchemy.orm import sessionmaker

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

def get_db():
    db = Session()
    try:
        yield db                                    #get database connection 
    finally:
        db.close()


