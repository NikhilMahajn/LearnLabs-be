import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_URI = os.environ.get('DB_URI')

import sqlalchemy
from sqlalchemy.orm import sessionmaker
# from psycopg2.extensions import register_adapter, AsIs

print(DB_URI)

engine = None
Session = None



def get_db_session():
    global Session
    if Session is None:
        engine = get_db_engine()
        Session = sessionmaker(bind=engine)
    return Session()


def get_db_engine():
    global engine
    if engine is None:
        connection_string = str(DB_URI)
        engine = sqlalchemy.create_engine(connection_string, isolation_level="READ UNCOMMITTED", query_cache_size=0)
    return engine

def get_db_session():
    global Session
    if Session is None:
        engine = get_db_engine()
        Session = sessionmaker(bind=engine)
    return Session()

session = get_db_session()

