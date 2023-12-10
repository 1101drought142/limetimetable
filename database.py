import os
from dotenv import load_dotenv, find_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
import logging

load_dotenv(find_dotenv())

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{os.environ.get("BD_LOGIN")}:{os.environ.get("BD_PASSWORD")}@{os.environ.get("BD_HOST")}/test'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase): 
    pass

2023-12-10 14:18:47.801626

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
