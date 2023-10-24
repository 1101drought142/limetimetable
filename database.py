from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import  Column, Integer, String, Date, Boolean, Time

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class TimeIntervalObjects(Base):
    __tablename__ = "time_interval_objects"
    id = Column(Integer, primary_key=True, index=True)
    time_object = Column(Time)

class Client(Base):
    id = Column(Integer, primary_key=True, index=True)
    client_bitrix_id = Column(Integer)
    client_name = Column(String)
    client_phone = Column(String)
    client_mail = Column(String)

class Order(Base):
    __tabblename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    starttime = relationship('TimeIntervalObjects', foreign_keys='TimeIntervalObjects.id')
    endtime = relationship('TimeIntervalObjects', foreign_keys='TimeIntervalObjects.id')
    client = relationship('Client', foreign_keys='Client.user_id')
    payed = Column(Boolean)

    def __init__(self, date: Date, starttime: int, endtime:int, payed: bool, client_bitrix_id: int|None, client_name: str|None, client_phone: str|None, client_mail: str|None):
        
        if (not(client_bitrix_id) or (client_name and client_mail and client_phone) ):
            raise ValueError("No client info given")
        
        if (starttime >= endtime):
            raise ValueError("Invalid time given")

        self.date = date
        self.payed = payed
        self.starttime = starttime
        self.endtime = endtime

        if (self.client_bitrix_id):
            
            self.client_bitrix_id = client_bitrix_id
        elif (client_name and client_mail and client_phone) :
            self.client_name = client_name
            self.client_phone = client_phone
            self.client_mail = client_mail