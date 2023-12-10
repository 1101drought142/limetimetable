import os
from dotenv import load_dotenv, find_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
import logging

load_dotenv(find_dotenv())
print(find_dotenv())
print(os.environ.get("BD_LOGIN"))

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{os.environ.get("BD_LOGIN")}:{os.environ.get("BD_PASSWORD")}@{os.environ.get("BD_HOST")}/test'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase): 
    pass


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        logger.exception("Session rollback because of exception")
        db.rollback()
        raise
    finally:
        db.close()
