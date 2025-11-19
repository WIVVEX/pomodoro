from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:password@127.0.0.1:5433/pomodoro")

Session = sessionmaker(engine)

def get_db_session():
    return Session


