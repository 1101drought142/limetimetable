from sqlalchemy import  Column, Integer, String, Date, Boolean, Time, ForeignKey, DateTime
from sqlalchemy.sql import func

from database import Base

class Cort(Base):
    __tablename__ = "cort"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(64))
    
class TimeIntervalObjects(Base):
    __tablename__ = "time_interval_objects"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    time_object = Column(Time)

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_bitrix_id = Column(Integer)
    client_name = Column(String(255))
    client_phone = Column(String(255))
    client_mail = Column(String(255))

class TypicalRaspisanieObject(Base):
    __tablename__ = "typical_raspisanie_objects"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    weekdays = Column(String(255)) # Formated list of Enum Weekdays
    starttime = Column(Integer, ForeignKey('time_interval_objects.id'))
    endtime = Column(Integer, ForeignKey('time_interval_objects.id'))
    description = Column(String(255))
    cort = Column(Integer, ForeignKey('cort.id'))

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date)
    client = Column(Integer, ForeignKey('clients.id'))
    payed = Column(Boolean)
    starttime = Column(Integer, ForeignKey('time_interval_objects.id'))
    endtime = Column(Integer, ForeignKey('time_interval_objects.id'))
    cort = Column(Integer, ForeignKey('cort.id'))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
