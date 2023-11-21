from sqlalchemy import  Column, Integer, String, Date, Boolean, Time, ForeignKey, DateTime

from database import Base


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