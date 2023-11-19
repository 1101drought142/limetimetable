from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import sessionmaker, relationship, Mapped
from sqlalchemy import  Column, Integer, String, Date, Boolean, Time, ForeignKey, DateTime, Enum, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func

import enum
import datetime
import bcrypt



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
    def get_rus_name(self):
        if (self == Weekday.monday):
            return "Понедельник"
        elif (self == Weekday.tuesday):
            return "Вторник"
        elif (self == Weekday.wednesday):
            return "Среда"
        elif (self == Weekday.thursday):
            return "Четверг"
        elif (self == Weekday.friday):
            return "Пятница"
        elif (self == Weekday.saturday):
            return "Суббота"
        elif (self == Weekday.sunday):
            return "Воскресенье"
        
class Users(enum.Enum):
    api = 0
    manager = 1 
    superuser = 2

class DataBaseFormatedWeekday():

    def format_to_string(weekdays):
        res_string = ""
        for weekday in weekdays:
            res_string += f'{weekday.value},'
        return res_string
    
    def format_from_string(string):
        res = []
        raw_array = string.split(",")
        for el in raw_array:
            if (el):
                res.append(Weekday(int(el)))
        return res

    def from_list_to_string(weekdays):
        res_string = ""
        for weekday in weekdays:
            res_string += f'{weekday},'
        return res_string

    def check_if_valid_or_raise(weekdays):
        for weekday in weekdays:
            try:
                Weekday(int(weekday))
            except:
                raise ValueError("Неправильный день недели")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    type = Enum(Users)
    fullname = Column(String)
    login = Column(String)
    password = Column(String)

class UserLog(Base):
    __tablename__ = "userlog"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey('users.id'))
    text = Column(Text)

class Cort(Base):
    __tablename__ = "cort"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
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


class TypicalRaspisanieObject(Base):
    __tablename__ = "typical_raspisanie_objects"
    id = Column(Integer, primary_key=True, index=True)
    weekdays = Column(String) # Formated list of Enum Weekdays
    starttime = Column(Integer, ForeignKey('time_interval_objects.id'))
    endtime = Column(Integer, ForeignKey('time_interval_objects.id'))
    description = Column(String)
    cort = Column(Integer, ForeignKey('cort.id'))


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    client = Column(Integer, ForeignKey('clients.id'))
    payed = Column(Boolean)
    starttime = Column(Integer, ForeignKey('time_interval_objects.id'))
    endtime = Column(Integer, ForeignKey('time_interval_objects.id'))
    cort = Column(Integer, ForeignKey('cort.id'))
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    
# User.__table__.drop(engine)
# UserLog.__table__.drop(engine)
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