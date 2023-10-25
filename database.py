from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import sessionmaker, relationship, Mapped
import enum
from sqlalchemy import  Column, Integer, String, Date, Boolean, Time, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

class Base(DeclarativeBase): pass

class Weekday(enum.Enum):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6



class TimeIntervalObjects(Base):
    __tablename__ = "time_interval_objects"
    id = Column(Integer, primary_key=True, index=True)
    time_object = Column(Time)

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    client_bitrix_id = Column(Integer)
    client_name = Column(String)
    client_phone = Column(String)
    client_mail = Column(String)

# class RaspisanieObject(Base):
#     __abstract__ = True
#     starttime = relationship('TimeIntervalObjects', foreign_keys='TimeIntervalObjects.id')
#     endtime = relationship('TimeIntervalObjects', foreign_keys='TimeIntervalObjects.id')
    
# class TypicalRaspisanieObject(RaspisanieObject):
#     __tablename__ = "typical_raspisanie_objects"
#     id = Column(Integer, primary_key=True, index=True)
#     weekdays = Column(Enum(Weekday))
#     description = Column(String)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    #client = relationship('Client', foreign_keys='Client.user_id')
    payed = Column(Boolean)
    starttime = Column(Integer, ForeignKey('time_interval_objects.id'))
    endtime = Column(Integer, ForeignKey('time_interval_objects.id'))
    def __init__(self, date: Date, starttime: int, endtime:int, payed: bool, client_bitrix_id: int|None, client_name: str|None, client_phone: str|None, client_mail: str|None):
        
        if (not(client_bitrix_id) and not(client_name and client_mail and client_phone) ):
            raise ValueError("No client info given")
        
        #if (starttime.time_object >= endtime.time_object):
            #raise ValueError("Invalid time given")

        self.date = date
        self.payed = payed
        self.starttime = starttime
        self.endtime = endtime

        if (client_bitrix_id):    
            self.client_bitrix_id = client_bitrix_id
        elif (client_name and client_mail and client_phone) :
            pass
            # self.client_name = client_name
            # self.client_phone = client_phone
            # self.client_mail = client_mail

    def get_interval(self) -> int:
        return self.starttime.time
    


# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# with Session(autoflush=False, bind=engine) as db:
#     #db.add(TypicalRaspisanieObject(weekdays=Weekday.saturday, description="test", starttime=TimeIntervalObjects(time_object="10:00"), endtime=TimeIntervalObjects(time_object="11:00")))
#     time_1 = TimeIntervalObjects(time_object=datetime.time(8, 0))
#     time_2 = TimeIntervalObjects(time_object=datetime.time(8, 30))
#     time_3 = TimeIntervalObjects(time_object=datetime.time(9, 0))
#     time_4 = TimeIntervalObjects(time_object=datetime.time(9, 30))
#     time_5 = TimeIntervalObjects(time_object=datetime.time(10, 0))
#     time_6 = TimeIntervalObjects(time_object=datetime.time(10, 30))
#     time_7 = TimeIntervalObjects(time_object=datetime.time(11, 0))
#     time_8 = TimeIntervalObjects(time_object=datetime.time(11, 30))
#     time_9 = TimeIntervalObjects(time_object=datetime.time(12, 0))
#     time_10 = TimeIntervalObjects(time_object=datetime.time(12, 30))
#     time_11 = TimeIntervalObjects(time_object=datetime.time(13, 0))
#     time_12 = TimeIntervalObjects(time_object=datetime.time(13, 30))
#     time_13 = TimeIntervalObjects(time_object=datetime.time(14, 0))
#     time_14 = TimeIntervalObjects(time_object=datetime.time(14, 30))
#     time_15 = TimeIntervalObjects(time_object=datetime.time(15, 0))
#     time_16 = TimeIntervalObjects(time_object=datetime.time(15, 30))
#     time_17 = TimeIntervalObjects(time_object=datetime.time(16, 0))
#     time_18 = TimeIntervalObjects(time_object=datetime.time(16, 30))
#     time_19 = TimeIntervalObjects(time_object=datetime.time(17, 0))
#     time_20 = TimeIntervalObjects(time_object=datetime.time(17, 30))
#     time_21 = TimeIntervalObjects(time_object=datetime.time(18, 0))
#     time_22 = TimeIntervalObjects(time_object=datetime.time(18, 30))
#     time_23 = TimeIntervalObjects(time_object=datetime.time(19, 0))
#     time_24 = TimeIntervalObjects(time_object=datetime.time(19, 30))
#     time_25 = TimeIntervalObjects(time_object=datetime.time(20, 0))
#     time_26 = TimeIntervalObjects(time_object=datetime.time(20, 30))
#     time_27 = TimeIntervalObjects(time_object=datetime.time(21, 0))
#     time_28 = TimeIntervalObjects(time_object=datetime.time(21, 30))
#     time_29 = TimeIntervalObjects(time_object=datetime.time(22, 0))
#     time_30 = TimeIntervalObjects(time_object=datetime.time(22, 30))
#     time_31 = TimeIntervalObjects(time_object=datetime.time(23, 0))

#     db.add_all([time_1, time_2, time_3, time_4, time_5, time_6, time_7, time_8, time_9, time_10, time_11, time_12, time_13, time_14, time_15, time_16, time_17, time_18, time_19, time_20, time_21, time_22, time_23, time_24, time_25, time_26, time_27, time_28, time_29, time_30, time_31])
#     db.commit()
#     db.flush()

    # db.add(Order( date=datetime.date(2021, 11, 26), starttime=time_1.id, endtime=time_2.id, payed=False, client_bitrix_id=None, client_name="test", client_phone="test", client_mail="test"))
    # db.add(Order( date=datetime.date(2021, 11, 26), starttime=time_3.id, endtime=time_4.id, payed=True, client_bitrix_id=None, client_name="test", client_phone="test", client_mail="test"))
    # db.commit()