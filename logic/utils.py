import enum
import datetime
from sqlalchemy.orm import aliased, Session
from sqlalchemy import update

from database import session, engine, Order, TimeIntervalObjects, Client




def get_order_objects():
    starttime_table = aliased(TimeIntervalObjects)
    endtime_table = aliased(TimeIntervalObjects)
    return session.query(Order, starttime_table, endtime_table).join(starttime_table, Order.starttime == starttime_table.id).join(endtime_table, Order.endtime == endtime_table.id).all()

def get_order_object(id: int):
    starttime_table = aliased(TimeIntervalObjects)
    endtime_table = aliased(TimeIntervalObjects)
    return session.query(Order, starttime_table, endtime_table, Client).join(starttime_table, Order.starttime == starttime_table.id).join(endtime_table, Order.endtime == endtime_table.id).join(Client, Order.client == Client.id).filter(Order.id == id).first()

def delete_order_object(id: int) -> bool:
    with Session(autoflush=False, bind=engine) as db:
        timetable_object = db.query(Order).filter(Order.id == id).first()
        if (timetable_object):
            db.delete(timetable_object)
            db.commit()
            return True
        else:
            raise ValueError("Нет объекта с таким id")

def create_new_object(date: datetime.date, starttime: datetime.time, endtime: datetime.time, payed: bool, client_name:str|None, client_phone: str|None, client_mail: str|None, bitrix_id: str|None, site_id: str|None):
    with Session(autoflush=False, bind=engine) as db:
        time_start = db.query(TimeIntervalObjects).filter(TimeIntervalObjects.time_object == starttime).first()
        time_end = db.query(TimeIntervalObjects).filter(TimeIntervalObjects.time_object == endtime).first()
        if not(site_id):
            client = Client(client_bitrix_id=bitrix_id, client_name=client_name, client_phone=client_phone, client_mail=client_mail)
            db.add(client)
            db.commit()
            client_id = client.id
        else:
            client_id = site_id
        db.add(Order( date=date, starttime=time_start.id, endtime=time_end.id, payed=payed, client=int(client_id)))
        db.commit()
        return True

def update_object_db(date: datetime.date, starttime: datetime.time, endtime: datetime.time, payed: bool, client_name:str|None, client_phone: str|None, client_mail: str|None, bitrix_id: str|None, site_id: str|None, block_id:int):
    with Session(autoflush=False, bind=engine) as db:
        order = db.query(Order).filter(Order.id == block_id).first()
        
        time_start = db.query(TimeIntervalObjects).filter(TimeIntervalObjects.time_object == starttime).first()
        time_end = db.query(TimeIntervalObjects).filter(TimeIntervalObjects.time_object == endtime).first()
        if not(site_id):
            client = Client(client_bitrix_id=bitrix_id, client_name=client_name, client_phone=client_phone, client_mail=client_mail)
            db.add(client)
            db.commit()
            client_id = client.id
        else:
            client_id = site_id
            
        db.execute(update(Order).where(Order.id==order.id).values(date=date, starttime=time_start.id, endtime=time_end.id, payed=payed, client=int(client_id)))
        db.commit()

def get_client_or_raise(id: int) -> bool:
    with Session(autoflush=False, bind=engine) as db:
        timetable_object = db.query(Client).filter(Client.id == id).first()
        if (timetable_object):
            return True
        else:
            raise ValueError("Нет клиента с таким id")
        
def get_clients() -> list:
    return session.query(Client).all()

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