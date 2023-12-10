from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
import logging

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:new-password@localhost/test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase): 
    pass

logger = logging.getLogger(__name__)
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
