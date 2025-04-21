from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:Kashiv%40882@localhost:5432/authdb"
# DATABASE_URL = "postgresql://postgres_feed_parser_user:SwEDl3mYGvi7ZYXxQgTnYAVidpAThKvo@dpg-cvvo2di4d50c739iov00-a/postgres_feed_parser"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
